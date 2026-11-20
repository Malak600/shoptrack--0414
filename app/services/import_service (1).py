"""Import products from a CSV file (with SHACL validation) and export them as JSON-LD (story S7)."""
import csv
import io
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from typing import Iterator

from pyshacl import validate
from rdflib import RDF, XSD, BNode, Graph, Literal, Namespace, URIRef

from app import db
from app.models.product import Product
from app.models.stock_movement import StockMovement

SCHEMA = Namespace("https://schema.org/")
SHOP = Namespace("https://shoptrack.example/vocab#")
SH = Namespace("http://www.w3.org/ns/shacl#")

REQUIRED_COLUMNS = {"name", "price", "stock"}

# SHACL shape: the rules every imported product must follow.
PRODUCT_SHAPE = """
@prefix sh:     <http://www.w3.org/ns/shacl#> .
@prefix xsd:    <http://www.w3.org/2001/XMLSchema#> .
@prefix schema: <https://schema.org/> .
@prefix shop:   <https://shoptrack.example/vocab#> .

shop:ProductShape a sh:NodeShape ;
    sh:targetClass schema:Product ;
    sh:property [
        sh:path schema:name ; sh:datatype xsd:string ;
        sh:minCount 1 ; sh:maxCount 1 ; sh:minLength 1 ; sh:maxLength 100 ;
        sh:message "name is missing or longer than 100 characters" ] ;
    sh:property [
        sh:path schema:price ; sh:datatype xsd:decimal ;
        sh:minCount 1 ; sh:maxCount 1 ; sh:minExclusive 0 ;
        sh:message "price must be a number greater than 0" ] ;
    sh:property [
        sh:path shop:stock ; sh:datatype xsd:integer ;
        sh:minCount 1 ; sh:maxCount 1 ; sh:minInclusive 0 ;
        sh:message "stock must be a whole number, 0 or more" ] ;
    sh:property [
        sh:path shop:reorderLevel ; sh:datatype xsd:integer ;
        sh:maxCount 1 ; sh:minInclusive 0 ;
        sh:message "reorder_level must be a whole number, 0 or more" ] .
"""

JSONLD_CONTEXT = {
    "schema": str(SCHEMA),
    "shop": str(SHOP),
    "name": "schema:name",
    "price": {"@id": "schema:price", "@type": "http://www.w3.org/2001/XMLSchema#decimal"},
    "stock": {"@id": "shop:stock", "@type": "http://www.w3.org/2001/XMLSchema#integer"},
    "reorderLevel": {"@id": "shop:reorderLevel", "@type": "http://www.w3.org/2001/XMLSchema#integer"},
}


class ImportFileError(Exception):
    """The file itself cannot be read (empty, not CSV, or required columns missing)."""


@dataclass
class ImportResult:
    created: int = 0
    updated: int = 0
    errors: list[tuple[int, str]] = field(default_factory=list)  # (line number, reason)


def _typed(value: str, datatype: URIRef) -> Literal:
    """Make an RDF literal; a value that does not fit the type stays a plain string, so SHACL reports it."""
    value = (value or "").strip()
    try:
        if datatype == XSD.decimal:
            return Literal(Decimal(value), datatype=XSD.decimal)
        if datatype == XSD.integer:
            return Literal(int(value), datatype=XSD.integer)
    except (InvalidOperation, ValueError):
        pass
    return Literal(value)


def iter_rows(text: str) -> Iterator[tuple[int, dict]]:
    """Generator: yield (line number, row) one at a time, so large files are not held twice in memory."""
    reader = csv.DictReader(io.StringIO(text))
    columns = {c.strip().lower() for c in (reader.fieldnames or [])}
    missing = REQUIRED_COLUMNS - columns
    if missing:
        raise ImportFileError(f"Missing column(s): {', '.join(sorted(missing))}")
    for row in reader:
        clean = {(k or "").strip().lower(): (v or "").strip() for k, v in row.items()}
        if any(clean.values()):  # skip blank lines
            yield reader.line_num, clean


def rows_to_graph(rows: list[tuple[int, dict]]) -> tuple[Graph, dict]:
    """Turn CSV rows into one RDF graph of schema:Product nodes; remember which node is which line."""
    graph = Graph()
    node_line = {}
    for line, row in rows:
        node = URIRef(f"urn:shoptrack:import:line:{line}")
        node_line[node] = line
        graph.add((node, RDF.type, SCHEMA.Product))
        if row.get("name"):
            graph.add((node, SCHEMA.name, Literal(row["name"], datatype=XSD.string)))
        graph.add((node, SCHEMA.price, _typed(row.get("price", ""), XSD.decimal)))
        graph.add((node, SHOP.stock, _typed(row.get("stock", ""), XSD.integer)))
        if row.get("reorder_level"):
            graph.add((node, SHOP.reorderLevel, _typed(row["reorder_level"], XSD.integer)))
    return graph, node_line


def validate_rows(graph: Graph, node_line: dict) -> dict[int, list[str]]:
    """Run pySHACL once over all rows; return {line number: [reasons]} for the rows that break the shape."""
    shapes = Graph().parse(data=PRODUCT_SHAPE, format="turtle")
    conforms, report, _ = validate(graph, shacl_graph=shapes)
    problems: dict[int, list[str]] = {}
    if conforms:
        return problems
    for result in report.subjects(RDF.type, SH.ValidationResult):
        focus = report.value(result, SH.focusNode)
        message = str(report.value(result, SH.resultMessage) or "invalid value")
        line = node_line.get(focus)
        if line is not None and message not in problems.setdefault(line, []):
            problems[line].append(message)
    return problems


class ImportService:
    """Import and export of the product list."""

    @staticmethod
    def import_csv(text: str) -> ImportResult:
        """Save valid rows (new products are created, existing names are updated); list invalid rows."""
        rows = list(iter_rows(text))
        if not rows:
            raise ImportFileError("The file has no product rows.")
        graph, node_line = rows_to_graph(rows)
        problems = validate_rows(graph, node_line)

        result = ImportResult()
        seen = set()
        for line, row in rows:
            name_key = row["name"].lower()
            if line in problems:
                result.errors.append((line, "; ".join(problems[line])))
                continue
            if name_key in seen:
                result.errors.append((line, f"duplicate of an earlier row for '{row['name']}'"))
                continue
            seen.add(name_key)

            price = float(row["price"])
            stock = int(row["stock"])
            reorder = int(row["reorder_level"]) if row.get("reorder_level") else 5
            product = Product.query.filter(db.func.lower(Product.name) == name_key).first()
            if product is None:
                product = Product(name=row["name"], price=price, stock=0, reorder_level=reorder)
                db.session.add(product)
                result.created += 1
                change, kind = stock, StockMovement.KIND_IN
            else:
                product.price, product.reorder_level = price, reorder
                result.updated += 1
                change, kind = stock - product.stock, StockMovement.KIND_CORRECTION
            product.stock = stock
            if change:
                db.session.add(StockMovement(product=product, quantity=change, kind=kind))
        db.session.commit()
        return result

    @staticmethod
    def export_jsonld() -> str:
        """All products as JSON-LD with schema.org terms."""
        graph = Graph()
        graph.bind("schema", SCHEMA)
        graph.bind("shop", SHOP)
        for p in Product.query.order_by(Product.name).all():
            node = URIRef(f"urn:shoptrack:product:{p.id}")
            graph.add((node, RDF.type, SCHEMA.Product))
            graph.add((node, SCHEMA.name, Literal(p.name)))
            graph.add((node, SCHEMA.price, Literal(Decimal(str(p.price)), datatype=XSD.decimal)))
            graph.add((node, SHOP.stock, Literal(p.stock, datatype=XSD.integer)))
            graph.add((node, SHOP.reorderLevel, Literal(p.reorder_level, datatype=XSD.integer)))
        return graph.serialize(format="json-ld", context=JSONLD_CONTEXT, indent=2)

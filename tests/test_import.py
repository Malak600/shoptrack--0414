"""Tests for CSV import with SHACL validation and JSON-LD export (story S7)."""
import io
import json

import pytest
from rdflib import RDF, Graph

from app import db
from app.models.product import Product
from app.models.stock_movement import StockMovement
from app.services.import_service import SCHEMA, SHOP, ImportFileError, ImportService


def make_csv(valid=18):
    """TC for S7: a CSV with `valid` good rows plus a negative price and a missing name."""
    lines = ["name,price,stock,reorder_level"]
    lines += [f"Product {i},{10 + i},{i},3" for i in range(1, valid + 1)]
    lines.append("Broken price,-5,10,3")      # line valid + 2
    lines.append(",12,4,2")                   # line valid + 3
    return "\n".join(lines) + "\n"


def test_valid_rows_saved_invalid_rows_listed_with_line_and_reason(app):
    result = ImportService.import_csv(make_csv())
    assert (result.created, result.updated) == (18, 0)
    assert Product.query.count() == 18
    lines = [line for line, _ in result.errors]
    assert lines == [20, 21]
    assert "price must be a number greater than 0" in result.errors[0][1]
    assert "name is missing" in result.errors[1][1]


def test_non_numeric_values_are_rejected(app):
    result = ImportService.import_csv("name,price,stock\nTea,abc,5\nSugar,4,two\nMilk,3,1.5\n")
    assert Product.query.count() == 0
    reasons = dict(result.errors)
    assert "price" in reasons[2]
    assert "stock" in reasons[3]
    assert "stock" in reasons[4]


def test_existing_product_is_updated_and_stock_change_recorded(app):
    tea = Product(name="Tea", price=10, stock=4, reorder_level=2)
    db.session.add(tea)
    db.session.commit()
    result = ImportService.import_csv("name,price,stock,reorder_level\ntea,12,10,5\n")
    assert (result.created, result.updated) == (0, 1)
    tea = db.session.get(Product, tea.id)
    assert (tea.price, tea.stock, tea.reorder_level) == (12, 10, 5)
    movement = StockMovement.query.one()
    assert (movement.quantity, movement.kind) == (6, "CORRECTION")


def test_duplicate_name_in_file_is_rejected(app):
    result = ImportService.import_csv("name,price,stock\nTea,10,5\nTEA,11,6\n")
    assert Product.query.count() == 1
    assert result.errors[0][0] == 3


def test_missing_column_is_a_file_error(app):
    with pytest.raises(ImportFileError):
        ImportService.import_csv("name,price\nTea,10\n")


def test_jsonld_export_uses_schema_org(app):
    db.session.add(Product(name="Tea", price=10.5, stock=4, reorder_level=2))
    db.session.commit()
    text = ImportService.export_jsonld()
    data = json.loads(text)
    assert data["@context"]["name"] == "schema:name"
    # read it back as RDF: the values keep their types
    graph = Graph().parse(data=text, format="json-ld")
    product = next(graph.subjects(RDF.type, SCHEMA.Product))
    assert str(graph.value(product, SCHEMA.name)) == "Tea"
    assert graph.value(product, SHOP.stock).toPython() == 4


def test_import_page_upload(client):
    response = client.post(
        "/data/import",
        data={"file": (io.BytesIO(make_csv(valid=3).encode()), "products.csv")},
        content_type="multipart/form-data",
    )
    assert response.status_code == 200
    assert b"3 added" in response.data
    assert b"Rejected rows" in response.data


def test_staff_cannot_import(staff_client):
    assert staff_client.get("/data/import").status_code == 403
    assert staff_client.get("/data/products.jsonld").status_code == 403

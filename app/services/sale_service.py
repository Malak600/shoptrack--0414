"""Business logic for recording and querying sales."""
from app import db
from app.models.product import Product
from app.models.sale import Sale, SaleItem


class EmptySaleError(Exception):
    """Raised when trying to record a sale with no items."""


class SaleService:
    """Service layer handling sale transactions and stock deduction."""

    @staticmethod
    def record_sale(items_data: list[dict], note: str | None = None) -> Sale:
        """
        Record a new sale and deduct stock from each product.

        :param items_data: List of dicts like [{"product_id": 1, "quantity": 2}, ...]
        :param note: Optional note for the sale
        :return: Saved Sale instance
        """
        if not items_data:
            raise EmptySaleError("Sale must include at least one item.")

        sale = Sale(note=note)
        db.session.add(sale)

        try:
            for entry in items_data:
                product_id = int(entry["product_id"])
                quantity = int(entry["quantity"])

                product = db.session.get(Product, product_id)
                if product is None:
                    raise ValueError(f"Product with ID {product_id} not found.")

                product.remove_stock(quantity)

                sale_item = SaleItem(
                    product_id=product.id,
                    quantity=quantity,
                    unit_price=product.price,
                )
                sale.items.append(sale_item)

            sale.calculate_total()
            db.session.commit()
            return sale

        except Exception:
            db.session.rollback()
            raise

    @staticmethod
    def get_all_sales() -> list[Sale]:
        """Return all sales ordered from newest to oldest."""
        return Sale.query.order_by(Sale.created_at.desc(), Sale.id.desc()).all()
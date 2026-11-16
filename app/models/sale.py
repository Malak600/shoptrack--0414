"""Sale and SaleItem models for recording shop transactions."""
from datetime import datetime, timezone
from app import db


class Sale(db.Model):
    """Represents a completed customer sale."""

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    total_amount = db.Column(db.Float, nullable=False, default=0.0)
    note = db.Column(db.String(200), nullable=True)

    items = db.relationship(
        "SaleItem",
        backref="sale",
        lazy=True,
        cascade="all, delete-orphan",
    )

    def calculate_total(self) -> float:
        """Recalculate and update the total amount from sale items."""
        self.total_amount = round(
            sum(item.subtotal for item in self.items), 2
        )
        return self.total_amount


class SaleItem(db.Model):
    """Represents a single product line inside a Sale."""

    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey("sale.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)

    product = db.relationship("Product", lazy=True)

    @property
    def subtotal(self) -> float:
        """Line total for this item."""
        return round(self.quantity * self.unit_price, 2)
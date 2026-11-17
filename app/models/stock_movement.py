"""StockMovement model: every change to a product's stock is recorded."""
from datetime import datetime, timezone

from app import db


class StockMovement(db.Model):
    """One change in stock: stock in from a supplier, a sale, or a correction."""

    KIND_IN = "IN"
    KIND_SALE = "SALE"
    KIND_CORRECTION = "CORRECTION"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    kind = db.Column(db.String(20), nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    product = db.relationship("Product", backref="movements")

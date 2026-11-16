"""Product model: an item the shop sells."""
from app import db


class NotEnoughStockError(Exception):
    """Raised when a sale asks for more than the stock."""


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    reorder_level = db.Column(db.Integer, nullable=False, default=5)

    def add_stock(self, qty: int) -> None:
        if qty <= 0:
            raise ValueError("Quantity must be positive")
        self.stock += qty

    def remove_stock(self, qty: int) -> None:
        if qty <= 0:
            raise ValueError("Quantity must be positive")
        if qty > self.stock:
            raise NotEnoughStockError(f"Not enough stock for {self.name}")
        self.stock -= qty

    def needs_reorder(self) -> bool:
        return self.stock <= self.reorder_level

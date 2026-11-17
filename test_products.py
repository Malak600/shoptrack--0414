"""Tests for the product pages (story S1) and stock-in (story S2)."""
from app import db
from app.models.product import Product
from app.models.stock_movement import StockMovement


def test_add_product_starts_with_stock_zero(client):
    """S1: a saved product appears in the list with stock 0."""
    response = client.post(
        "/products/new",
        data={"name": "Tea 500g", "price": "85", "reorder_level": "5"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Tea 500g" in response.data
    product = Product.query.filter_by(name="Tea 500g").one()
    assert product.stock == 0
    assert product.reorder_level == 5


def test_add_product_rejects_negative_price(client):
    response = client.post("/products/new", data={"name": "Bad", "price": "-3", "reorder_level": "5"})
    assert response.status_code == 400
    assert Product.query.count() == 0


def test_edit_product_changes_price_not_stock(client):
    p = Product(name="Sugar", price=10, stock=8, reorder_level=2)
    db.session.add(p)
    db.session.commit()
    client.post(f"/products/{p.id}/edit", data={"name": "Sugar 1kg", "price": "12", "reorder_level": "3"})
    p = db.session.get(Product, p.id)
    assert (p.name, p.price, p.reorder_level, p.stock) == ("Sugar 1kg", 12, 3, 8)


def test_stock_in_increases_stock_and_records_movement(client):
    """S2: stock 4 + 10 arriving = 14, and a stock movement is recorded."""
    p = Product(name="Coffee", price=25, stock=4, reorder_level=3)
    db.session.add(p)
    db.session.commit()
    client.post(f"/products/{p.id}/stock-in", data={"quantity": "10"})
    assert db.session.get(Product, p.id).stock == 14
    movement = StockMovement.query.one()
    assert (movement.quantity, movement.kind) == (10, "IN")


def test_stock_in_rejects_zero(client):
    p = Product(name="Milk", price=5, stock=4, reorder_level=3)
    db.session.add(p)
    db.session.commit()
    client.post(f"/products/{p.id}/stock-in", data={"quantity": "0"})
    assert db.session.get(Product, p.id).stock == 4
    assert StockMovement.query.count() == 0

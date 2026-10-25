import pytest

from app import db
from app.models.product import NotEnoughStockError, Product


def make_product(stock=10, reorder_level=5):
    p = Product(name="Tea 500g", price=85, stock=stock, reorder_level=reorder_level)
    db.session.add(p)
    db.session.commit()
    return p


def test_home_page_loads(client):
    assert client.get("/").status_code == 200


def test_sale_reduces_stock(app):
    p = make_product(stock=10)
    p.remove_stock(3)
    assert p.stock == 7


def test_sale_larger_than_stock_is_refused(app):
    p = make_product(stock=2)
    with pytest.raises(NotEnoughStockError):
        p.remove_stock(5)
    assert p.stock == 2


def test_reorder_alert_at_reorder_level(app):
    p = make_product(stock=6, reorder_level=5)
    p.remove_stock(1)
    assert p.needs_reorder()

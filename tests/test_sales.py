"""Unit tests for Sale models and SaleService."""
import pytest
from app import create_app, db
from app.models.product import NotEnoughStockError, Product
from app.services.sale_service import EmptySaleError, SaleService


@pytest.fixture
def app_ctx():
    """Provide an isolated in-memory database for each test."""
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )
    with app.app_context():
        yield app
        db.session.remove()
        db.drop_all()


def test_record_sale_deducts_stock_and_calculates_total(app_ctx):
    coffee = Product(name="Arabic Coffee", price=25.0, stock=10, reorder_level=3)
    mug = Product(name="Koozie Mug", price=40.0, stock=5, reorder_level=2)
    db.session.add_all([coffee, mug])
    db.session.commit()

    sale = SaleService.record_sale(
        [
            {"product_id": coffee.id, "quantity": 2},
            {"product_id": mug.id, "quantity": 1},
        ],
        note="Morning customer",
    )

    assert sale.id is not None
    assert sale.total_amount == 90.0
    assert len(sale.items) == 2
    assert db.session.get(Product, coffee.id).stock == 8
    assert db.session.get(Product, mug.id).stock == 4


def test_record_sale_insufficient_stock_rolls_back(app_ctx):
    coffee = Product(name="Arabic Coffee", price=25.0, stock=2, reorder_level=1)
    mug = Product(name="Koozie Mug", price=40.0, stock=5, reorder_level=1)
    db.session.add_all([coffee, mug])
    db.session.commit()

    with pytest.raises(NotEnoughStockError):
        SaleService.record_sale(
            [
                {"product_id": mug.id, "quantity": 1},
                {"product_id": coffee.id, "quantity": 5},
            ]
        )

    assert db.session.get(Product, mug.id).stock == 5
    assert SaleService.get_all_sales() == []


def test_record_empty_sale_raises_error(app_ctx):
    with pytest.raises(EmptySaleError):
        SaleService.record_sale([])
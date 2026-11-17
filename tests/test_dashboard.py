"""Tests for the dashboard reports (stories S5 and S6)."""
from datetime import date, datetime, timedelta

from app import db
from app.models.product import Product
from app.models.sale import Sale, SaleItem
from app.services.report_service import ReportService

TODAY = date(2026, 12, 10)


def add_sale(product, quantity, days_ago):
    """Create a sale of one product, dated a number of days before TODAY."""
    created = datetime.combine(TODAY - timedelta(days=days_ago), datetime.min.time()) + timedelta(hours=12)
    sale = Sale(created_at=created)
    sale.items.append(SaleItem(product_id=product.id, quantity=quantity, unit_price=product.price))
    sale.calculate_total()
    db.session.add(sale)
    db.session.commit()


def make_products():
    tea = Product(name="Tea", price=10, stock=20, reorder_level=5)
    coffee = Product(name="Coffee", price=25, stock=4, reorder_level=5)
    db.session.add_all([tea, coffee])
    db.session.commit()
    return tea, coffee


def test_low_stock_lists_products_at_reorder_level(app):
    """S5: a product whose stock falls to its reorder level appears in the alerts."""
    tea, coffee = make_products()
    assert [p.name for p in ReportService.low_stock()] == ["Coffee"]
    tea.stock = 5
    db.session.commit()
    assert [p.name for p in ReportService.low_stock()] == ["Coffee", "Tea"]


def test_weekly_total_ignores_older_sales(app):
    """S6: only the last 7 days count toward the weekly total."""
    tea, coffee = make_products()
    add_sale(tea, 2, days_ago=0)      # 20
    add_sale(coffee, 1, days_ago=6)   # 25, still inside the week
    add_sale(tea, 9, days_ago=7)      # outside the week
    assert ReportService.weekly_total(TODAY) == 45.0
    daily = ReportService.daily_totals(TODAY)
    assert len(daily) == 7
    assert daily[0] == (TODAY - timedelta(days=6), 25.0)
    assert daily[-1] == (TODAY, 20.0)


def test_best_sellers_ordered_by_quantity(app):
    """S6: top products are ordered by quantity sold this week."""
    tea, coffee = make_products()
    add_sale(tea, 3, days_ago=1)
    add_sale(coffee, 1, days_ago=2)
    add_sale(tea, 2, days_ago=3)
    assert ReportService.best_sellers(TODAY) == [("Tea", 5), ("Coffee", 1)]


def test_dashboard_empty_state(client):
    """With no sales, the dashboard shows zero and an empty-state message, not an error."""
    response = client.get("/dashboard/")
    assert response.status_code == 200
    assert b"0.00" in response.data
    assert b"No sales recorded this week yet." in response.data


def test_chart_is_a_png(client):
    response = client.get("/dashboard/chart.png")
    assert response.status_code == 200
    assert response.data[:8] == b"\x89PNG\r\n\x1a\n"

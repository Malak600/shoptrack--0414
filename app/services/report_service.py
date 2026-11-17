"""Reports for the dashboard: weekly sales, best sellers and low-stock alerts."""
from datetime import date, datetime, time, timedelta

from sqlalchemy import func

from app import db
from app.models.product import Product
from app.models.sale import Sale, SaleItem


class ReportService:
    """Read-only queries used by the dashboard (stories S5 and S6)."""

    DAYS = 7

    @staticmethod
    def _week_start(today: date) -> datetime:
        """Start of the 7-day window that ends today."""
        return datetime.combine(today - timedelta(days=ReportService.DAYS - 1), time.min)

    @staticmethod
    def daily_totals(today: date | None = None) -> list[tuple[date, float]]:
        """Sales total for each of the last 7 days, oldest first; days without sales are 0."""
        today = today or date.today()
        start = ReportService._week_start(today)
        totals = {start.date() + timedelta(days=i): 0.0 for i in range(ReportService.DAYS)}
        for sale in Sale.query.filter(Sale.created_at >= start).all():
            day = sale.created_at.date()
            if day in totals:
                totals[day] += sale.total_amount
        return [(day, round(amount, 2)) for day, amount in totals.items()]

    @staticmethod
    def weekly_total(today: date | None = None) -> float:
        """Sum of all sales in the last 7 days."""
        return round(sum(amount for _, amount in ReportService.daily_totals(today)), 2)

    @staticmethod
    def best_sellers(today: date | None = None, limit: int = 5) -> list[tuple[str, int]]:
        """Top products by quantity sold in the last 7 days."""
        start = ReportService._week_start(today or date.today())
        rows = (
            db.session.query(Product.name, func.sum(SaleItem.quantity).label("qty"))
            .join(SaleItem, SaleItem.product_id == Product.id)
            .join(Sale, Sale.id == SaleItem.sale_id)
            .filter(Sale.created_at >= start)
            .group_by(Product.id)
            .order_by(func.sum(SaleItem.quantity).desc(), Product.name)
            .limit(limit)
            .all()
        )
        return [(name, int(qty)) for name, qty in rows]

    @staticmethod
    def low_stock() -> list[Product]:
        """Products whose stock is at or below their reorder level, lowest stock first."""
        products = Product.query.order_by(Product.stock, Product.name).all()
        return [p for p in products if p.needs_reorder()]

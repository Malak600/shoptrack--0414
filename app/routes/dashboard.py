"""Dashboard page: weekly total, daily sales chart, best sellers and low-stock alerts."""
import io

import matplotlib

matplotlib.use("Agg")  # draw charts without a screen (server side)
import matplotlib.pyplot as plt  # noqa: E402
from flask import Blueprint, Response, render_template  # noqa: E402

from app.services.report_service import ReportService  # noqa: E402

bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@bp.route("/", methods=["GET"])
def index():
    """Show the owner's dashboard."""
    daily = ReportService.daily_totals()
    return render_template(
        "dashboard.html",
        weekly_total=ReportService.weekly_total(),
        best_sellers=ReportService.best_sellers(),
        low_stock=ReportService.low_stock(),
        has_sales=any(amount > 0 for _, amount in daily),
    )


@bp.route("/chart.png", methods=["GET"])
def chart():
    """Bar chart of the last 7 days' sales, as a PNG image."""
    daily = ReportService.daily_totals()
    labels = [day.strftime("%a %d") for day, _ in daily]
    values = [amount for _, amount in daily]

    fig, ax = plt.subplots(figsize=(7, 3), dpi=100)
    ax.bar(labels, values, color="#2f6f9f")
    ax.set_ylabel("Sales")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    plt.close(fig)
    return Response(buffer.getvalue(), mimetype="image/png")

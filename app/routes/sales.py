"""Sales routes for recording transactions and viewing sales history."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from app.models.product import Product, NotEnoughStockError
from app.services.sale_service import SaleService, EmptySaleError

bp = Blueprint("sales", __name__, url_prefix="/sales")


@bp.route("/", methods=["GET"])
def index():
    """Show sales history and a form to record a new sale."""
    sales = SaleService.get_all_sales()
    products = Product.query.all()
    return render_template("sales/index.html", sales=sales, products=products)


@bp.route("/record", methods=["POST"])
def record():
    """Handle the form submission to record a new sale."""
    product_id = request.form.get("product_id")
    quantity = request.form.get("quantity")
    note = request.form.get("note", "")

    try:
        if not product_id or not quantity:
            raise ValueError("Please select a product and quantity.")
        
        items_data = [{"product_id": int(product_id), "quantity": int(quantity)}]
        SaleService.record_sale(items_data, note=note)
        flash("Sale recorded successfully!", "success")
    except (NotEnoughStockError, EmptySaleError, ValueError) as e:
        flash(str(e), "danger")

    return redirect(url_for("sales.index"))
import csv
from flask import make_response

@bp.route("/export/csv", methods=["GET"])
def export_csv():
    """Export all sales records as a downloadable CSV file."""
    sales = SaleService.get_all_sales()
    
    response = make_response()
    response.headers["Content-Disposition"] = "attachment; filename=sales_report.csv"
    response.headers["Content-Type"] = "text/csv"
    
    writer = csv.writer(response.stream)
    writer.writerow(["Sale ID", "Date", "Note", "Total Amount ($)"])
    
    for sale in sales:
        writer.writerow([
            sale.id,
            sale.created_at.strftime('%Y-%m-%d %H:%M'),
            sale.note or "",
            sale.total_amount
        ])
        
    return response
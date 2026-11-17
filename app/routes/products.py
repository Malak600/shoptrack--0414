"""Product pages: list, add, edit products and register stock arriving from suppliers."""
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from app import db
from app.auth import login_required, owner_required
from app.models.product import Product
from app.models.stock_movement import StockMovement

bp = Blueprint("products", __name__, url_prefix="/products")


def _read_product_form(form):
    """Read and validate the product form. Returns (data, error)."""
    name = (form.get("name") or "").strip()
    try:
        price = float(form.get("price", ""))
        reorder_level = int(form.get("reorder_level", "5"))
    except ValueError:
        return None, "Price and reorder level must be numbers."
    if not name:
        return None, "Name is required."
    if price <= 0:
        return None, "Price must be greater than zero."
    if reorder_level < 0:
        return None, "Reorder level cannot be negative."
    return {"name": name, "price": price, "reorder_level": reorder_level}, None


@bp.route("/", methods=["GET"])
@login_required
def index():
    """Show all products with their stock and a stock-in form."""
    products = Product.query.order_by(Product.name).all()
    return render_template("products/list.html", products=products)


@bp.route("/new", methods=["GET", "POST"])
@owner_required
def new():
    """Add a new product. New products start with stock 0."""
    if request.method == "POST":
        data, error = _read_product_form(request.form)
        if error:
            flash(error, "danger")
            return render_template("products/form.html", product=None, form=request.form), 400
        db.session.add(Product(stock=0, **data))
        db.session.commit()
        flash(f"Product '{data['name']}' added.", "success")
        return redirect(url_for("products.index"))
    return render_template("products/form.html", product=None, form={})


@bp.route("/<int:product_id>/edit", methods=["GET", "POST"])
@owner_required
def edit(product_id):
    """Edit a product's name, price and reorder level (not its stock)."""
    product = db.session.get(Product, product_id) or abort(404)
    if request.method == "POST":
        data, error = _read_product_form(request.form)
        if error:
            flash(error, "danger")
            return render_template("products/form.html", product=product, form=request.form), 400
        for key, value in data.items():
            setattr(product, key, value)
        db.session.commit()
        flash(f"Product '{product.name}' updated.", "success")
        return redirect(url_for("products.index"))
    return render_template("products/form.html", product=product, form={})


@bp.route("/<int:product_id>/stock-in", methods=["POST"])
@login_required
def stock_in(product_id):
    """Register stock arriving from a supplier and record the movement."""
    product = db.session.get(Product, product_id) or abort(404)
    try:
        qty = int(request.form.get("quantity", ""))
        product.add_stock(qty)
    except ValueError:
        flash("Quantity must be a whole number greater than zero.", "danger")
        return redirect(url_for("products.index"))
    db.session.add(StockMovement(product=product, quantity=qty, kind=StockMovement.KIND_IN))
    db.session.commit()
    flash(f"Added {qty} to '{product.name}'. Stock is now {product.stock}.", "success")
    return redirect(url_for("products.index"))

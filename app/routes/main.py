"""Main pages."""
from flask import Blueprint, render_template

from app.models.product import Product

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    products = Product.query.order_by(Product.name).all()
    return render_template("index.html", products=products)

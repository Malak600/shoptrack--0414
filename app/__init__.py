"""ShopTrack application factory."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config=None):
    """Create and configure the Flask app."""
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shoptrack.db"
    app.config["SECRET_KEY"] = "dev"
    if config:
        app.config.update(config)

    db.init_app(app)

    from app.auth import bp as auth_bp, require_login_for_blueprint
    from app.routes.main import bp as main_bp
    from app.routes.dashboard import bp as dashboard_bp
    from app.routes.data import bp as data_bp
    from app.routes.products import bp as products_bp
    from app.routes.sales import bp as sales_bp
    # every sales page needs a signed-in user (staff and owner may both sell)
    app.before_request_funcs.setdefault("sales", []).append(require_login_for_blueprint)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(data_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(sales_bp)

    with app.app_context():
        from app.models import product, sale, stock_movement, user  # noqa: F401  (register the models)
        db.create_all()

    return app

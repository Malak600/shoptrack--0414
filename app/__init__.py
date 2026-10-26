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

    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)

    with app.app_context():
        from app.models import product  # noqa: F401  (register the model)
        db.create_all()

    return app

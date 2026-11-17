import pytest

from app import create_app, db
from app.models.user import User


@pytest.fixture
def app():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    with app.app_context():
        yield app
        db.drop_all()


def make_user(username, role, password="secret123"):
    user = User(username=username, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def anon_client(app):
    """A browser that is not signed in."""
    return app.test_client()


@pytest.fixture
def client(app):
    """A browser signed in as the shop owner."""
    make_user("owner", User.ROLE_OWNER)
    c = app.test_client()
    c.post("/auth/login", data={"username": "owner", "password": "secret123"})
    return c


@pytest.fixture
def staff_client(app):
    """A browser signed in as a staff member."""
    make_user("owner", User.ROLE_OWNER)
    make_user("staff", User.ROLE_STAFF)
    c = app.test_client()
    c.post("/auth/login", data={"username": "staff", "password": "secret123"})
    return c

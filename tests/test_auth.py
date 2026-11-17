"""Tests for sign-in and the owner/staff permissions (story S8)."""
from app import db
from app.models.product import Product
from app.models.user import User


def test_password_is_stored_as_hash(app):
    user = User(username="hiyam", role=User.ROLE_OWNER)
    user.set_password("secret123")
    assert user.password_hash != "secret123"
    assert user.check_password("secret123")
    assert not user.check_password("wrong")


def test_first_visit_creates_owner_account(anon_client):
    assert anon_client.get("/auth/login").headers["Location"].endswith("/auth/setup")
    response = anon_client.post("/auth/setup", data={"username": "hiyam", "password": "secret123"})
    assert response.status_code == 302
    assert User.query.one().is_owner


def test_pages_need_sign_in(anon_client):
    for url in ["/products/", "/sales/", "/dashboard/"]:
        response = anon_client.get(url)
        assert response.status_code == 302
        assert "/auth/login" in response.headers["Location"]


def test_wrong_password_is_refused(client, app):
    other = app.test_client()
    response = other.post("/auth/login", data={"username": "owner", "password": "nope"})
    assert response.status_code == 401


def test_staff_cannot_edit_price(staff_client):
    """S8: given I am signed in as staff, when I open the edit-price page, then access is refused."""
    p = Product(name="Tea", price=10, stock=5, reorder_level=2)
    db.session.add(p)
    db.session.commit()
    assert staff_client.get(f"/products/{p.id}/edit").status_code == 403
    assert staff_client.post(f"/products/{p.id}/edit", data={"name": "Tea", "price": "1", "reorder_level": "2"}).status_code == 403
    assert db.session.get(Product, p.id).price == 10
    assert staff_client.get("/products/new").status_code == 403
    assert staff_client.get("/dashboard/").status_code == 403


def test_staff_can_sell_and_register_stock(staff_client):
    p = Product(name="Tea", price=10, stock=5, reorder_level=2)
    db.session.add(p)
    db.session.commit()
    assert staff_client.get("/sales/").status_code == 200
    staff_client.post(f"/products/{p.id}/stock-in", data={"quantity": "3"})
    staff_client.post("/sales/record", data={"product_id": str(p.id), "quantity": "2"})
    assert db.session.get(Product, p.id).stock == 6


def test_owner_adds_staff_account(client):
    client.post("/auth/staff", data={"username": "ali", "password": "secret123"})
    assert User.query.filter_by(username="ali").one().role == User.ROLE_STAFF

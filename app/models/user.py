"""User model: the shop owner (all rights) or a staff member (sales and stock-in only)."""
from werkzeug.security import check_password_hash, generate_password_hash

from app import db


class User(db.Model):
    """A person who signs in to ShopTrack."""

    ROLE_OWNER = "OWNER"
    ROLE_STAFF = "STAFF"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    role = db.Column(db.String(10), nullable=False, default=ROLE_STAFF)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password: str) -> None:
        """Store only a hash of the password, never the password itself."""
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters.")
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @property
    def is_owner(self) -> bool:
        return self.role == self.ROLE_OWNER

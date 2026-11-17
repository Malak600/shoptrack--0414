"""Sign-in, sign-out, user management and the access-control decorators (story S8)."""
from functools import wraps

from flask import (Blueprint, abort, flash, g, redirect, render_template, request,
                   session, url_for)

from app import db
from app.models.user import User

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.before_app_request
def load_user():
    """Make the signed-in user available as g.user on every request."""
    user_id = session.get("user_id")
    g.user = db.session.get(User, user_id) if user_id else None


def login_required(view):
    """Decorator: the page needs a signed-in user (owner or staff)."""
    @wraps(view)
    def wrapped(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("auth.login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


def owner_required(view):
    """Decorator: the page is for the shop owner only; staff get 403 Forbidden."""
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if not g.user.is_owner:
            abort(403)
        return view(*args, **kwargs)
    return wrapped


def require_login_for_blueprint():
    """before_request hook: protect every page of a blueprint (used for sales)."""
    if g.user is None:
        return redirect(url_for("auth.login", next=request.path))
    return None


@bp.route("/setup", methods=["GET", "POST"])
def setup():
    """Create the first owner account. Only works while no user exists."""
    if User.query.count() > 0:
        return redirect(url_for("auth.login"))
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        if not username:
            flash("Username is required.", "danger")
            return render_template("setup.html"), 400
        user = User(username=username, role=User.ROLE_OWNER)
        try:
            user.set_password(request.form.get("password", ""))
        except ValueError as e:
            flash(str(e), "danger")
            return render_template("setup.html"), 400
        db.session.add(user)
        db.session.commit()
        session["user_id"] = user.id
        flash("Owner account created.", "success")
        return redirect(url_for("dashboard.index"))
    return render_template("setup.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if User.query.count() == 0:
        return redirect(url_for("auth.setup"))
    if request.method == "POST":
        user = User.query.filter_by(username=(request.form.get("username") or "").strip()).first()
        if user is None or not user.check_password(request.form.get("password", "")):
            flash("Wrong username or password.", "danger")
            return render_template("login.html"), 401
        session.clear()
        session["user_id"] = user.id
        next_url = request.args.get("next")
        if next_url and next_url.startswith("/"):
            return redirect(next_url)
        return redirect(url_for("dashboard.index" if user.is_owner else "sales.index"))
    return render_template("login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@bp.route("/staff", methods=["POST"])
@owner_required
def add_staff():
    """The owner creates a staff account."""
    username = (request.form.get("username") or "").strip()
    if not username or User.query.filter_by(username=username).first():
        flash("Choose a new, non-empty username.", "danger")
        return redirect(url_for("dashboard.index"))
    user = User(username=username, role=User.ROLE_STAFF)
    try:
        user.set_password(request.form.get("password", ""))
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("dashboard.index"))
    db.session.add(user)
    db.session.commit()
    flash(f"Staff account '{username}' created.", "success")
    return redirect(url_for("dashboard.index"))

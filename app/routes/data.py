"""Import page (CSV with validation) and JSON-LD export of products, for the owner (story S7)."""
from flask import Blueprint, Response, flash, render_template, request

from app.auth import owner_required
from app.services.import_service import ImportFileError, ImportService

bp = Blueprint("data", __name__, url_prefix="/data")


@bp.route("/import", methods=["GET", "POST"])
@owner_required
def import_products():
    """Upload a CSV file; valid rows are saved and invalid rows are listed with line number and reason."""
    result = None
    if request.method == "POST":
        upload = request.files.get("file")
        if upload is None or not upload.filename:
            flash("Choose a CSV file first.", "danger")
            return render_template("import.html", result=None), 400
        try:
            text = upload.read().decode("utf-8-sig")
            result = ImportService.import_csv(text)
        except UnicodeDecodeError:
            flash("The file is not a UTF-8 text/CSV file. In Excel use 'Save as > CSV UTF-8'.", "danger")
            return render_template("import.html", result=None), 400
        except ImportFileError as e:
            flash(str(e), "danger")
            return render_template("import.html", result=None), 400
        flash(f"{result.created} added, {result.updated} updated, {len(result.errors)} rejected.",
              "warning" if result.errors else "success")
    return render_template("import.html", result=result)


@bp.route("/products.jsonld", methods=["GET"])
@owner_required
def export_products_jsonld():
    """Download all products as JSON-LD (schema.org terms)."""
    return Response(
        ImportService.export_jsonld(),
        mimetype="application/ld+json",
        headers={"Content-Disposition": "attachment; filename=products.jsonld"},
    )

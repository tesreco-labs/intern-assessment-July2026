from flask import Blueprint, abort, current_app, jsonify, redirect, render_template, request, url_for

from database.intern_crud import (
    delete_intern,
    get_all_interns,
    get_intern_by_id,
    insert_intern,
    update_intern,
)

intern_bp = Blueprint("intern", __name__)


@intern_bp.route("/add-intern")
def add_page():
    return render_template("add_intern.html")


@intern_bp.route("/view-interns")
@intern_bp.route("/view-intern")
def view_page():
    interns = get_all_interns()

    return render_template(
        "view_intern.html",
        interns=interns,
    )


@intern_bp.route("/register-form", methods=["POST"])
def register_form():
    try:
        insert_intern(
            request.form["name"],
            request.form["email"],
            request.form["domain"],
            request.form["duration"],
        )
    except Exception:
        current_app.logger.exception("Failed to register intern from form")
        raise

    return redirect(url_for("intern.view_page"))


@intern_bp.route("/edit-intern/<int:id>")
def edit_intern_page(id):
    intern = get_intern_by_id(id)
    if intern is None:
        abort(404)

    return render_template("edit_intern.html", intern=intern)


@intern_bp.route("/update-intern/<int:id>", methods=["POST"])
def update_intern_form(id):
    try:
        updated_rows = update_intern(
            id,
            request.form["name"],
            request.form["email"],
            request.form["domain"],
            request.form["duration"],
        )
    except Exception:
        current_app.logger.exception("Failed to update intern %s from form", id)
        raise

    if updated_rows == 0:
        abort(404)

    return redirect(url_for("intern.view_page"))


@intern_bp.route("/delete-intern/<int:id>")
def delete_intern_page(id):
    try:
        delete_intern(id)
    except Exception:
        current_app.logger.exception("Failed to delete intern %s from page", id)
        raise

    return redirect(url_for("intern.view_page"))


@intern_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}

    name = data.get("name")
    email = data.get("email")
    domain = data.get("domain")
    duration = data.get("duration")

    try:
        intern_id = insert_intern(name, email, domain, duration)
    except Exception:
        current_app.logger.exception("Failed to register intern from API")
        raise

    return jsonify({
        "id": intern_id,
        "message": "Intern registered successfully",
    }), 201


@intern_bp.route("/interns", methods=["GET"])
def view_interns():
    interns = get_all_interns()

    return jsonify([dict(row) for row in interns])


@intern_bp.route("/intern/<int:id>", methods=["PUT"])
def edit_intern(id):
    data = request.get_json() or {}

    try:
        updated_rows = update_intern(
            id,
            data["name"],
            data["email"],
            data["domain"],
            data["duration"],
        )
    except Exception:
        current_app.logger.exception("Failed to update intern %s from API", id)
        raise

    if updated_rows == 0:
        return jsonify({"error": "Intern not found"}), 404

    return jsonify({
        "message": "Updated successfully",
    })


@intern_bp.route("/intern/<int:id>", methods=["DELETE"])
def remove_intern(id):
    try:
        deleted_rows = delete_intern(id)
    except Exception:
        current_app.logger.exception("Failed to delete intern %s from API", id)
        raise

    if deleted_rows == 0:
        return jsonify({"error": "Intern not found"}), 404

    return jsonify({
        "message": "Deleted successfully",
    })

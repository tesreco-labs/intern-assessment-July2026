import logging
import re
import sqlite3
from pathlib import Path
from urllib.parse import quote

from flask import Flask, jsonify, redirect, render_template, request, url_for
from werkzeug.exceptions import HTTPException


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "interns.db"
LOG_PATH = BASE_DIR / "tesreco.log"
DOMAINS = ["Python Programming", "Flask Web Development", "Data Science", "Database Handling"]

app = Flask(__name__)


def get_logger():
    logger = logging.getLogger("tesreco-flask")
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler = logging.FileHandler(LOG_PATH)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


logger = get_logger()
EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def get_connection():
    db_uri = f"file:{quote(DB_PATH.resolve().as_posix(), safe='/:')}?nolock=1"
    connection = sqlite3.connect(db_uri, uri=True)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA journal_mode = OFF")
    connection.execute("PRAGMA temp_store = MEMORY")
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS Interns (
                intern_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                domain TEXT NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS Mentors (
                mentor_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                specialization TEXT NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS Attendance (
                attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
                intern_id TEXT NOT NULL,
                date TEXT NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (intern_id) REFERENCES Interns(intern_id) ON DELETE CASCADE
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS MentorAssignments (
                assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                intern_id TEXT NOT NULL,
                mentor_id TEXT NOT NULL,
                assigned_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (intern_id, mentor_id),
                FOREIGN KEY (intern_id) REFERENCES Interns(intern_id) ON DELETE CASCADE,
                FOREIGN KEY (mentor_id) REFERENCES Mentors(mentor_id) ON DELETE CASCADE
            )
            """
        )
        connection.executemany(
            """
            INSERT OR IGNORE INTO Mentors (mentor_id, name, specialization)
            VALUES (?, ?, ?)
            """,
            [
                ("M001", "Amit", "Python"),
                ("M002", "Neha", "Data Science"),
                ("M003", "Rohit", "Flask"),
            ],
        )
        connection.commit()


def row_to_dict(row):
    return dict(row) if row else None


def get_all_interns():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT intern_id, name, email, domain FROM Interns ORDER BY intern_id"
        ).fetchall()
        return [row_to_dict(row) for row in rows]


def get_intern(intern_id):
    with get_connection() as connection:
        row = connection.execute(
            "SELECT intern_id, name, email, domain FROM Interns WHERE intern_id = ?",
            (intern_id,),
        ).fetchone()
        return row_to_dict(row)


def next_intern_id():
    with get_connection() as connection:
        rows = connection.execute("SELECT intern_id FROM Interns").fetchall()

    highest_number = 0
    for row in rows:
        value = row["intern_id"]
        if value.startswith("TES") and value[3:].isdigit():
            highest_number = max(highest_number, int(value[3:]))
    return f"TES{highest_number + 1:03d}"


def validate_intern_payload(data):
    required_fields = ["name", "email", "domain"]
    missing = [field for field in required_fields if not data.get(field)]
    if missing:
        return f"Missing fields: {', '.join(missing)}"
    if not EMAIL_PATTERN.match(data["email"]):
        return "Invalid email address"
    return None


def insert_intern(name, email, domain):
    intern_id = next_intern_id()
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO Interns (intern_id, name, email, domain)
            VALUES (?, ?, ?, ?)
            """,
            (intern_id, name, email, domain),
        )
        connection.commit()
    return get_intern(intern_id)


@app.route("/")
def home():
    return render_template("home.html", domains=DOMAINS, interns=get_all_interns())


@app.route("/about")
def about():
    return render_template("about.html", domains=DOMAINS)


@app.route("/register", methods=["POST"])
def register_intern():
    data = request.get_json(silent=True) or {}
    error = validate_intern_payload(data)
    if error:
        logger.error("Error: %s", error)
        return jsonify({"error": error}), 400

    try:
        intern = insert_intern(data["name"], data["email"], data["domain"])
    except sqlite3.IntegrityError:
        logger.error("Error: Email already registered")
        return jsonify({"error": "Email already registered"}), 409

    return jsonify({"message": "Intern registered successfully", "intern": intern}), 201


@app.route("/interns", methods=["GET"])
def interns_api():
    logger.info("Report generation activity: Intern list generated")
    return jsonify(get_all_interns())


@app.route("/intern/<intern_id>", methods=["PUT"])
def update_intern_api(intern_id):
    current = get_intern(intern_id)
    if not current:
        return jsonify({"error": "Intern not found"}), 404

    data = request.get_json(silent=True) or {}
    updated = {
        "name": data.get("name", current["name"]),
        "email": data.get("email", current["email"]),
        "domain": data.get("domain", current["domain"]),
    }
    error = validate_intern_payload(updated)
    if error:
        logger.error("Error: %s", error)
        return jsonify({"error": error}), 400

    try:
        with get_connection() as connection:
            connection.execute(
                """
                UPDATE Interns
                SET name = ?, email = ?, domain = ?
                WHERE intern_id = ?
                """,
                (updated["name"], updated["email"], updated["domain"], intern_id),
            )
            connection.commit()
    except sqlite3.IntegrityError:
        logger.error("Error: Email already registered")
        return jsonify({"error": "Email already registered"}), 409

    return jsonify({"message": "Intern updated successfully", "intern": get_intern(intern_id)})


@app.route("/intern/<intern_id>", methods=["DELETE"])
def delete_intern_api(intern_id):
    with get_connection() as connection:
        cursor = connection.execute("DELETE FROM Interns WHERE intern_id = ?", (intern_id,))
        connection.commit()

    if cursor.rowcount == 0:
        return jsonify({"error": "Intern not found"}), 404

    return jsonify({"message": "Intern deleted successfully"})


@app.route("/attendance", methods=["POST"])
def attendance_api():
    data = request.get_json(silent=True) or {}
    required_fields = ["intern_id", "date", "status"]
    missing = [field for field in required_fields if not data.get(field)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400
    if not get_intern(data["intern_id"]):
        return jsonify({"error": "Intern not found"}), 404

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO Attendance (intern_id, date, status)
            VALUES (?, ?, ?)
            """,
            (data["intern_id"], data["date"], data["status"]),
        )
        connection.commit()

    return jsonify({"message": "Attendance stored successfully"}), 201


@app.route("/assign-mentor", methods=["POST"])
def assign_mentor_api():
    data = request.get_json(silent=True) or {}
    required_fields = ["intern_id", "mentor_id"]
    missing = [field for field in required_fields if not data.get(field)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    with get_connection() as connection:
        intern = connection.execute(
            "SELECT intern_id FROM Interns WHERE intern_id = ?",
            (data["intern_id"],),
        ).fetchone()
        mentor = connection.execute(
            "SELECT mentor_id FROM Mentors WHERE mentor_id = ?",
            (data["mentor_id"],),
        ).fetchone()
        if not intern:
            return jsonify({"error": "Intern not found"}), 404
        if not mentor:
            return jsonify({"error": "Mentor not found"}), 404
        try:
            connection.execute(
                """
                INSERT INTO MentorAssignments (intern_id, mentor_id)
                VALUES (?, ?)
                """,
                (data["intern_id"], data["mentor_id"]),
            )
            connection.commit()
        except sqlite3.IntegrityError:
            return jsonify({"error": "Mentor already assigned to this intern"}), 409

    return jsonify({"message": "Mentor assigned successfully"}), 201


@app.route("/add-intern", methods=["GET", "POST"])
def add_intern_page():
    if request.method == "POST":
        form_data = {
            "name": request.form.get("name", "").strip(),
            "email": request.form.get("email", "").strip(),
            "domain": request.form.get("domain", "").strip(),
        }
        error = validate_intern_payload(form_data)
        if error:
            return render_template("interns/add.html", error=error, form=form_data)
        try:
            insert_intern(form_data["name"], form_data["email"], form_data["domain"])
        except sqlite3.IntegrityError:
            return render_template(
                "interns/add.html",
                error="Email already registered",
                form=form_data,
            )
        return redirect(url_for("view_interns_page"))

    return render_template("interns/add.html", form={})


@app.route("/view-interns")
def view_interns_page():
    return render_template("interns/list.html", interns=get_all_interns())


@app.route("/edit-intern/<intern_id>", methods=["GET", "POST"])
def edit_intern_page(intern_id):
    intern = get_intern(intern_id)
    if not intern:
        return render_template("interns/list.html", interns=get_all_interns(), error="Intern not found"), 404

    if request.method == "POST":
        form_data = {
            "name": request.form.get("name", "").strip(),
            "email": request.form.get("email", "").strip(),
            "domain": request.form.get("domain", "").strip(),
        }
        error = validate_intern_payload(form_data)
        if error:
            return render_template("interns/edit.html", intern={**intern, **form_data}, error=error)

        try:
            with get_connection() as connection:
                connection.execute(
                    """
                    UPDATE Interns
                    SET name = ?, email = ?, domain = ?
                    WHERE intern_id = ?
                    """,
                    (form_data["name"], form_data["email"], form_data["domain"], intern_id),
                )
                connection.commit()
        except sqlite3.IntegrityError:
            return render_template("interns/edit.html", intern={**intern, **form_data}, error="Email already registered")
        return redirect(url_for("view_interns_page"))

    return render_template("interns/edit.html", intern=intern)


@app.route("/delete-intern/<intern_id>", methods=["GET", "POST"])
def delete_intern_page(intern_id):
    intern = get_intern(intern_id)
    if not intern:
        return render_template("interns/list.html", interns=get_all_interns(), error="Intern not found"), 404

    if request.method == "POST":
        with get_connection() as connection:
            connection.execute("DELETE FROM Interns WHERE intern_id = ?", (intern_id,))
            connection.commit()
        return redirect(url_for("view_interns_page"))

    return render_template("interns/delete.html", intern=intern)


@app.errorhandler(Exception)
def handle_error(error):
    if isinstance(error, HTTPException):
        return error

    logger.exception("Error: %s", error)
    return jsonify({"error": "Internal server error"}), 500


init_db()


if __name__ == "__main__":
    logger.info("Login event: Flask application started")
    app.run(debug=True)

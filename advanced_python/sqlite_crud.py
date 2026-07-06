import sqlite3
from pathlib import Path
from urllib.parse import quote


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "interns.db"


def get_connection(db_path=DB_PATH):
    db_uri = f"file:{quote(Path(db_path).resolve().as_posix(), safe='/:')}?nolock=1"
    connection = sqlite3.connect(db_uri, uri=True)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA journal_mode = OFF")
    connection.execute("PRAGMA temp_store = MEMORY")
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db(db_path=DB_PATH):
    with get_connection(db_path) as connection:
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
        connection.commit()


def create_intern(intern_id, name, email, domain, db_path=DB_PATH):
    with get_connection(db_path) as connection:
        connection.execute(
            """
            INSERT OR REPLACE INTO Interns (intern_id, name, email, domain)
            VALUES (?, ?, ?, ?)
            """,
            (intern_id, name, email, domain),
        )
        connection.commit()


def read_interns(db_path=DB_PATH):
    with get_connection(db_path) as connection:
        rows = connection.execute("SELECT * FROM Interns ORDER BY intern_id").fetchall()
        return [dict(row) for row in rows]


def update_intern(intern_id, name, email, domain, db_path=DB_PATH):
    with get_connection(db_path) as connection:
        cursor = connection.execute(
            """
            UPDATE Interns
            SET name = ?, email = ?, domain = ?
            WHERE intern_id = ?
            """,
            (name, email, domain, intern_id),
        )
        connection.commit()
        return cursor.rowcount > 0


def delete_intern(intern_id, db_path=DB_PATH):
    with get_connection(db_path) as connection:
        cursor = connection.execute(
            "DELETE FROM Interns WHERE intern_id = ?",
            (intern_id,),
        )
        connection.commit()
        return cursor.rowcount > 0


def create_mentor(mentor_id, name, specialization, db_path=DB_PATH):
    with get_connection(db_path) as connection:
        connection.execute(
            """
            INSERT OR REPLACE INTO Mentors (mentor_id, name, specialization)
            VALUES (?, ?, ?)
            """,
            (mentor_id, name, specialization),
        )
        connection.commit()


def read_mentors(db_path=DB_PATH):
    with get_connection(db_path) as connection:
        rows = connection.execute("SELECT * FROM Mentors ORDER BY mentor_id").fetchall()
        return [dict(row) for row in rows]


def update_mentor(mentor_id, name, specialization, db_path=DB_PATH):
    with get_connection(db_path) as connection:
        cursor = connection.execute(
            """
            UPDATE Mentors
            SET name = ?, specialization = ?
            WHERE mentor_id = ?
            """,
            (name, specialization, mentor_id),
        )
        connection.commit()
        return cursor.rowcount > 0


def delete_mentor(mentor_id, db_path=DB_PATH):
    with get_connection(db_path) as connection:
        cursor = connection.execute(
            "DELETE FROM Mentors WHERE mentor_id = ?",
            (mentor_id,),
        )
        connection.commit()
        return cursor.rowcount > 0

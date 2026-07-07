import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from database.db_connect import db_connection


REQUIRED_NOT_NULL = {
    "interns": {"name", "email", "domain", "duration"},
    "attendance": {"intern_id", "date", "status"},
    "mentors": {"name", "specialization"},
    "assignment": {"intern_id", "mentor_id"},
}


CREATE_TABLES_SQL = """
    CREATE TABLE IF NOT EXISTS interns(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        domain TEXT NOT NULL,
        duration INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS attendance(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        intern_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY(intern_id) REFERENCES interns(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS mentors(
        mentor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialization TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS assignment(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        intern_id INTEGER NOT NULL,
        mentor_id INTEGER NOT NULL,
        FOREIGN KEY(intern_id) REFERENCES interns(id) ON DELETE CASCADE,
        FOREIGN KEY(mentor_id) REFERENCES mentors(mentor_id) ON DELETE CASCADE
    );
"""


REBUILD_SCHEMA_SQL = """
    CREATE TABLE interns_new(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        domain TEXT NOT NULL,
        duration INTEGER NOT NULL
    );

    CREATE TABLE attendance_new(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        intern_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY(intern_id) REFERENCES interns_new(id) ON DELETE CASCADE
    );

    CREATE TABLE mentors_new(
        mentor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialization TEXT NOT NULL
    );

    CREATE TABLE assignment_new(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        intern_id INTEGER NOT NULL,
        mentor_id INTEGER NOT NULL,
        FOREIGN KEY(intern_id) REFERENCES interns_new(id) ON DELETE CASCADE,
        FOREIGN KEY(mentor_id) REFERENCES mentors_new(mentor_id) ON DELETE CASCADE
    );

    INSERT INTO interns_new(id, name, email, domain, duration)
    SELECT id, name, email, domain, duration
    FROM interns
    WHERE name IS NOT NULL
      AND email IS NOT NULL
      AND domain IS NOT NULL
      AND duration IS NOT NULL;

    INSERT INTO mentors_new(mentor_id, name, specialization)
    SELECT mentor_id, name, specialization
    FROM mentors
    WHERE name IS NOT NULL
      AND specialization IS NOT NULL;

    INSERT INTO attendance_new(id, intern_id, date, status)
    SELECT a.id, a.intern_id, a.date, a.status
    FROM attendance a
    JOIN interns_new i ON a.intern_id = i.id
    WHERE a.intern_id IS NOT NULL
      AND a.date IS NOT NULL
      AND a.status IS NOT NULL;

    INSERT INTO assignment_new(id, intern_id, mentor_id)
    SELECT a.id, a.intern_id, a.mentor_id
    FROM assignment a
    JOIN interns_new i ON a.intern_id = i.id
    JOIN mentors_new m ON a.mentor_id = m.mentor_id
    WHERE a.intern_id IS NOT NULL
      AND a.mentor_id IS NOT NULL;

    DROP TABLE assignment;
    DROP TABLE attendance;
    DROP TABLE mentors;
    DROP TABLE interns;

    ALTER TABLE interns_new RENAME TO interns;
    ALTER TABLE attendance_new RENAME TO attendance;
    ALTER TABLE mentors_new RENAME TO mentors;
    ALTER TABLE assignment_new RENAME TO assignment;
"""


def _has_required_not_null(conn, table):
    required_columns = REQUIRED_NOT_NULL[table]
    columns = conn.execute(f"PRAGMA table_info({table})").fetchall()
    not_null_columns = {column[1] for column in columns if column[3]}
    return required_columns.issubset(not_null_columns)


def _has_cascade_foreign_keys(conn, table, expected_foreign_tables):
    foreign_keys = conn.execute(f"PRAGMA foreign_key_list({table})").fetchall()
    cascaded_tables = {row[2] for row in foreign_keys if row[6].upper() == "CASCADE"}
    return expected_foreign_tables.issubset(cascaded_tables)


def _schema_needs_rebuild(conn):
    for table in REQUIRED_NOT_NULL:
        if not _has_required_not_null(conn, table):
            return True

    return not (
        _has_cascade_foreign_keys(conn, "attendance", {"interns"})
        and _has_cascade_foreign_keys(conn, "assignment", {"interns", "mentors"})
    )


def init_db():
    with db_connection(commit=True) as conn:
        conn.executescript(CREATE_TABLES_SQL)

        if _schema_needs_rebuild(conn):
            conn.execute("PRAGMA foreign_keys = OFF")
            conn.executescript(REBUILD_SCHEMA_SQL)
            conn.execute("PRAGMA foreign_keys = ON")

            violations = conn.execute("PRAGMA foreign_key_check").fetchall()
            if violations:
                raise RuntimeError(f"Foreign key violations after schema migration: {violations}")


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")

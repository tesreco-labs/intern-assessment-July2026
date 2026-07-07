from database.db_connect import db_connection


def insert_intern(name, email, domain, duration):
    with db_connection(commit=True) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO interns(name,email,domain,duration)
            VALUES(?,?,?,?)
            """,
            (name, email, domain, duration),
        )
        return cursor.lastrowid


def get_all_interns():
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM interns ORDER BY id DESC")
        return cursor.fetchall()


def get_intern_by_id(id):
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM interns WHERE id=?", (id,))
        return cursor.fetchone()


def update_intern(id, name, email, domain, duration):
    with db_connection(commit=True) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE interns
            SET name=?, email=?, domain=?, duration=?
            WHERE id=?
            """,
            (name, email, domain, duration, id),
        )
        return cursor.rowcount


def delete_intern(id):
    with db_connection(commit=True) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM interns WHERE id=?",
            (id,),
        )
        return cursor.rowcount


def count_interns():
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM interns")
        return cursor.fetchone()["total"]

from database.db_connect import db_connection


# Create Mentor
def insert_mentor(name, specialization):
    with db_connection(commit=True) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO mentors(name, specialization)
            VALUES (?, ?)
            """,
            (name, specialization),
        )
        return cursor.lastrowid


# Get All Mentors
def get_all_mentors():
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM mentors ORDER BY mentor_id DESC
            """
        )
        return cursor.fetchall()


# Assign Mentor to Intern
def assign_mentor(intern_id, mentor_id):
    with db_connection(commit=True) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO assignment(intern_id, mentor_id)
            VALUES (?, ?)
            """,
            (intern_id, mentor_id),
        )
        return cursor.lastrowid


# View Assignments
def get_assignments():
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                a.id,
                i.name AS intern_name,
                m.name AS mentor_name,
                m.specialization
            FROM assignment a
            JOIN interns i ON a.intern_id = i.id
            JOIN mentors m ON a.mentor_id = m.mentor_id
            ORDER BY a.id DESC
            """
        )
        return cursor.fetchall()


def count_mentors():
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM mentors")
        return cursor.fetchone()["total"]


def count_assignments():
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM assignment")
        return cursor.fetchone()["total"]

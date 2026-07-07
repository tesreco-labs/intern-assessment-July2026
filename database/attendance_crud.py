from database.db_connect import db_connection


def add_attendance(intern_id, date, status):
    with db_connection(commit=True) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO attendance(intern_id,date,status)
            VALUES(?,?,?)
        """, (intern_id, date, status))
        return cursor.lastrowid


def get_attendance():
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                attendance.id,
                attendance.intern_id,
                interns.name AS intern_name,
                attendance.date,
                attendance.status
            FROM attendance
            LEFT JOIN interns ON attendance.intern_id = interns.id
            ORDER BY attendance.date DESC, attendance.id DESC
        """)
        return cursor.fetchall()


def count_attendance():
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM attendance")
        return cursor.fetchone()["total"]

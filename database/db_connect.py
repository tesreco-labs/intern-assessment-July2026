import sqlite3
from contextlib import contextmanager

from utils.logger_config import logger


def get_connection():
    conn = sqlite3.connect("interns.db")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@contextmanager
def db_connection(commit=False):
    conn = get_connection()

    try:
        yield conn
        if commit:
            conn.commit()
    except Exception:
        if commit:
            conn.rollback()
        logger.exception("Database operation failed")
        raise
    finally:
        conn.close()

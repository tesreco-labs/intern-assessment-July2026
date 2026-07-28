# Architecture Notes

## Application structure

```text
app.py                 Flask app factory-style entry point and blueprint registration
database/              SQLite connection, schema initialization, and CRUD helpers
routes/                Flask blueprints for web pages and JSON endpoints
models/                OOP examples used for assessment concepts
utils/                 Utility examples for decorators, iterators, generators, validation, logging, and functional programming
concurrency/           Threading example
templates/             Jinja2 HTML templates
static/                CSS and images
docs/                  Project documentation
```

## Runtime sequence

1. The developer runs `python app.py`.
2. `app.py` imports `init_db` and calls it before registering blueprints.
3. `init_db()` opens a SQLite connection with foreign keys enabled.
4. The schema is created if it does not exist.
5. Existing schema constraints are inspected and rebuilt if required.
6. Flask registers home, intern, attendance, and mentor blueprints.
7. Browser routes render templates and API routes return JSON responses.

## Database behavior

- Connections are created by `database/db_connect.py`.
- `db_connection(commit=True)` commits successful write operations and rolls back failed write operations.
- Foreign keys are enabled with `PRAGMA foreign_keys = ON` for each connection.
- Attendance records reference `interns.id`.
- Assignment records reference both `interns.id` and `mentors.mentor_id`.
- Deleting an intern cascades to related attendance and assignment records.
- Deleting a mentor cascades to related assignment records.

## Blueprint responsibilities

| Blueprint | File | Responsibility |
| --- | --- | --- |
| `home_bp` | `routes/home_routes.py` | Login, home, dashboard, and about pages. |
| `intern_bp` | `routes/intern_routes.py` | Intern forms and intern JSON API. |
| `attendance_bp` | `routes/attendance_routes.py` | Attendance page and attendance JSON API. |
| `mentor_bp` | `routes/mentor_routes.py` | Mentor page, assignment page, and mentor JSON APIs. |

## Current limitations and improvement opportunities

- Authentication is a simple hard-coded credential check and should not be used as production security.
- Dependencies are not pinned in a requirements file.
- API validation is minimal; missing fields or invalid foreign keys rely mostly on Python exceptions or SQLite constraints.
- Automated tests are not currently included.
- The SQLite database path is relative to the command working directory.

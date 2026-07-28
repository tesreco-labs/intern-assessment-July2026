# Project Information

## What this project does

The TESRECO Internship Management Portal is a Flask web application backed by SQLite. It supports basic internship operations for TESRECO, including intern registration and CRUD, attendance tracking, mentor creation, mentor assignment, dashboard metrics, browser-rendered pages, and JSON API endpoints.

## Main application flow

1. `app.py` creates the Flask application, initializes the database schema, and registers the route blueprints.
2. `database/init_db.py` creates or migrates the SQLite schema for interns, attendance, mentors, and mentor assignments.
3. `routes/` contains Flask blueprints for home/dashboard pages, intern operations, attendance operations, and mentor operations.
4. `database/*_crud.py` files contain the SQL operations used by the routes.
5. `templates/` contains the Jinja2 pages used by the web interface.
6. `static/` contains shared CSS and image assets.

## Core features

- Login page with a simple hard-coded admin credential check.
- Dashboard summary cards for total interns, mentors, attendance records, and assignments.
- Intern web workflow: add, view, edit, update, and delete interns.
- Intern JSON API: create, list, update, and delete interns.
- Attendance web and JSON API workflows.
- Mentor creation through web forms and JSON APIs.
- Mentor-to-intern assignment through web forms and JSON APIs.
- SQLite foreign keys with cascade delete behavior for dependent attendance and assignment records.

## Database tables

| Table | Purpose | Important columns |
| --- | --- | --- |
| `interns` | Stores intern profile records. | `id`, `name`, `email`, `domain`, `duration` |
| `attendance` | Stores dated attendance records for interns. | `id`, `intern_id`, `date`, `status` |
| `mentors` | Stores mentor records. | `mentor_id`, `name`, `specialization` |
| `assignment` | Stores intern-to-mentor assignments. | `id`, `intern_id`, `mentor_id` |

## Routes overview

### Browser pages

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/` | Login/index page. |
| `POST` | `/login` | Validates hard-coded admin credentials and redirects to dashboard. |
| `GET` | `/home` | Home page. |
| `GET` | `/dashboard` | Dashboard with aggregate counts. |
| `GET` | `/about` | About page. |
| `GET` | `/add-intern` | Intern registration form. |
| `POST` | `/register-form` | Creates an intern from form data. |
| `GET` | `/view-interns` or `/view-intern` | Lists interns. |
| `GET` | `/edit-intern/<id>` | Intern edit form. |
| `POST` | `/update-intern/<id>` | Updates an intern from form data. |
| `GET` | `/delete-intern/<id>` | Deletes an intern and redirects to the intern list. |
| `GET` | `/attendance-page` | Attendance form and attendance list. |
| `POST` | `/attendance-form` | Creates attendance from form data. |
| `GET` | `/mentor-page` | Mentor form and mentor list. |
| `POST` | `/mentor-form` | Creates a mentor from form data. |
| `GET` | `/assign-page` | Mentor assignment form and assignment list. |
| `POST` | `/assign-form` | Assigns a mentor from form data. |

### JSON APIs

| Method | Path | Description |
| --- | --- | --- |
| `POST` | `/register` | Creates an intern. |
| `GET` | `/interns` | Lists interns. |
| `PUT` | `/intern/<id>` | Updates an intern. |
| `DELETE` | `/intern/<id>` | Deletes an intern. |
| `POST` | `/attendance` | Creates attendance. |
| `GET` | `/attendance` | Lists attendance. |
| `POST` | `/mentor` | Creates a mentor. |
| `GET` | `/mentors` | Lists mentors. |
| `POST` | `/assign-mentor` | Assigns a mentor to an intern. |
| `GET` | `/assignments` | Lists assignments. |

## Advanced Python assessment examples

The repository also includes standalone examples that map to the technical assessment requirements:

- `utils/decorators.py`: execution-time logging decorator.
- `utils/iterator.py`: `TES001`, `TES002`, ... ID iterator.
- `utils/generators.py`: certificate generator.
- `utils/exceptions.py`: custom validation exceptions.
- `utils/copy_demo.py`: shallow copy vs. deep copy demonstration.
- `utils/functional.py`: `map`, `filter`, and `reduce` usage.
- `utils/logger_config.py`: file logger setup for `tesreco.log`.
- `models/mentor.py`: multiple inheritance and MRO demonstration.
- `models/reports.py`: abstract report base class and concrete reports.
- `concurrency/multithreading_demo.py`: multithreading example.
- `multiprocessing_demo.py`: multiprocessing report-generation example.

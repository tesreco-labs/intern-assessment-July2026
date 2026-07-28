# Setup Guide

## Prerequisites

- Python 3.10 or newer
- `pip`
- SQLite, which is included with standard Python installations

## Create a virtual environment

From the repository root:

```bash
python -m venv .venv
```

Activate it on Linux/macOS:

```bash
source .venv/bin/activate
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Activate it on Windows Command Prompt:

```bat
.venv\Scripts\activate.bat
```

## Install dependencies

The application currently depends on Flask:

```bash
pip install flask
```

## Initialize the database

```bash
python database/init_db.py
```

This creates or migrates `interns.db` with the required tables and foreign-key behavior.

## Run the application

```bash
python app.py
```

Open the app in a browser at:

```text
http://127.0.0.1:5000
```

## Default login

The current login route accepts these hard-coded credentials:

```text
Email: admin@tesreco.com
Password: admin123
```

## Useful manual checks

### Create an intern with the API

```bash
curl -X POST http://127.0.0.1:5000/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Vaibhav","email":"vaibhav@example.com","domain":"Data Science","duration":3}'
```

### List interns

```bash
curl http://127.0.0.1:5000/interns
```

### Create attendance

```bash
curl -X POST http://127.0.0.1:5000/attendance \
  -H "Content-Type: application/json" \
  -d '{"intern_id":1,"date":"2026-07-28","status":"Present"}'
```

### Create a mentor

```bash
curl -X POST http://127.0.0.1:5000/mentor \
  -H "Content-Type: application/json" \
  -d '{"name":"Rahul Sharma","specialization":"Machine Learning"}'
```

### Assign a mentor

```bash
curl -X POST http://127.0.0.1:5000/assign-mentor \
  -H "Content-Type: application/json" \
  -d '{"intern_id":1,"mentor_id":1}'
```

## Notes for development

- `app.py` calls `init_db()` on startup, so the schema is checked whenever the app starts.
- The SQLite database file path is currently relative: `interns.db` in the working directory.
- Logs are written to `tesreco.log` through `utils/logger_config.py`.
- There is no pinned dependency file yet; install Flask manually unless a dependency manifest is added later.

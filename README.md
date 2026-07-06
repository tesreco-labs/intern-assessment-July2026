# Intern Management System

This is a Flask project for managing interns and mentors. It allows you to add, edit, view, and delete interns, log their attendance, and assign them mentors.

## Features
- **Intern Management:** Create, read, update, and delete interns.
- **Attendance Tracking:** Log daily attendance for interns.
- **Mentor Assignment:** Assign specialized mentors to interns.
- **REST APIs:** Use APIs to manage interns and attendance programmatically.
- **Demo Page:** View demonstrations of advanced Python concepts in the project.

## How to Run the Project

1. Install Python (if you don't have it).
2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask application:
   ```bash
   python app.py
   ```
4. Open your browser and go to `http://127.0.0.1:5000/`.

## Folder Structure
- `app.py`: Main Flask application file.
- `config.py`: Configuration settings.
- `interns.db`: SQLite database file (created automatically).
- `templates/`: HTML files for the website.
- `advanced_python/`: Python scripts demonstrating different programming concepts.
- `requirements.txt`: List of dependencies.

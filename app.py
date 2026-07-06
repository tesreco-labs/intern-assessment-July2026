"""
TESRECO Intern Management Portal 
============================================================
"""

import os
import sqlite3
import time
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash

# Define file paths relative to root directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, 'interns.db')
LOG_FILE = os.path.join(BASE_DIR, 'tesreco.log')

# Setup Logging System
def setup_application_logging():
    logger = logging.getLogger('tesreco_app')
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
        file_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s'))
        logger.addHandler(file_handler)
    return logger

logger = setup_application_logging()

# Helper Function: Connect to SQLite DB
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Database Initialization
def init_sqlite_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Create Interns Table (Matches User Specified Schema Exactly)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interns(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            domain TEXT,
            duration INTEGER
        )
    ''')
    
    # 2. Create Attendance Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            intern_id INTEGER,
            date TEXT,
            status TEXT,
            FOREIGN KEY (intern_id) REFERENCES interns(id)
        )
    ''')
    
    # 3. Create Mentors Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mentors(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT NOT NULL
        )
    ''')
    
    # 4. Create Mentor Assignments Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mentor_assignments(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            intern_id INTEGER,
            mentor_id INTEGER,
            assigned_date TEXT,
            FOREIGN KEY (intern_id) REFERENCES interns(id),
            FOREIGN KEY (mentor_id) REFERENCES mentors(id)
        )
    ''')
    
    # Pre-populate sample mentors if table is empty
    cursor.execute('SELECT COUNT(*) FROM mentors')
    if cursor.fetchone()[0] == 0:
        sample_mentors = [
            ('Dr. Sharma', 'Machine Learning'),
            ('Prof. Gupta', 'Web Development'),
            ('Ms. Patel', 'Data Science'),
            ('Mr. Singh', 'Python Development'),
            ('Dr. Verma', 'AI & NLP')
        ]
        cursor.executemany('INSERT INTO mentors (name, specialization) VALUES (?, ?)', sample_mentors)
        logger.info("Sample mentors populated in SQLite.")

    conn.commit()
    conn.close()

# Flask Setup
app = Flask(__name__)
app.secret_key = 'tesreco_super_secret_portal_key_2026'

# Initialize database at startup
init_sqlite_db()
logger.info("Database initialized successfully at startup.")


# =========================================================================
# PART B: WEB PAGE ROUTES (JINJA2 TEMPLATES)
# =========================================================================

# 16. TESRECO Home Page
@app.route('/')
def home():
    conn = get_db_connection()
    intern_count = conn.execute('SELECT COUNT(*) FROM interns').fetchone()[0]
    mentor_count = conn.execute('SELECT COUNT(*) FROM mentors').fetchone()[0]
    conn.close()
    
    return render_template('home.html', stats={"interns": intern_count, "mentors": mentor_count})

# 17. About TESRECO
@app.route('/about')
def about():
    domains = [
        {"name": "Data Science", "icon": "📊", "desc": "Analyze data, build models, and derive insights using Python, Pandas, and ML libraries."},
        {"name": "Web Development", "icon": "🌐", "desc": "Build modern web applications using Flask, SQLite, HTML/CSS, and JavaScript."},
        {"name": "Artificial Intelligence", "icon": "🤖", "desc": "Develop AI solutions including NLP, computer vision, and deep learning models."},
        {"name": "Python Development", "icon": "🐍", "desc": "Master Python programming with OOP, APIs, automation, and software design patterns."},
        {"name": "Cloud & DevOps", "icon": "☁️", "desc": "Learn cloud deployment, CI/CD pipelines, Docker, and infrastructure automation."},
        {"name": "Cybersecurity", "icon": "🔒", "desc": "Explore security testing, ethical hacking, and secure software development practices."}
    ]
    return render_template('about.html', domains=domains)

# 24. Flask CRUD Web Application: Add Intern Page
@app.route('/add-intern', methods=['GET', 'POST'])
def add_intern_page():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        domain = request.form.get('domain', '').strip()
        duration = request.form.get('duration', '').strip()

        if not name or not email or not domain or not duration:
            flash("All fields are required!", "error")
            return redirect(url_for('add_intern_page'))

        try:
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO interns (name, email, domain, duration) VALUES (?, ?, ?, ?)',
                (name, email, domain, int(duration))
            )
            conn.commit()
            conn.close()
            
            logger.info(f"Intern registered: {name} ({email})")
            flash(f"Intern {name} registered successfully!", "success")
            return redirect(url_for('view_interns_page'))
        except sqlite3.IntegrityError:
            flash(f"Error: Email '{email}' is already registered.", "error")
            logger.error(f"Failed registration attempt: duplicate email '{email}'")
        except Exception as e:
            flash(f"Registration Error: {str(e)}", "error")
            logger.error(f"Error saving intern: {str(e)}")

    return render_template('add_intern.html')

# 24. Flask CRUD Web Application: View Interns Page
@app.route('/view-interns')
def view_interns_page():
    conn = get_db_connection()
    interns = conn.execute('SELECT * FROM interns ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('view_interns.html', interns=interns)

# 24. Flask CRUD Web Application: Edit Intern Details Page
@app.route('/edit-intern/<int:id>', methods=['GET', 'POST'])
def edit_intern_page(id):
    conn = get_db_connection()
    intern = conn.execute('SELECT * FROM interns WHERE id = ?', (id,)).fetchone()
    
    if not intern:
        conn.close()
        flash("Intern record not found.", "error")
        return redirect(url_for('view_interns_page'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        domain = request.form.get('domain', '').strip()
        duration = request.form.get('duration', '').strip()

        if not name or not email or not domain or not duration:
            flash("All fields are required!", "error")
            return redirect(url_for('edit_intern_page', id=id))

        try:
            conn.execute(
                'UPDATE interns SET name = ?, email = ?, domain = ?, duration = ? WHERE id = ?',
                (name, email, domain, int(duration), id)
            )
            conn.commit()
            flash("Intern details updated successfully!", "success")
            logger.info(f"Intern ID {id} details updated.")
            conn.close()
            return redirect(url_for('view_interns_page'))
        except sqlite3.IntegrityError:
            flash(f"Error: Email '{email}' is already used by another intern.", "error")
        except Exception as e:
            flash(f"Update Error: {str(e)}", "error")
            logger.error(f"Error updating intern: {str(e)}")

    conn.close()
    return render_template('edit_intern.html', intern=intern)

# 24. Flask CRUD Web Application: Delete Intern Page
@app.route('/delete-intern/<int:id>', methods=['POST'])
def delete_intern_page(id):
    conn = get_db_connection()
    intern = conn.execute('SELECT * FROM interns WHERE id = ?', (id,)).fetchone()
    if not intern:
        conn.close()
        flash("Intern record not found.", "error")
        return redirect(url_for('view_interns_page'))

    conn.execute('DELETE FROM interns WHERE id = ?', (id,))
    # Delete related attendance and assignments to maintain reference integrity
    conn.execute('DELETE FROM attendance WHERE intern_id = ?', (id,))
    conn.execute('DELETE FROM mentor_assignments WHERE intern_id = ?', (id,))
    conn.commit()
    conn.close()
    
    flash(f"Intern record deleted successfully.", "success")
    logger.info(f"Intern ID {id} deleted along with attendance & mentor assignments.")
    return redirect(url_for('view_interns_page'))

# 22. Attendance Web Module & Listing Page
@app.route('/attendance', methods=['GET', 'POST'])
def attendance_page():
    conn = get_db_connection()
    if request.method == 'POST':
        intern_id = request.form.get('intern_id')
        date = request.form.get('date')
        status = request.form.get('status')

        if not intern_id or not date or not status:
            flash("All fields are required to log attendance!", "error")
        else:
            conn.execute(
                'INSERT INTO attendance (intern_id, date, status) VALUES (?, ?, ?)',
                (int(intern_id), date, status)
            )
            conn.commit()
            flash("Attendance logged successfully!", "success")
            logger.info(f"Attendance recorded for intern ID {intern_id} on {date}: {status}")

    interns = conn.execute('SELECT * FROM interns ORDER BY name').fetchall()
    # Fetch log with join
    records = conn.execute('''
        SELECT a.date, a.status, i.name as intern_name 
        FROM attendance a 
        JOIN interns i ON a.intern_id = i.id 
        ORDER BY a.id DESC
    ''').fetchall()
    conn.close()
    return render_template('attendance.html', interns=interns, records=records)

# 23. Mentor Assignment Module & Listing Page
@app.route('/assign-mentor', methods=['GET', 'POST'])
def assign_mentor_page():
    conn = get_db_connection()
    if request.method == 'POST':
        intern_id = request.form.get('intern_id')
        mentor_id = request.form.get('mentor_id')

        if not intern_id or not mentor_id:
            flash("All fields are required to assign a mentor!", "error")
        else:
            today_str = datetime.now().strftime("%Y-%m-%d")
            conn.execute(
                'INSERT INTO mentor_assignments (intern_id, mentor_id, assigned_date) VALUES (?, ?, ?)',
                (int(intern_id), int(mentor_id), today_str)
            )
            conn.commit()
            flash("Mentor assigned successfully!", "success")
            logger.info(f"Mentor ID {mentor_id} assigned to intern ID {intern_id}")

    interns = conn.execute('SELECT * FROM interns ORDER BY name').fetchall()
    mentors = conn.execute('SELECT * FROM mentors ORDER BY name').fetchall()
    assignments = conn.execute('''
        SELECT i.name as intern_name, m.name as mentor_name, m.specialization 
        FROM mentor_assignments ma 
        JOIN interns i ON ma.intern_id = i.id 
        JOIN mentors m ON ma.mentor_id = m.id 
        ORDER BY ma.id DESC
    ''').fetchall()
    conn.close()
    return render_template('assign_mentor.html', interns=interns, mentors=mentors, assignments=assignments)


# =========================================================================
# PART B: REST API ENDPOINTS (RETURNS JSON)
# =========================================================================

# 18. Register Intern API
@app.route('/register', methods=['POST'])
def register_intern_api():
    """
    Registers an intern.
    Expects JSON: { "name": "Vaibhav", "email": "Vaibhav@gmail.com", "domain": "Data Science" }
    Optional: "duration" (defaults to 3)
    """
    if not request.is_json:
        return jsonify({"error": "Request must be JSON format"}), 400
    
    data = request.get_json()
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    domain = data.get('domain', '').strip()
    duration = data.get('duration', 3)

    if not name or not email or not domain:
        return jsonify({"error": "Missing required fields (name, email, domain)"}), 400

    try:
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO interns (name, email, domain, duration) VALUES (?, ?, ?, ?)',
            (name, email, domain, int(duration))
        )
        conn.commit()
        conn.close()
        
        logger.info(f"API Register Success: {name}")
        return jsonify({"message": f"Intern {name} registered successfully!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": f"Email '{email}' is already registered."}), 400
    except Exception as e:
        logger.error(f"API Register Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

# 19. View Interns API
@app.route('/interns', methods=['GET'])
def view_interns_api():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM interns ORDER BY id').fetchall()
    conn.close()
    
    intern_list = [dict(row) for row in rows]
    return jsonify(intern_list), 200

# 20. Update Intern Details API
@app.route('/intern/<int:id>', methods=['PUT'])
def update_intern_api(id):
    if not request.is_json:
        return jsonify({"error": "Request must be JSON format"}), 400

    data = request.get_json()
    conn = get_db_connection()
    intern = conn.execute('SELECT * FROM interns WHERE id = ?', (id,)).fetchone()
    
    if not intern:
        conn.close()
        return jsonify({"error": "Intern record not found"}), 404

    name = data.get('name', intern['name'])
    email = data.get('email', intern['email'])
    domain = data.get('domain', intern['domain'])
    duration = data.get('duration', intern['duration'])

    try:
        conn.execute(
            'UPDATE interns SET name = ?, email = ?, domain = ?, duration = ? WHERE id = ?',
            (name, email, domain, int(duration), id)
        )
        conn.commit()
        conn.close()
        logger.info(f"API Update Success for Intern ID {id}")
        return jsonify({"message": "Intern updated successfully!"}), 200
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": f"Email '{email}' is already in use."}), 400
    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)}), 500

# 21. Delete Intern API
@app.route('/intern/<int:id>', methods=['DELETE'])
def delete_intern_api(id):
    conn = get_db_connection()
    intern = conn.execute('SELECT * FROM interns WHERE id = ?', (id,)).fetchone()
    
    if not intern:
        conn.close()
        return jsonify({"error": "Intern record not found"}), 404

    conn.execute('DELETE FROM interns WHERE id = ?', (id,))
    conn.execute('DELETE FROM attendance WHERE intern_id = ?', (id,))
    conn.execute('DELETE FROM mentor_assignments WHERE intern_id = ?', (id,))
    conn.commit()
    conn.close()
    
    logger.info(f"API Delete Success for Intern ID {id}")
    return jsonify({"message": f"Intern ID {id} deleted successfully."}), 200

# 22. Attendance Record API
@app.route('/attendance', methods=['POST'])
def attendance_api():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON format"}), 400
        
    data = request.get_json()
    intern_id = data.get('intern_id')
    date = data.get('date')
    status = data.get('status')
    
    if not intern_id or not date or not status:
        return jsonify({"error": "Missing required fields (intern_id, date, status)"}), 400
        
    conn = get_db_connection()
    intern = conn.execute('SELECT * FROM interns WHERE id = ?', (int(intern_id),)).fetchone()
    if not intern:
        conn.close()
        return jsonify({"error": f"Intern with ID {intern_id} does not exist"}), 404
        
    conn.execute(
        'INSERT INTO attendance (intern_id, date, status) VALUES (?, ?, ?)',
        (int(intern_id), date, status)
    )
    conn.commit()
    conn.close()
    logger.info(f"API Attendance logged for intern ID {intern_id}")
    return jsonify({"message": "Attendance logged successfully!"}), 201

# 23. Mentor Assignment API
@app.route('/assign-mentor', methods=['POST'])
def assign_mentor_api():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
        
    data = request.get_json()
    intern_id = data.get('intern_id')
    mentor_id = data.get('mentor_id')
    
    if not intern_id or not mentor_id:
        return jsonify({"error": "Missing required fields (intern_id, mentor_id)"}), 400
        
    conn = get_db_connection()
    intern = conn.execute('SELECT * FROM interns WHERE id = ?', (int(intern_id),)).fetchone()
    mentor = conn.execute('SELECT * FROM mentors WHERE id = ?', (int(mentor_id),)).fetchone()
    
    if not intern or not mentor:
        conn.close()
        return jsonify({"error": "Invalid Intern ID or Mentor ID"}), 400
        
    today_str = datetime.now().strftime("%Y-%m-%d")
    conn.execute(
        'INSERT INTO mentor_assignments (intern_id, mentor_id, assigned_date) VALUES (?, ?, ?)',
        (int(intern_id), int(mentor_id), today_str)
    )
    conn.commit()
    conn.close()
    logger.info(f"API Mentor ID {mentor_id} assigned to intern ID {intern_id}")
    return jsonify({"message": "Mentor assigned successfully!"}), 201


# =========================================================================
# INTERACTIVE DEMO PAGE: RUNS AND DISPLAYS TASKS 1-13
# =========================================================================
@app.route('/demo')
def python_demo_page():
    # 1. Intern Class
    from advanced_python.intern_class import Intern
    intern_obj = Intern("TES001", "Khushi", "khushi@tesreco.com", "Data Science", 3)
    intern_str = str(intern_obj)

    # 2. Performance Calculator
    from advanced_python.performance_calculator import calculate_performance
    scores = [78, 90, 65, 88, 95]
    perf_result = calculate_performance(scores)

    # 3. Custom Iterator
    from advanced_python.custom_iterator import InternIDIterator
    iterator = InternIDIterator(start=101, stop=105)
    generated_ids = list(iterator)

    # 4. Generator Function
    from advanced_python.certificate_generator import simple_certificate_generator
    generator_output = list(simple_certificate_generator(["Khushi", "Raushan"]))

    # 5. Exception Handling
    from advanced_python.exceptions import validate_intern_data, InvalidEmailError, InvalidDurationError
    exception_logs = []
    try:
        val_res = validate_intern_data("Khushi", "khushi@tesreco.com", "Data Science", 3)
        exception_logs.append(f"Valid Input Validated: {val_res}")
    except Exception as e:
        exception_logs.append(f"Error: {str(e)}")
    try:
        validate_intern_data("Raushan", "raushantesreco.com", "Data Science", 3)
    except InvalidEmailError as e:
        exception_logs.append(f"InvalidEmailError Caught: {str(e)}")
    try:
        validate_intern_data("Vaibhav", "vaibhav@tesreco.com", "Data Science", 15)
    except InvalidDurationError as e:
        exception_logs.append(f"InvalidDurationError Caught: {str(e)}")

    # 6. Shallow Copy vs Deep Copy
    from advanced_python.copy_demo import InternWithProjects
    import copy
    orig = InternWithProjects("Khushi", ["Web App", "API Design"])
    shallow = copy.copy(orig)
    deep = copy.deepcopy(orig)
    shallow.projects.append("ML Model")
    shallow_same = orig.projects is shallow.projects
    deep_same = orig.projects is deep.projects
    copy_results = {
        "original_projects": orig.projects,
        "shallow_projects": shallow.projects,
        "deep_projects": deep.projects,
        "shallow_shares_ref": shallow_same,
        "deep_shares_ref": deep_same
    }

    # 7. Multiple Inheritance & MRO
    from advanced_python.multiple_inheritance import TESRECOMentor
    mro_list = [cls.__name__ for cls in TESRECOMentor.__mro__]
    mentor_inst = TESRECOMentor("Dr. Sharma", 38, "EMP109", "AI & ML", "Natural Language Processing", 12)
    mentor_info = mentor_inst.display_info()
    mentor_greet = mentor_inst.greet()
    mentor_work = mentor_inst.work()
    mentor_advise = mentor_inst.mentor_intern("Khushi")

    # 8. Abstract Class
    from advanced_python.abstract_reports import AttendanceReport, PerformanceReport
    att_report = AttendanceReport().generate_report()
    perf_report = PerformanceReport().generate_report()

    # 9. Lambda & Functional Programming
    from advanced_python.functional_programming import functional_programming_demo
    func_prog_results = functional_programming_demo()

    # 10. File Handling
    from advanced_python.file_handling import add_record, search_record, delete_record, get_all_records
    add_record("DEMO99", "Demo User", "demo@tesreco.com", "Testing", 1)
    demo_search = search_record("name", "Demo User")
    demo_delete_status = delete_record("DEMO99")
    all_csv_records = get_all_records()

    # 11. Multithreading & 12. Multiprocessing
    thread_status = "Multithreading module runs Attendance Processing and Certificate Generation simultaneously."
    process_status = "Multiprocessing module utilizes a Pool of workers to calculate intern performance scores in parallel."

    # 13. Logging Output
    logger.info("Accessed Advanced Python Demonstration page from client.")
    with open(LOG_FILE, 'r', encoding='utf-8') as lf:
        log_lines = lf.readlines()[-15:]

    demo_data = {
        "intern_str": intern_str,
        "perf_result": perf_result,
        "generated_ids": generated_ids,
        "generator_output": generator_output,
        "exception_logs": exception_logs,
        "copy_results": copy_results,
        "mro_list": mro_list,
        "mentor_info": mentor_info,
        "mentor_greet": mentor_greet,
        "mentor_work": mentor_work,
        "mentor_advise": mentor_advise,
        "att_report": att_report,
        "perf_report": perf_report,
        "func_prog": func_prog_results,
        "csv_records": all_csv_records[:5],
        "csv_search": demo_search,
        "csv_delete": demo_delete_status,
        "thread_status": thread_status,
        "process_status": process_status,
        "log_lines": log_lines
    }

    return render_template('demo.html', demo=demo_data)


# 404 Error page handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('base.html', error_message="404 Page Not Found", title="Page Not Found"), 404

@app.route('/predict', methods=['POST'])
def predict():
    if not request.is_json:
        return jsonify({"error": "Request must be in JSON format"}), 400

    data = request.get_json()

    weight = data.get('weight')

    if weight is None:
        return jsonify({"error": "Weight is required"}), 400

    # Dummy prediction logic
    predicted_height = round((float(weight) * 0.5) + 100, 2)

    return jsonify({
        "weight": weight,
        "predicted_height": predicted_height
    }), 200

if __name__ == '__main__':
    # Clean setup & run
    print("--------------------------------------------------")
    print("TESRECO Intern Management Portal starting locally.")
    print("URL: http://127.0.0.1:5000/")
    print("--------------------------------------------------")
    app.run(host='127.0.0.1', port=5000, debug=True)

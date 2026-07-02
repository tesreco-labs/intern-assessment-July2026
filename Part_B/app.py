from flask import Flask, render_template, request, jsonify, redirect
from db import connect_db

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=['GET'])
def register_intern_get():
    return render_template('register_intern.html')

@app.route('/register', methods=['POST'])
def register_intern():
    # data = request.form.get('name')
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO interns(name,email,domain)
        VALUES(?,?,?)
    """, (
        request.form.get('name'),
        request.form.get('email'),
        request.form.get('domain')
    ))

    connection.commit()
    connection.close()

    return redirect('/interns')

@app.route('/interns', methods=['GET'])
def get_interns():

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM interns")

    interns = cursor.fetchall()

    data = []

    for row in interns:
        data.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "domain": row[3]
        })

    connection.close()

    return render_template('interns.html', interns=data)

@app.route('/intern/<int:id>', methods=['GET'])
def get_intern(id):
    
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT * FROM interns WHERE id=?               
    """, (id,))

    row = cursor.fetchone()

    connection.close()

    if not row:
        return "Not Found", 404

    intern = {
        "id": row[0],
        "name": row[1],
        "email": row[2],
        "domain": row[3]
    }

    return render_template("intern.html", intern=intern)

@app.route('/edit-intern/<int:id>')
def edit_page(id):
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM interns WHERE id=?", (id,))
    row = cursor.fetchone()

    intern = {
        "id": row[0],
        "name": row[1],
        "email": row[2],
        "domain": row[3]
    }

    return render_template("edit_intern.html", intern=intern)


@app.route('/attendance-form/<int:id>')
def attendance_page(id):
    return render_template("attendance.html", intern_id=id)


@app.route('/assign-mentor-form/<int:id>')
def mentor_page(id):
    return render_template("assign_mentor.html", intern_id=id)

@app.route('/intern/<int:id>', methods=['PUT'])
def update_intern(id):

    data = request.get_json()
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE interns
    SET name=?, email=?, domain=?
    WHERE id=?
    """, (
        data["name"],
        data["email"],
        data["domain"],
        id
    ))

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Intern Updated Successfully"
    })

@app.route('/intern/<int:id>', methods=['DELETE'])
def delete_intern(id):

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM interns WHERE id=?",
        (id,)
    )

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Intern Deleted Successfully"
    })

@app.route('/attendance', methods=['POST'])
def attendance():

    data = request.get_json()

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO attendance(
        intern_id,
        date,
        status
    )
    VALUES(?,?,?)
    """, (
        data['intern_id'],
        data['date'],
        data['status']
    ))

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Attendance Added"
    })

@app.route('/assign-mentor', methods=['POST'])
def assign_mentor():

    data = request.get_json()

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO mentors(
        intern_id,
        mentor_name
    )
    VALUES(?,?)
    """, (
        data['intern_id'],
        data['mentor_name']
    ))

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Mentor Assigned Successfully"
    })


if __name__ == "__main__":
    connect_db()
    app.run(debug=True)
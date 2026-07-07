from flask import Flask

from routes.intern_routes import intern_bp
from routes.attendance_routes import attendance_bp
from routes.mentor_routes import mentor_bp
from routes.home_routes import home_bp
from database.init_db import init_db

app = Flask(__name__)
init_db()

app.register_blueprint(home_bp)
app.register_blueprint(intern_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(mentor_bp)

if __name__ == "__main__":
    app.run(debug=True)

import os

class Config:
    # app secret key for sessions
    SECRET_KEY = 'secret_key_123'
    
    # database path
    basedir = os.path.abspath(os.path.dirname(__name__))
    DATABASE_URI = os.path.join(basedir, 'interns.db')

from flask import Flask
from utility import *
from database import db
import models

app = Flask(__name__)


# Create models












# Setup routes

@app.route('/')
def api_root():
    return 'Welcome'

@app.route('/hello')
def api_hello():
    return get_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
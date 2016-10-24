from flask import Flask
from utility import *
from database import db
import query
import models
import config

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


# Create models




# Setup routes

@app.route('/')
def api_root():
    return 'Welcome'

@app.route('/hello')
def api_hello():
    return get_db()

@app.route('/add/user')
def add_user():
    user = models.User(
        # device_id = "0001",
        first_name = "Christina",
        last_name = "Mosnick",
        username = "cmosnick",
        password = "pass",
        email = "cmosnick07@gmail.com",
        phone_number = "8159751442"
    )
    # return user.first_name
    # session = create_session
    return query.add(user)
    # return "User added: ";

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
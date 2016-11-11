from flask import Flask
import config
from app.database import db
from flask_cors import CORS, cross_origin
import os
from app.api.views import api

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    # Register blueprints below when created:
    app.register_blueprint(api, url_prefix='/api')


    CORS(app)
    app.secret_key = os.urandom(24)
    return app

app = create_app()
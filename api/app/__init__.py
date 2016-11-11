from flask import Flask
import config
from app.database import db
from flask_cors import CORS, cross_origin
import os
from app.views.image import image
from app.views.log import log
from app.views.settings import settings
from app.views.user import user

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    # Register blueprints below when created:
    app.register_blueprint(image, url_prefix='/image')
    app.register_blueprint(log, url_prefix='/log')
    app.register_blueprint(settings, url_prefix='') # do not chnage prefix here, keep routes as-is
    app.register_blueprint(user, url_prefix='/user')

    CORS(app)
    app.secret_key = os.urandom(24)
    return app

app = create_app()
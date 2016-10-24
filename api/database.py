from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import config

db = SQLAlchemy()
engine = create_engine(config.SQLALCHEMY_DATABASE_URI, echo=True)
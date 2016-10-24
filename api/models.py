# import json
# from flask import Flask
# from flask import jsonify
# from database import db
# from flask_sqlalchemy import SQLAlchemy
# import sqlalchemy
# from sqlalchemy.orm import class_mapper
# from sqlalchemy.ext.declarative import declared_attr
import config

from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine



# 
#   Base class for all models
# 

# class BaseModel(db.Model):
#     __abstract__ = True

#     # createdDate = db.Column(db.DateTime, server_default=db.func.now())
#     # modifiedDate = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
#     # versionID = db.Column(db.Integer, nullable=False)

#     __mapper_args__ = {
#         # "version_id_col": versionID
#     }

#     def dict(self):
#             result = {}
#             for prop in class_mapper(self.__class__).iterate_properties:
#                 if isinstance(prop, sqlalchemy.orm.ColumnProperty):
#                     result[prop.key] = getattr(self, prop.key)
#             return result

#     def json(self):
#         return jsonify(self.dict())

# # 
# #   Tables
# # 
# class User(BaseModel):
#     __tablename__ = 'users'

#     user_id = db.Column('user_id', db.Integer, primary_key=True)
#     device_id = db.Column('device_id', db.String, primary_key=True)
#     first_name = db.Column('first_name', db.String)
#     last_name = db.Column('last_name', db.String)
#     username = db.Column('username', db.String)
#     password = db.Column('password', db.String)
#     email = db.Column('email', db.String)
#     phone_number = db.Column('phone_number', db.String)


# class UserSettings(BaseModel):
#     __tablename__ = 'user_settings'

#     setting_id = db.Column('setting_id', db.Integer, primary_key=True)
#     user_id=db.Column('user_id', db.Integer, sqlalchemy.ForeignKey("users.user_id"), primary_key=True)
#     notification_option_id = db.Column('notification_option_id', db.Integer, sqlalchemy.ForeignKey("notification_options.notification_id"))
#     # TOOD: I don't think date time is correct.  Just want ToD?
#     start_time = db.Column('start_time', db.Time)
#     end_time = db.Column('end_time', db.Time)

# class Log(BaseModel):
#     __tablename__ = 'log'

#     log_id = db.Column('log_id', db.Integer, primary_key = True)
#     user_id = db.Column('user_id', db.Integer, sqlalchemy.ForeignKey("users.user_id"))
#     action = db.Column('action', db.Enum('image taken', 'text sent', 'sign in', 'sign out', 'alter accout', 'initial activation'))
#     date_time = db.Column('date_time', db.TIMESTAMP)
    
# class Images(BaseModel):
#     __tablename__ = 'images'

#     image_id = db.Column('image_id', db.Integer, primary_key = True)
#     user_id = db.Column('user_id', db.Integer, sqlalchemy.ForeignKey("users.user_id"))
#     image = db.Column('image', db.String)
#     date_time = db.Column('date_time', db.TIMESTAMP)

# class SentImages(BaseModel):
#     __tablename__ = 'sent_images'

#     image_id = db.Column('image_id', db.Integer, sqlalchemy.ForeignKey("images.image_id"), primary_key = True)
#     user_id = db.Column('user_id', db.Integer, sqlalchemy.ForeignKey("users.user_id"), primary_key=True)
#     date_time = db.Column('date_time', db.TIMESTAMP)
#     action = db.Column('action', db.Enum('text', 'email'))




# Auto map

Base = automap_base()
engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
Base.prepare(engine, reflect=True)

User = Base.classes.users


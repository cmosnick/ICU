from flask import jsonify
from sqlalchemy.ext.automap import automap_base
from app.database import engine



# Auto map databse tables into sqlalchemy objects
Base = automap_base()
Base.prepare(engine, reflect=True)

# Name the Sqlalchemy classes
SQLAUser = Base.classes.users
SQLANotOpts = Base.classes.notification_options
SQLAUserSetting = Base.classes.user_settings
SQLALog = Base.classes.log
SQLAImage = Base.classes.images
SQLASentImage = Base.classes.sent_images




# 
# Create an extension class for all sqlalchemy classes
# for easier querying and manipulation
# 

class CustomBase():
    fields = []

    def __init__(self, sqlAlchemyObject):
        self.sqlObj = sqlAlchemyObject
        
    def to_json(self):
        return jsonify(self.to_dict())

    def to_dict(self):
        obj = {}
        for field in self.fields:
            print self.sqlObj.__dict__[field]
            obj[field] = str(self.sqlObj.__dict__[field])
        return obj


# Customize for each table
class User(CustomBase, SQLAUser):
    fields = ["user_id", "device_id", "first_name", "last_name", "username", "hash", "phone_number", "email"]


class NotOpt(CustomBase, SQLANotOpts):
    fields = ["notification_id", "name"]


class UserSetting(CustomBase, SQLAUserSetting):
    fields = ["setting_id", "user_id", "notification_option_id", "start_time", "end_time"]


class Log(CustomBase, SQLALog):
    fields = ["log_id", "user_id", "action", "date_time"]


class Image(CustomBase, SQLAImage):
    fields = ["image_id", "user_id", "image", "date_time"]
    

class SentImage(CustomBase, SQLASentImage):
    fields = ["image_id", "user_id", "date_time", "action"]

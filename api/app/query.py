# TODO: determine standard return format for insert and update
from flask import jsonify
from app.database import engine
from app.models import *
from sqlalchemy.orm import sessionmaker


Session = sessionmaker(bind=engine)


def add(obj):
    session = Session()
    session.add(obj)
    session.commit()
    usersarray = []
    for row in session.query(SQLAUser).all():
        usersarray.append(SQLAUser)
    return jsonify(SQLAUser)

# TODO : don't search for device id in users table
# TODO : create function to look for device ID in devices table to retrieve user_id??
def get_user(user_id=None, username=None, device_id=None):
    session = Session()
    if user_id is not None:
        print user_id
        return session.query(SQLAUser).filter_by(user_id=user_id).first()
    elif username is not None:
        print username
        return session.query(SQLAUser).filter_by(username=username).first()
    elif device_id is not None:
        print device_id
        return session.query(SQLAUser).filter_by(device_id=device_id).first()
    else:
        raise Exception("Could not retrieve user")

def get_all_users():
    session = Session()
    return session.query(SQLAUser).order_by(User.username).all()

def get_user_id(username):
    session = Session()
    return session.query(SQLAUser).with_entities(SQLAUser.user_id).filter_by(username = username).first()

# TODO: hash password?
def login(user):
    session = Session()
    return session.query(SQLAUser).filter_by(username = user["username"]).first()

def update_user_settings(user_id, update_fields):
    session = Session()
    for field_w_value in update_fields:
        print field_w_value
        session.query(SQLAUserSetting).filter_by(user_id = user_id).update(field_w_value)
    session.commit()
    return str(user_id)


def add_user_settings(user_settings_info):
    session = Session()
    user_settings = SQLAUserSetting(
        user_id = int(user_settings_info['user_id']),
        notification_option_id = int(user_settings_info['notification_option_id']),
        start_time = user_settings_info['start_time'],
        end_time = user_settings_info['end_time']
    )
    session.add(user_settings)
    session.commit()
    return jsonify(user_settings_info)

#TODO : get rid of device id from this
def add_user(user_info):
    session = Session()
    user = SQLAUser(
        device_id = user_info['device_id'],
        first_name = user_info['first_name'],
        last_name = user_info['last_name'],
        username = user_info['username'],
        hash = user_info['hash'],
        phone_number = user_info['phone_number'],
        email = user_info['email']
    )
    session.add(user)
    session.flush()
    session.refresh(user)
    session.commit()
    return user.user_id


def add_log(log_info):
    session = Session()
    log = SQLALog(
        user_id = log_info['user_id'],
        action = log_info['action']
    )
    session.add(log)
    session.commit()
    return jsonify(log_info)


def get_logs_by_user(user_id=None, username=None):
    session = Session()
    if user_id is not None:
        return session.query(SQLALog).filter_by(user_id = user_id).all()
    elif username is not None:
        user = session.query(SQLAUser).filter_by(username = username).first()
        if user is not None:
            user_id = user.to_dict()['user_id']
            return session.query(SQLALog).filter_by(user_id = user_id).all()
        else:
            raise Exception("Could not find user based on username", 1)
    else:
        raise Exception("Could not retrieve logs for user", 1)


def get_not_opts(not_id=None):
    session = Session()
    return session.query(SQLANotOpts).filter_by(notification_id=not_id).all()


def get_all_not_opts():
    session = Session()
    return session.query(SQLANotOpts).order_by(SQLANotOpts.notification_id).all()


# TODO: change to all()? There can be multiple options per user
def get_user_settings(setting_id = None, user_id = None):
    session = Session()
    if setting_id is not None:
        return session.query(SQLAUserSetting).filter_by(setting_id=setting_id).first()
    if user_id is not None:
        return session.query(SQLAUserSetting).filter_by(user_id=user_id).all()


def get_log(log_id):
    session = Session()
    return session.query(SQLALog).filter_by(log_id=log_id).first()


def add_image_info(imageInfo):
    session = Session()
    info = SQLAImage(
        user_id = imageInfo['user_id'],
        image = imageInfo['image']
    )
    session.add(info)
    session.commit()
    return jsonify(imageInfo)


def get_image_info(image_id):
    session = Session()
    return session.query(SQLAImage).filter_by(image_id=image_id).first()


def get_sent_image(image_id):
    session = Session()
    return session.query(SQLASentImage).filter_by(image_id=image_id).first()


def get_images_by_user(user_id=None, username=None):
    session = Session()
    if user_id is not None:
        return session.query(SQLAImage).filter_by(user_id = user_id).all()
    elif username is not None:
        user = session.query(SQLAUser).filter_by(username = username).first()
        if user is not None:
            user_id = user.to_dict()['user_id']
            return session.query(SQLAImage).filter_by(user_id = user_id).all()
        else:
            raise Exception("Could not find user based on username", 1)
    else:
        raise Exception("Could not retrieve images for user", 1)

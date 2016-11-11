# TODO: user authentication for any api endpoint use
# TODO: # need to add functionality in other functions for logs to be sent to
# the add_log function. actions are: 'image taken', 'text sent', 'email sent',
# 'sign in', 'sign out', 'alter accout', 'initial activation'
#
# TODO: add custom 404 message / page

from flask import Flask, jsonify, request, send_file, session
from flask_cors import CORS, cross_origin
from utility import *
from database import db
from models import *
import query
import config
import os
from werkzeug.utils import secure_filename
import uuid
from sqlalchemy import DateTime
import datetime


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
CORS(app)
app.secret_key = os.urandom(24)


# Create error messages
def internal_error(e):
    return jsonify({"Error": str(e)}), 500

def error_message(message):
    return jsonify({"Error": message}), 400

def success_message(message):
    return jsonify({"Success": message}), 200

################
################
# SETUP ROUTES #
################
################

@app.route('/')
def api_root():
    return 'Welcome'


#########
# USERS #
#########

# Get user info by id or username
@app.route('/user/id/<int:user_id>',  methods = ['GET'])
@app.route('/user/device/<int:device_id>',  methods = ['GET'])
@app.route('/user/<username>', methods = ['GET'])
@app.route('/user/', methods = ["GET"])
def get_user(user_id = None, username = None, device_id=None):
    try:
        if ((user_id is not None) or (username is not None) or (device_id is not None)):
            sqlaUser = query.get_user(user_id, username, device_id)
            if sqlaUser is not None:
                user = User(sqlaUser)
                return user.to_json()
            else:
                return error_message("Could not retrieve user ". user_id if user_id else username)
        else:
            return error_message("Please specify id/<user_id> or <username>")

    except Exception as e:
        return internal_error(e)

# Get all users
# TODO: add extra info like 'count'
@app.route('/users/',  methods = ['GET'])
@app.route('/users/all/',  methods = ['GET'])
def get_all_users():
    try:
        # return list of all users
        users = query.get_all_users()
        if users is not None:
            usersList = []
            for sqlauser in users:
                user = User(sqlauser)
                usersList.append(user.to_dict())
            return jsonify(usersList)
        else:
            return error_message("Could not retrieve users")

    except Exception as e:
        return internal_error(e)

# logs a user in
# TODO: hash password
@app.route('/user/login/', methods = ["POST"])
def login():
    try:
        if request.method == 'POST':
        # TODO: check all fields are in request before accessing request args
            username = request.form.get('username')
            password = request.form.get('password')            

            sqlaUser = query.login({
            	"username" : username, 
            	"password" : password
            })
            if sqlaUser is not None:
                session['username'] = username
                return "success"
            else:
                return error_message("Could not retrieve user")
        else:
            return error_message("POST required for user insertion")

    except Exception as e:
        return internal_error(e)

# logs a user out
@app.route('/user/logout')
def logout():
    try:
        session.pop('username', None)

    except Exception as e:
        return internal_error(e)

# Add a user
@app.route('/user/add/', methods = ['POST'])
def add_user():
    try:
        if request.method == 'POST':
        # TODO: check all fields are in request before accessing request args
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            device_id = request.form.get('device_id')
            username = request.form.get('username')
            password = request.form.get('password')
            phone_number = request.form.get('phone_number')
            email = request.form.get('email')
            

            user_id = query.add_user({
                "first_name" : first_name,
                "last_name" : last_name,
                "device_id" : device_id,
                "username" : username,
                "password" : password,
                "phone_number" : phone_number,
                "email" : email
            })
            if user_id >= 0:
            	session['username'] = username
                # Add default notification settings for user
                print "here"
                add_default_user_settings(user_id)
                print "here2"
                return success_message("Added user " + str(user_id))
            else:
                return error_message("Could not add user")
        else:
            return error_message("POST required for user insertion")
    except Exception as e:
            return internal_error(e)

@app.route('/user/add/settings_test/', methods = ['GET'])
def add_default_user_settings(user_id = 5):
    print "here"
    return add_user_settings({
        "notification_option_id" : 1,
        "user_id" : 5,
        "start_time" : "00:00",
        "end_time" : "23:59"
        })

# Add user settings
@app.route('/user_settings/add/', methods = ['POST'])
def add_user_settings(params = None):
    try:
        if params is not None:
            # TODO: check params
            return query.add_user_settings(params)
        else:
            # TODO: check if this works?
            # TODO: decide if notification_option id should be the enum string instead "text", "email", "both"
            # name = request.form.get('notification_option_id')
            return query.add_user_settings({
                "user_id" : request.form.get('user_id'),
                "notification_option_id" : request.form.get('notification_option_id'),
                "start_time" : request.form.get('start_time'),
                "end_time" : request.form.get('end_time')
            })
    except Exception as e:
        return internal_error(e)


# Update user settings
# TODO: filter update to not require all fields
@app.route('/user_settings/update/', methods = ['POST'])
def update_user_settings():
    if request.method == 'POST':
        try:
            if request.form.has_key('user_id'):
                user_id = request.form.get('user_id')

                update_fields = []

                if request.form.has_key('notification_option_id'):
                    update_fields.append({'notification_option_id' : request.form.get('notification_option_id')})

                if request.form.has_key('start_time'):
                    update_fields.append({'start_time' : request.form.get('start_time')})

                if request.form.has_key('end_time'):
                    update_fields.append({'end_time' : request.form.get('end_time')})

                return query.update_user_settings(user_id, update_fields)               

            else:
                return error_message("Must specify user_id to update")

        except Exception as e:
            return internal_error(e)
    else:
        return error_message("POST required for user insertion")


# TODO: add route to update user info

#########################
# NOTIFICATION SETTINGS #
#########################

#TODO: should not_opts table and user settings table be combined?  m-m relationship?
# Get options by not_opt id, user id, or username
@app.route('/notification_options/<int:not_id>', methods = ['GET'])
def get_notification_options(not_id=None):
    try:
        if (not_id is not None):
            sqlaNotOpts = query.get_not_opts(not_id)
            if sqlaNotOpts is not None:
                options = []
                for sqlaOption in sqlaNotOpts:
                    option = NotOpt(sqlaOption)
                    options.append(option.to_dict())
                return jsonify(options)
            else:
                return error_message("Could not retrieve notification options")
        else:
            return error_message("Please specify id to get notification options")

    except Exception as e:
        return internal_error(e)


# get all notification options for all users
@app.route('/notification_options/', methods = ['GET'])
@app.route('/notification_options/all/', methods = ['GET'])
def get_all_notification_options():
    try:
        # return list of all notification options
        sqlaOptions = query.get_all_not_opts()
        if sqlaOptions is not None:
            optionsList = []
            print "here"
            for sqlOption in sqlaOptions:
                option = NotOpt(sqlOption)
                optionsList.append(option.to_dict())
            return jsonify(optionsList)
        else:
            return error_message("Could not retrieve users")

    except Exception as e:
        return internal_error(e)



#################
# USER SETTINGS #
#################
# TODO: do a join with user info?
@app.route('/user_settings/setting/<int:setting_id>', methods = ['GET'])
@app.route('/user_settings/<username>', methods = ['GET'])
@app.route('/user_settings/id/<int:user_id>', methods = ['GET'])
def get_user_settings(username = None, user_id = None, setting_id = None):
    try:
        if username is not None:
            # get user id for that username
            user_id = query.get_user_id(username)
            if user_id is None:
                return error_message("no user found for username " + username)
        if user_id is not None:
            # Get notification settings for user_id
            sql_user_settings = query.get_user_settings(None, user_id)
            print sql_user_settings
            if sql_user_settings is not None:
                user_settings = UserSetting(sql_user_settings)
                return user_settings.to_json()
            else:
                return error_message("No user found for user_id " +str(user_id))
        if setting_id is not None:
            sql_user_settings = query.get_user_settings(setting_id)
            if sql_user_settings is not None:
                user_settings = UserSetting(sql_user_settings)
                return user_settings.to_json()
            else:
                return error_message("No settings found for id " + str(setting_id))
        return error_message("Please specify notification id, username, or user_id")
    except Exception as e:
        return internal_error(e)


# TODO: make route to retrieve user info, user settings all in one



# TODO: make route to retrieve ALL user info all at once
# user settings, user info, all pictures (filepaths) associated with user, etc.

##########
# IMAGES #
##########

# Get image by id
@app.route('/image/id/', methods = ['GET'])
@app.route('/image/id/<int:image_id>', methods = ['GET'])
def get_image(image_id = None):
    # try:
    #     if image_id is not None:
    #         info = get_image_info(image_id)
    #         filename = info.image
    #         # Todo: complete the actual sending of the image
    #         return send_file(filename, )

    #     else:
    #         return error_message("Please specify image_id")
    # except Exception as e:
    #     return internal_error(e)
    try:
        if image_id is not None:
            # Get filename
            image_info = query.get_image_info(image_id)
            if image_info is not None:
                filename =  app.config['IMAGE_DIRECTORY'] + image_info.__dict__['image']
                print filename
                if ((filename is not None) and (os.path.isfile(filename)) ):
                    # send file
                    return send_file(filename, mimetype='image/jpeg')
                else:
                    return error_message("Image not found")
            else:
                return error_message("No image found for image_id")       
        else:
            return error_message("Please include image_id or post array of image_ids")
    except Exception as e:
        return internal_error(e)


# Get image by filepath?  *Idk if that is safe*

# Get image info by image id
@app.route('/image/info/id/', methods = ['GET'])
@app.route('/image/info/id/<int:image_id>', methods = ['GET'])
def get_image_info(image_id = None):
    try:
        if image_id is not None:
            sqlImageInfo = query.get_image_info(image_id)
            if sqlImageInfo is not None:
                imageInfo = Image(sqlImageInfo)
                return imageInfo.to_json()
            else:
                return error_message("Could not retrieve image info")
        else:
            return error_message("Please specify image_id")
    except Exception as e:
        return internal_error(e)


# Get all image ids for a user
@app.route('/image/info/user/id/<int:user_id>', methods = ['GET'])
@app.route('/image/info/user/<username>', methods = ['GET'])
def get_images_by_user(user_id = None, username = None):
    try:
        if ((username is not None) or (user_id is not None)):
            sqlImages = query.get_images_by_user(user_id, username)
            if sqlImages is not None:
                imagesList = []
                for sqlImage in sqlImages:
                    image = Image(sqlImage)
                    imagesList.append(image.to_dict())
                return jsonify(imagesList)
            else:
                return error_message("Unable to retrieve image infos for "  . user_id if user_id else username)
        else:
            return error_message("Please specify user name or id to retrieve image infos")
    except Exception as e:
        return internal_error(e)





################
# UPLOAD IMAGE #
################

# Add image to database
@app.route('/image/add/', methods=['POST'])
@app.route('/image/add/<int:device_id>', methods=['POST'])
def upload_file(device_id = None):
    try:
        if request.method == 'POST':
            if device_id is not None:
                # check if the post request has the file part
                if 'file' not in request.files:
                    return error_message('No file attached in request')
                file = request.files['file']
                # Rename file so no conflicts in directory
                filename, fileExtension = os.path.splitext(file.filename)
                # TODO: put check for file extension (what does Pi take?) .jp(e)g
                filename = str(uuid.uuid4()) + fileExtension
                print filename
                if file and allowed_file(filename):
                    filename = secure_filename(filename)
                    file.save(os.path.join(app.config['IMAGE_DIRECTORY'], filename))
                    # Get user id from sender device
                    sqlaUser = query.get_user(device_id=device_id)
                    user = User(sqlaUser)
                    print user.to_json()
                    if user is None:
                        return error_message("No user associated with device id")
                    user = User(sqlaUser)
                    print user.to_json()
                    user_id = user.to_dict()['user_id']
                    print user_id
                    # Add image info to db
                    return query.add_image_info({
                        "user_id" : user_id,
                        "image" : filename
                    })
                    # TODO: send image to user (James)

                else:
                    return error_message("Bad filename. Our bad.")
            else:
                return error_message("Specify device id corresponding to image")
    except Exception as e:
        return internal_error(e)


# # Route to retrieve image(s) by id. Can receive filename or json array of filenames
# @app.route('/image/file/id/<int:image_id>', methods=['GET', 'POST'])
# # @app.route('/image/files/<int:image_id>', methods=['GET', 'POST'])
# def download_image(image_id=None):
#     try:
#         if image_id is not None:
#             # Get filename
#             image_info = query.get_image_info(image_id)
#             if image_info is not None:
#                 filename = app.config['IMAGE_DIRECTORY'] + image_info.__dict__['image']
#                 print filename
#                 if ((filename is not None) and (os.path.isfile(filename)) ):
#                     # send file
#                     return send_file(filename, mimetype='image/jpeg')
#                 else:
#                     return error_message("Image not found")
#             else:
#                 return error_message("No image found for image_id")       
#         else:
#             return error_message("Please include image_id or post array of image_ids")
#     except Exception as e:
#         return internal_error(e)



##################################
# TODO: CREATE LOGGING FUNCTIONS #
##################################

# Add a log to the log table
# TODO: need to add functionality in other functions for logs to be sent to this function
# actions are: 'image taken', 'text sent', 'email sent',
# 'sign in', 'sign out', 'alter accout', 'initial activation'
@app.route('/log/id/<int:user_id>/action/<action>',  methods = ['GET'])
def add_log(user_id = None, action = None):
    try:
        return query.add_log({
            "user_id" : user_id,
            "action" : action
        })

    except Exception as e:
        return internal_error(e)


# Get all logs related to a user
@app.route('/log/info/user/id/<int:user_id>', methods = ['GET'])
@app.route('/log/info/user/<username>', methods = ['GET'])
def get_logs_by_user(user_id = None, username = None):
    try:
        if ((username is not None) or (user_id is not None)):
            sqlLogs = query.get_logs_by_user(user_id, username)
            if sqlLogs is not None:
                LogsList = []
                for sqlLog in sqlLogs:
                    log = Log(sqlLog)
                    logsList.append(log.to_dict())
                return jsonify(logsList)
            else:
                return error_message("Unable to retrieve log infos for "  . user_id if user_id else username)
        else:
            return error_message("Please specify user name or id to retrieve log infos")
    except Exception as e:
        return internal_error(e)



# Start app finally
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

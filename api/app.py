# TODO: user authentication for any api endpoint use
# TODO: # need to add functionality in other functions for logs to be sent to
# the add_log function. actions are: 'image taken', 'text sent', 'email sent',
# 'sign in', 'sign out', 'alter accout', 'initial activation'

from flask import Flask, jsonify, request
from utility import *
from database import db
import query
from models import *
import config
import os
from werkzeug.utils import secure_filename
import uuid


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


# Create error messages
def internal_error(e):
    return jsonify({"Error": str(e)}), 500

def error_message(message):
    return jsonify({"Error": message}), 400

################
################
# SETUP ROUTES #
################
################

@app.route('/')
def api_root():
    return 'Welcome'

@app.route('/hello')
def api_hello():
    return get_db()

# @app.route('/add/user')
# def add_user():
#     user = SQLAUser(
#         device_id = "0001",
#         first_name = "Christina",
#         last_name = "Mosnick",
#         username = "cmosnick",
#         password = "pass",
#         email = "cmosnick07@gmail.com",
#         phone_number = "8159751442"
#     )
#     # return user.first_name
#     # session = create_session
#     return query.add(user)
#     # return "User added: ";


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

# Add a user
@app.route('/user/add/', methods = ['POST'])
def add_user():
    if request.method == 'POST':
        # TODO: check all fields are in request before accessing request args
        try:
            first_name = request.args.get('first_name')
            last_name = request.args.get('last_name')
            device_id = request.args.get('device_id')
            username = request.args.get('username')
            password = request.args.get('password')
            phone_number = request.args.get('phone_number')
            email = request.args.get('email')
            return query.add_user({
                "first_name" : first_name,
                "last_name" : last_name,
                "device_id" : device_id,
                "username" : username,
                "password" : password,
                "phone_number" : phone_number,
                "email" : email
            })

        except Exception as e:
            return internal_error(e)
    else:
        return error_message("POST required for user insertion")


#########################
# NOTIFICATION SETTINGS #
#########################

# Get options by not_opt id, user id, or username
@app.route('/notification_options/<int:not_id>', methods = ['GET'])
@app.route('/notification_options/user/<username>',  methods = ['GET'])
@app.route('/notification_options/user/id/<int:user_id>',  methods = ['GET'])
def get_notification_options(not_id=None, username=None, user_id = None):
    try:
        if ((not_id is not None) or (username is not None) or (user_id is not None)):
            sqlaNotOpts = query.get_not_opts(not_id, username, user_id)
            if sqlaNotOpts is not None:
                options = []
                for sqlaOption in sqlaNotOpts:
                    option = NotOPt(sqlaOption)
                    options.append(option.to_dict())
                return jsonify(options)
            else:
                return error_message("Could not retrieve notification options")
        else:
            return error_message("Please specify user or id to get notification options")

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
            for sqlOption in sqlaOptions:
                option = NotOPt(sqlaOptions)
                optionsList.append(option.to_dict())
            return jsonify(optionsList)
        else:
            return error_message("Could not retrieve users")

    except Exception as e:
        return internal_error(e)


##########
# IMAGES #
##########

# Get image by id
@app.route('/image/id/', methods = ['GET'])
@app.route('/image/id/<int:image_id>', methods = ['GET'])
def get_image(image_id = None):
    try:
        if image_id is not None:
            # info = loads(get_image_info(image_id))
            # filePath = info.image
            # Todo: complete the actual sending of the image
            return "hello"
        else:
            return error_message("Please specify image_id")
    except Exception as e:
        return internal_error(e)


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
            # TODO: implement query function
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
    if request.method == 'POST':
        if device_id is not None:
            # check if the post request has the file part
            if 'file' not in request.files:
                return error_message('No file attached in request')
            file = request.files['file']
            # Rename file so no conflicts in directory
            filename, fileExtension = os.path.splitext(file.filename)
            # TODO: put check for file extension (what does Pi take?)
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
            else:
                return error_message("Bad filename. Our bad.")
        else:
            return error_message("Specify device id corresponding to image")


# Route to retrieve image(s) by id. Can receive filename or json array of filenames
@app.route('/image/file/', methods=['POST'])
@app.route('/image/files/<int:image_id>', methods=['GET', 'POST'])
def download(image_id=None):
    try:
        if ((image_id is None) and (request.method == 'POST')):
            return "Thanks for posting"
        elif image_id is not None:
            # check if filename exists
            return image_id
        else:
            return error_message("Please include image_id or post array of image_ids")
    except Exception as e:
        return internal_error(e)



##################################
# TODO: CREATE LOGGING FUNCTIONS #
##################################

# Add a log to the log table
# need to add functionality in other functions for logs to be sent to this function
# actions are: 'image taken', 'text sent', 'email sent',
# 'sign in', 'sign out', 'alter accout', 'initial activation'
@app.route('/log/id/<int:user_id>/action/<action>',  methods = ['GET'])
def add_log():
    try:
        return query.add_log({
            "user_id" : user_id,
            "action" : action
        })

    except Exception as e:
        return internal_error(e)



# Start app finally
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

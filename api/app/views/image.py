from flask import jsonify, request, send_file, session, Blueprint
from app.utility import *
from app.database import db
from app.models import *
import app.query as query
from app.routing_utils import *
import os
from werkzeug.utils import secure_filename
import uuid
from config import IMAGE_DIRECTORY


# Declare blueprint named image
image = Blueprint('image', __name__, template_folder='templates')


################
################
# SETUP ROUTES #
################
################


##########
# IMAGES #
##########

# Get image by id
@image.route('/id/', methods = ['GET'])
@image.route('/id/<int:image_id>', methods = ['GET'])
def get_image(image_id = None):
    try:
        if image_id is not None:
            # Get filename
            image_info = query.get_image_info(image_id)
            if image_info is not None:
                filename = IMAGE_DIRECTORY + image_info.__dict__['image']
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
@image.route('/info/id/', methods = ['GET'])
@image.route('/info/id/<int:image_id>', methods = ['GET'])
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
@image.route('/info/user/id/<int:user_id>', methods = ['GET'])
@image.route('/info/user/<username>', methods = ['GET'])
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
# TODO : search in devices table for user_id instead of user tables
@image.route('/add/', methods=['POST'])
@image.route('/add/<int:device_id>', methods=['POST'])
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
                    file.save(os.path.join(IMAGE_DIRECTORY, filename))
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
                    # Determine user settings

                    # Text: number, filepath

                    # Email: email, filepath, name, 

                else:
                    return error_message("Bad filename. Our bad.")
            else:
                return error_message("Specify device id corresponding to image")
    except Exception as e:
        return internal_error(e)
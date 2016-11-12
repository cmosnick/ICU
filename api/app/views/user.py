from flask import jsonify, request, send_file, Blueprint, session
from app.utility import *
from app.database import db
from app.models import *
import app.query as query
from app.routing_utils import *
import os
from werkzeug.utils import secure_filename
import uuid
from passlib.hash import md5_crypt

import app.views.settings as settings
import app.views.session as sessionView

# from app import appSession

# Declare blueprint name api
user = Blueprint('user',__name__,template_folder='templates')


################
################
# SETUP ROUTES #
################
################

#########
# USERS #
#########

# Get all users
# TODO: add extra info like 'count'
# TODO: change to user/all in README
# @user.route('/users/',  methods = ['GET'])
@user.route('/all/',  methods = ['GET'])
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


# Get user info by id or username
# TODO: fix error message "Error: <username>. MAke more descriptive."
# TODO : search in devices table for user_id instead of searching the users table
@user.route('/id/<int:user_id>',  methods = ['GET'])
@user.route('/device/<int:device_id>',  methods = ['GET'])
@user.route('/<username>', methods = ['GET'])
@user.route('/', methods = ["GET"])
def get_user(user_id = None, username = None, device_id=None):
    try:
        if ((user_id is not None) or (username is not None) or (device_id is not None)):
            sqlaUser = query.get_user(user_id, username, device_id)
            if sqlaUser is not None:
                print "HERE"
                user = User(sqlaUser)
                print "\nhere\n"
                return user.to_json()
            else:
                return error_message("Could not retrieve user " + (str(user_id) if user_id else str(username)))
        else:
            return error_message("Please specify id/<user_id> or <username>")

    except Exception as e:
        return internal_error(e)


# Add a user
# TODO: add sessions
# TODO: get rid of device ID in users table
@user.route('/add/', methods = ['POST'])
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
                "hash" : md5_crypt.encrypt(password),
                "phone_number" : phone_number,
                "email" : email
            })
            if user_id >= 0:

                #session['username'] = username
                # Add default notification settings for user
                #print "here"
                settings.add_default_user_settings(user_id)
                return success_message("Added user " + str(user_id))
            else:
                return error_message("Could not add user")
        else:
            return error_message("POST required for user insertion")
    except Exception as e:
            return internal_error(e)

# logs a user in
# TODO: add sessions
@user.route('/login/', methods = ["POST"])
def login():
    try:
        if request.method == 'POST':
        # TODO: check all fields are in request before accessing request args
            username = request.form.get('username')
            password = request.form.get('password')            

            sqlaUser = query.login({
              "username" : username
            })

            if sqlaUser is not None:
                #session['username'] = username
                #print "here3"
                if md5_crypt.verify(password, sqlaUser.__dict__["hash"]) is True:
                    return success_message("User successfully logged in")
                else:
                    return error_message("User info inncorrect")
            else:
                return error_message("Could not retrieve user")
        else:
            return error_message("POST required for user insertion")

    except Exception as e:
        return internal_error(e)

# logs a user out
# TODO: add sessions
@user.route('/logout/', methods=['GET'])
def logout():
    try:
        if(sessionView.check_session() == "success"):
            #session.pop("Username", None)
            return success_message("The user has successfully logged out")
        else:
            return error_message("The user is not logged in. Logout unsuccessful.")
    except Exception as e:
        return internal_error(e)

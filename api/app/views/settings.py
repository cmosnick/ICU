from flask import jsonify, request, send_file, session, Blueprint
from app.utility import *
from app.database import db
from app.models import *
import app.query as query
from app.routing_utils import *
import os
from werkzeug.utils import secure_filename
import uuid
import datetime



# Declare blueprint name api
settings = Blueprint('settings',__name__,template_folder='templates')


################
################
# SETUP ROUTES #
################
################


@settings.route('/add/settings_test/', methods = ['GET'])
def add_default_user_settings(user_id = 5):
    print "here"
    return add_user_settings({
        "notification_option_id" : 1,
        "user_id" : user_id,
        "start_time" : datetime.datetime.strptime("00:00", '%H:%M').time(),
        "end_time" : datetime.datetime.strptime("23:59", '%H:%M').time()
    })

# Add user settings
@settings.route('/user_settings/add/', methods = ['GET', 'POST'])
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
@settings.route('/user_settings/update/', methods = ['POST'])
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
@settings.route('/notification_options/<int:not_id>', methods = ['GET'])
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
@settings.route('/notification_options/', methods = ['GET'])
@settings.route('/notification_options/all/', methods = ['GET'])
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
# TODO: make sure user settings are insterted on user add
@settings.route('/user_settings/setting/<int:setting_id>', methods = ['GET'])
@settings.route('/user_settings/<username>', methods = ['GET'])
@settings.route('/user_settings/id/<int:user_id>', methods = ['GET'])
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
                settings = []
                for sql_user_setting in sql_user_settings:
                    user_setting = UserSetting(sql_user_setting)
                    settings.append(user_setting.to_dict())
                return jsonify(settings)
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
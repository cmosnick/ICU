from flask import jsonify, request, send_file, session, Blueprint
from app.utility import *
from app.database import db
from app.models import *
import app.query as query
from app.routing_utils import *
import os
from werkzeug.utils import secure_filename
import uuid


# Declare blueprint name api
log = Blueprint('log',__name__,template_folder='templates')


################
################
# SETUP ROUTES #
################
################

# Add a log to the log table
# TODO: need to add functionality in other functions for logs to be sent to this function
# actions are: 'image taken', 'text sent', 'email sent',
# 'sign in', 'sign out', 'alter accout', 'initial activation'
@log.route('/id/<int:user_id>/action/<action>',  methods = ['GET'])
def add_log(user_id = None, action = None):
    try:
        return query.add_log({
            "user_id" : user_id,
            "action" : action
        })

    except Exception as e:
        return internal_error(e)


# Get all logs related to a user
@log.route('/info/user/id/<int:user_id>', methods = ['GET'])
@log.route('/info/user/<username>', methods = ['GET'])
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

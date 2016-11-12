from flask import jsonify, request, send_file, session, Blueprint
from app.utility import *
from app.database import db
from app.models import *
import app.query as query
from app.routing_utils import *
import os
from werkzeug.utils import secure_filename



##################################
        # SESSION CHECKING #
##################################

# Checks if a session exists
@app.route('/session/', methods = ['GET'])
def check_session():
    try:
        #if (request.cookies.get('login') == True):
        if 'username' in session:
            return success_message("The session exists")
        else:
            return "The session does not exist"
    except Exception as e:
        return internal_error(e)


# Start app finally
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
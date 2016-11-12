from flask import jsonify

# Create error messages
def internal_error(e):
    return jsonify({"Error": str(e)}), 500

def error_message(message):
    return jsonify({"Error": message}), 400

def success_message(message):
    return jsonify({"Success": message}), 200

def failure_message(message):
    return jsonify({"Failure": message}), 200
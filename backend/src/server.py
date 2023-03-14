from json import dumps
from flask import Flask, request, send_from_directory
from flask_cors import CORS

'''
def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response
'''
APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
#APP.register_error_handler(Exception, defaultHandler)


# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
        pass #raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })
    
#ADMIN ROUTES

@APP.route("/admin/give_admin", methods=["POST"])
def admin_give_admin():
    """
    give_admin flask
    """
    data = request.get_json()
    return dumps(give_admin(int(data["uid_admin"]), int(data["uid_user"])))
    
@APP.route("/admin/ban_user", methods=["POST"])
def admin_ban_user():
    """
    ban_user flask
    """
    data = request.get_json()
    return dumps(ban_user(int(data["uid_admin"]), int(data["uid_user"])))
    
@APP.route("/admin/unban_user", methods=["POST"])
def admin_unban_user():
    """
    unban_user flask
    """
    data = request.get_json()
    return dumps(unban_user(int(data["uid_admin"]), int(data["uid_user"])))
    
@APP.route("/admin/remove_user", methods=["POST"])
def admin_remove_user():
    """
    remove_user flask
    """
    data = request.get_json()
    return dumps(remove_user(int(data["uid_admin"]), int(data["uid_user"])))
    
@APP.route("/admin/readd_user", methods=["POST"])
def admin_readd_user():
    """
    readd_user flask
    """
    data = request.get_json()
    return dumps(readd_user(int(data["uid_admin"]), int(data["uid_user"])))

from json import dumps
from flask import Flask, request, send_from_directory
from flask_cors import CORS
import os
from admin import give_admin, ban_user, unban_user, remove_user, readd_user

from flask_mail import Mail, Message
from flask import Flask, request

from proj_master import *
from profile_page import *

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

app = Flask(__name__, static_url_path= '/' + os.path.dirname(__file__))
CORS(app)
mail = Mail(app)
app.register_error_handler(Exception, defaultHandler)
#APP.register_error_handler(Exception, defaultHandler)

app.config['TRAP_HTTP_EXCEPTIONS'] = True
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'compgpt3900@gmail.com'
app.config['MAIL_PASSWORD'] = "gqjtjsnnaxwqeeeg"

sending_email = "compgpt3900@gmail.com"


# Example
@app.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
        pass #raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })
    
#ADMIN ROUTES#
@app.route("/admin/give_admin", methods=["POST"])
def admin_give_admin():
    """
    give_admin flask
    """
    data = request.get_json()
    return dumps(give_admin(data["uid_admin"], data["uid_user"]))
    
@app.route("/admin/ban_user", methods=["POST"])
def admin_ban_user():
    """
    ban_user flask
    """
    data = request.get_json()
    return dumps(ban_user(data["uid_admin"], data["uid_user"]))
    
@app.route("/admin/unban_user", methods=["POST"])
def admin_unban_user():
    """
    unban_user flask
    """
    data = request.get_json()
    return dumps(unban_user(data["uid_admin"], data["uid_user"]))
    
@app.route("/admin/remove_user", methods=["POST"])
def admin_remove_user():
    """
    remove_user flask
    """
    data = request.get_json()
    return dumps(remove_user(data["uid_admin"], data["uid_user"]))
    
@app.route("/admin/readd_user", methods=["POST"])
def admin_readd_user():
    """
    readd_user flask
    """
    data = request.get_json()
    return dumps(readd_user(data["uid_admin"], data["uid_user"]))




#PROJECT ROUTES
@app.route("/project/create/project", methods=["POST"])
def create_project():
    """
    create_project_user flask
    """
    data = request.get_json()
    return dumps(create_project(data["uid"], data["name"], data["description"], 
                data["status"], data["team_strength"], data["picture"]))

@app.route("/project/revive/completed/project", methods=["POST"])
def revive_completed_project():
    """
    revive_completed_project flask
    """
    data = request.get_json()
    return dumps(revive_completed_project(data["pid"], data["uid"], data["new_status"]))


@app.route('/invite/to/project', methods=['POST'])
def invite_to_project_flask():
    inputs = request.get_json()
    proj_inv = invite_to_project(inputs['pid'], inputs['sender_uid'], inputs['receiver_uid'])

    receipient_email = proj_inv[0]
    msg_title = proj_inv[1]
    msg_body = proj_inv[2]

    msg = Message(msg_title, sender = sending_email, recipients = [receipient_email])
    msg.body = msg_body
    mail.send(msg)
    
@app.route("/project/remove/user", methods=["POST"])
def project_remove_user():
    """
    project_remove_user flask
    """
    data = request.get_json()
    return dumps(readd_user(data["pid"], data["uid"], data["uid_to_be_removed"]))
    
    
@app.route('/user/details', methods=['GET'])
def user_details():
    #name, email, role, photo_url, num_connections, rating
    data = request.get_json()
    uid = data["uid"]
    display_name = str(get_display_name(uid))
    email = str(get_email(uid))
    photo_url = str(get_photo(uid))
    return dumps(display_name, email, photo_url, int(0), int(0))

@app.route('/profile/update', methods=['PUT'])
def profile_update():
    data = request.get_json()
    uid = data["uid"]
    email = data["email"]
    role = data["role"]
    photo_url = data["photo_url"]
    try:
        update_email(uid, email)
    except ValueError:
        return "Invalid Email", 400
    update_role(uid, role)
    update_photo(uid, photo_url)
    
if __name__ == "__main__":
    app.run()
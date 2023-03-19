from json import dumps
from flask import Flask, request, send_from_directory, Response
from flask_cors import CORS
import os
from flask_mail import Mail, Message
from flask import Flask, request, Response

from .authentication import *
from .admin import *
from .proj_master import *
from .profile_page import *
from .projects import *

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

#--- Authentication Routes ---#
@app.route("/authentication/reset_password", methods=["POST"])
def flask_reset_password():
    data = request.get_json()
    res = get_reset_password_link(data["uid"])
    if res == -1:
        return Response(status=400)
    else:
        return dumps(res)
    
#Profile Routes#
@app.route('/user/details', methods=['GET'])
def user_details():
    #name, email, role, photo_url, num_connections, rating
    data = request.get_json()
    uid = data["uid"]
    if is_valid_user(uid) == False:
        return Response(status=400)
    else:
        display_name = str(get_display_name(uid))
        email = str(get_email(uid))
        photo_url = str(get_photo(uid))
        role = str(get_role(uid))
        return dumps({"display_name": display_name, "email": email, "role": role, "photo_url": photo_url, "num_connections": int(0), "rating": int(0)}), 200

@app.route('/profile/update', methods=['PUT'])
def profile_update():
    data = request.get_json()
    uid = data["uid"]
    if is_valid_user(uid) == False:
        return Response(status=400)
    else:
        email = data["email"]
        role = data["role"]
        photo_url = data["photo_url"]
        try:
            update_email(uid, email)
        except ValueError:
            return "Invalid Email"
        update_role(uid, role)
        update_photo(uid, photo_url)
        return Response(status=200)

@app.route('/get/tasks', methods=['GET'])
def get_user_tasks():
    data = request.get_json()
    uid = data["uid"]
    if is_valid_user(uid) == False:
        return Response(status=400)
    else:
        return Response(get_tasks(uid), status=200)

@app.route('/create/user', methods=['PUTS'])
def create_user():
    data = request.get_json()
    uid = data["uid"]
    create_user_firestore(uid)


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
@app.route("/projects/create", methods=["POST"])
def flask_create_project():
    data = request.get_json()
    pid = create_project(data["uid"], data["name"], data["description"], data["due_date"], data["team_strength"], data["picture"])
    return dumps(pid)

@app.route("/projects/revive", methods=["POST"])
def flask_revive_project():
    data = request.get_json()
    res = revive_completed_project(data["pid"], data["uid"], data["new_status"])
    return dumps(res)

@app.route("/projects/remove", methods=["POST"])
def flask_remove_project_member():
    data = request.get_json()
    res = remove_project_member(data["pid"], data["uid"], data["uid_to_be_removed"])
    return dumps(res)

@app.route("/projects/invite", methods=["POST"])
def flask_invite_to_project():
    data = request.get_json()

    uid_list = []
    for email in data["receiver_uids"]:

        try:
            uid = auth.get_user_by_email(email).uid
        except auth.UserNotFoundError:
            return Response(
                f"Specified email {email} does not exist",
                status=400
            )
        else:
            uid_list.append(uid)

    res = invite_to_project(data["pid"], data["sender_uid"], uid_list)

    # Send email to all users in uid_list
    for uid, data in res.items():
        receipient_email = data[0]
        msg_title = data[1]
        msg_body = data[2]

        msg = Message(msg_title, sender=sending_email, recipients=[receipient_email])
        msg.body = msg_body
        mail.send(msg)

    return dumps(res)

@app.route("/projects/update", methods=["POST"])
def flask_update_project():
    data = request.get_json()

    res = update_project(data["pid"], data["uid"], data["updates"])

    return dumps(res)

# NOTIFICATIONS ROUTES #
@app.route('/notification/get/notifications', methods=['GET'])
def get_notifications():
    data = request.get_json()
    return dumps(get_notifications(data['uid']))

@app.route('/notification/clear/notification', methods=['DELETE'])
def clear_notification():
    data = request.get_json()
    return dumps(clear_notification(data['uid'], data['notf_dict']))

@app.route('/notification/clear/all/notifications', methods=['DELETE'])
def clear_all_notifications():
    data = request.get_json()
    return dumps(clear_all_notifications(data['uid']))

# PROJECT MANAGEMENT ROUTES #
@app.route("/projects/view", methods=["GET"])
def flask_view_project():
    data = request.get_json()
    return dumps(view_project(data["pid"], data["uid"]))

@app.route("/projects/search", methods=["GET"])
def flask_search_project():
    data = request.get_json()
    return dumps(search_project(data["uid"], data["query"]))

if __name__ == "__main__":
    app.run()


# CONNECTION ROUTES #


from json import dumps
from flask import Flask, current_app, redirect, request, send_from_directory, Response
from flask_cors import CORS
import os
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from flask import Flask, request, Response
from waitress import serve

from .authentication import *
from .admin import *
from .proj_master import *
from .profile_page import *
from .projects import *
from .connections import *
from .taskboard import *
from .helper import *

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

#--- Authentication Routes ---#
@app.route("/authentication/reset_password", methods=["POST"])
def flask_reset_password():
    uid = request.headers.get('Authorization')
    res = get_reset_password_link(uid)
    if res == -1:
        return Response(status=400)
    else:
        # Send email
        msg_title = "TaskForge: Reset Password"
        receipient_email = auth.get_user(uid).email
        msg = Message(msg_title, sender=sending_email, recipients=[receipient_email])
        msg.body = "Click link to reset your password: {res}"
        mail.send(msg)
        return dumps(res)
    
#Profile Routes#
@app.route('/profile/details', methods=['GET'])
def user_details():
    # name, email, role, photo_url, num_connections, rating
    uid = request.headers.get('Authorization')
    if is_valid_user(uid) == False:
        return Response(status=400)
    else:
        display_name = str(get_display_name(uid))
        email = str(get_email(uid))
        photo_url = str(get_photo(uid))
        role = str(get_role(uid))
        connections = len(get_connection_list(uid))
        return dumps({"display_name": display_name, "email": email, "role": role, "photo_url": photo_url, "num_connections": str(connections), "rating": int(0)}), 200

@app.route('/profile/update', methods=['PUT'])
def profile_update():
    data = request.get_json()
    uid = request.headers.get('Authorization')
    if is_valid_user(uid) == False:
        return Response(status=400)
    else:
        email = data["email"]
        role = data["role"]
        photo_url = data["photo_url"]
        display_name = data["display_name"]
        if email:
            try:
                update_email(uid, email)
            except ValueError:
                return "Invalid Email"
        if role: update_role(uid, role)
        if photo_url: update_photo(uid, photo_url)
        if display_name: update_display_name(uid, display_name)
        return Response(status=200)

@app.route('/profile/tasks', methods=['GET'])
def get_user_tasks():
    uid = request.headers.get('Authorization')
    if is_valid_user(uid) == False:
        return Response(status=400)
    else:
        return Response(get_tasks(uid), status=200)

@app.route('/profile/create', methods=['PUT'])
def create_user():
    uid = request.headers.get('Authorization')
    create_user_firestore(uid)
    return Response(status=200)


#ADMIN ROUTES#
@app.route("/admin/is_admin", methods=["GET"])
def admin_is_admin():
    uid = request.headers.get('Authorization')
    return dumps(is_admin(uid))

@app.route("/admin/give_admin", methods=["POST"])
def admin_give_admin():
    """
    give_admin flask
    """
    data = request.get_json()
    uid_user = request.headers.get('Authorization')
    return dumps(give_admin(data["uid_admin"], uid_user))

@app.route("/admin/ban_user", methods=["POST"])
def admin_ban_user():
    """
    ban_user flask
    """
    data = request.get_json()
    uid_user = request.headers.get('Authorization')
    return dumps(ban_user(data["uid_admin"], uid_user))
    
@app.route("/admin/unban_user", methods=["POST"])
def admin_unban_user():
    """
    unban_user flask
    """
    data = request.get_json()
    uid_user = request.headers.get('Authorization')
    return dumps(unban_user(data["uid_admin"], uid_user))
    
@app.route("/admin/remove_user", methods=["POST"])
def admin_remove_user():
    """
    remove_user flask
    """
    data = request.get_json()
    uid_user = request.headers.get('Authorization')
    return dumps(remove_user(data["uid_admin"], uid_user))

@app.route("/admin/readd_user", methods=["POST"])
def admin_readd_user():
    """
    readd_user flask
    """
    data = request.get_json()
    uid_user = request.headers.get('Authorization')
    return dumps(readd_user(data["uid_admin"], uid_user))


#PROJECT MASTER ROUTES
@app.route("/projects/create", methods=["POST"])
def flask_create_project():
    data = request.get_json()
    uid = request.headers.get('Authorization')
    pid = create_project(uid, data["name"], data["description"], data["due_date"], data["team_strength"], data["picture"])
    return dumps(pid)

@app.route("/projects/revive", methods=["POST"])
def flask_revive_project():
    data = request.get_json()
    uid = request.headers.get('Authorization')
    res = revive_completed_project(data["pid"], uid, data["new_status"])
    return dumps(res)

@app.route("/projects/remove", methods=["POST"])
def flask_remove_project_member():
    data = request.get_json()
    uid = request.headers.get('Authorization')
    res = remove_project_member(data["pid"], uid, data["uid_to_be_removed"])
    return dumps(res)

@app.route("/projects/invite", methods=["POST"])
def flask_invite_to_project():
    data = request.get_json()
    sender_uid = request.headers.get('Authorization')

    uid_list = []
    for email in data["receiver_emails"]:

        try:
            uid = auth.get_user_by_email(email).uid
        except auth.UserNotFoundError:
            return Response(
                f"Specified email {email} does not exist",
                status=400
            )
        else:
            uid_list.append(uid)

    res = invite_to_project(data["pid"], sender_uid, uid_list)

    # # Send email to all users in uid_list
    # for uid, data in res.items():
    #     receipient_email = data[0]
    #     msg_title = data[1]
    #     msg_body = data[2]

    #     msg = Message(msg_title, sender=sending_email, recipients=[receipient_email])
    #     msg.body = msg_body
    #     mail.send(msg)

    return dumps(res)

@app.route("/projects/update", methods=["POST"])
def flask_update_project():
    data = request.get_json()
    uid = request.headers.get('Authorization')
    res = update_project(data["pid"], uid, data["updates"])
    return dumps(res)

@app.route("/projects/delete", methods=["POST"])
def flask_delete_project():
    data = request.get_json()
    uid = request.headers.get('Authorization')
    res = delete_project(data["pid"], uid)
    return dumps(res)

# NOTIFICATIONS ROUTES #
@app.route('/notifications/get', methods=['GET'])
def get_notifications():
    uid = request.headers.get('Authorization')
    return dumps(get_notifications(uid))

@app.route('/notifications/clear', methods=['DELETE'])
def clear_notification():
    data = request.get_json()
    uid = request.headers.get('Authorization')
    return dumps(clear_notification(uid, data['notf_dict']))

@app.route('/notifications/clearall', methods=['DELETE'])
def clear_all_notifications():
    uid = request.headers.get('Authorization')
    return dumps(clear_all_notifications(uid))


@app.route('/notification/connection/request', methods=['POST'])
def flask_notification_connection_request():
    data = request.get_json()
    return dumps(notification_connection_request(data["uid"], data["uid_sender"]))

# PROJECT MANAGEMENT ROUTES #
@app.route("/projects/view", methods=["GET"])
def flask_view_project():
    pid = int(request.args.get('pid'))
    uid = request.headers.get('Authorization')
    return dumps(view_project(pid, uid))

@app.route("/projects/search", methods=["GET"])
def flask_search_project():
    uid = request.headers.get('Authorization')
    query = request.args.get('query')
    return dumps(search_project(uid, query))

@app.route("/projects/leave", methods=["POST"])
def flask_request_leave_project():
    uid = request.headers.get("Authorization")
    data = request.get_json()
    res = request_leave_project(data["pid"], uid, data["msg"])
    return dumps(res)

@app.route("/projects/invite/respond", methods=["POST"])
def flask_respond_project_invitation():
    uid = request.headers.get("Authorization")
    data = request.get_json()
    res = respond_project_invitation(data["pid"], uid, data["accept"], data["msg"])
    return dumps(res)

@app.route("/projects/pin", methods=["POST"])
def flask_pin_project():
    uid = request.headers.get("Authorization")
    data = request.get_json()
    res = pin_project(data["pid"], uid, data["is_pinned"])
    return dumps(res)

# CONNECTION ROUTES #

@app.route("/connections/request_respond", methods=["POST"])
def flask_connection_request_respond():
    """
    connection_request_respond flask
    """
    uid = request.headers.get("Authorization")
    data = request.get_json()
    return dumps(connection_request_respond(str(uid), data["nid"], data["response"]))
    
@app.route("/connections/get_connection_requests", methods=["GET", "POST"])
def flask_get_connection_requests():
    """
    get_connection_requests flask
    """
    uid = request.headers.get("Authorization")
    return dumps(get_connection_requests(uid), indent=4, sort_keys=True, default=str)

@app.route("/connections/get_connected_taskmasters", methods=["GET", "POST"])
def flask_get_connected_taskmasters():
    """
    get_connection_requests flask
    """
    uid = request.headers.get("Authorization")
    return dumps(get_connected_taskmasters(uid))
    
# TASK MANAGEMENT #	
@app.route('/upload_file1', methods = ['POST'])
def flask_upload_file():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(f"src/{filename}")
    return 'File Uploaded'
    
@app.route('/upload_file2', methods = ['POST'])
def flask_upload_file2():
    uid = request.headers.get('Authorization')
    data = request.get_json()
    upload_file(uid, data['file'], data["destination_name"], data["tid"])
    return 'File Saved'

@app.route('/download_file', methods = ['GET'])
def flask_download_file():
    uid = request.headers.get('Authorization')
    fileName = request.get_json()['fileName']
    download_file(uid, fileName)
    newName = re.sub('.*' + '/', '', fileName) #test.jpg
    send_from_directory(app.root_path, newName)
    os.remove(f"{app.root_path}/{newName}")
    return 'File Sent'

# CREATE #
@app.route("/epic/create", methods=["POST"])
def flask_create_epic():
    """
    Creates an epic
    """
    data = request.get_json()
    return create_epic(data["uid"], data["pid"], data["title"], data["description"], data["colour"])

@app.route("/task/create", methods=["POST"])
def flask_create_task():
    """
    Creates a task
    """
    data = request.get_json()
    return create_task(data["uid"], data["pid"], data["eid"], data["assignees"], data["title"], data["description"], data["deadline"],
                data["workload"], data["priority"], data["status"])

@app.route("/subtask/create", methods=["POST"])
def flask_create_subtask():
    """
    Creates a subtask
    """
    data = request.get_json()
    return create_subtask(data["tid"], data["pid"], data["eid"], data["assignees"], data["title"], data["description"], data["deadline"],
                          data["workload"], data["priority"], data["status"])

# DETAILS #
@app.route("/epic/details", methods=["GET"])
def flask_epic_details():
    """
    Gets epic detail
    """
    eid = int(request.args.get('eid'))
    uid = request.headers.get("Authorization")
    return dumps(get_epic_details(uid, eid))

@app.route("/task/details", methods=["GET"])
def flask_task_details():
    """
    Gets task detail
    """
    tid = int(request.args.get('tid'))
    uid = request.headers.get("Authorization")
    return get_task_details(uid, tid)

@app.route("/subtask/details", methods=["GET"])
def flask_subtask_details():
    """
    Gets subtask detail
    """
    stid = int(request.args.get('stid'))
    uid = request.headers.get("Authorization")
    return dumps(get_subtask_details(uid, stid))

# Update task management
@app.route("/epic/update", methods=["POST"])
def flask_epic_update():
    """
    update epic
    """
    data = request.get_json()
    uid = request.headers.get("Authorization")
    return dumps(update_epic(uid, data["eid"], data["title"], 
                             data["description"], data["colour"]))

@app.route("/task/update", methods=["POST"])
def flask_task_update():
    """
    update task
    """
    data = request.get_json()
    uid = request.headers.get("Authorization")
    return dumps(update_task(uid, data["tid"], data["eid"], data["assignees"], 
                             data["title"], data["description"], data["deadline"], 
                             data["workload"], data["priority"], data["status"], data["flagged"]))

@app.route("/subtask/update", methods=["POST"])
def flask_subtask_update():
    """
    update subtask
    """
    data = request.get_json()
    uid = request.headers.get("Authorization")
    return dumps(update_subtask(uid, data["stid"], data["eid"], data["assignees"], 
                                data["title"], data["description"], data["deadline"], 
                                data["workload"], data["priority"], data["status"]))

@app.route("/task/comment", methods=["POST"])
def flask_task_comment():
    """
    Comment on a task
    """
    data = request.get_json()
    uid = request.headers.get("Authorization")
    return comment_task(uid, data["tid"], data["comment"])

# Taskboard
@app.route("/taskboard/show", methods=["GET"])
def flask_taskboard_show():
    """
    retrieves the taskboard
    """
    uid = request.headers.get("Authorization")
    pid = request.headers.get("pid")
    hidden = request.headers.get("hidden")
    return dumps(get_taskboard(uid, pid, hidden))

# Search task in project
@app.route("/taskboard/search", methods=["GET"])
def flask_taskboard_search():
    """
    Retrieve list of tasks in project using query
    """
    uid = request.headers.get("Authorization")
    pid = request.headers.get("pid")
    query = request.headers.get("query")
    return dumps(search_taskboard(uid, pid, query))

# Assigned Task List
@app.route("/tasklist/show", methods=["GET"])
def flask_tasklist_show():
    """
    Retrieve the tasklist
    """
    uid = request.headers.get("Authorization")
    show_completed = request.headers.get("show_completed")
    return dumps(get_user_assigned_task(uid, show_completed))

# if __name__ == "__main__":
#     # app.run(port=8000, debug=True)
#     serve(app, host="0.0.0.1", port=8000, debug=True)
from json import dumps
from flask import Flask, current_app, redirect, request, send_from_directory, Response
from flask_cors import CORS
from flask_mail import Mail, Message
import os
from werkzeug.utils import secure_filename
from flask import Flask, request, Response

from.achievement import *
from .authentication import *
from .admin import *
from .projmaster import *
from .profile_page import *
from .projects import *
from .connections import *
from .taskboard import *
from .tasklist import *
from .helper import *
from .reputation import *
from .workload import *
from .tasks import upload_file, get_file_link, create_task, get_task_details, assign_task, update_task, comment_task
from .epics import create_epic, get_epic_details, update_epic
from .subtasks import create_subtask, get_subtask_details, assign_subtask, update_subtask, get_all_subtasks

def defaultHandler(err):
    response = err.get_response()
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
    
#--- Profile Routes ---#
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
        rating = get_avg_overall_profile(uid)
        return dumps({"uid": uid, "display_name": display_name, "email": email, "role": role, "photo_url": photo_url, "num_connections": str(connections), "rating": rating}), 200

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
        return dumps({})

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

#--- Admin Routes ---#
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
    uid_admin = request.headers.get('Authorization')
    uid_user = auth.get_user_by_email(data["uid_user"]).uid
    return dumps(give_admin(uid_admin, uid_user))

@app.route("/admin/ban_user", methods=["POST"])
def admin_ban_user():
    """
    ban_user flask
    """
    data = request.get_json()
    uid_admin = request.headers.get('Authorization')
    uid_user = auth.get_user_by_email(data["uid_user"]).uid
    return dumps(ban_user(uid_admin, uid_user))
    
@app.route("/admin/unban_user", methods=["POST"])
def admin_unban_user():
    """
    unban_user flask
    """
    data = request.get_json()
    uid_admin = request.headers.get('Authorization')
    uid_user = auth.get_user_by_email(data["uid_user"]).uid
    return dumps(unban_user(uid_admin, uid_user))
    
@app.route("/admin/remove_user", methods=["POST"])
def admin_remove_user():
    """
    remove_user flask
    """
    data = request.get_json()
    uid_admin = request.headers.get('Authorization')
    uid_user = auth.get_user_by_email(data["uid_user"]).uid
    return dumps(remove_user(uid_admin, uid_user))

#--- Project Master Routes ---#
@app.route("/projects/create", methods=["POST"])
def flask_create_project():
    data = request.get_json()
    uid = request.headers.get('Authorization')
    pid = create_project(uid, data["name"], data["description"], data["due_date"], data["picture"])
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
    uid_to_be_removed = auth.get_user_by_email(data["email_removed"]).uid
    res = remove_project_member(data["pid"], uid, uid_to_be_removed)
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
    res = delete_project(int(data["pid"]), uid)
    return dumps(res)

#--- Notification Routes ---#

@app.route('/notifications/get', methods=['GET'])
def flask_get_notifications():
    uid = request.headers.get('Authorization')
    return dumps(get_notifications(uid))

@app.route('/notifications/clear', methods=['DELETE'])
def flask_clear_notification():
    data = request.get_json()
    uid = request.headers.get('Authorization')
    return dumps(clear_notification(uid, data['nid']))

@app.route('/notifications/clearall', methods=['DELETE'])
def flask_clear_all_notifications():
    uid = request.headers.get('Authorization')
    return dumps(clear_all_notifications(uid))

@app.route('/notification/connection/request', methods=['POST'])
def flask_notification_connection_request():
    data = request.get_json()
    uid = request.headers.get('Authorization')
    return dumps(notification_connection_request(data["user_email"], uid))

#--- Project Management Routes ---#
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
    res = respond_project_invitation(data["pid"], uid, data["accept"])
    return dumps(res)

@app.route("/projects/pin", methods=["POST"])
def flask_pin_project():
    uid = request.headers.get("Authorization")
    data = request.get_json()
    res = pin_project(data["pid"], uid, data["action"])
    return dumps(res)

#--- Connection Routes ---#
@app.route("/connections/request_respond", methods=["POST"])
def flask_connection_request_respond():
    """
    connection_request_respond flask
    """
    uid = request.headers.get("Authorization")
    data = request.get_json()
    return dumps(connection_request_respond(str(uid), data["nid"], data["response"]))
    
@app.route("/connections/get_connection_requests", methods=["GET"])
def flask_get_connection_requests():
    """
    get_connection_requests flask
    """
    uid = request.headers.get("Authorization")
    return dumps(get_connection_requests(uid), indent=4, sort_keys=True, default=str)

@app.route("/connections/get_connected_taskmasters", methods=["GET"])
def flask_get_connected_taskmasters():
    """
    get_connection_requests flask
    """
    uid = request.headers.get("Authorization")
    return dumps(get_connected_taskmasters(uid))

@app.route('/connections/details', methods=['GET'])
def connection_details():
    # name, role, photo_url
    curr_uid = request.headers.get("Authorization")
    uid = request.args.get("uid")
    if is_valid_user(uid) == False:
        return Response(status=400)
    else:
        display_name = str(get_display_name(uid))
        photo_url = str(get_photo(uid))
        role = str(get_role(uid))
        connections = len(get_connection_list(uid))
        rating = get_avg_overall_conn(curr_uid, uid)
        email = str(get_email(uid))
        return dumps({"display_name": display_name, "role": role, "photo_url": photo_url, "num_connections": str(connections), "rating": rating, "email": email})

@app.route('/connections/remove_taskmaster', methods=['POST'])
def flask_remove_connected_taskmaster():
    """
    remove_connected_taskmaster flask
    """
    uid = request.headers.get("Authorization")
    data = request.get_json()
    return dumps(remove_connected_taskmaster(uid, data["uid_remove"]))

@app.route('/connections/search_taskmasters', methods=['GET'])
def flask_search_taskmasters():
    """
    search_taskmasters flask
    """
    uid = request.headers.get("Authorization")
    data = request.get_json()
    return dumps(search_taskmasters(uid, data["search_string"]))
    
#--- Task Management Routes ---#
@app.route('/upload_file1', methods = ['POST'])
def flask_upload_file():
    """
    Flask upload file to storage
    """
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(f"src/{filename}")
    return dumps(filename)
    
@app.route('/upload_file2', methods = ['POST'])
def flask_upload_file2():
    """
    Flask upload file details to firestore
    """
    uid = request.headers.get('Authorization')
    data = request.get_json()
    data = upload_file(uid, data['file'], data["destination_name"], data["tid"])
    return dumps(data, indent=4, sort_keys=True, default=str)

@app.route('/get_file_link', methods = ['GET'])
def flask_get_file_link():
    """
    Flask get link to file on storage
    """
    uid = request.headers.get('Authorization')
    tid = request.args.get("tid")
    fileName = request.args.get("fileName")
    return dumps(get_file_link(uid, tid, fileName))

# CREATE #
@app.route("/epic/create", methods=["POST"])
def flask_create_epic():
    """
    Creates an epic
    """
    data = request.get_json()
    uid = request.headers.get("Authorization")
    return dumps(create_epic(uid, data["pid"], data["title"], data["description"], data["colour"]))

@app.route("/task/create", methods=["POST"])
def flask_create_task():
    """
    Creates a task
    """
    data = request.get_json()
    uid = request.headers.get("Authorization")
    return dumps(create_task(uid, data["pid"], data["eid"], data["assignees"], data["title"], data["description"], data["deadline"],
                data["workload"], data["priority"], data["status"]))

@app.route("/subtask/create", methods=["POST"])
def flask_create_subtask():
    """
    Creates a subtask
    """
    data = request.get_json()
    uid = request.headers.get("Authorization")
    return dumps(create_subtask(uid, data["tid"], int(data["pid"]), data["assignees"], data["title"], data["description"], data["deadline"],
                          data["workload"], data["priority"], data["status"]))

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

@app.route("/task/assign", methods=["POST"])
def flask_task_assign():
    """
    assign task
    """
    data = request.get_json()
    uid = request.headers.get("Authorization")
    return dumps(assign_task(uid, data["tid"], data["new_assignees"]))

@app.route("/subtask/assign", methods=["POST"])
def flask_subtask_assign():
    """
    assign subtask
    """
    data = request.get_json()
    uid = request.headers.get("Authorization")
    return dumps(assign_subtask(uid, data["stid"], data["new_assignees"]))

# UPDATE #
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
    return dumps(update_task(uid, data["tid"], data["eid"], 
                             data["title"], data["description"], data["deadline"], 
                             data["workload"], data["priority"], data["status"], data["flagged"]))

@app.route("/subtask/update", methods=["POST"])
def flask_subtask_update():
    """
    update subtask
    """
    data = request.get_json()
    uid = request.headers.get("Authorization")
    return dumps(update_subtask(uid, data["stid"], data["assignees"], 
                                data["title"], data["description"], data["deadline"], 
                                data["workload"], data["priority"], data["status"]))

@app.route("/task/comment", methods=["POST"])
def flask_task_comment():
    """
    Comment on a task
    """
    data = request.get_json()
    uid = request.headers.get("Authorization")
    return dumps(comment_task(uid, data["tid"], data["comment"]))

# TASKBOARD #
@app.route("/taskboard/show", methods=["GET"])
def flask_taskboard_show():
    """
    retrieves the taskboard
    """
    uid = request.headers.get("Authorization")
    pid = request.args.get("pid")
    hidden = request.args.get("hidden")
    return dumps(get_taskboard(uid, int(pid), bool(hidden)), indent=4, sort_keys=True, default=str)

# SEARCH #
@app.route("/taskboard/search", methods=["GET"])
def flask_taskboard_search():
    """
    Retrieve list of tasks in project using query
    """
    uid = request.headers.get("Authorization")
    pid = request.args.get("pid")
    query = request.args.get("query")
    return dumps(search_taskboard(uid, pid, query))

# ASSIGNED TASK LIST #
@app.route("/tasklist/show", methods=["GET"])
def flask_tasklist_show():
    """
    Retrieve the tasklist
    """
    uid = request.headers.get("Authorization")
    show_completed = True
    return dumps(get_user_assigned_task(uid, show_completed))

@app.route("/tasklist/search", methods=["GET"])
def flask_tasklist_search():
    """
    searches the tasklist using a couple of queries
    including id, title, description and deadline
    """
    uid = request.headers.get("Authorization")
    query_tid = request.args.get("query_tid")
    query_title = request.args.get("query_title")
    query_description = request.args.get("query_description")
    query_deadline = request.args.get("query_deadline")
    return dumps(search_tasklist(uid, query_tid, query_title, query_description, query_deadline))

#--- Achievement Routes ---#
@app.route("/achievements/view/my", methods=["GET"])
def flask_view_achievements():
    uid = request.headers.get("Authorization")

    return dumps(view_achievement(uid))

@app.route("/achievements/view/notmy", methods=["GET"])
def flask_view_connected_tm_achievement():
    uid = request.headers.get("Authorization")

    conn_uid = request.args.get("conn_uid")
    return dumps(view_connected_tm_achievement(uid, conn_uid))

@app.route("/achievements/toggle_visibility", methods=["POST"])
def flask_toggle_achievement_visibility():
    uid = request.headers.get("Authorization")
    data = request.get_json()
    return dumps(toggle_achievement_visibility(uid, data["action"]))

@app.route("/achievements/get_hide_visibility", methods=["GET"])
def flask_check_achievement_visibility():
    uid = request.args.get("uid")

    return dumps(check_achievement_visibility(uid))

@app.route("/achievements/share", methods=["POST"])
def flask_share_achievement():
    sender_uid = request.headers.get('Authorization')
    data = request.get_json()
    uid_list = []
    for email in data["receiver_emails"]:
        uid_list.append(auth.get_user_by_email(email).uid)
    return dumps(share_achievement(sender_uid, uid_list, data["aid"]))

@app.route("/achievements/locked", methods=["GET"])
def flask_locked_achievement():
    uid = request.args.get("uid")

    return dumps(list_unachieved(uid))

@app.route('/achievements/name', methods=['GET'])
def flask_get_name_achievement():
    uid = request.args.get("uid")
    display_name = str(get_display_name(uid))
    return dumps({"display_name": display_name})

#--- Reputation Routes ---#
@app.route("/reputation/add_review", methods=["POST"])
def flask_add_review():
    reviewer_uid = request.headers.get("Authorization")
    data = request.get_json()
    
    return dumps(write_review(reviewer_uid, data["reviewee_uid"], data["pid"], 
                              data["communication"], data["time_management"], 
                              data["task_quality"], data["comment"]))

@app.route("/reputation/view_reputation", methods=["GET"])
def flask_view_reputation():
    viewer_uid = request.headers.get("Authorization")
    viewee_uid = request.args.get("viewee_uid")
    return dumps(view_reviews(viewer_uid, viewee_uid))

@app.route("/reputation/toggle_visibility", methods=["POST"])
def flask_toggle_reputation_visibility():
    uid = request.headers.get("Authorization")
    data = request.get_json()
    return dumps(change_review_visibility(uid, data["visibility"]))

@app.route("/reputation/get_visibility", methods=["GET"])
def flask_get_reputation_visibility():
    uid = request.args.get("uid")
    return dumps(get_review_visibility(uid))

@app.route("/reputation/update_review", methods=["POST"])
def flask_update_review():
    reviewer_uid = request.headers.get("Authorization")
    data = request.get_json()
    return dumps(update_review(reviewer_uid, data["reviewee_uid"], data["pid"], 
                               data["communication"], data["time_management"], 
                               data["task_quality"], data["comment"]))

@app.route("/reputation/get_avg_reviews", methods=['GET'])
def flask_get_avg_reviews():
    viewer_uid = request.headers.get("Authorization")
    viewee_uid = request.args.get("viewee_uid")
    return dumps(get_avg_reviews(viewer_uid, viewee_uid))

#--- Workload Routes ---#
@app.route("/workload/get_user_workload", methods=["GET"])
def flask_get_user_workload():
    """
    Returns workload of a user for a certain project
    """
    uid = request.headers.get("Authorization")
    return dumps(get_user_workload(uid))

@app.route("/workload/update_user_availability", methods=["POST"])
def flask_update_user_availability():
    """
    Updates availability of a user for a certain project
    """
    uid = request.headers.get("Authorization")
    data = request.get_json()
    return dumps(update_user_availability(uid, data["availability"]))

@app.route("/workload/get_availability", methods=["GET"])
def flask_get_availability():
    """
    Returns users availability for a certain project
    """
    uid = request.headers.get("Authorization")
    return dumps(get_availability(uid))

@app.route("/workload/get_availability_ratio", methods=["GET"])
def flask_get_availability_ratio():
    """
    Returns availability ratio of a user in a certain project
    """
    uid = request.headers.get("Authorization")
    return dumps(get_availability_ratio(uid))

@app.route("/workload/calculate_supply_demand", methods=["GET"])
def flask_calculate_supply_demand():
    """
    Calculates and adds snd into a project
    """
    uid = request.headers.get("Authorization")
    return dumps(calculate_supply_demand(uid), indent=4, sort_keys=True, default=str)

@app.route("/workload/get_supply_demand", methods=["GET"])
def flask_get_supply_and_demand():
    """
    Returns snd list for a project
    """
    uid = request.headers.get("Authorization")
    return dumps(get_supply_and_demand(uid))
    
@app.route("/subtasks/get_all", methods=["GET"])
def flask_subtask_get_all():
    uid = request.headers.get("Authorization")
    tid = int(request.args.get('tid'))
    return dumps(get_all_subtasks(uid, tid))

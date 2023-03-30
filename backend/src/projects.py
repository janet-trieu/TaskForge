'''
Feature: Project Management
Functionalities:
 - view_project()
 - request_leave_project()
'''

'''
TO-DO get stuff related to tasks and epics
'''

from firebase_admin import firestore, auth

from .error import *
from .notifications import *
from .test_helpers import *
from .proj_class import *

db = firestore.client()

def view_project(pid, uid):
    '''
    Takes in project id, and a user id, to view the specified project
    If the specified user is not a part of the project, they cannot view the project

    Arguments:
    - pid (project id)
    - uid (user id)

    Returns:
    - full project details if user is part of the project

    Raises:
    - InputError for any incorrect values
    '''

    if pid < 0:
        raise InputError(f"ERROR: Invalid project id supplied {pid}")
    
    project = get_project(pid)
    if project == None:
        raise InputError(f"ERROR: Failed to get reference for project {pid}")
    
    # check whether the specified uid exists
    check_valid_uid(uid)

    if not uid in project["project_members"]:
        raise AccessError(f"ERROR: User is not in the project")
    
    return project

def search_project(uid, query):
    '''
    Takes in user id and a search query (string)
    Returns the project details of all the projects that the user is a part of

    Arguments:
    - uid (user id)
    - query (string)

    Returns:
    - full project details if user is part of the project (dictionary)

    Raises:
    '''
    
    check_valid_uid(uid)

    docs = db.collection("projects").stream()

    return_list = []
    for doc in docs:
        pid = doc.to_dict().get("pid")
        project = get_project(pid)
        pm_uid = project["uid"]
        pm_name = auth.get_user(str(pm_uid)).display_name

        if query.lower() in project["name"].lower() or query.lower() in project["description"].lower() or query.lower() in pm_name.lower() or query == "":
            if uid in project["project_members"]:
                return_list.append(get_project(pid))
                print(f"Successfully added {project['name']} to list of search result")

    return_list = list(filter(None, return_list))

    if len(return_list) == 1:
        return return_list[0]

    return return_list

def request_leave_project(pid, uid, msg):
    '''
    Request to leave a project 
    Cannot request if the user is not in that project

    Arguments:
    - pid (project id)
    - uid (task master id)
    - msg (string, message of the reason to request to leave the project)

    Returns:
    A dictionary of:
    - project master email
    - the requesting task master's email
    - msg title
    - msg body

    Raises:
    - AccessError for uid not in project
    - InputError for invalid pid, invalid uid, no msg
    '''

    if pid < 0:
        raise InputError(f"ERROR: Invalid project id supplied {pid}")
    
    proj_ref = db.collection("projects").document(str(pid))
    if proj_ref == None:
        raise InputError(f"ERROR: Failed to get reference for project {pid}")
    
    # check whether the specified uid exists
    check_valid_uid(uid)

    if uid not in proj_ref.get().get("project_members"):
        raise AccessError("Cannot request to leave a project the user is not a part of")

    if len(msg) <= 0:
        raise InputError("Need a message to request to leave project")

    pm_uid = proj_ref.get().get("uid")
    pm_email = auth.get_user(pm_uid).email
    sender_email = auth.get_user(uid).email
    proj_name = proj_ref.get().get("name")

    return_dict = {
        "receipient_email": pm_email,
        "sender_email": sender_email,
        "msg_title": f"Request to leave {proj_name}",
        "msg_body": msg
    }

    return return_dict


def respond_project_invitation(pid, uid, accept, msg):
    '''
    Respond to a project invitation
    - either accept to be added to the project
    - reject to not be added to the project

    Arguments:
    - pid (project id)
    - uid (task master id)
    - msg (string, msg to respond back to the project master)

    Returns:
    - 0 for successful response

    Raises:
    - AccessError for incorrect uid
    - InputError for invalid pid, or invalid new project details
    '''

    if pid < 0:
        raise InputError(f"ERROR: Invalid project id supplied {pid}")
    
    check_valid_uid(uid)

    proj_ref = db.collection("projects").document(str(pid))
    if proj_ref == None:
        raise InputError(f"ERROR: Failed to get reference for project {pid}")

    if msg == "":
        raise InputError("ERROR: Need to give response message to the invitation")

    doc = db.collection("notifications").document(uid).get().to_dict()

    for key, val in doc.items():
        if val.get("pid") == pid and "project_invite" in key:
            notif_id = key
            invite_ref = val

    time_sent = invite_ref.get("time_sent")
    notif_type = invite_ref.get("notif_type")

    pm_uid = proj_ref.get().get("uid")
    pm_name = auth.get_user(pm_uid).display_name

    # if accepted == True, change the notification to be read, and for the response to be set as True
    # else, change the notification to be read, but response kept as False
    if accept == True:
        notification = {
            notif_id : {
                "has_read": True,
                "notification_msg": f"{pm_name} has invited you to join {proj_ref.get().get('name')}.",
                "pid": pid,
                "time_sent": time_sent,
                "type": notif_type,
                "uid_sender": pm_uid,
                "response": True,
                "nid": notif_id
            }
        }

        db.collection("notifications").document(uid).update(notification)

        # add the invited task master to the project
        add_tm_to_project(pid, uid)
    else:
        notification = {
            notif_id : {
                "has_read": True,
                "notification_msg": f"{pm_name} has invited you to join {proj_ref.get().get('name')}.",
                "pid": pid,
                "time_sent": time_sent,
                "type": notif_type,
                "uid_sender": pm_uid,
                "response": False,
                "nid": notif_id
            }
        }

    db.collection("notifications").document(uid).update(notification)

    # send notification to the project master
    # TODO

    return 0

def pin_project(pid, uid, is_pinned):
    '''
    Pin or unpin a project 
    - has to be in the project
    - cannot "pin" a pinned project

    Arguments:
    - pid (project id)
    - uid (project or task master id)
    - is_pinned (bool)

    Returns:
    - 0 for successful response

    Raises:
    - AccessError for uid not in project
    - InputError for invalid pid, trying to pin a pinned project 
        or vice versa
    '''

    if pid < 0:
        raise InputError(f"ERROR: Invalid project id supplied {pid}")
    
    check_valid_uid(uid)

    proj_ref = db.collection("projects").document(str(pid))
    if proj_ref == None:
        raise InputError(f"ERROR: Failed to get reference for project {pid}")

    if uid not in proj_ref.get().get("project_members"):
        raise AccessError(f"ERROR: Cannot pin/unpin a project you are not in")

    curr_pin = proj_ref.get().get("is_pinned")

    # specified project is not pinned, and user wants to pin
    if (curr_pin == False and is_pinned == True) or (curr_pin == True and is_pinned == False):
        proj_ref.update({
            "is_pinned": is_pinned
        })

    else:
        raise InputError(f"ERROR: Cannot pin/unpin a project that is already pinned/unpinned")

    return 0

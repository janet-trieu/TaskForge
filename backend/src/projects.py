'''
Feature: Project Management
Functionalities:
 - view_project()
 - request_leave_project()
'''

from firebase_admin import firestore, auth
from .global_counters import *
from .error import *
from .notifications import *
from .helper import *

db = firestore.client()

'''
Takes in project id, and a user id, to view the specified project
If the specified user is not a part of the project, they have restricted views
 - only project master name, and project name

Arguments:
- pid (project id)
- uid (user id)

Returns:
- full project details if user is part of the project
- restrictied details if user is not part of the project

Raises:
- InputError for any incorrect values
'''
def view_project(pid, uid):

    if pid < 0:
        raise InputError(f"ERROR: Invalid project id supplied {pid}")
    
    proj_ref = db.collection("projects").document(str(pid))
    if proj_ref == None:
        raise InputError(f"ERROR: Failed to get reference for project {pid}")
    
    # check whether the specified uid exists
    check_valid_uid(uid)

    pm_id = proj_ref.get().get("uid")
    pm_name = get_display_name(pm_id)
    project_name = proj_ref.get().get("name")
    description = proj_ref.get().get("description")
    project_members = proj_ref.get().get("project_members")

    return_dict = {}

    if uid in proj_ref.get().get("project_members"):
        return_dict = {
            "project_master": pm_name,
            "name": project_name,
            "description": description,
            "project_members": project_members,
            "tasks": []
        }
    else:
        return_dict = {
            "project_master": pm_name,
            "name": project_name,
        }

    return return_dict

'''
Takes in user id and a search query (string)
Returns the project details of all the projects that the user is a part of
Any project the user is not a part of, has restricted information
 - only project master name, and project name

Arguments:
- uid (user id)
- query (string)

Returns:
- full project details if user is part of the project
- restrictied details if user is not part of the project
Above are returned as a list of dictionary

Raises:
'''
def search_project(uid, query):

    check_valid_uid(uid)

    docs = db.collection("projects").stream()

    return_list = []
    for doc in docs:
        return_dict = {}
        pm_uid = doc.to_dict().get("uid")
        pm_name = auth.get_user(pm_uid).display_name
        proj_name = doc.to_dict().get("name")
        status = doc.to_dict().get("status")

        description = doc.to_dict().get("description")
        project_members = doc.to_dict().get("project_members")
        if query.lower() in proj_name.lower() or query.lower() in description.lower() or query.lower() in pm_name.lower() or query == "":
            if uid in project_members:
                return_dict = {
                    "project_master": pm_name,
                    "name": proj_name,
                    "description": description,
                    "project_members": project_members,
                    "tasks": [],
                    "status": status
                }
            else:
                return_dict = {
                    "project_master": pm_name,
                    "name": proj_name
                }
        
        return_list.append(return_dict)
        print(f"Successfully added {proj_name} to list of search result")

    return_list = list(filter(None, return_list))

    return return_list


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
def request_leave_project(pid, uid, msg):

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
    pm_name = auth.get_user(pm_uid).display_name
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
        
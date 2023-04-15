'''
Feature: Project Master
Functionalities:
 - revive_completed_project()
 - remove_project_member()
 - request_leave_project()
 - invite_to_project()
 - update_project()
'''
from firebase_admin import firestore

from .global_counters import *
from .error import *
from .notifications import *
from .helper import *
from .connections import *
from .classes import *
from .profile_page import *
from .achievement import *

db = firestore.client()

def create_project(uid, name, description, due_date, team_strength, picture):
    '''
    Create a project with the given arguments
    * project status is initialised to Not Started

    Arguments:
    - uid (user that creates the project, also becomes the project master)
    - name (project name)
    - description (project description)
    - due_date (project due date, can be None)
    - team_strength (can be None)
    - picture (can be None)

    Returns:
    - pid (project id) when successful

    Raises:
    - InputError for any incorrect values
    '''

    # setting default values 
    if team_strength == None or team_strength == "":
        team_strength = ""
    if picture == None or picture == "":
        picture = "bleh.png"

    check_valid_uid(uid)

    # check for invalid type inputs:
    if not type(name) == str:
        raise InputError("Project name has to be type of string!!!")
    if not type(description) == str:
        raise InputError("Project description has to be type of string!!!")
    # if not due_date == None:
    #     if not isinstance(due_date, date):
    #         raise InputError("Project due date has to be type of date!!!")
    if not type(team_strength) == str:
        raise InputError("Project team strength has to be type of str!!!")
    # below will have to have more checks implemented to ensure the input is a valid picture, type of png, jpg or jpeg
    if not type(picture) == str:
        raise InputError("Project picture has to be type of string!!!")

    # check for invalid value inputs:
    if len(name) >= 50:
        raise InputError("Project name is too long. Please keep it below 50 characters.")
    if len(name) <= 0:
        raise InputError("Project requires a name!!!")
    if len(description) >= 1000:
        raise InputError("Project description is too long. Please keep it below 1000 characters.")
    if len(description) <= 0:
        raise InputError("Project requies a description!!!")
    
    # TO-DO: check for due date being less than 1 day away from today
    if not team_strength == "" and int(team_strength) < 0:
        raise InputError("Team strength cannot be less than 0!!!")

    proj_ref = db.collection("projects")
    value = get_curr_pid()
    tasks = {
            "Not Started": [],
            "In Progress": [],
            "Blocked": [],
            "In Review/Testing": [],
            "Completed": []
    }
    project = Project(value, uid, name, description, "Not Started", due_date, team_strength, picture, [uid], [], tasks, [], [])
    proj_ref.document(str(value)).set(project.to_dict())

    # add the newly generated pid into the project master's project list
    user_ref = db.collection("users").document(str(uid))
    proj_list = user_ref.get().get("projects")
    proj_list.append(value)
    user_ref.update({"projects": proj_list})
    
    # update the pid after creating a project
    update_pid()

    return value

def is_user_project_master(pid, uid):
    '''
    Helper function for project master:
    Checks whether the uid given is the project master id of the specified project

    Arguments:
    - pid (project id)
    - uid (user id)

    Returns:
    - 0 if the supplied uid is a project master of the specified project

    Raises:
    - AccessError if the supplied user id is not the project master
    '''

    proj_ref = db.collection("projects").document(str(pid))
    proj_master_id = proj_ref.get().get("uid")

    if uid == proj_master_id:
        return 0
    else:
        raise AccessError(f"ERROR: Supplied user id:{uid} is not the project master of project:{pid}")

def revive_completed_project(pid, uid, new_status):
    '''
    Revives a project where its status has been set to Completed
    The new status can be anything except Completed

    Arguments:
    - pid (project id)
    - uid (user id)
    - new_status (new status of the project)

    Returns:
    - 0 if the revival was successful

    Raises:
    - AccessError for incorrect uid
    - InputError for invalid pid, or invalid project status value
    '''

    if pid < 0:
        raise InputError(f"ERROR: Invalid project id supplied {pid}")

    is_valid_uid = is_user_project_master(pid, uid)

    if not is_valid_uid == 0:
        raise AccessError(f"ERROR: Supplied uid is not the project master of project:{pid}" )
    
    proj_ref = db.collection("projects").document(str(pid))
    if proj_ref == None:
        raise InputError(f"ERROR: Failed to get reference for project {pid}")
    
    # check whether the specified uid exists
    check_valid_uid(uid)

    if not proj_ref.get().get("status") == "Completed":
        raise InputError(f"ERROR: Cannot revive a project that is not Completed")

    if new_status not in ["Not Started", "In Progress", "In Review", "Blocked"]:
        raise InputError("Selected Status not available")

    proj_ref.update({
        "status": new_status
    })

    return 0

def remove_project_member(pid, uid, uid_to_be_removed):
    '''
    Removes a specific project member within the project

    Arguments:
    - pid (project id)
    - uid (user id)
    - uid_to_be_removed (user id of the member to be removed)

    Returns:
    - 0 if the removal was successful

    Raises:
    - AccessError for incorrect uid
    - InputError for invalid pid, or invalid uid_to_be_removed
    '''

    '''
    assumption: project already has members
    '''
    if pid < 0:
        raise InputError(f"ERROR: Invalid project id supplied {pid}")

    is_valid_uid = is_user_project_master(pid, uid)

    if not is_valid_uid == 0:
        raise AccessError(f"ERROR: Supplied uid:{uid} is not the project master of project:{pid}")

    proj_ref = db.collection("projects").document(str(pid))
    if proj_ref == None:
        raise InputError(f"ERROR: Failed to get reference for project {pid}")

    # check whether the specified uid exists
    check_valid_uid(uid)

    # check if the uid_to_be_removed is in the project
    project_members = proj_ref.get().get("project_members")

    if not uid_to_be_removed in project_members:
        raise InputError(f"ERROR: Failed to remove the specified user {uid_to_be_removed} from project {pid}")

    project_members.remove(uid_to_be_removed)

    proj_ref.update({
        "project_members": project_members
    })

    return 0

def invite_to_project(pid, sender_uid, receiver_uids):
    '''
    Invite a specific user to a project

    Arguments:
    - pid (project id)
    - sender_uid (project master id)
    - receiver_uids (list of the uids to be invited to project)

    Returns:
    - 0 for success

    Raises:
    - AccessError for incorrect uid
    - InputError for invalid pid, or invalid receiver_uids, or inviting a user thats already in the project
    '''
    
    if pid < 0:
        raise InputError(f"ERROR: Invalid project id supplied {pid}")
    
    is_valid_uid = is_user_project_master(pid, sender_uid)

    if not is_valid_uid == 0:
        raise AccessError(f"ERROR: Supplied uid is not the project master of project:{pid}")

    project = get_project(pid)
    if project == None:
        raise InputError(f"ERROR: Failed to get reference for project {pid}")

    project_members = project["project_members"]

    connection_list = get_connected_taskmasters(sender_uid)
    connection_uid_list = []
    for connection in connection_list:
        connection_uid_list.append(connection["uid"])

    for uid in receiver_uids:
        # check whether the specified uid exists
        check_valid_uid(uid)

        if uid not in connection_uid_list:
            raise InputError(f"ERROR: specifid uid {uid} is not connected to the project master {sender_uid}")

        if uid in project_members:
            raise InputError(f"ERROR: Specified uid:{uid} is already a project member of project:{pid}")

        # Add project invitation notification data in database
        notification_project_invite(uid, sender_uid, pid)

    return 0

def update_project(pid, uid, updates):
    '''
    Update a specific project's details
    - Can update any detail except the project master uid

    Arguments:
    - pid (project id)
    - uid (project master id)
    - updates (dictionary, containing the key (project detail type) and the value (new project detail)

    Returns:
    - 0 for successful update

    Raises:
    - AccessError for incorrect uid
    - InputError for invalid pid, or invalid new project details
    '''
    
    if pid < 0:
        raise InputError(f"ERROR: Invalid project id supplied {pid}")
    
    is_valid_uid = is_user_project_master(pid, uid)

    if not is_valid_uid == 0:
        raise AccessError(f"ERROR: Supplied uid is not the project master of project:{pid}")

    proj_ref = db.collection("projects").document(str(pid))
    if proj_ref == None:
        raise InputError(f"ERROR: Failed to get reference for project {pid}")

    if updates == {}:
        raise InputError(f"ERROR: Cannot call this function without making any updates")

    for key, val in updates.items():
        if key == "name":
            if not type(val) == str:
                raise InputError("Project name has to be type of string")
            elif len(val) >= 50:
                raise InputError("Project name is too long. Please keep it below 50 characters.")
            elif len(val) <= 0:
                raise InputError("Project requires a name!!!")
            else:
                proj_ref.update({
                    "name": val
                })
        elif key == "description":
            if not type(val) == str:
                raise InputError("Project description has to be type of string")
            elif len(val) >= 1000:
                raise InputError("Project description is too long. Please keep it below 1000 characters.")
            elif len(val) <= 0:
                raise InputError("Project requies a description!!!")
            else:
                proj_ref.update({
                    "description": val
                })
        elif key == "status":
            if not type(val) == str:
                raise InputError("Project status has to be type of string")
            elif not val in ("Not Started", "In Progress", "In Review", "Blocked", "Completed"):
                raise InputError("Project status is incorrect. Please choose an appropriate staus of 'Not Started', 'In Progress', 'In Review', 'Blocked', 'Completed'.")
            # elif val == proj_ref.get().get("status"):
            #     raise InputError("Cannot update the status of the project to its current status")
            elif proj_ref.get().get("status") == "Completed":
                raise AccessError(f"ERROR: Cannot update the status of a completed project. Please use revive_completed_project instead")
            else:
                proj_ref.update({
                    "status": val
                })
                if val == "Completed":
                    update_user_num_projs_completed(uid)
                    check_achievement("project_completion", uid)
        elif key == "due_date":
            if not type(val) == str:
                raise InputError("Project due date has to be type of string")
            proj_ref.update({
                    "due_date": val
            })
        elif key == "team_strength":
            if not type(val) == str:
                raise InputError("Project team strength has to be type of str")
            elif not val == "" and int(val) < 0:
                raise InputError("Team strength cannot be less than 0!!!")
            else:
                proj_ref.update({
                    "team_strength": val
                })
        elif key == "picture":
            if not type(val) == str:
                raise InputError("Project picture url has to be type of string")
            proj_ref.update({
                "picture": val
            })
        else:
            raise InputError(f"Specified project detail {key} does not exist")
    
    return 0

def delete_project(pid, uid):
    '''
    Delete a specified project
    - Can only be done by a project master

    Arguments:
    - pid (project id)
    - uid (project master id)

    Returns:
    - 0 for successful update

    Raises:
    - AccessError for incorrect uid
    - InputError for invalid pid
    '''

    if pid < 0:
        raise InputError(f"ERROR: Invalid project id supplied {pid}")
    
    is_valid_uid = is_user_project_master(pid, uid)

    if not is_valid_uid == 0:
        raise AccessError(f"ERROR: Supplied uid is not the project master of project:{pid}")

    proj_ref = db.collection("projects").document(str(pid))
    if proj_ref == None:
        raise InputError(f"ERROR: Failed to get reference for project {pid}")

    db.collection("projects").document(str(pid)).delete()

    return 0
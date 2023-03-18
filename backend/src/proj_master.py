'''
Feature: Project Master
Functionalities:
 - revive_completed_project()
 - remove_project_member()
 - request_leave_project()
 - invite_to_project()
 - update_project()
'''
from firebase_admin import firestore, auth
from .global_counters import *
from .error import *
from .notifications import *
from .helper import *

db = firestore.client()

'''
Create a project with supplied arguments
Returns:
 - pid of newly generated project if successful
 - error if failed to create project
'''
def create_project(uid, name, description, due_date, team_strength, picture):

    # setting default values 
    if due_date == None:
        due_date = None
    if team_strength == None:
        team_strength = None
    if picture == None:
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
    if not team_strength == None:
        if not type(team_strength) == int:
            raise InputError("Project team strength has to be type of int!!!")
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
    if not team_strength == None:
        if team_strength < 0:
            raise InputError("Team strength cannot be less than 0!!!")

    data = {
        "uid": uid,
        "name": name,
        "description": description,
        "status": "Not Started",
        "due_date": due_date,
        "team_strength": team_strength,
        "picture": picture,
        "project_members": [uid]
    }

    # get the current pid to return
    curr_pid = get_curr_pid()

    db.collection("projects").document(str(curr_pid)).set(data)
    
    # update the pid after creating a project
    update_pid()

    return curr_pid

'''
Checks whether the uid given is the project master id of the specified project
Returns:
 - 0 if True
 - error if False
'''
def is_user_project_master(pid, uid):

    proj_ref = db.collection("projects").document(str(pid))
    proj_master_id = proj_ref.get().get("uid")

    if uid == proj_master_id:
        return 0
    else:
        raise AccessError(f"ERROR: Supplied user id:{uid} is not the project master of project:{pid}")

'''
Revives a project where its status has been set to complete,
but have be able to bring it back into progress
pid = project id
uid = user id
'''
def revive_completed_project(pid, uid, new_status):

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

'''
Remove a specific member within the project
Returns:
 - 0 for successful remove
 - Error for failed removal
'''
def remove_project_member(pid, uid, uid_to_be_removed):
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

''''
Invite a specific user to a project
Returns:
 - parameters required to send email for success
 - Error for failed invite
'''
def invite_to_project(pid, sender_uid, receiver_uids):
    
    if pid < 0:
        raise InputError(f"ERROR: Invalid project id supplied {pid}")
    
    is_valid_uid = is_user_project_master(pid, sender_uid)

    if not is_valid_uid == 0:
        raise AccessError(f"ERROR: Supplied uid is not the project master of project:{pid}")

    proj_ref = db.collection("projects").document(str(pid))
    if proj_ref == None:
        raise InputError(f"ERROR: Failed to get reference for project {pid}")

    project_members = proj_ref.get().get("project_members")

    return_dict = {}
    for uid in receiver_uids:

        # check whether the specified uid exists
        check_valid_uid(uid)

        if uid in project_members:
            raise InputError(f"ERROR: Specified uid:{uid} is already a project member of project:{pid}")

        receipient_name = auth.get_user(uid).display_name
        sender_name = auth.get_user(sender_uid).display_name
        project_name = proj_ref.get().get("name")

        # Add project invitation notification data in database
        notification_project_invite(uid, sender_uid, pid)

        receipient_email = auth.get_user(uid).email
        msg_title = f"TaskForge: Project Invitation to {project_name}"
        msg_body = f"Hi {receipient_name}, \n{sender_name} is inviting you to project {project_name}.\nPlease follow the link below to accept or reject this request: https://will_be_added.soon."

        return_dict[uid] = [receipient_email, msg_title, msg_body]

    return return_dict

''''
Update a specific project details
Returns:
 - 0 for successful update
 - Error for failed update
'''
def update_project(pid, uid, updates):
    
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
            elif val == proj_ref.get().get("status"):
                raise InputError("Cannot update the status of the project to its current status")
            elif proj_ref.get().get("status") == "Completed":
                raise AccessError(f"ERROR: Cannot update the status of a completed project. Please use revive_completed_project instead")
            else:
                proj_ref.update({
                    "status": val
                })
        elif key == "due_date":
            if not type(val) == str:
                raise InputError("Project due date has to be type of string")
            proj_ref.update({
                    "due_date": val
            })
        elif key == "team_strength":
            if not type(val) == int:
                raise InputError("Project team strength has to be type of int")
            elif val < 0:
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

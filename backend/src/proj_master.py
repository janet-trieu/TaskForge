'''
Feature: Project Master
Functionalities:
 - revive_completed_project()
 - remove_project_member()
 - request_leave_project()
 - invite_to_project()
'''
from firebase_admin import firestore, auth
from src.global_counters import *

from src.notifications import *

db = firestore.client()

'''
Create a project with supplied arguments
Returns:
 - pid of newly generated project if successful
 - error if failed to create project
'''
def create_project(uid, name, description, status, due_date, team_strength, picture):

    # setting default values 
    if status == None:
        status = "Not Started"
    if due_date == None:
        due_date = None
    if team_strength == None:
        team_strength = None
    if picture == None:
        picture = "bleh.png"

    # check for invalid type inputs:
    if not type(uid) == str:
        raise TypeError("uid has to be type of string!!!")
    if not type(name) == str:
        raise TypeError("Project name has to be type of string!!!")
    if not type(description) == str:
        raise TypeError("Project description has to be type of string!!!")
    if not type(status) == str:
        raise TypeError("Project status has to be type of string!!!")
    # if not due_date == None:
    #     if not isinstance(due_date, date):
    #         raise TypeError("Project due date has to be type of date!!!")
    if not team_strength == None:
        if not type(team_strength) == int:
            raise TypeError("Project team strength has to be type of int!!!")
    # below will have to have more checks implemented to ensure the input is a valid picture, type of png, jpg or jpeg
    if not type(picture) == str:
        raise TypeError("Project picture has to be type of string!!!")

    # check for invalid value inputs:
    if not len(uid) == 28:
        raise ValueError("Invalid uid entered!!!")
    if len(name) >= 50:
        raise ValueError("Project name is too long. Please keep it below 50 characters.")
    if len(name) <= 0:
        raise ValueError("Project requires a name!!!")
    if len(description) >= 1000:
        raise ValueError("Project description is too long. Please keep it below 1000 characters.")
    if len(description) <= 0:
        raise ValueError("Project requies a description!!!")
    
    if not status in ("Not Started", "In Progress", "In Review", "Blocked", "Completed"):
        raise ValueError("Project status is incorrect. Please choose an appropriate staus of 'Not Started', 'In Progress', 'In Review', 'Blocked', 'Completed'.")
    # TO-DO: check for due date being less than 1 day away from today
    if not team_strength == None:
        if team_strength < 0:
            raise ValueError("Team strength cannot be less than 0!!!")

    data = {
        "uid": uid,
        "name": name,
        "description": description,
        "status": status,
        "due_date": due_date,
        "team_strength": team_strength,
        "picture": picture,
        "project_members": [uid]
    }

    # get the current pid to return
    curr_pid = get_curr_pid()

    db.collection("projects_test").document(str(curr_pid)).set(data)

    data = {
        "pid": curr_pid
    }
    db.collection("counters").document("project").set(data)
    
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

    proj_ref = db.collection("projects_test").document(str(pid))
    proj_master_id = proj_ref.get().get("uid")

    if uid == proj_master_id:
        return 0
    else:
        return f"ERROR: Supplied user id:{uid} is not the project master of project:{pid}"

'''
Revives a project where its status has been set to complete,
but have be able to bring it back into progress
pid = project id
uid = user id
'''
def revive_completed_project(pid, uid, new_status):

    is_valid_uid = is_user_project_master(pid, uid)

    if not is_valid_uid == 0:
        return f"ERROR: Supplied uid is not the project master of project:{pid}" 

    if pid < 0:
        return f"ERROR: Invalid project id supplied {pid}"
    
    proj_ref = db.collection("projects_test").document(str(pid))
    if proj_ref == None:
        return f"ERROR: Failed to get reference for project {pid}"
    
    '''
    check if uid exists, assuming exists for now
    '''

    if not proj_ref.get().get("status") == "Completed":
        return f"ERROR: Cannot revive a project that is not Completed"

    if new_status not in ["Not Started", "In Progress", "In Review", "Blocked"]:
        raise ValueError("Selected Status not available")

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

    is_valid_uid = is_user_project_master(pid, uid)

    if not is_valid_uid == 0:
        return f"ERROR: Supplied uid:{uid} is not the project master of project:{pid}" 

    if pid < 0:
        return f"ERROR: Invalid project id supplied {pid}"

    proj_ref = db.collection("projects_test").document(str(pid))
    if proj_ref == None:
        return f"ERROR: Failed to get reference for project {pid}"

    '''
    check if uid exists, assuming exists for now
    '''

    # check if the uid_to_be_removed is in the project
    project_members = proj_ref.get().get("project_members")

    if not uid_to_be_removed in project_members:
        return f"ERROR: Failed to remove the specified user {uid_to_be_removed} from project {pid}"

    project_members.remove(uid_to_be_removed)

    proj_ref.update({
        "project_members": project_members
    })

    return 0
    

# Below shouldnt be in proj_master, but keeping it here till we find somewhere more appropriate
# def reqeust_leave_project():
#     pass

'''
Invite a specific user to a project
Returns:
 - 0 for successful invite
 - Error for failed invite
'''
def invite_to_project(pid, sender_uid, receiver_uid):
    
    is_valid_uid = is_user_project_master(pid, sender_uid)

    if not is_valid_uid == 0:
        return f"ERROR: Supplied uid is not the project master of project:{pid}" 

    if pid < 0:
        return f"ERROR: Invalid project id supplied {pid}"

    proj_ref = db.collection("projects_test").document(str(pid))
    if proj_ref == None:
        return f"ERROR: Failed to get reference for project {pid}"

    print(f"THIS IS RECEIVER UID{receiver_uid}")
    does_uid_exist = auth.get_users([auth.UidIdentifier(receiver_uid)])

    if does_uid_exist == "":
        return f"ERROR: Supplied receiver uid: {receiver_uid} does not exist"

    proj_ref = db.collection("projects_test").document(str(pid))
    project_members = proj_ref.get().get("project_members")

    if receiver_uid in project_members:
        return f"ERROR: Specified uid:{receiver_uid} is already a project member of project:{pid}"

    print(f"THIS IS SENDER UID{sender_uid}")
    receipient_name = auth.get_user(receiver_uid).display_name
    sender_name = auth.get_user(sender_uid).display_name
    project_name = proj_ref.get().get("name")

    notification_project_invite(receiver_uid, sender_uid, pid)

    receipient_email = auth.get_user(receiver_uid).email
    msg_title = f"Hi {receipient_name}, {sender_name} is inviting you to this project: {project_name}"
    msg_body = "Please follow the link below to accept or reject this request: https://will_be_added.soon"

    return (receipient_email, msg_title, msg_body)
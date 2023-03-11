'''
Feature: Project Master
Functionalities:
 - revive_completed_project()
 - remove_project_member()
 - request_leave_project()
 - invite_to_project()
'''
from firebase_admin import firestore
from src.global_counters import *

db = firestore.client()

def check_uid_is_proj_master(pid, uid):
    pass

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

    # print(f"THIS IS team strength @@@@@@@@@@@@@ {team_strength}")
    # print(f"THIS IS team strength @@@@@@@@@@@@@ {type(team_strength)}")

    # check for invalid type inputs:
    if not type(uid) == int:
        raise TypeError("uid has to be type of integer!!!")
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
    if uid < 0:
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
    # check for due date being less than 1 day away from today
    # if due_date <= date.today().strftime('%Y-%m-%d') or due_date <:
    #     raise ValueError("Project due date cannot be less than 1 day away")
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
    print(f"THIS IS CURR PID {curr_pid}")

    return curr_pid

def add_tm_to_project(pid, new_uid):
    proj_ref = db.collection("projects_test").document(str(pid))
    project_members = proj_ref.get().get("project_members")

    if not new_uid in project_members:
        project_members.append(new_uid)

    proj_ref.update({
        "project_members": project_members
    })

'''
Revives a project where its status has been set to complete,
but have be able to bring it back into progress
pid = project id
uid = user id
'''
def revive_completed_project(pid, uid, new_status):
    '''
    check whether supplied pid exists
    check whether supplied uid exists

    set project's status back into review
    '''

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

def remove_project_member(pid, uid, uid_to_be_removed):
    '''
    assumption: project already has members
    '''

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

def invite_to_project():
    pass
'''
Test file for Flask http testing of project master feature
'''
import pytest
import requests
from src.test_helpers import *
from src.helper import *
port = 5000
url = f"http://localhost:{port}/"

try:
    pm_uid = create_user_email("projectmaster@gmail.com", "admin123", "Project Master")
    tm1_uid = create_user_email("projecttest.tm1@gmail.com", "taskmaster1", "Task Master1")
    tm2_uid = create_user_email("projecttest.tm2@gmail.com", "taskmaster1", "Task Master2")
    tm3_uid = create_user_email("projecttest.tm3@gmail.com", "taskmaster1", "Task Master3")
except:
    print("project master and users already created")
else:
    pm_uid = auth.get_user_by_email("projectmaster@gmail.com").uid
    tm1_uid = auth.get_user_by_email("projecttest.tm1@gmail.com").uid
    tm2_uid = auth.get_user_by_email("projecttest.tm2@gmail.com").uid
    tm3_uid = auth.get_user_by_email("projecttest.tm3@gmail.com").uid

############################################################
#                   Test for create_project                #
############################################################

def test_create_project_use_default_vals():

    create_resp = requests.post(url + "projects/create", json={
        "uid": pm_uid,
        "name": "Project0",
        "description": "Creating Project0 for testing",
        "status": None,
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 200

    reset_projects()

def test_create_project_use_all_vals():

    create_resp = requests.post(url + "projects/create", json={
        "uid": pm_uid,
        "name": "Project0",
        "description": "Creating Project0 for testing",
        "status": "Not Started",
        "due_date": "2023-12-31",
        "team_strength": 5,
        "picture": "test1.jpg"
    })

    assert create_resp.status_code == 200

    reset_projects() 

def test_create_multiple_projects():

    create_resp = requests.post(url + "projects/create", json={
        "uid": pm_uid,
        "name": "Project0",
        "description": "Creating Project0 for testing",
        "status": None,
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 200

    create_resp = requests.post(url + "projects/create", json={
        "uid": pm_uid,
        "name": "Project1",
        "description": "Creating Project1 for testing",
        "status": "Not Started",
        "due_date": "2023-12-31",
        "team_strength": 5,
        "picture": "test1.jpg"
    })

    assert create_resp.status_code == 200

    reset_projects() 

def test_create_project_TypeError():

    create_resp = requests.post(url + "projects/create", json={
        "uid": pm_uid,
        "name": -1,
        "description": "Creating Project0 for testing",
        "status": None,
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 400

    reset_projects()

def test_create_project_ValueError():

    create_resp = requests.post(url + "projects/create", json={
        "uid": pm_uid,
        "name": "Project0",
        "description": "",
        "status": None,
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 400

    reset_projects()

def test_create_project_invalid_uid():

    create_resp = requests.post(url + "projects/create", json={
        "uid": "invalid",
        "name": "Project0",
        "description": "Creating Project0 for testing",
        "status": None,
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 400

    reset_projects()

############################################################
#           Test for revive_completed_project              #
############################################################

def test_revive_completed_project():

    create_resp = requests.post(url + "projects/create", json={
        "uid": pm_uid,
        "name": "Project0",
        "description": "Creating Project0 for testing",
        "status": "Completed",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 200
    create_json = create_resp.json()

    print(f"this is create_json: {create_json}")

    # revive completed project back into "In Progress"
    revive_resp = requests.post(url + "projects/revive", json={
        "pid": create_json,
        "uid": pm_uid,
        "new_status": "In Progress"
    })

    assert revive_resp.status_code == 200

    proj_ref = db.collection("projects").document(str(create_json))
    assert proj_ref.get().get("status") == "In Progress"

    reset_projects()

def test_revive_completed_project_not_proj_master():

    incorrect_uid = tm1_uid

    create_resp = requests.post(url + "projects/create", json={
        "uid": pm_uid,
        "name": "Project0",
        "description": "Creating Project0 for testing",
        "status": "Completed",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 200
    create_json = create_resp.json()

    revive_resp = requests.post(url + "projects/revive", json={
        "pid": create_json,
        "uid": incorrect_uid,
        "new_status": "In Progress"

    })

    assert revive_resp.status_code == 403

    proj_ref = db.collection("projects").document(str(create_json))
    assert proj_ref.get().get("status") == "Completed"

    reset_projects()

def test_revive_non_completed_project():

    create_resp = requests.post(url + "projects/create", json={
        "uid": pm_uid,
        "name": "Project0",
        "description": "Creating Project0 for testing",
        "status": "In Progress",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 200
    create_json = create_resp.json()

    revive_resp = requests.post(url + "projects/revive", json={
        "pid": create_json,
        "uid": pm_uid,
        "new_status": "In Review"

    })

    assert revive_resp.status_code == 400

    proj_ref = db.collection("projects").document(str(create_json))
    assert proj_ref.get().get("status") == "In Progress"

    reset_projects()

############################################################
#             Test for remove_project_member               #
############################################################

def test_remove_project_member():

    create_resp = requests.post(url + "projects/create", json={
        "uid": pm_uid,
        "name": "Project0",
        "description": "Creating Project0 for testing",
        "status": "In Progress",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 200
    create_json = create_resp.json()

    add_tm_to_project(create_json, tm1_uid)
    add_tm_to_project(create_json, tm2_uid)
    add_tm_to_project(create_json, tm3_uid)

    remove_resp = requests.post(url + "projects/remove", json={
        "pid": create_json,
        "uid": pm_uid,
        "uid_to_be_removed": tm1_uid
    })

    assert remove_resp.status_code == 200

    proj_ref = db.collection("projects").document(str(create_json))
    
    assert tm1_uid not in proj_ref.get().get("project_members")

    reset_projects() 

def test_remove_project_member_not_proj_master():

    create_resp = requests.post(url + "projects/create", json={
        "uid": pm_uid,
        "name": "Project0",
        "description": "Creating Project0 for testing",
        "status": "In Progress",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 200
    create_json = create_resp.json()

    add_tm_to_project(create_json, tm1_uid)

    remove_resp = requests.post(url + "projects/remove", json={
        "pid": create_json,
        "uid": tm2_uid,
        "uid_to_be_removed": tm1_uid
    })

    assert remove_resp.status_code == 403

    proj_ref = db.collection("projects").document(str(create_json))

    assert tm1_uid in proj_ref.get().get("project_members")

    reset_projects() 

def test_remove_project_member_invalid_pid():

    create_resp = requests.post(url + "projects/create", json={
        "uid": pm_uid,
        "name": "Project0",
        "description": "Creating Project0 for testing",
        "status": "In Progress",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 200
    create_json = create_resp.json()

    add_tm_to_project(create_json, tm1_uid)
    add_tm_to_project(create_json, tm2_uid)
    add_tm_to_project(create_json, tm3_uid)

    remove_resp = requests.post(url + "projects/remove", json={
        "pid": -1,
        "uid": pm_uid,
        "uid_to_be_removed": tm1_uid
    })

    assert remove_resp.status_code == 400

    proj_ref = db.collection("projects").document(str(create_json))
    assert tm1_uid in proj_ref.get().get("project_members")

    reset_projects() 

def test_remove_invalid_project_member():

    create_resp = requests.post(url + "projects/create", json={
        "uid": pm_uid,
        "name": "Project0",
        "description": "Creating Project0 for testing",
        "status": "In Progress",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 200
    create_json = create_resp.json()

    remove_resp = requests.post(url + "projects/remove", json={
        "pid": create_json,
        "uid": pm_uid,
        "uid_to_be_removed": tm1_uid
    })

    assert remove_resp.status_code == 400

    reset_projects() 

############################################################
#               Test for invite_to_project                 #
############################################################

def test_invite_to_project():

    tm1_email = auth.get_user(tm1_uid).email

    create_resp = requests.post(url + "projects/create", json={
        "uid": pm_uid,
        "name": "Project0",
        "description": "Creating Project0 for testing",
        "status": "In Progress",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 200
    create_json = create_resp.json()

    invite_resp = requests.post(url + "projects/invite", json={
        "pid": create_json,
        "sender_uid": pm_uid,
        "receiver_uids": [tm1_email]
    })

    assert invite_resp.status_code == 200

    reset_projects() 

def test_multiple_invite_to_project():

    tm1_email = auth.get_user(tm1_uid).email
    tm2_email = auth.get_user(tm2_uid).email
    tm3_email = auth.get_user(tm3_uid).email

    create_resp = requests.post(url + "projects/create", json={
        "uid": pm_uid,
        "name": "Project0",
        "description": "Creating Project0 for testing",
        "status": "In Progress",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 200
    create_json = create_resp.json()

    invite_resp = requests.post(url + "projects/invite", json={
        "pid": create_json,
        "sender_uid": pm_uid,
        "receiver_uids": [tm1_email, tm2_email, tm3_email]
    })

    assert invite_resp.status_code == 200

    reset_projects() 

def test_invite_to_invalid_project():
    
    tm1_email = auth.get_user(tm1_uid).email

    create_resp = requests.post(url + "projects/create", json={
        "uid": pm_uid,
        "name": "Project0",
        "description": "Creating Project0 for testing",
        "status": "In Progress",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 200
    create_json = create_resp.json()

    invite_resp = requests.post(url + "projects/invite", json={
        "pid": -1,
        "sender_uid": pm_uid,
        "receiver_uids": [tm1_email]
    })

    assert invite_resp.status_code == 400

    reset_projects() 

def test_invite_invalid_receiver_uid():
    
    

    create_resp = requests.post(url + "projects/create", json={
        "uid": pm_uid,
        "name": "Project0",
        "description": "Creating Project0 for testing",
        "status": "In Progress",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 200
    create_json = create_resp.json()

    invite_resp = requests.post(url + "projects/invite", json={
        "pid": create_json,
        "sender_uid": pm_uid,
        "receiver_uids": ["doesnt.exist@gmail.com"]
    })

    assert invite_resp.status_code == 400

    reset_projects() 

def test_invite_uid_already_in_project():

    tm1_email = auth.get_user(tm1_uid).email

    create_resp = requests.post(url + "projects/create", json={
        "uid": pm_uid,
        "name": "Project0",
        "description": "Creating Project0 for testing",
        "status": "In Progress",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 200
    create_json = create_resp.json()

    add_tm_to_project(create_json, tm1_uid)

    proj_ref = db.collection("projects").document(str(create_json))

    assert tm1_uid in proj_ref.get().get("project_members")

    invite_resp = requests.post(url + "projects/invite", json={
        "pid": create_json,
        "sender_uid": pm_uid,
        "receiver_uids": [tm1_email]
    })

    assert invite_resp.status_code == 400

    reset_projects() 
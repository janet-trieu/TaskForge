'''
Test file for Flask http testing of project master feature
'''
import pytest
import requests
from test_helpers import *
port = 5000
url = f"http://localhost:{port}/"

proj_master = auth.get_user_by_email("project.master@gmail.com")

task_master1 = auth.get_user_by_email("testingtm1@gmail.com")
task_master2 = auth.get_user_by_email("testingtm2@gmail.com")
task_master3 = auth.get_user_by_email("testingtm3@gmail.com")

############################################################
#                   Test for create_project                #
############################################################

def test_create_project_use_default_vals():

    reset_project_count()

    create_resp = requests.post(url + "projects/create", json={
        "uid": proj_master.uid,
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

    reset_project_count()

    create_resp = requests.post(url + "projects/create", json={
        "uid": proj_master.uid,
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

    reset_project_count()

    create_resp = requests.post(url + "projects/create", json={
        "uid": proj_master.uid,
        "name": "Project0",
        "description": "Creating Project0 for testing",
        "status": None,
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 200

    create_resp = requests.post(url + "projects/create", json={
        "uid": proj_master.uid,
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

    reset_project_count()

    create_resp = requests.post(url + "projects/create", json={
        "uid": proj_master.uid,
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

    reset_project_count()

    create_resp = requests.post(url + "projects/create", json={
        "uid": proj_master.uid,
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

    reset_project_count()

    create_resp = requests.post(url + "projects/create", json={
        "uid": "invalid",
        "name": "Project0",
        "description": "Creating Project0 for testing",
        "status": None,
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 403

    reset_projects()

############################################################
#           Test for revive_completed_project              #
############################################################

def test_revive_completed_project():

    reset_project_count()

    create_resp = requests.post(url + "projects/create", json={
        "uid": proj_master.uid,
        "name": "Project0",
        "description": "Creating Project0 for testing",
        "status": "Completed",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })


    assert create_resp.status_code == 200
    create_json = create_resp.json()

    # revive completed project back into "In Progress"
    revive_resp = requests.post(url + "projects/revive", json={
        "pid": create_json,
        "uid": proj_master.uid,
        "new_status": "In Progress"
    })

    assert revive_resp.status_code == 200

    proj_ref = db.collection("projects_test").document(str(create_json))
    assert proj_ref.get().get("status") == "In Progress"

    reset_projects()

def test_revive_completed_project_not_proj_master():
    
    reset_project_count()

    incorrect_uid = task_master1.uid

    create_resp = requests.post(url + "projects/create", json={
        "uid": proj_master.uid,
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

    proj_ref = db.collection("projects_test").document(str(create_json))
    assert proj_ref.get().get("status") == "Completed"

    reset_projects()

def test_revive_non_completed_project():

    reset_project_count()

    create_resp = requests.post(url + "projects/create", json={
        "uid": proj_master.uid,
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
        "uid": proj_master.uid,
        "new_status": "In Review"

    })

    assert revive_resp.status_code == 400

    proj_ref = db.collection("projects_test").document(str(create_json))
    assert proj_ref.get().get("status") == "In Progress"

    reset_projects()

############################################################
#             Test for remove_project_member               #
############################################################

def test_remove_project_member():

    reset_project_count()

    create_resp = requests.post(url + "projects/create", json={
        "uid": proj_master.uid,
        "name": "Project0",
        "description": "Creating Project0 for testing",
        "status": "In Progress",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 200
    create_json = create_resp.json()

    add_tm_to_project(create_json, task_master1.uid)
    add_tm_to_project(create_json, task_master2.uid)
    add_tm_to_project(create_json, task_master3.uid)

    remove_resp = requests.post(url + "projects/remove", json={
        "pid": create_json,
        "uid": proj_master.uid,
        "uid_to_be_removed": task_master1.uid
    })

    assert remove_resp.status_code == 200

    proj_ref = db.collection("projects_test").document(str(create_json))
    
    assert task_master1.uid not in proj_ref.get().get("project_members")

    reset_projects() 

def test_remove_project_member_not_proj_master():

    reset_project_count()

    create_resp = requests.post(url + "projects/create", json={
        "uid": proj_master.uid,
        "name": "Project0",
        "description": "Creating Project0 for testing",
        "status": "In Progress",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 200
    create_json = create_resp.json()

    add_tm_to_project(create_json, task_master1.uid)

    remove_resp = requests.post(url + "projects/remove", json={
        "pid": create_json,
        "uid": task_master2.uid,
        "uid_to_be_removed": task_master1.uid
    })

    assert remove_resp.status_code == 403

    proj_ref = db.collection("projects_test").document(str(create_json))

    assert task_master1.uid in proj_ref.get().get("project_members")

    reset_projects() 

def test_remove_project_member_invalid_pid():

    reset_project_count()

    create_resp = requests.post(url + "projects/create", json={
        "uid": proj_master.uid,
        "name": "Project0",
        "description": "Creating Project0 for testing",
        "status": "In Progress",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 200
    create_json = create_resp.json()

    add_tm_to_project(create_json, task_master1.uid)
    add_tm_to_project(create_json, task_master2.uid)
    add_tm_to_project(create_json, task_master3.uid)

    remove_resp = requests.post(url + "projects/remove", json={
        "pid": -1,
        "uid": proj_master.uid,
        "uid_to_be_removed": task_master1.uid
    })

    assert remove_resp.status_code == 400

    proj_ref = db.collection("projects_test").document(str(create_json))
    assert task_master1.uid in proj_ref.get().get("project_members")

    reset_projects() 

def test_remove_invalid_project_member():

    reset_project_count()

    create_resp = requests.post(url + "projects/create", json={
        "uid": proj_master.uid,
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
        "uid": proj_master.uid,
        "uid_to_be_removed": task_master1.uid
    })

    assert remove_resp.status_code == 400

    reset_projects() 

############################################################
#               Test for invite_to_project                 #
############################################################

def test_invite_to_project():

    reset_project_count()

    create_resp = requests.post(url + "projects/create", json={
        "uid": proj_master.uid,
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
        "sender_uid": proj_master.uid,
        "receiver_uids": [task_master1.email]
    })

    assert invite_resp.status_code == 200

    reset_projects() 

def test_multiple_invite_to_project():

    reset_project_count()

    create_resp = requests.post(url + "projects/create", json={
        "uid": proj_master.uid,
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
        "sender_uid": proj_master.uid,
        "receiver_uids": [task_master1.email, task_master2.email, task_master3.email]
    })

    assert invite_resp.status_code == 200

    reset_projects() 

def test_invite_to_invalid_project():
    
    reset_project_count()

    create_resp = requests.post(url + "projects/create", json={
        "uid": proj_master.uid,
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
        "sender_uid": proj_master.uid,
        "receiver_uids": [task_master1.email]
    })

    assert invite_resp.status_code == 400

    reset_projects() 

def test_invite_invalid_receiver_uid():
    
    reset_project_count()

    create_resp = requests.post(url + "projects/create", json={
        "uid": proj_master.uid,
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
        "sender_uid": proj_master.uid,
        "receiver_uids": ["doesnt.exist@gmail.com"]
    })

    assert invite_resp.status_code == 400

    reset_projects() 

def test_invite_uid_already_in_project():
    
    reset_project_count()

    create_resp = requests.post(url + "projects/create", json={
        "uid": proj_master.uid,
        "name": "Project0",
        "description": "Creating Project0 for testing",
        "status": "In Progress",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 200
    create_json = create_resp.json()

    add_tm_to_project(create_json, task_master1.uid)

    proj_ref = db.collection("projects_test").document(str(create_json))

    assert task_master1.uid in proj_ref.get().get("project_members")

    invite_resp = requests.post(url + "projects/invite", json={
        "pid": create_json,
        "sender_uid": proj_master.uid,
        "receiver_uids": [task_master1.email]
    })

    assert invite_resp.status_code == 400

    reset_projects() 
'''
Test file for Flask http testing of project management feature
'''
import pytest
import requests
from src.test_helpers import *
from src.helper import *
port = 5000
url = f"http://localhost:{port}/"

reset_projects() 
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
#                     Test for view_project                #
############################################################
def test_view_project():
    
    create_resp = requests.post(url + "projects/create", json={
        "uid": pm_uid,
        "name": "Project0",
        "description": "Creating Project0 for testing",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 200
    create_json = create_resp.json()
    proj_ref = db.collection("projects").document(str(create_json))

    # add tm to project
    add_tm_to_project(create_json, tm1_uid)

    view_resp = requests.get(url + "projects/view", json={
        "pid": create_json,
        "uid": tm1_uid
    })

    pm_name = auth.get_user(pm_uid).display_name
    proj_ref = db.collection("projects").document(str(create_json))
    proj_members = proj_ref.get().get("project_members")

    assert view_resp.status_code == 200
    view_json = view_resp.json()


    assert view_json == {
        "project_master": pm_name,
        "name": "Project0",
        "description": "Creating Project0 for testing",
        "project_members": proj_members,
        "tasks": []
    }

    reset_projects()

def test_view_project_invalid_pid():

    create_resp = requests.post(url + "projects/create", json={
        "uid": pm_uid,
        "name": "Project0",
        "description": "Creating Project0 for testing",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 200
    create_json = create_resp.json()

    view_resp = requests.get(url + "projects/view", json={
        "pid": -1,
        "uid": tm1_uid
    })

    assert view_resp.status_code == 400
        
    reset_projects()

def test_view_project_invalid_uid():

    create_resp = requests.post(url + "projects/create", json={
        "uid": pm_uid,
        "name": "Project0",
        "description": "Creating Project0 for testing",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 200
    create_json = create_resp.json()

    view_resp = requests.get(url + "projects/view", json={
        "pid": create_json,
        "uid": "invalid"
    })

    assert view_resp.status_code == 400

    reset_projects()

def test_view_project_not_in_project():

    create_resp = requests.post(url + "projects/create", json={
        "uid": pm_uid,
        "name": "Project0",
        "description": "Creating Project0 for testing",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 200
    create_json = create_resp.json()
    proj_ref = db.collection("projects").document(str(create_json))

    view_resp = requests.get(url + "projects/view", json={
        "pid": create_json,
        "uid": tm1_uid
    })

    pm_name = auth.get_user(pm_uid).display_name
    proj_ref = db.collection("projects").document(str(create_json))

    assert view_resp.status_code == 200
    view_json = view_resp.json()

    assert view_json == {
        "project_master": pm_name,
        "name": "Project0",
    }
      
    reset_projects()
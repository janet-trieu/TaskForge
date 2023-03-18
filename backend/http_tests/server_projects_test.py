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

############################################################
#                   Test for search_project                #
############################################################

def test_search_project_simple():

    create_resp = requests.post(url + "projects/create", json={
        "uid": pm_uid,
        "name": "Project Alpha",
        "description": "Alpha does Spiking",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 200
    create_json = create_resp.json()

    add_tm_to_project(create_json, tm1_uid)

    proj1 = db.collection("projects").document(str(create_json))
    pm_name = auth.get_user(pm_uid).display_name

    query = "Alpha"

    search_resp = requests.get(url + "projects/search", json={
        "uid": tm1_uid,
        "query": query 
    })

    assert search_resp.status_code == 200
    search_json = search_resp.json()

    assert search_json == [
        {
            "description": proj1.get().get("description"),
            "name": proj1.get().get("name"),
            "project_master": pm_name,
            "project_members": proj1.get().get("project_members"),
            "status": proj1.get().get("status"),
            "tasks": []
        }
    ]

    reset_projects()

def test_search_project_pm_name():

    create_resp = requests.post(url + "projects/create", json={
        "uid": pm_uid,
        "name": "Project Alpha",
        "description": "Alpha does Spiking",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 200
    create_json = create_resp.json()

    add_tm_to_project(create_json, tm1_uid)

    proj1 = db.collection("projects").document(str(create_json))
    pm_name = auth.get_user(pm_uid).display_name

    query = "Master"

    search_resp = requests.get(url + "projects/search", json={
        "uid": tm1_uid,
        "query": query 
    })

    assert search_resp.status_code == 200
    search_json = search_resp.json()

    assert search_json == [
        {
            "description": proj1.get().get("description"),
            "name": proj1.get().get("name"),
            "project_master": pm_name,
            "project_members": proj1.get().get("project_members"),
            "status": proj1.get().get("status"),
            "tasks": []
        }
    ]

    reset_projects()

def test_search_project_verbose():

    create_resp1 = requests.post(url + "projects/create", json={
        "uid": pm_uid,
        "name": "Project Alpha",
        "description": "Alpha does Spiking",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })
    assert create_resp1.status_code == 200

    create_resp2 = requests.post(url + "projects/create", json={
        "uid": pm_uid,
        "name": "Project Beta",
        "description": "Beta does Receiving",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })
    assert create_resp2.status_code == 200

    create_resp3 = requests.post(url + "projects/create", json={
        "uid": pm_uid,
        "name": "Project Gamma",
        "description": "Gamma does Serving",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })
    assert create_resp3.status_code == 200

    create_json1 = create_resp1.json()
    create_json2 = create_resp2.json()
    create_json3 = create_resp3.json()

    add_tm_to_project(create_json1, tm1_uid)
    add_tm_to_project(create_json2, tm1_uid)
    add_tm_to_project(create_json3, tm1_uid)

    proj1 = db.collection("projects").document(str(create_json1))
    proj2 = db.collection("projects").document(str(create_json2))
    proj3 = db.collection("projects").document(str(create_json3))

    pm_name = auth.get_user(pm_uid).display_name

    # tm1 is a part of the 3 projects created above
    query = "Alpha"
    
    search_resp = requests.get(url + "projects/search", json={
        "uid": tm1_uid,
        "query": query 
    })
    assert search_resp.status_code == 200
    search_json = search_resp.json()

    assert search_json == [
        {
            "description": proj1.get().get("description"),
            "name": proj1.get().get("name"),
            "project_master": pm_name,
            "project_members": proj1.get().get("project_members"),
            "status": proj1.get().get("status"),
            "tasks": []
        }
    ]

    query = "Receiving"

    search_resp = requests.get(url + "projects/search", json={
        "uid": tm1_uid,
        "query": query 
    })
    assert search_resp.status_code == 200
    search_json = search_resp.json()

    assert search_json == [
        {
            "description": proj2.get().get("description"),
            "name": proj2.get().get("name"),
            "project_master": pm_name,
            "project_members": proj2.get().get("project_members"),
            "status": proj2.get().get("status"),
            "tasks": []
        }
    ]

    query = "Project"

    search_resp = requests.get(url + "projects/search", json={
        "uid": tm1_uid,
        "query": query 
    })
    assert search_resp.status_code == 200
    search_json = search_resp.json()

    assert search_json == [
        {
            "description": proj1.get().get("description"),
            "name": proj1.get().get("name"),
            "project_master": pm_name,
            "project_members": proj1.get().get("project_members"),
            "status": proj1.get().get("status"),
            "tasks": []
        },
        {
            "description": proj2.get().get("description"),
            "name": proj2.get().get("name"),
            "project_master": pm_name,
            "project_members": proj2.get().get("project_members"),
            "status": proj2.get().get("status"),
            "tasks": []
        },
        {
            "description": proj3.get().get("description"),
            "name": proj3.get().get("name"),
            "project_master": pm_name,
            "project_members": proj3.get().get("project_members"),
            "status": proj3.get().get("status"),
            "tasks": []
        }
    ]

    reset_projects()

def test_search_partial_member():

    create_resp1 = requests.post(url + "projects/create", json={
        "uid": pm_uid,
        "name": "Project Alpha",
        "description": "Alpha does Spiking",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })
    assert create_resp1.status_code == 200

    create_resp2 = requests.post(url + "projects/create", json={
        "uid": pm_uid,
        "name": "Project Beta",
        "description": "Beta does Receiving",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })
    assert create_resp2.status_code == 200

    create_resp3 = requests.post(url + "projects/create", json={
        "uid": pm_uid,
        "name": "Project Gamma",
        "description": "Gamma does Serving",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })
    assert create_resp3.status_code == 200

    create_json1 = create_resp1.json()
    create_json2 = create_resp2.json()
    create_json3 = create_resp3.json()

    # tm1 is a part of the 2 projects created above
    add_tm_to_project(create_json1, tm1_uid)
    add_tm_to_project(create_json2, tm1_uid)

    proj1 = db.collection("projects").document(str(create_json1))
    proj2 = db.collection("projects").document(str(create_json2))
    proj3 = db.collection("projects").document(str(create_json3))

    pm_name = auth.get_user(pm_uid).display_name

    query = "Project"

    search_resp = requests.get(url + "projects/search", json={
        "uid": tm1_uid,
        "query": query 
    })
    assert search_resp.status_code == 200
    search_json = search_resp.json()

    assert search_json == [
        {
            "description": proj1.get().get("description"),
            "name": proj1.get().get("name"),
            "project_master": pm_name,
            "project_members": proj1.get().get("project_members"),
            "status": proj1.get().get("status"),
            "tasks": []
        },
        {
            "description": proj2.get().get("description"),
            "name": proj2.get().get("name"),
            "project_master": pm_name,
            "project_members": proj2.get().get("project_members"),
            "status": proj2.get().get("status"),
            "tasks": []
        },
        {
            "name": proj3.get().get("name"),
            "project_master": pm_name,
        }
    ]

    reset_projects()

def test_search_return_nothing():

    query = "asdwqdasd"
    search_resp = requests.get(url + "projects/search", json={
        "uid": tm1_uid,
        "query": query 
    })
    assert search_resp.status_code == 200
    search_json = search_resp.json()

    assert search_json == []
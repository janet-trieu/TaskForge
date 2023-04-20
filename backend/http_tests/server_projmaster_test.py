'''
Test file for Flask http testing of project master feature
'''
import pytest
import requests

from src.test_helpers import *
from src.helper import *
from src.profile_page import *
from src.connections import *
from src.projmaster import *

port = 8000
url = f"http://localhost:{port}/"

try:
    pm_uid = create_user_email("projectmaster@gmail.com", "admin123", "Project Master")
    tm0_uid = create_user_email("pmtest.tm0@gmail.com", "taskmaster0", "Task Master0")
    tm1_uid = create_user_email("pmtest.tm1@gmail.com", "taskmaster1", "Task Master1")
    tm2_uid = create_user_email("pmtest.tm2@gmail.com", "taskmaster2", "Task Master2")
    tm3_uid = create_user_email("pmtest.tm3@gmail.com", "taskmaster3", "Task Master3")
except auth.EmailAlreadyExistsError:
    pass
pm_uid = auth.get_user_by_email("projectmaster@gmail.com").uid
tm0_uid = auth.get_user_by_email("pmtest.tm0@gmail.com").uid
tm1_uid = auth.get_user_by_email("pmtest.tm1@gmail.com").uid
tm2_uid = auth.get_user_by_email("pmtest.tm2@gmail.com").uid
tm3_uid = auth.get_user_by_email("pmtest.tm3@gmail.com").uid

############################################################
#                   Test for create_project                #
############################################################

def test_create_project_use_default_vals():
    header = {'Authorization': pm_uid}
    create_resp = requests.post(url + "projects/create", headers=header, json={
        "name": "Project0",
        "description": "Creating Project0 for testing",
        "due_date": None,
        "picture": None
    })

    assert create_resp.status_code == 200

def test_create_project_use_all_vals():
    header = {'Authorization': pm_uid}
    create_resp = requests.post(url + "projects/create", headers=header, json={
        "name": "Project0",
        "description": "Creating Project0 for testing",
        "due_date": "31/12/2023",
        "picture": "test1.jpg"
    })

    assert create_resp.status_code == 200

def test_create_multiple_projects():
    header = {'Authorization': pm_uid}
    create_resp = requests.post(url + "projects/create", headers=header, json={
        "name": "Project0",
        "description": "Creating Project0 for testing",
        "due_date": None,
        "picture": None
    })

    assert create_resp.status_code == 200

    create_resp = requests.post(url + "projects/create", headers=header, json={
        "name": "Project1",
        "description": "Creating Project1 for testing",
        "due_date": "31/12/2023",
        "picture": "test1.jpg"
    })

    assert create_resp.status_code == 200

def test_create_project_TypeError():
    header = {'Authorization': pm_uid}
    create_resp = requests.post(url + "projects/create", headers=header, json={
        "name": -1,
        "description": "Creating Project0 for testing",
        "due_date": None,
        "picture": None
    })

    assert create_resp.status_code == 400

def test_create_project_ValueError():
    header = {'Authorization': pm_uid}
    create_resp = requests.post(url + "projects/create", headers=header, json={
        "name": "Project0",
        "description": "",
        "due_date": None,
        "picture": None
    })

    assert create_resp.status_code == 400

def test_create_project_invalid_uid():
    header = {'Authorization': "invalid"}
    create_resp = requests.post(url + "projects/create", headers=header, json={
        "name": "Project0",
        "description": "Creating Project0 for testing",
        "due_date": None,
        "picture": None
    })

    assert create_resp.status_code == 400

############################################################
#           Test for revive_completed_project              #
############################################################

def test_revive_completed_project():

    pid = create_project(pm_uid, "Project0", "Creating Project0 for testing", None, None)

    proj_ref = db.collection("projects").document(str(pid))

    assert proj_ref.get().get("status") == "Not Started"

    res = update_project(pid, pm_uid, {"status": "Completed"})

    assert res == 0
    assert proj_ref.get().get("status") == "Completed"

    # revive completed project back into "In Progress"
    header = {'Authorization': pm_uid}
    revive_resp = requests.post(url + "projects/revive", headers=header, json={
        "pid": pid,
        "new_status": "In Progress"
    })

    assert revive_resp.status_code == 200
    
    assert proj_ref.get().get("status") == "In Progress"

def test_revive_completed_project_not_proj_master():

    incorrect_uid = tm1_uid

    pid = create_project(pm_uid, "Project 123", "description", None, None)

    proj_ref = db.collection("projects").document(str(pid))

    res = update_project(pid, pm_uid, {"status": "Completed"})

    assert res == 0
    assert proj_ref.get().get("status") == "Completed"

    header = {'Authorization': incorrect_uid}
    revive_resp = requests.post(url + "projects/revive", headers=header, json={
        "pid": pid,
        "new_status": "In Progress"

    })
    assert revive_resp.status_code == 403

    proj_ref = db.collection("projects").document(str(pid))
    assert proj_ref.get().get("status") == "Completed"

def test_revive_non_completed_project():

    pid = create_project(pm_uid, "Project 123", "description", None, None)
    
    proj_ref = db.collection("projects").document(str(pid))

    assert proj_ref.get().get("status") == "Not Started"

    header = {'Authorization': pm_uid}
    revive_resp = requests.post(url + "projects/revive", headers=header, json={
        "pid": pid,
        "new_status": "In Review"

    })

    assert revive_resp.status_code == 400
    assert proj_ref.get().get("status") == "Not Started"

############################################################
#             Test for remove_project_member               #
############################################################

def test_remove_project_member():

    pid = create_project(pm_uid, "Project 123", "description", None, None)

    add_tm_to_project(pid, tm1_uid)
    add_tm_to_project(pid, tm2_uid)
    add_tm_to_project(pid, tm3_uid)

    header = {'Authorization': pm_uid}
    remove_resp = requests.post(url + "projects/remove", headers=header, json={
        "pid": pid,
        "uid_to_be_removed": tm1_uid
    })

    assert remove_resp.status_code == 200

    proj_ref = db.collection("projects").document(str(pid))
    
    assert tm1_uid not in proj_ref.get().get("project_members")

def test_remove_project_member_not_proj_master():

    pid = create_project(pm_uid, "Project 123", "description", None, None)

    add_tm_to_project(pid, tm1_uid)

    header = {'Authorization': tm2_uid}
    remove_resp = requests.post(url + "projects/remove", headers=header, json={
        "pid": pid,
        "uid_to_be_removed": tm1_uid
    })

    assert remove_resp.status_code == 403

    proj_ref = db.collection("projects").document(str(pid))

    assert tm1_uid in proj_ref.get().get("project_members")

def test_remove_project_member_invalid_pid():

    pid = create_project(pm_uid, "Project 123", "description", None, None)

    add_tm_to_project(pid, tm1_uid)
    add_tm_to_project(pid, tm2_uid)
    add_tm_to_project(pid, tm3_uid)

    header = {'Authorization': pm_uid}
    remove_resp = requests.post(url + "projects/remove", headers=header, json={
        "pid": -1,
        "uid_to_be_removed": tm1_uid
    })

    assert remove_resp.status_code == 400

    proj_ref = db.collection("projects").document(str(pid))
    assert tm1_uid in proj_ref.get().get("project_members")

def test_remove_invalid_project_member():

    pid = create_project(pm_uid, "Project 123", "description", None, None)

    header = {'Authorization': pm_uid}
    remove_resp = requests.post(url + "projects/remove", headers=header, json={
        "pid": pid,
        "uid_to_be_removed": tm1_uid
    })

    assert remove_resp.status_code == 400

############################################################
#               Test for invite_to_project                 #
############################################################

def test_invite_to_project():

    tm0_email = auth.get_user(tm0_uid).email
    pid = create_project(pm_uid, "Project 123", "description", None, None)

    nid = notification_connection_request(tm0_email, pm_uid)
    connection_request_respond(tm0_uid, nid, True)

    header = {'Authorization': pm_uid}
    invite_resp = requests.post(url + "projects/invite", headers=header, json={
        "pid": pid,
        "receiver_emails": [tm0_email]
    })

    assert invite_resp.status_code == 200

def test_multiple_invite_to_project():

    tm1_email = auth.get_user(tm1_uid).email
    tm2_email = auth.get_user(tm2_uid).email
    tm3_email = auth.get_user(tm3_uid).email

    pid = create_project(pm_uid, "Project 123", "description", None, None)

    nid1 = notification_connection_request(tm1_email, pm_uid)
    nid2 = notification_connection_request(tm2_email, pm_uid)
    nid3 = notification_connection_request(tm3_email, pm_uid)
    connection_request_respond(tm1_uid, nid1, True)
    connection_request_respond(tm2_uid, nid2, True)
    connection_request_respond(tm3_uid, nid3, True)

    header = {'Authorization': pm_uid}
    invite_resp = requests.post(url + "projects/invite", headers=header, json={
        "pid": pid,
        "receiver_emails": [tm1_email, tm2_email, tm3_email]
    })

    assert invite_resp.status_code == 200

def test_invite_to_invalid_project():
    
    tm1_email = auth.get_user(tm1_uid).email

    pid = create_project(pm_uid, "Project 123", "description", None, None)

    header = {'Authorization': pm_uid}
    invite_resp = requests.post(url + "projects/invite", headers=header, json={
        "pid": -1,
        "receiver_emails": [tm1_email]
    })

    assert invite_resp.status_code == 400

def test_invite_invalid_receiver_uid():

    pid = create_project(pm_uid, "Project 123", "description", None, None)

    header = {'Authorization': pm_uid}
    invite_resp = requests.post(url + "projects/invite", headers=header, json={
        "pid": pid,
        "receiver_emails": ["doesnt.exist@gmail.com"]
    })

    assert invite_resp.status_code == 400

def test_invite_uid_already_in_project():

    tm1_email = auth.get_user(tm1_uid).email

    pid = create_project(pm_uid, "Project 123", "description", None, None)

    add_tm_to_project(pid, tm1_uid)

    proj_ref = db.collection("projects").document(str(pid))

    assert tm1_uid in proj_ref.get().get("project_members")

    header = {'Authorization': pm_uid}
    invite_resp = requests.post(url + "projects/invite", headers=header, json={
        "pid": pid,
        "receiver_emails": [tm1_email]
    })

    assert invite_resp.status_code == 400

############################################################
#                   Test for update_project                #
############################################################

def test_update_project():

    pid = create_project(pm_uid, "Project 123", "description", None, None)

    proj_ref = db.collection("projects").document(str(pid))

    updates = {
        "name": "Project 123",
        "description": "description 123",
        "status": "In Progress",
        "due_date": "31/12/2023",
        "picture": "testing.png"
    }

    header = {'Authorization': pm_uid}
    update_resp = requests.post(url + "projects/update", headers=header, json={
        "pid": pid,
        "updates": updates
    })

    assert update_resp.status_code == 200

    name = proj_ref.get().get("name")
    description = proj_ref.get().get("description")
    status = proj_ref.get().get("status")
    due_date = proj_ref.get().get("due_date")
    picture = proj_ref.get().get("picture")

    assert name == "Project 123"
    assert description == "description 123"
    assert status == "In Progress"
    assert due_date == "31/12/2023"
    assert picture == "testing.png"

def test_update_project_invalid_type():

    pid = create_project(pm_uid, "Project 123", "description", None, None)

    updates = {
        "name": -1,
        "description": -1,
        "status": -1,
        "due_date": -1,
        "picture": -1
    }

    header = {'Authorization': pm_uid}
    update_resp = requests.post(url + "projects/update", headers=header, json={
        "pid": pid,
        "updates": updates
    })

    assert update_resp.status_code == 400

def test_update_project_invalid_value():

    pid = create_project(pm_uid, "Project 123", "description", None, None)

    updates = {
        "name": "A"*2000,
        "description": "A"*2000,
        "status": "bleh",
        "due_date": "202020",
        "picture": "hi"
    }

    header = {'Authorization': pm_uid}
    update_resp = requests.post(url + "projects/update", headers=header, json={
        "pid": pid,
        "updates": updates
    })

    assert update_resp.status_code == 400

def test_update_project_completed():

    pid = create_project(pm_uid, "Project 123", "description", None, None)

    updates = {
        "status": "Completed",
    }

    header = {'Authorization': pm_uid}
    update_resp = requests.post(url + "projects/update", headers=header, json={
        "pid": pid,
        "updates": updates
    })

    assert update_resp.status_code == 200

    # try to update again
    updates = {
        "status": "In Progress",
    }

    update_resp = requests.post(url + "projects/update", headers=header, json={
        "pid": pid,
        "updates": updates
    })

    assert update_resp.status_code == 403

def test_update_project_invalid_pid():

    pid = create_project(pm_uid, "Project 123", "description", None, None)

    updates = {
        "status": "Completed",
    }

    header = {'Authorization': pm_uid}
    update_resp = requests.post(url + "projects/update", headers=header, json={
        "pid": -1,
        "updates": updates
    })

    assert update_resp.status_code == 400

def test_update_project_not_project_master():

    pid = create_project(pm_uid, "Project 123", "description", None, None)

    updates = {
        "status": "Completed",
    }

    header = {'Authorization': tm1_uid}
    update_resp = requests.post(url + "projects/update", headers=header, json={
        "pid": pid,
        "updates": updates
    })

    assert update_resp.status_code == 403

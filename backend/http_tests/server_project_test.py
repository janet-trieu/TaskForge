'''
Test file for Flask http testing of project management feature
'''
import pytest
import requests

from src.test_helpers import *
from src.helper import *
from src.profile_page import *
from src.projects import *
from src.projmaster import *

port = 8000
url = f"http://localhost:{port}/"

try:
    pm_uid = create_user_email("projectmaster@gmail.com", "admin123", "Project Master")
    tm0_uid = create_user_email("projecttest.tm0@gmail.com", "taskmaster0", "Task Master0")
    tm1_uid = create_user_email("projecttest.tm1@gmail.com", "taskmaster1", "Task Master1")
    tm2_uid = create_user_email("projecttest.tm2@gmail.com", "taskmaster2", "Task Master2")
    tm3_uid = create_user_email("projecttest.tm3@gmail.com", "taskmaster3", "Task Master3")
    tm4_uid = create_user_email("projecttest.tm4@gmail.com", "taskmaster4", "Task Master4")
except auth.EmailAlreadyExistsError:
    pass
pm_uid = auth.get_user_by_email("projectmaster@gmail.com").uid
tm0_uid = auth.get_user_by_email("projecttest.tm0@gmail.com").uid
tm1_uid = auth.get_user_by_email("projecttest.tm1@gmail.com").uid
tm2_uid = auth.get_user_by_email("projecttest.tm2@gmail.com").uid
tm3_uid = auth.get_user_by_email("projecttest.tm3@gmail.com").uid
tm4_uid = auth.get_user_by_email("projecttest.tm4@gmail.com").uid

############################################################
#                     Test for view_project                #
############################################################
def test_view_project():

    pid = create_project(pm_uid, "Project 123", "description", None, None)

    # add tm to project
    add_tm_to_project(pid, tm1_uid)

    header = {'Authorization': tm1_uid}
    params = {'pid': pid}
    view_resp = requests.get(url + "projects/view", headers=header, params=params)

    project = get_project(pid)

    assert view_resp.status_code == 200
    view_json = view_resp.json()

    assert view_json == {
        "pid": pid,
        "pm_uid": project["uid"],
        "name": project["name"],
        "description": project["description"],
        "status": project["status"],
        "due_date": project["due_date"],
        "picture": project["picture"],
        "project_members": project["project_members"],
        "project_member_names": [get_display_name(pm_uid), get_display_name(tm1_uid)],
        "epics": extract_epics(pid),
        "tasks": extract_tasks(pid),
        "is_pinned": False
    }

def test_view_project_invalid_pid():

    pid = create_project(pm_uid, "Project 123", "description", None, None)

    header = {'Authorization': tm1_uid}
    params = {'pid': -1}
    view_resp = requests.get(url + "projects/view", headers=header, params=params)

    assert view_resp.status_code == 400

def test_view_project_invalid_uid():

    pid = create_project(pm_uid, "Project 123", "description", None, None)

    header = {'Authorization': "invalid"}
    params = {'pid': pid}
    view_resp = requests.get(url + "projects/view", headers=header, params=params)

    assert view_resp.status_code == 400

def test_view_project_not_in_project():

    pid = create_project(pm_uid, "Project 123", "description", None, None)

    header = {'Authorization': tm1_uid}
    params = {'pid': pid}
    view_resp = requests.get(url + "projects/view", headers=header, params=params)

    assert view_resp.status_code == 403

############################################################
#                   Test for search_project                #
############################################################

def test_search_empty_query():

    pid = create_project(pm_uid, "Project 123", "description", None, None)

    add_tm_to_project(pid, tm0_uid)

    project = get_project(pid)
    project["pinned"] = False

    query = ""
    header = {'Authorization': tm0_uid}
    params = {'query': query}
    search_resp = requests.get(url + "projects/search", headers=header, params=params)

    assert search_resp.status_code == 200
    search_json = search_resp.json()

    assert search_json == [project]

def test_search_project_simple():

    pid = create_project(pm_uid, "Project Alpha", "Alpha does spiking", None, None)

    add_tm_to_project(pid, tm1_uid)

    project = get_project(pid)
    project["pinned"] = False

    query = "Alpha"
    header = {'Authorization': tm1_uid}
    params = {'query': query}
    search_resp = requests.get(url + "projects/search", headers=header, params=params)

    assert search_resp.status_code == 200
    search_json = search_resp.json()

    assert search_json == [project]

def test_search_project_pm_name():

    pid = create_project(pm_uid, "Project Alpha", "Alpha does spiking", None, None)

    add_tm_to_project(pid, tm2_uid)

    project = get_project(pid)
    project["pinned"] = False

    query = "Master"
    header = {'Authorization': tm2_uid}
    params = {'query': query}
    search_resp = requests.get(url + "projects/search", headers=header, params=params)

    assert search_resp.status_code == 200
    search_json = search_resp.json()

    assert search_json == [project]

def test_search_project_verbose():

    reset_projects()

    pid1 = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None)
    pid2 = create_project(pm_uid, "Project Beta", "Beta does Receiving", None, None)
    pid3 = create_project(pm_uid, "Project Gamma", "Gamma does Serving", None, None)

    add_tm_to_project(pid1, tm3_uid)
    add_tm_to_project(pid2, tm3_uid)
    add_tm_to_project(pid3, tm3_uid)

    proj1 = get_project(pid1)
    proj2 = get_project(pid2)
    proj3 = get_project(pid3)
    proj1["pinned"] = False
    proj2["pinned"] = False
    proj3["pinned"] = False

    # tm1 is a part of the 3 projects created above
    query = "Alpha"
    header = {'Authorization': tm3_uid}
    params = {'query': query}
    search_resp = requests.get(url + "projects/search", headers=header, params=params)
    assert search_resp.status_code == 200
    search_json = search_resp.json()

    assert search_json == [proj1]

    query = "Receiving"
    header = {'Authorization': tm3_uid}
    params = {'query': query}
    search_resp = requests.get(url + "projects/search", headers=header, params=params)
    assert search_resp.status_code == 200
    search_json = search_resp.json()

    assert search_json == [proj2]

    query = "Project"
    header = {'Authorization': tm3_uid}
    params = {'query': query}
    search_resp = requests.get(url + "projects/search", headers=header, params=params)
    assert search_resp.status_code == 200
    search_json = search_resp.json()

    assert search_json == [proj1, proj2, proj3]

def test_search_partial_member():

    pid1 = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None)
    pid2 = create_project(pm_uid, "Project Beta", "Beta does Receiving", None, None)
    pid3 = create_project(pm_uid, "Project Gamma", "Gamma does Serving", None, None)

    add_tm_to_project(pid1, tm4_uid)
    add_tm_to_project(pid2, tm4_uid)

    proj1 = get_project(pid1)
    proj2 = get_project(pid2)
    proj1["pinned"] = False
    proj2["pinned"] = False

    query = "Project"
    header = {'Authorization': tm4_uid}
    params = {'query': query}
    search_resp = requests.get(url + "projects/search", headers=header, params=params)
    assert search_resp.status_code == 200
    search_json = search_resp.json()

    # no proj3
    assert search_json == [proj1, proj2]

def test_search_return_nothing():

    pid1 = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None)
    pid2 = create_project(pm_uid, "Project Beta", "Beta does Receiving", None, None)
    pid3 = create_project(pm_uid, "Project Gamma", "Gamma does Serving", None, None)

    query = "asdwqdasd"
    header = {'Authorization': tm1_uid}
    params = {'query': query}
    search_resp = requests.get(url + "projects/search", headers=header, params=params)
    assert search_resp.status_code == 200
    search_json = search_resp.json()

    assert search_json == []

############################################################
#               Test for request_leave_project             #
############################################################
def test_leave_project():

    pid = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None)

    add_tm_to_project(pid, tm1_uid)

    msg = "Hi Project Master, I would like to leave the project Project Alpha due to xyz reasons."

    header = {'Authorization': tm1_uid}
    leave_resp = requests.post(url + "projects/leave", headers=header, json={
        "pid": pid,
        "msg": msg
    })

    assert leave_resp.status_code == 200
    leave_json = leave_resp.json()

    assert leave_json == 0

def test_leave_project_invalid_pid():

    pid = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None)

    add_tm_to_project(pid, tm1_uid)

    msg = "Hi Project Master, I would like to leave the project Project Alpha due to xyz reasons."

    header = {'Authorization': tm1_uid}
    leave_resp = requests.post(url + "projects/leave", headers=header, json={
        "pid": -1,
        "msg": msg
    })

    assert leave_resp.status_code == 400

def test_leave_project_invalid_uid():
    
    pid = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None)

    add_tm_to_project(pid, tm1_uid)

    msg = "Hi Project Master, I would like to leave the project Project Alpha due to xyz reasons."

    header = {'Authorization': "invalid"}
    leave_resp = requests.post(url + "projects/leave", headers=header, json={
        "pid": pid,
        "msg": msg
    })

    assert leave_resp.status_code == 400

def test_leave_project_not_in_project():
    
    pid = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None)

    msg = "Hi Project Master, I would like to leave the project Project Alpha due to xyz reasons."

    header = {'Authorization': tm1_uid}
    leave_resp = requests.post(url + "projects/leave", headers=header, json={
        "pid": pid,
        "msg": msg
    })

    assert leave_resp.status_code == 403

############################################################
#                 Test for respond_invitation              #
############################################################

def test_accept_invitation():

    pid = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None)

    tm1_email = auth.get_user(tm1_uid).email

    nid = notification_connection_request(tm1_email, pm_uid)
    connection_request_respond(tm1_uid, nid, True)

    res = invite_to_project(pid, pm_uid, [tm1_uid])
    assert res == 0

    invite_ref = get_notif_ref_proj_invite(pid, tm1_uid)

    notif_pid = invite_ref.get("pid")
    has_read = invite_ref.get("has_read")
    response = invite_ref.get("response")

    assert has_read == False
    assert response == False
    assert pid == notif_pid

    accept = True

    header = {'Authorization': tm1_uid}
    respond_resp = requests.post(url + "projects/invite/respond", headers=header, json={
        "pid": pid,
        "accept": accept
    })

    assert respond_resp.status_code == 200

    invite_ref = get_notif_ref_proj_invite(pid, tm1_uid)

    has_read = invite_ref.get("has_read")
    response = invite_ref.get("response")

    assert response == True
    assert has_read == True

    proj_ref = db.collection("projects").document(str(pid))
    project_members = proj_ref.get().get("project_members")

    assert tm1_uid in project_members

def test_reject_invitation():
    
    pid = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None)

    tm2_email = auth.get_user(tm2_uid).email

    nid = notification_connection_request(tm2_email, pm_uid)
    connection_request_respond(tm2_uid, nid, True)

    res = invite_to_project(pid, pm_uid, [tm2_uid])
    assert res == 0

    invite_ref = get_notif_ref_proj_invite(pid, tm2_uid)

    notif_pid = invite_ref.get("pid")
    has_read = invite_ref.get("has_read")
    response = invite_ref.get("response")

    assert has_read == False
    assert response == False
    assert pid == notif_pid

    accept = False

    header = {'Authorization': tm2_uid}
    respond_resp = requests.post(url + "projects/invite/respond", headers=header, json={
        "pid": pid,
        "accept": accept
    })

    assert respond_resp.status_code == 200

    invite_ref = get_notif_ref_proj_invite(pid, tm2_uid)

    has_read = invite_ref.get("has_read")
    response = invite_ref.get("response")

    assert response == False
    assert has_read == True

    proj_ref = db.collection("projects").document(str(pid))
    project_members = proj_ref.get().get("project_members")

    assert not tm2_uid in project_members

############################################################
#                     Test for pin_project                 #
############################################################
def test_pin_unpin_project():

    pid = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None)

    user_ref = get_user_ref(pm_uid)
    assert pid not in user_ref.get("pinned_projects")

    # pin project
    header = {'Authorization': pm_uid}
    pin_resp = requests.post(url + "projects/pin", headers=header, json={
        "pid": pid,
        "action": 0
    })
    assert pin_resp.status_code == 200

    user_ref = get_user_ref(pm_uid)
    assert pid in user_ref.get("pinned_projects")

    # unpin project
    unpin_resp = requests.post(url + "projects/pin", headers=header, json={
        "pid": pid,
        "action": 1
    })
    assert unpin_resp.status_code == 200

    user_ref = get_user_ref(pm_uid)
    assert pid not in user_ref.get("pinned_projects")

    # unpin project again
    unpin_resp = requests.post(url + "projects/pin", headers=header, json={
        "pid": pid,
        "action": 1
    })
    assert unpin_resp.status_code == 400

def test_pin_invalid_project():
    pid = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None)

    # pin project
    header = {'Authorization': pm_uid}
    pin_resp = requests.post(url + "projects/pin", headers=header, json={
        "pid": -1,
        "action": 0
    })
    assert pin_resp.status_code == 400

def test_pin_not_in_project():

    pid = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None)

    # pin project
    header = {'Authorization': tm3_uid}
    pin_resp = requests.post(url + "projects/pin", headers=header, json={
        "pid": pid,
        "action": 0
    })
    assert pin_resp.status_code == 403

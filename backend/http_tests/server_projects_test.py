'''
Test file for Flask http testing of project management feature
'''
import pytest
import requests
from src.test_helpers import *
from src.helper import *
from src.profile_page import *
<<<<<<< HEAD
from src.projects import *
from src.proj_master import *
=======

>>>>>>> 790334a5f339802e80f9f93f1593d35e14f3dc0a

port = 5000
url = f"http://localhost:{port}/"

try:
    pm_uid = create_user_email("projectmaster@gmail.com", "admin123", "Project Master")
    tm1_uid = create_user_email("projecttest.tm1@gmail.com", "taskmaster1", "Task Master1")
    tm2_uid = create_user_email("projecttest.tm2@gmail.com", "taskmaster1", "Task Master2")
    tm3_uid = create_user_email("projecttest.tm3@gmail.com", "taskmaster1", "Task Master3")
except auth.EmailAlreadyExistsError:
    pass
pm_uid = auth.get_user_by_email("projectmaster@gmail.com").uid
tm1_uid = auth.get_user_by_email("projecttest.tm1@gmail.com").uid
tm2_uid = auth.get_user_by_email("projecttest.tm2@gmail.com").uid
tm3_uid = auth.get_user_by_email("projecttest.tm3@gmail.com").uid
'''
############################################################
#                     Test for view_project                #
############################################################
def test_view_project():

    header = {'Authorization': pm_uid}
    create_resp = requests.post(url + "projects/create", headers=header, json={
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

    header = {'Authorization': tm1_uid}
    params = {'pid': create_json}
    view_resp = requests.get(url + "projects/view", headers=header, params=params)

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

    header = {'Authorization': pm_uid}
    create_resp = requests.post(url + "projects/create", headers=header, json={
        "name": "Project0",
        "description": "Creating Project0 for testing",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 200
    create_json = create_resp.json()

    header = {'Authorization': tm1_uid}
    params = {'pid': -1}
    view_resp = requests.get(url + "projects/view", headers=header, params=params)

    assert view_resp.status_code == 400
        
    reset_projects()

def test_view_project_invalid_uid():

    header = {'Authorization': pm_uid}
    create_resp = requests.post(url + "projects/create", headers=header, json={
        "name": "Project0",
        "description": "Creating Project0 for testing",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 200
    create_json = create_resp.json()

    header = {'Authorization': "invalid"}
    params = {'pid': create_json}
    view_resp = requests.get(url + "projects/view", headers=header, params=params)

    assert view_resp.status_code == 400

    reset_projects()

def test_view_project_not_in_project():

    header = {'Authorization': pm_uid}
    create_resp = requests.post(url + "projects/create", headers=header, json={
        "name": "Project0",
        "description": "Creating Project0 for testing",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 200
    create_json = create_resp.json()
    proj_ref = db.collection("projects").document(str(create_json))

    header = {'Authorization': tm1_uid}
    params = {'pid': create_json}
    view_resp = requests.get(url + "projects/view", headers=header, params=params)

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

def test_search_empty_query():
    header = {'Authorization': pm_uid}
    create_resp = requests.post(url + "projects/create", headers=header, json={
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

    query = ""
    header = {'Authorization': tm1_uid}
    params = {'query': query}
    search_resp = requests.get(url + "projects/search", headers=header, params=params)

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

def test_search_project_simple():

    header = {'Authorization': pm_uid}
    create_resp = requests.post(url + "projects/create", headers=header, json={
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
    header = {'Authorization': tm1_uid}
    params = {'query': query}
    search_resp = requests.get(url + "projects/search", headers=header, params=params)

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

    header = {'Authorization': pm_uid}
    create_resp = requests.post(url + "projects/create", headers=header, json={
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
    header = {'Authorization': tm1_uid}
    params = {'query': query}
    search_resp = requests.get(url + "projects/search", headers=header, params=params)

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

    header = {'Authorization': pm_uid}
    create_resp1 = requests.post(url + "projects/create", headers=header, json={
        "name": "Project Alpha",
        "description": "Alpha does Spiking",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })
    assert create_resp1.status_code == 200

    create_resp2 = requests.post(url + "projects/create", headers=header, json={
        "name": "Project Beta",
        "description": "Beta does Receiving",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })
    assert create_resp2.status_code == 200

    create_resp3 = requests.post(url + "projects/create", headers=header, json={
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
    header = {'Authorization': tm1_uid}
    params = {'query': query}
    search_resp = requests.get(url + "projects/search", headers=header, params=params)
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
    header = {'Authorization': tm1_uid}
    params = {'query': query}
    search_resp = requests.get(url + "projects/search", headers=header, params=params)
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
    header = {'Authorization': tm1_uid}
    params = {'query': query}
    search_resp = requests.get(url + "projects/search", headers=header, params=params)
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

    header = {'Authorization': pm_uid}
    create_resp1 = requests.post(url + "projects/create", headers=header, json={
        "name": "Project Alpha",
        "description": "Alpha does Spiking",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })
    assert create_resp1.status_code == 200

    create_resp2 = requests.post(url + "projects/create", headers=header, json={
        "uid": pm_uid,
        "name": "Project Beta",
        "description": "Beta does Receiving",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })
    assert create_resp2.status_code == 200

    create_resp3 = requests.post(url + "projects/create", headers=header, json={
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
    header = {'Authorization': tm1_uid}
    params = {'query': query}
    search_resp = requests.get(url + "projects/search", headers=header, params=params)
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
        }
    ]

    reset_projects()

def test_search_return_nothing():

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

    header = {'Authorization': pm_uid}
    create_resp = requests.post(url + "projects/create", headers=header, json={
        "name": "Project Alpha",
        "description": "Alpha does Spiking",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 200
    create_json = create_resp.json()

    add_tm_to_project(create_json, tm1_uid)

    msg = "Hi Project Master, I would like to leave the project Project Alpha due to xyz reasons."

    header = {'Authorization': tm1_uid}
    leave_resp = requests.post(url + "projects/leave", headers=header, json={
        "pid": create_json,
        "msg": msg
    })

    assert leave_resp.status_code == 200
    leave_json = leave_resp.json()

    assert leave_json == {
        "receipient_email": "projectmaster@gmail.com",
        "sender_email": "projecttest.tm1@gmail.com",
        "msg_title": "Request to leave Project Alpha",
        "msg_body": msg
    }

    reset_projects()

def test_leave_project_invalid_pid():

    header = {'Authorization': pm_uid}
    create_resp = requests.post(url + "projects/create", headers=header, json={
        "name": "Project Alpha",
        "description": "Alpha does Spiking",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 200
    create_json = create_resp.json()

    add_tm_to_project(create_json, tm1_uid)

    msg = "Hi Project Master, I would like to leave the project Project Alpha due to xyz reasons."

    header = {'Authorization': tm1_uid}
    leave_resp = requests.post(url + "projects/leave", headers=header, json={
        "pid": -1,
        "msg": msg
    })

    assert leave_resp.status_code == 400

    reset_projects()

def test_leave_project_invalid_uid():
    
    header = {'Authorization': pm_uid}
    create_resp = requests.post(url + "projects/create", headers=header, json={
        "name": "Project Alpha",
        "description": "Alpha does Spiking",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 200
    create_json = create_resp.json()

    add_tm_to_project(create_json, tm1_uid)

    msg = "Hi Project Master, I would like to leave the project Project Alpha due to xyz reasons."

    header = {'Authorization': "invalid"}
    leave_resp = requests.post(url + "projects/leave", headers=header, json={
        "pid": create_json,
        "msg": msg
    })

    assert leave_resp.status_code == 400

    reset_projects()

def test_leave_project_not_in_project():
    
    header = {'Authorization': pm_uid}
    create_resp = requests.post(url + "projects/create", headers=header, json={
        "name": "Project Alpha",
        "description": "Alpha does Spiking",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 200
    create_json = create_resp.json()

    msg = "Hi Project Master, I would like to leave the project Project Alpha due to xyz reasons."

    header = {'Authorization': tm1_uid}
    leave_resp = requests.post(url + "projects/leave", headers=header, json={
        "pid": create_json,
        "msg": msg
    })

    assert leave_resp.status_code == 403

    reset_projects()
'''
############################################################
#                 Test for respond_invitation              #
############################################################

def test_accept_invitation():

    tm1_email = auth.get_user(tm1_uid).email
    header = {'Authorization': pm_uid}
    create_resp = requests.post(url + "projects/create", headers=header, json={
        "name": "Project A",
        "description": "Creating Project A for testing",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 200
    create_json = create_resp.json()

    invite_resp = requests.post(url + "projects/invite", headers=header, json={
        "pid": create_json,
        "receiver_uids": [tm1_email]
    })

    assert invite_resp.status_code == 200

    invite_ref = get_notif_ref_proj_invite(create_json, tm1_uid)

    notif_pid = invite_ref.get("pid")
    has_read = invite_ref.get("has_read")
    response = invite_ref.get("response")

    assert has_read == False
    assert response == False
    assert create_json == notif_pid

    accept = True
    msg = "Hi Project Master, I will gladly join Project A!"

    header = {'Authorization': tm1_uid}
    respond_resp = requests.post(url + "projects/invite/respond", headers=header, json={
        "pid": create_json,
        "accept": accept,
        "msg": msg
    })

    assert respond_resp.status_code == 200

    invite_ref = get_notif_ref_proj_invite(create_json, tm1_uid)

    has_read = invite_ref.get("has_read")
    response = invite_ref.get("response")

    assert response == True
    assert has_read == True

    proj_ref = db.collection("projects").document(str(create_json))
    project_members = proj_ref.get().get("project_members")

    assert tm1_uid in project_members

    reset_projects()

def test_reject_invitation():
    
    tm1_email = auth.get_user(tm1_uid).email
    header = {'Authorization': pm_uid}
    create_resp = requests.post(url + "projects/create", headers=header, json={
        "name": "Project A",
        "description": "Creating Project A for testing",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 200
    create_json = create_resp.json()

    invite_resp = requests.post(url + "projects/invite", headers=header, json={
        "pid": create_json,
        "receiver_uids": [tm1_email]
    })

    assert invite_resp.status_code == 200

    invite_ref = get_notif_ref_proj_invite(create_json, tm1_uid)

    notif_pid = invite_ref.get("pid")
    has_read = invite_ref.get("has_read")
    response = invite_ref.get("response")

    assert has_read == False
    assert response == False
    assert create_json == notif_pid

    accept = True
    msg = "Hi Project Master, I cannot join"

    header = {'Authorization': tm1_uid}
    respond_resp = requests.post(url + "projects/invite/respond", headers=header, json={
        "pid": create_json,
        "accept": accept,
        "msg": msg
    })

    assert respond_resp.status_code == 200

    invite_ref = get_notif_ref_proj_invite(create_json, tm1_uid)

    has_read = invite_ref.get("has_read")
    response = invite_ref.get("response")

    assert response == False
    assert has_read == True

    proj_ref = db.collection("projects").document(str(create_json))
    project_members = proj_ref.get().get("project_members")

    assert not tm1_uid in project_members

    reset_projects()

def test_reject_invitation_no_msg():
    
    tm1_email = auth.get_user(tm1_uid).email
    header = {'Authorization': pm_uid}
    create_resp = requests.post(url + "projects/create", headers=header, json={
        "name": "Project A",
        "description": "Creating Project A for testing",
        "due_date": None,
        "team_strength": None,
        "picture": None
    })

    assert create_resp.status_code == 200
    create_json = create_resp.json()

    invite_resp = requests.post(url + "projects/invite", headers=header, json={
        "pid": create_json,
        "receiver_uids": [tm1_email]
    })

    assert invite_resp.status_code == 200

    invite_ref = get_notif_ref_proj_invite(create_json, tm1_uid)

    notif_pid = invite_ref.get("pid")
    has_read = invite_ref.get("has_read")
    response = invite_ref.get("response")

    assert has_read == False
    assert response == False
    assert create_json == notif_pid

    accept = True
    msg = ""

    header = {'Authorization': tm1_uid}
    respond_resp = requests.post(url + "projects/invite/respond", headers=header, json={
        "pid": create_json,
        "accept": accept,
        "msg": msg
    })

    assert respond_resp.status_code == 400

    proj_ref = db.collection("projects").document(str(create_json))
    project_members = proj_ref.get().get("project_members")

    assert not tm1_uid in project_members

    reset_projects()
'''
Unit test file for Project Management feature
'''
import pytest
from src.projects import *
from src.proj_master import *
from src.test_helpers import *
from src.helper import *
from src.projects import *
from src.profile_page import *

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

############################################################
#                    Test for view_project                 #
############################################################

def test_view_project():
    
    pid = create_project(pm_uid, "Project0", "Creating Project0 for testing", None, None, None)

    # add tm to project
    add_tm_to_project(pid, tm1_uid)

    res = view_project(pid, tm1_uid)

    pm_name = auth.get_user(pm_uid).display_name
    proj_ref = db.collection("projects").document(str(pid))
    proj_members = proj_ref.get().get("project_members")

    assert res == {
        "project_master": pm_name,
        "name": "Project0",
        "description": "Creating Project0 for testing",
        "project_members": proj_members,
        "tasks": []
    }

    reset_projects()

def test_view_project_invalid_pid():

    pid = create_project(pm_uid, "Project0", "Creating Project0 for testing", None, None, None)

    # add tm to project
    add_tm_to_project(pid, tm1_uid)

    with pytest.raises(InputError):
        view_project(-1, tm1_uid)
        
    reset_projects()

def test_view_project_invalid_uid():

    pid = create_project(pm_uid, "Project0", "Creating Project0 for testing", None, None, None)

    with pytest.raises(InputError):
        view_project(pid, "invalid")

    reset_projects()

def test_view_project_not_in_project():

    pid = create_project(pm_uid, "Project0", "Creating Project0 for testing", None, None, None)

    res = view_project(pid, tm1_uid)

    pm_name = auth.get_user(pm_uid).display_name

    assert res == {
        "project_master": pm_name,
        "name": "Project0"
    }
        
    reset_projects()

############################################################
#                   Test for search_project                #
############################################################

def test_search_empty_query():

    pid1 = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None, None)

    add_tm_to_project(pid1, tm1_uid)
    proj1 = db.collection("projects").document(str(pid1))

    query = ""
    res = search_project(tm1_uid, query)

    pm_name = auth.get_user(pm_uid).display_name

    assert res == [
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

    pid1 = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None, None)
    add_tm_to_project(pid1, tm1_uid)
    proj1 = db.collection("projects").document(str(pid1))

    query = "Alpha"
    res = search_project(tm1_uid, query)

    pm_name = auth.get_user(pm_uid).display_name

    assert res == [
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

def test_search_project_upper_lower():

    pid1 = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None, None)
    add_tm_to_project(pid1, tm1_uid)
    proj1 = db.collection("projects").document(str(pid1))

    query = "alpha"
    res = search_project(tm1_uid, query)

    pm_name = auth.get_user(pm_uid).display_name

    assert res == [
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

    pid1 = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None, None)

    add_tm_to_project(pid1, tm1_uid)
    proj1 = db.collection("projects").document(str(pid1))

    query = "Master"
    res = search_project(tm1_uid, query)

    pm_name = auth.get_user(pm_uid).display_name

    assert res == [
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

    pid1 = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None, None)
    pid2 = create_project(pm_uid, "Project Beta", "Beta does Receiving", None, None, None)
    pid3 = create_project(pm_uid, "Project Gamma", "Gamma does Serving", None, None, None)

    add_tm_to_project(pid1, tm1_uid)
    add_tm_to_project(pid2, tm1_uid)
    add_tm_to_project(pid3, tm1_uid)

    proj1 = db.collection("projects").document(str(pid1))
    proj2 = db.collection("projects").document(str(pid2))
    proj3 = db.collection("projects").document(str(pid3))

    # tm1 is a part of the 3 projects created above
    query = "Alpha"
    res = search_project(tm1_uid, query)

    pm_name = auth.get_user(pm_uid).display_name

    assert res == [
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
    res = search_project(tm1_uid, query)
    print(res)

    assert res == [
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
    res = search_project(tm1_uid, query)

    assert res == [
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
    pid1 = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None, None)
    pid2 = create_project(pm_uid, "Project Beta", "Beta does Receiving", None, None, None)
    pid3 = create_project(pm_uid, "Project Gamma", "Gamma does Serving", None, None, None)

    add_tm_to_project(pid1, tm1_uid)
    add_tm_to_project(pid2, tm1_uid)

    proj1 = db.collection("projects").document(str(pid1))
    proj2 = db.collection("projects").document(str(pid2))
    proj3 = db.collection("projects").document(str(pid3))

    # tm1 is a part of the 2 projects created above
    query = "Project"
    res = search_project(tm1_uid, query)

    pm_name = auth.get_user(pm_uid).display_name

    assert res == [
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
    res = search_project(tm1_uid, query)

    assert res == []

############################################################
#                    Test for leave_project                #
############################################################

def test_leave_project():

    pid = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None, None)

    # add tm1 into project
    add_tm_to_project(pid, tm1_uid)

    msg = "Hi Project Master, I would like to leave the project Project Alpha due to xyz reasons."
    res = request_leave_project(pid, tm1_uid, msg)

    pm_name = auth.get_user(pm_uid).display_name
    proj_ref = db.collection("projects").document(str(pid))
    proj_name = proj_ref.get().get("name")

    assert res == {
        "receipient_email": "projectmaster@gmail.com",
        "sender_email": "projecttest.tm1@gmail.com",
        "msg_title": "Request to leave Project Alpha",
        "msg_body": msg
    }

    reset_projects()

def test_leave_project_invalid_pid():

    pid = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None, None)

    # add tm1 into project
    add_tm_to_project(pid, tm1_uid)

    msg = "Hi Project Master, I would like to leave the project Project Alpha due to xyz reasons."

    with pytest.raises(InputError):
        request_leave_project(-1, tm1_uid, msg)

    reset_projects()

def test_leave_project_invalid_uid():
    
    pid = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None, None)

    # add tm1 into project
    add_tm_to_project(pid, tm1_uid)

    msg = "Hi Project Master, I would like to leave the project Project Alpha due to xyz reasons."

    with pytest.raises(InputError):
        request_leave_project(pid, "invalid", msg)

    reset_projects()

def test_leave_project_not_in_project():
    
    pid = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None, None)

    # add tm1 is not a part of project 

    msg = "Hi Project Master, I would like to leave the project Project Alpha due to xyz reasons."

    with pytest.raises(AccessError):
        request_leave_project(pid, tm1_uid, msg)

    reset_projects()

############################################################
#                 Test for respond_invitation              #
############################################################

def test_accept_invitation():
    
    pid = create_project(pm_uid, "Project A", "Projec A xyz", None, None, None)

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
    msg = "Hi Project Master, I will gladly join Project A!"

    res = respond_project_invitation(notif_pid, tm1_uid, accept, msg)
    assert res == 0

    invite_ref = get_notif_ref_proj_invite(pid, tm1_uid)

    has_read = invite_ref.get("has_read")
    response = invite_ref.get("response")

    assert response == True
    assert has_read == True
    proj_ref = db.collection("projects").document(str(pid))
    project_members = proj_ref.get().get("project_members")

    assert tm1_uid in project_members

def test_reject_invitation():
    
    pid = create_project(pm_uid, "Project B", "Projec B xyz", None, None, None)

    res = invite_to_project(pid, pm_uid, [tm1_uid])
    assert res == 0

    invite_ref = get_notif_ref_proj_invite(pid, tm1_uid)

    notif_pid = invite_ref.get("pid")
    has_read = invite_ref.get("has_read")
    response = invite_ref.get("response")

    assert has_read == False
    assert response == False
    assert pid == notif_pid

    accept = False
    msg = "Hi Project Master, sorry, but I cannot join Project A"

    res = respond_project_invitation(notif_pid, tm1_uid, accept, msg)
    assert res == 0

    invite_ref = get_notif_ref_proj_invite(pid, tm1_uid)

    has_read = invite_ref.get("has_read")
    response = invite_ref.get("response")

    assert has_read == True
    assert response == False

    proj_ref = db.collection("projects").document(str(pid))
    project_members = proj_ref.get().get("project_members")

    assert not tm1_uid in project_members

def test_reject_invitation_no_msg():
    
    pid = create_project(pm_uid, "Project A", "Projec A xyz", None, None, None)

    res = invite_to_project(pid, pm_uid, [tm1_uid])
    assert res == 0

    invite_ref = get_notif_ref_proj_invite(pid, tm1_uid)

    notif_pid = invite_ref.get("pid")
    has_read = invite_ref.get("has_read")
    response = invite_ref.get("response")

    assert has_read == False
    assert response == False
    assert pid == notif_pid

    accept = False
    msg = ""

    with pytest.raises(InputError):
        respond_project_invitation(notif_pid, tm1_uid, accept, msg)

    reset_projects()

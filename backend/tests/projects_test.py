'''
Unit test file for Project Management feature
'''
import pytest

from src.projects import *
from src.projmaster import *
from src.test_helpers import *
from src.helper import *
from src.projects import *
from src.profile_page import *

try:
    pm_uid = create_user_email("projtest.pm@gmail.com", "admin123", "Project Master")
except auth.EmailAlreadyExistsError:
    pass
pm_uid = auth.get_user_by_email("projtest.pm@gmail.com").uid

############################################################
#                    Test for view_project                 #
############################################################

def test_view_project():

    tm_uid = create_test_user("project", 0)
    
    pid = create_project(pm_uid, "Project0", "Creating Project0 for testing", None, None)

    # add tm to project
    add_tm_to_project(pid, tm_uid)

    project = get_project(pid)

    res = view_project(pid, tm_uid)

    assert res == {
        "pid": pid,
        "pm_uid": project["uid"],
        "name": project["name"],
        "description": project["description"],
        "status": project["status"],
        "due_date": project["due_date"],
        "picture": project["picture"],
        "project_members": project["project_members"],
        "project_member_names": [get_display_name(pm_uid), get_display_name(tm_uid)],
        "epics": extract_epics(pid),
        "tasks": extract_tasks(pid),
        "is_pinned": False
    }

def test_view_project_invalid_pid():

    pid = create_project(pm_uid, "Project0", "Creating Project0 for testing", None, None)

    with pytest.raises(InputError):
        view_project(-1, pm_uid)

def test_view_project_invalid_uid():

    pid = create_project(pm_uid, "Project0", "Creating Project0 for testing", None, None)

    with pytest.raises(InputError):
        view_project(pid, "invalid")

def test_view_project_not_in_project():

    tm_uid = create_test_user("project", 0)

    pid = create_project(pm_uid, "Project1231231", "Creating Project0 for testing", None, None)

    with pytest.raises(AccessError):
        view_project(pid, tm_uid)

############################################################
#                   Test for search_project                #
############################################################

def test_search_empty_query():

    tm_uid = create_test_user("project", 1)

    pid = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None)

    add_tm_to_project(pid, tm_uid)

    query = ""
    res = search_project(tm_uid, query)

    project = get_project(pid)
    project["pinned"] = False

    assert res == [project]

def test_search_project_simple():

    tm_uid = create_test_user("project", 2)

    pid = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None)
    add_tm_to_project(pid, tm_uid)

    query = "Alpha"
    res = search_project(tm_uid, query)

    project = get_project(pid)
    project["pinned"] = False

    assert res == [project]
    
def test_search_project_upper_lower():

    tm_uid = create_test_user("project", 3)

    pid = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None)
    add_tm_to_project(pid, tm_uid)

    query = "alpha"
    res = search_project(tm_uid, query)

    project = get_project(pid)
    project["pinned"] = False

    assert res == [project]

def test_search_project_pm_name():

    tm_uid = create_test_user("project", 4)

    pid = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None)

    add_tm_to_project(pid, tm_uid)

    query = "Project Master"
    res = search_project(tm_uid, query)

    project = get_project(pid)
    project["pinned"] = False

    assert res == [project]

def test_search_project_verbose():

    tm_uid = create_test_user("project", 5)

    pid1 = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None)
    pid2 = create_project(pm_uid, "Project Beta", "Beta does Receiving", None, None)
    pid3 = create_project(pm_uid, "Project Gamma", "Gamma does Serving", None, None)

    add_tm_to_project(pid1, tm_uid)
    add_tm_to_project(pid2, tm_uid)
    add_tm_to_project(pid3, tm_uid)

    proj1 = get_project(pid1)
    proj2 = get_project(pid2)
    proj3 = get_project(pid3)
    proj1["pinned"] = False
    proj2["pinned"] = False
    proj3["pinned"] = False

    query = "Project"
    res = search_project(tm_uid, query)

    assert res == [proj1, proj2, proj3]

def test_search_partial_member():

    tm_uid = create_test_user("project", 6)

    pid1 = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None)
    pid2 = create_project(pm_uid, "Project Beta", "Beta does Receiving", None, None)
    pid3 = create_project(pm_uid, "Project Gamma", "Gamma does Serving", None, None)

    add_tm_to_project(pid1, tm_uid)
    add_tm_to_project(pid2, tm_uid)

    proj1 = get_project(pid1)
    proj2 = get_project(pid2)
    proj1["pinned"] = False
    proj2["pinned"] = False

    # tm1 is a part of the 2 projects created above
    query = "Project"
    res = search_project(tm_uid, query)

    assert res == [proj1, proj2]

def test_search_return_nothing():

    tm_uid = create_test_user("project", 7)

    query = "asdwqdasd"
    res = search_project(tm_uid, query)

    assert res == []

############################################################
#                    Test for leave_project                #
############################################################

def test_leave_project():

    tm_uid = create_test_user("project", 0)

    pid = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None)

    # add tm1 into project
    add_tm_to_project(pid, tm_uid)

    msg = "Hi Project Master, I would like to leave the project Project Alpha due to xyz reasons."
    res = request_leave_project(pid, tm_uid, msg)

    assert res == 0

def test_leave_project_invalid_pid():

    tm_uid = create_test_user("project", 0)

    pid = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None)

    # add tm1 into project
    add_tm_to_project(pid, tm_uid)

    msg = "Hi Project Master, I would like to leave the project Project Alpha due to xyz reasons."

    with pytest.raises(InputError):
        request_leave_project(-1, tm_uid, msg)

def test_leave_project_invalid_uid():

    tm_uid = create_test_user("project", 0)
    
    pid = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None)

    # add tm1 into project
    add_tm_to_project(pid, tm_uid)

    msg = "Hi Project Master, I would like to leave the project Project Alpha due to xyz reasons."

    with pytest.raises(InputError):
        request_leave_project(pid, "invalid", msg)

def test_leave_project_not_in_project():

    tm_uid = create_test_user("project", 0)
    
    pid = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None)

    # tm is not a part of the project 

    msg = "Hi Project Master, I would like to leave the project Project Alpha due to xyz reasons."

    with pytest.raises(AccessError):
        request_leave_project(pid, tm_uid, msg)

############################################################
#                 Test for respond_invitation              #
############################################################

def test_accept_invitation():

    pm_email = auth.get_user(pm_uid).email

    tm_uid = create_test_user("project", 0)
    
    pid = create_project(pm_uid, "Project A", "Projec A xyz", None, None)

    nid = notification_connection_request(pm_email, tm_uid)
    connection_request_respond(pm_uid, nid, True)

    res = invite_to_project(pid, pm_uid, [tm_uid])
    assert res == 0

    invite_ref = get_notif_ref_proj_invite(pid, tm_uid)

    notif_pid = invite_ref.get("pid")
    has_read = invite_ref.get("has_read")
    response = invite_ref.get("response")

    assert has_read == False
    assert response == False
    assert pid == notif_pid

    accept = True

    res = respond_project_invitation(notif_pid, tm_uid, accept)
    assert res == 0

    invite_ref = get_notif_ref_proj_invite(pid, tm_uid)

    has_read = invite_ref.get("has_read")
    response = invite_ref.get("response")

    assert response == True
    assert has_read == True
    proj_ref = db.collection("projects").document(str(pid))
    project_members = proj_ref.get().get("project_members")

    assert tm_uid in project_members

def test_reject_invitation():

    pm_email = auth.get_user(pm_uid).email

    tm_uid = create_test_user("project", 1)
    
    pid = create_project(pm_uid, "Project B", "Projec B xyz", None, None)

    nid = notification_connection_request(pm_email, tm_uid)
    connection_request_respond(pm_uid, nid, True)

    res = invite_to_project(pid, pm_uid, [tm_uid])
    assert res == 0

    invite_ref = get_notif_ref_proj_invite(pid, tm_uid)

    notif_pid = invite_ref.get("pid")
    has_read = invite_ref.get("has_read")
    response = invite_ref.get("response")

    assert has_read == False
    assert response == False
    assert pid == notif_pid

    accept = False

    res = respond_project_invitation(notif_pid, tm_uid, accept)
    assert res == 0

    invite_ref = get_notif_ref_proj_invite(pid, tm_uid)

    has_read = invite_ref.get("has_read")
    response = invite_ref.get("response")

    assert has_read == True
    assert response == False

    proj_ref = db.collection("projects").document(str(pid))
    project_members = proj_ref.get().get("project_members")

    assert not tm_uid in project_members

############################################################
#                    Test for pin_project                  #
############################################################
def test_pin_unpin_project():

    pid = create_project(pm_uid, "Project A", "Projec A xyz", None, None)

    res = pin_project(pid, pm_uid, 0)
    assert res == 0
    
    user_ref = get_user_ref(pm_uid)
    assert pid in user_ref.get("pinned_projects")

    # now unpin
    res = pin_project(pid, pm_uid, 1)
    assert res == 0

    user_ref = get_user_ref(pm_uid)
    assert pid not in user_ref.get("pinned_projects")

def test_pin_invalid_project():

    pid = create_project(pm_uid, "Project A", "Projec A xyz", None, None)

    with pytest.raises(InputError):
        pin_project(-1, pm_uid, 0)

def test_pin_not_in_project():
    tm_uid = create_test_user("project", 0)
    pid = create_project(pm_uid, "Project 123123123", "Projec A xyz", None, None)

    with pytest.raises(AccessError):
        pin_project(pid, tm_uid, 0)

def test_pin_pinned_project():

    pid = create_project(pm_uid, "Project A", "Projec A xyz", None, None)

    pin_project(pid, pm_uid, 0)

    with pytest.raises(InputError):
        pin_project(pid, pm_uid, 0)

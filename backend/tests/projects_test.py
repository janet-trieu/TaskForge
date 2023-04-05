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

    reset_projects()
    
    pid = create_project(pm_uid, "Project0", "Creating Project0 for testing", None, None, None)

    # add tm to project
    add_tm_to_project(pid, tm1_uid)

    project = get_project(pid)

    res = view_project(pid, tm1_uid)

    assert res == {
        "pid": pid,
        "name": project["name"],
        "description": project["description"],
        "status": project["status"],
        "due_date": project["due_date"],
        "team_strength": project["team_strength"],
        "picture": project["picture"],
        "project_members": project["project_members"],
        "epics": extract_epics(pid),
        "tasks": extract_tasks(pid),
        "is_pinned": project["is_pinned"]
    }

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

    with pytest.raises(AccessError):
        view_project(pid, tm1_uid)

############################################################
#                   Test for search_project                #
############################################################

def test_search_empty_query():

    reset_projects()

    pid = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None, None)

    add_tm_to_project(pid, tm1_uid)

    query = ""
    res = search_project(tm1_uid, query)

    project = get_project(pid)

    assert res == [project]

def test_search_project_simple():

    reset_projects()

    pid1 = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None, None)
    add_tm_to_project(pid1, tm1_uid)

    query = "Alpha"
    res = search_project(tm1_uid, query)

    assert res == [get_project(pid1)]
    
def test_search_project_upper_lower():
    reset_projects()

    pid1 = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None, None)
    add_tm_to_project(pid1, tm1_uid)

    query = "alpha"
    res = search_project(tm1_uid, query)

    assert res == [get_project(pid1)]

def test_search_project_pm_name():
    reset_projects()

    pid1 = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None, None)

    add_tm_to_project(pid1, tm1_uid)

    query = "Master"
    res = search_project(tm1_uid, query)

    assert res == [get_project(pid1)]

def test_search_project_verbose():
    reset_projects()

    pid1 = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None, None)
    pid2 = create_project(pm_uid, "Project Beta", "Beta does Receiving", None, None, None)
    pid3 = create_project(pm_uid, "Project Gamma", "Gamma does Serving", None, None, None)

    add_tm_to_project(pid1, tm1_uid)
    add_tm_to_project(pid2, tm1_uid)
    add_tm_to_project(pid3, tm1_uid)

    proj1 = get_project(pid1)
    proj2 = get_project(pid2)
    proj3 = get_project(pid3)

    # tm1 is a part of the 3 projects created above
    query = "Alpha"
    res = search_project(tm1_uid, query)

    assert res == [proj1]

    query = "Receiving"
    res = search_project(tm1_uid, query)

    assert res == [proj2]

    query = "Project"
    res = search_project(tm1_uid, query)

    assert res == [proj1, proj2, proj3]

    reset_projects()

def test_search_partial_member():
    reset_projects()

    pid1 = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None, None)
    pid2 = create_project(pm_uid, "Project Beta", "Beta does Receiving", None, None, None)
    pid3 = create_project(pm_uid, "Project Gamma", "Gamma does Serving", None, None, None)

    add_tm_to_project(pid1, tm1_uid)
    add_tm_to_project(pid2, tm1_uid)

    proj1 = get_project(pid1)
    proj2 = get_project(pid2)

    # tm1 is a part of the 2 projects created above
    query = "Project"
    res = search_project(tm1_uid, query)

    assert res == [proj1, proj2]

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

    assert res == 0

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

    nid = notification_connection_request(tm1_uid, pm_uid)
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

    nid = notification_connection_request(tm2_uid, pm_uid)
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
    msg = "Hi Project Master, sorry, but I cannot join Project A"

    res = respond_project_invitation(notif_pid, tm2_uid, accept, msg)
    assert res == 0

    invite_ref = get_notif_ref_proj_invite(pid, tm2_uid)

    has_read = invite_ref.get("has_read")
    response = invite_ref.get("response")

    assert has_read == True
    assert response == False

    proj_ref = db.collection("projects").document(str(pid))
    project_members = proj_ref.get().get("project_members")

    assert not tm2_uid in project_members

def test_reject_invitation_no_msg():
    
    pid = create_project(pm_uid, "Project A", "Projec A xyz", None, None, None)

    nid = notification_connection_request(tm3_uid, pm_uid)
    connection_request_respond(tm3_uid, nid, True)

    res = invite_to_project(pid, pm_uid, [tm3_uid])
    assert res == 0

    invite_ref = get_notif_ref_proj_invite(pid, tm3_uid)

    notif_pid = invite_ref.get("pid")
    has_read = invite_ref.get("has_read")
    response = invite_ref.get("response")

    assert has_read == False
    assert response == False
    assert pid == notif_pid

    accept = False
    msg = ""

    with pytest.raises(InputError):
        respond_project_invitation(notif_pid, tm3_uid, accept, msg)

    reset_projects()

############################################################
#                    Test for pin_project                  #
############################################################

def test_pin_project():
    pid = create_project(pm_uid, "Project A", "Projec A xyz", None, None, None)

    proj_ref = db.collection("projects").document(str(pid))
    is_pinned = proj_ref.get().get("is_pinned")

    assert is_pinned == False

    res = pin_project(pid, pm_uid, True)
    assert res == 0

    proj_ref = db.collection("projects").document(str(pid))
    is_pinned = proj_ref.get().get("is_pinned")

    assert is_pinned == True

def test_unpin_project():
    pid = create_project(pm_uid, "Project A", "Projec A xyz", None, None, None)

    proj_ref = db.collection("projects").document(str(pid))
    is_pinned = proj_ref.get().get("is_pinned")

    assert is_pinned == False

    res = pin_project(pid, pm_uid, True)
    assert res == 0

    proj_ref = db.collection("projects").document(str(pid))
    is_pinned = proj_ref.get().get("is_pinned")
    
    assert is_pinned == True

    # now unpin
    res = pin_project(pid, pm_uid, False)
    assert res == 0

    proj_ref = db.collection("projects").document(str(pid))
    is_pinned = proj_ref.get().get("is_pinned")
    
    assert is_pinned == False

def test_pin_invalid_project():
    pid = create_project(pm_uid, "Project A", "Projec A xyz", None, None, None)

    proj_ref = db.collection("projects").document(str(pid))

    is_pinned = proj_ref.get().get("is_pinned")

    assert is_pinned == False

    with pytest.raises(InputError):
        pin_project(-1, pm_uid, True)

def test_pin_not_in_project():
    pid = create_project(pm_uid, "Project A", "Projec A xyz", None, None, None)

    proj_ref = db.collection("projects").document(str(pid))

    is_pinned = proj_ref.get().get("is_pinned")

    assert is_pinned == False

    with pytest.raises(AccessError):
        pin_project(pid, tm1_uid, True)

def test_pin_pinned_project():
    pid = create_project(pm_uid, "Project A", "Projec A xyz", None, None, None)

    proj_ref = db.collection("projects").document(str(pid))

    is_pinned = proj_ref.get().get("is_pinned")

    assert is_pinned == False

    with pytest.raises(InputError):
        pin_project(pid, pm_uid, False)

'''
Unit test file for Project Management feature
'''
import pytest
from operator import itemgetter
from src.projects import *
from src.proj_master import *
from src.test_helpers import *
from src.helper import *
from src.projects import *

# ============ SET UP ============ #
@pytest.fixture
def set_up():
    reset_database() # Ensure database is clear for testing
    pm_uid = create_user_email("projectmaster@gmail.com", "admin123", "Project Master")
    tm1_uid = create_user_email("projecttest.tm1@gmail.com", "taskmaster1", "Task Master1")
    tm2_uid = create_user_email("projecttest.tm2@gmail.com", "taskmaster1", "Task Master2")
    tm3_uid = create_user_email("projecttest.tm3@gmail.com", "taskmaster1", "Task Master3")
    return {'pm_uid': pm_uid, 'tm1_uid': tm1_uid, 'tm2_uid': tm2_uid, 'tm3_uid': tm3_uid}

############################################################
#                    Test for view_project                 #
############################################################

def test_view_project(set_up):
    pm_uid, tm1_uid, tm2_uid, tm3_uid = itemgetter('pm_uid', 'tm1_uid', 'tm2_uid', 'tm3_uid')(set_up)
    
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

def test_view_project_invalid_pid(set_up):
    pm_uid, tm1_uid, tm2_uid, tm3_uid = itemgetter('pm_uid', 'tm1_uid', 'tm2_uid', 'tm3_uid')(set_up)

    pid = create_project(pm_uid, "Project0", "Creating Project0 for testing", None, None, None)

    # add tm to project
    add_tm_to_project(pid, tm1_uid)

    with pytest.raises(InputError):
        view_project(-1, tm1_uid)

def test_view_project_invalid_uid(set_up):
    pm_uid, tm1_uid, tm2_uid, tm3_uid = itemgetter('pm_uid', 'tm1_uid', 'tm2_uid', 'tm3_uid')(set_up)

    pid = create_project(pm_uid, "Project0", "Creating Project0 for testing", None, None, None)

    with pytest.raises(InputError):
        view_project(pid, "invalid")

def test_view_project_not_in_project(set_up):
    pm_uid, tm1_uid, tm2_uid, tm3_uid = itemgetter('pm_uid', 'tm1_uid', 'tm2_uid', 'tm3_uid')(set_up)

    pid = create_project(pm_uid, "Project0", "Creating Project0 for testing", None, None, None)

    res = view_project(pid, tm1_uid)

    pm_name = auth.get_user(pm_uid).display_name

    assert res == {
        "project_master": pm_name,
        "name": "Project0"
    }

############################################################
#                   Test for search_project                #
############################################################

def test_search_empty_query(set_up):
    pm_uid, tm1_uid, tm2_uid, tm3_uid = itemgetter('pm_uid', 'tm1_uid', 'tm2_uid', 'tm3_uid')(set_up)

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


def test_search_project_simple(set_up):
    pm_uid, tm1_uid, tm2_uid, tm3_uid = itemgetter('pm_uid', 'tm1_uid', 'tm2_uid', 'tm3_uid')(set_up)

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

def test_search_project_upper_lower(set_up):
    pm_uid, tm1_uid, tm2_uid, tm3_uid = itemgetter('pm_uid', 'tm1_uid', 'tm2_uid', 'tm3_uid')(set_up)

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

def test_search_project_pm_name(set_up):
    pm_uid, tm1_uid, tm2_uid, tm3_uid = itemgetter('pm_uid', 'tm1_uid', 'tm2_uid', 'tm3_uid')(set_up)
    
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

def test_search_project_verbose(set_up):
    pm_uid, tm1_uid, tm2_uid, tm3_uid = itemgetter('pm_uid', 'tm1_uid', 'tm2_uid', 'tm3_uid')(set_up)
    
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

def test_search_partial_member(set_up):
    pm_uid, tm1_uid, tm2_uid, tm3_uid = itemgetter('pm_uid', 'tm1_uid', 'tm2_uid', 'tm3_uid')(set_up)
    
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

def test_search_return_nothing(set_up):
    pm_uid, tm1_uid, tm2_uid, tm3_uid = itemgetter('pm_uid', 'tm1_uid', 'tm2_uid', 'tm3_uid')(set_up)
    
    query = "asdwqdasd"
    res = search_project(tm1_uid, query)

    assert res == []

############################################################
#                    Test for leave_project                #
############################################################

def test_leave_project(set_up):
    pm_uid, tm1_uid, tm2_uid, tm3_uid = itemgetter('pm_uid', 'tm1_uid', 'tm2_uid', 'tm3_uid')(set_up)
    
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

def test_leave_project_invalid_pid(set_up):
    pm_uid, tm1_uid, tm2_uid, tm3_uid = itemgetter('pm_uid', 'tm1_uid', 'tm2_uid', 'tm3_uid')(set_up)
    
    pid = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None, None)

    # add tm1 into project
    add_tm_to_project(pid, tm1_uid)

    msg = "Hi Project Master, I would like to leave the project Project Alpha due to xyz reasons."

    with pytest.raises(InputError):
        request_leave_project(-1, tm1_uid, msg)

def test_leave_project_invalid_uid(set_up):
    pm_uid, tm1_uid, tm2_uid, tm3_uid = itemgetter('pm_uid', 'tm1_uid', 'tm2_uid', 'tm3_uid')(set_up)
    
    pid = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None, None)

    # add tm1 into project
    add_tm_to_project(pid, tm1_uid)

    msg = "Hi Project Master, I would like to leave the project Project Alpha due to xyz reasons."

    with pytest.raises(InputError):
        request_leave_project(pid, "invalid", msg)

def test_leave_project_not_in_project(set_up):
    pm_uid, tm1_uid, tm2_uid, tm3_uid = itemgetter('pm_uid', 'tm1_uid', 'tm2_uid', 'tm3_uid')(set_up)
    
    pid = create_project(pm_uid, "Project Alpha", "Alpha does Spiking", None, None, None)

    # add tm1 is not a part of project 

    msg = "Hi Project Master, I would like to leave the project Project Alpha due to xyz reasons."

    with pytest.raises(AccessError):
        request_leave_project(pid, tm1_uid, msg)
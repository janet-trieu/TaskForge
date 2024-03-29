'''
Unit test file for Project Master feature
'''
import pytest
from firebase_admin import auth

from src.projmaster import *
from src.profile_page import *
from src.test_helpers import *
from src.helper import *

# test set up
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

    reset_projects()

    # test for project creation
    pid = create_project(pm_uid, "Project0", "Creating Project0 for testing", None, None)

    assert pid == 0

def test_create_project_every_args():

    reset_projects()
    
    # test for project creation
    pid = create_project(pm_uid, "Project1", "Creating Project1 for testing", "31/12/2023", "test1.jpg")

    assert pid == 0

def test_create_multiple_projects():

    reset_projects()

    # test for project1 creation
    pid = create_project(pm_uid, "Project1", "Creating Project1 for testing", None, None)
    
    assert pid == 0

    # test for project2 creation
    pid = create_project(pm_uid, "Project2", "Creating Project2 for testing", None, None)

    assert pid == 1

def test_create_project_invalid_uid():

    # test for project creation with invalid input
    with pytest.raises(InputError):
        create_project("Invalid", "Project1", "Creating Project1 for testing", None, None)

def test_create_project_invalid_uid_type():

    # test for project creation with invalid input
    with pytest.raises(InputError):
        create_project(-1, "Project1", "Creating Project1 for testing", None, None)

def test_create_project_invalid_name_type():

    # test for project creation with invalid input
    with pytest.raises(InputError):
        create_project(pm_uid, 1, "Creating Project1 for testing", None, None)

def test_create_project_empty_name():

    # test for project creation with invalid input
    with pytest.raises(InputError):
        create_project(pm_uid, "", "Creating Project1 for testing", None, None)

def test_create_project_invalid_name_length():

    # test for project creation with invalid input
    with pytest.raises(InputError):
        create_project(pm_uid, "A"*51, "Creating Project1 for testing", None, None)

def test_create_project_empty_description():

    # test for project creation with invalid input
    with pytest.raises(InputError):
        create_project(pm_uid, "Project1", "", None, None)

def test_create_project_invalid_description_type():

    # test for project creation with invalid input
    with pytest.raises(InputError):
        create_project(pm_uid, "Project1", 1, None, None)

def test_create_project_invalid_description_length():

    # test for project creation with invalid input
    with pytest.raises(InputError):
        create_project(pm_uid, "Project1", "A"*1001, None, None)

def test_create_project_invalid_due_date_type():

    with pytest.raises(InputError):
        create_project(pm_uid, "Project1", "Creating Project1 for testing", -1, None)

def test_create_project_invalid_due_date_format():

    with pytest.raises(ValueError):
        create_project(pm_uid, "Project1", "Creating Project1 for testing", "2023/1/1", None)

############################################################
#           Test for revive_completed_project              #
############################################################

def test_revive_completed_project_not_proj_master():
    
    incorrect_uid = tm1_uid

    pid = create_project(pm_uid, "Project 123", "description", None, None)

    res = update_project(pid, pm_uid, {"status": "Completed"})

    with pytest.raises(AccessError):
        revive_completed_project(pid, incorrect_uid, "In Review")

def test_revive_completed_project_invalid_pid():

    invalid_pid = -1

    pid = create_project(pm_uid, "Project 123", "description", None, None)

    res = update_project(pid, pm_uid, {"status": "Completed"})

    with pytest.raises(InputError):
        revive_completed_project(invalid_pid, pm_uid, "In Progress")

def test_revive_completed_project():

    pid = create_project(pm_uid, "Project 123", "description", None, None)

    proj_ref = db.collection("projects").document(str(pid))

    assert proj_ref.get().get("status") == "Not Started"

    res = update_project(pid, pm_uid, {"status": "Completed"})

    assert res == 0
    assert proj_ref.get().get("status") == "Completed"

    # revive completed project back into "In Progress"
    revive_completed_project(pid, pm_uid, "In Progress")

    assert proj_ref.get().get("status") == "In Progress"

def test_revive_non_completed_project():

    pid = create_project(pm_uid, "Project X", "description", None, None)

    proj_ref = db.collection("projects").document(str(pid))

    proj_status = proj_ref.get().get("status")

    assert proj_status == "Not Started"

    with pytest.raises(InputError):
        revive_completed_project(pid, pm_uid, "In Review")

############################################################
#             Test for remove_project_member               #
############################################################

def test_remove_project_member_not_proj_master():

    incorrect_uid = tm1_uid

    pid = create_project(pm_uid, "Project X", "description", None, None)

    add_tm_to_project(pid, tm1_uid)
    uid_to_be_removed = tm1_uid

    with pytest.raises(AccessError):
        remove_project_member(pid, incorrect_uid, uid_to_be_removed)

def test_remove_project_member_invalid_pid():

    pid = create_project(pm_uid, "Project X", "description", None, None)

    uid_to_be_removed = tm1_uid
    invalid_pid = -1

    with pytest.raises(InputError):
        remove_project_member(invalid_pid, pm_uid, uid_to_be_removed)

def test_remove_project_member():
    """
    Assumption: project already has members
    """

    pid = create_project(pm_uid, "Project X", "description", None, None)

    proj_ref = db.collection("projects").document(str(pid))
    project_members = proj_ref.get().get("project_members")

    uid_to_be_removed = tm1_uid

    add_tm_to_project(pid, tm1_uid)
    add_tm_to_project(pid, tm2_uid)
    add_tm_to_project(pid, tm3_uid)

    assert pm_uid == proj_ref.get().get("uid")
    res = remove_project_member(pid, pm_uid, uid_to_be_removed)

    assert res == 0

    proj_ref = db.collection("projects").document(str(pid))
    project_members = proj_ref.get().get("project_members")

    assert tm1_uid not in project_members

def test_remove_invalid_project_member():

    pid = create_project(pm_uid, "Project X", "description", None, None)

    uid_to_be_removed = tm1_uid

    with pytest.raises(InputError):
        remove_project_member(pid, pm_uid, uid_to_be_removed)

############################################################
#               Test for invite_to_project                 #
############################################################

def test_invite_to_project_not_proj_master():

    receiver_uids = []

    incorrect_uid = tm3_uid

    pid = create_project(pm_uid, "Project X", "description", None, None)

    receiver_uid = tm1_uid

    receiver_uids.append(receiver_uid)

    with pytest.raises(AccessError):
        invite_to_project(pid, incorrect_uid, receiver_uids)

def test_invite_to_project():
    
    receiver_uids = []

    sender_uid = pm_uid

    pid = create_project(sender_uid, "Project X", "description", None, None)

    receiver_uids.append(tm0_uid)

    tm_email = auth.get_user(tm0_uid).email
    nid = notification_connection_request(tm_email, pm_uid)
    connection_request_respond(tm0_uid, nid, True)

    res = invite_to_project(pid, sender_uid, receiver_uids)

    assert res == 0

def test_multiple_invite_to_project():

    receiver_uids = []

    sender_uid = pm_uid

    pid = create_project(sender_uid, "Project X", "description", None, None)

    receiver_uids.append(tm1_uid)
    receiver_uids.append(tm2_uid)
    receiver_uids.append(tm3_uid)

    tm1_email = auth.get_user(tm1_uid).email
    tm2_email = auth.get_user(tm2_uid).email
    tm3_email = auth.get_user(tm3_uid).email

    nid1 = notification_connection_request(tm1_email, pm_uid)
    nid2 = notification_connection_request(tm2_email, pm_uid)
    nid3 = notification_connection_request(tm3_email, pm_uid)
    connection_request_respond(tm1_uid, nid1, True)
    connection_request_respond(tm2_uid, nid2, True)
    connection_request_respond(tm3_uid, nid3, True)

    res = invite_to_project(pid, sender_uid, receiver_uids)

    assert res == 0

def test_invite_to_invalid_project():

    receiver_uids = []

    sender_uid = pm_uid

    pid = create_project(sender_uid, "Project X", "description", None, None)

    receiver_uid = tm1_uid

    receiver_uids.append(receiver_uid)

    incorrect_pid = -1

    with pytest.raises(InputError):
        invite_to_project(incorrect_pid, sender_uid, receiver_uids)

def test_invite_invalid_receiver_uid():

    receiver_uids = []

    sender_uid = pm_uid

    pid = create_project(sender_uid, "Project X", "description", None, None)

    receiver_uid = "fbWQa7QApSXhhx4usHOllqjuhRW2"

    receiver_uids.append(receiver_uid)

    with pytest.raises(InputError):
        invite_to_project(pid, sender_uid, receiver_uids)

def test_invite_uid_already_in_project():

    receiver_uids = []

    sender_uid = pm_uid

    pid = create_project(sender_uid, "Project X", "description", None, None)

    receiver_uid = tm1_uid

    receiver_uids.append(receiver_uid)

    add_tm_to_project(pid, tm1_uid)

    with pytest.raises(InputError):    
        invite_to_project(pid, sender_uid, receiver_uids)

############################################################
#                   Test for update_project                #
############################################################

def test_update_project():

    pid = create_project(pm_uid, "Project 0", "description", None, None)

    proj_ref = db.collection("projects").document(str(pid))

    updates = {
        "name": "Project 123",
        "description": "description 123",
        "status": "In Progress",
        "due_date": "31/12/2023",
        "picture": "testing.png"
    }

    res = update_project(pid, pm_uid, updates)

    name = proj_ref.get().get("name")
    description = proj_ref.get().get("description")
    status = proj_ref.get().get("status")
    due_date = proj_ref.get().get("due_date")
    picture = proj_ref.get().get("picture")

    assert res == 0
    assert name == "Project 123"
    assert description == "description 123"
    assert status == "In Progress"
    assert due_date == "31/12/2023"
    assert picture == "testing.png"

def test_update_project_invalid_name_type():

    pid = create_project(pm_uid, "Project 0", "description", None, None)

    with pytest.raises(InputError):
        update_project(pid, pm_uid, {"name": -1})

def test_update_project_invalid_name_value():

    pid = create_project(pm_uid, "Project 0", "description", None, None)

    with pytest.raises(InputError):
        update_project(pid, pm_uid, {"name": "A"*200})

def test_update_project_invalid_description_type():

    pid = create_project(pm_uid, "Project 0", "description", None, None)

    with pytest.raises(InputError):
        update_project(pid, pm_uid, {"description": 200})

def test_update_project_invalid_description_value():

    pid = create_project(pm_uid, "Project 0", "description", None, None)

    with pytest.raises(InputError):
        update_project(pid, pm_uid, {"description": "A"*2001})

def test_update_project_invalid_status_type():

    pid = create_project(pm_uid, "Project 0", "description", None, None)

    with pytest.raises(InputError):
        update_project(pid, pm_uid, {"status": -1})

def test_update_project_invalid_status_value():

    pid = create_project(pm_uid, "Project 0", "description", None, None)

    with pytest.raises(InputError):
        update_project(pid, pm_uid, {"status": "abc"})

def test_update_project_completed():

    pid = create_project(pm_uid, "Project 0", "description", None, None)

    proj_ref = db.collection("projects").document(str(pid))

    assert proj_ref.get().get("status") == "Not Started"

    res = update_project(pid, pm_uid, {"status": "Completed"})

    assert res == 0
    assert proj_ref.get().get("status") == "Completed"

    # fail because should be calling revive_completed_project
    with pytest.raises(AccessError):
        update_project(pid, pm_uid, {"status": "In Progress"})

def test_update_project_invalid_due_date_type():

    pid = create_project(pm_uid, "Project 0", "description", None, None)

    with pytest.raises(InputError):
        update_project(pid, pm_uid, {"due_date": -1})

def test_update_project_invalid_due_date_format():

    pid = create_project(pm_uid, "Project 0", "description", None, None)

    with pytest.raises(ValueError):
        update_project(pid, pm_uid, {"due_date": "2023/1/1"})

def test_update_project_not_project_master():

    pid = create_project(pm_uid, "Project 0", "description", None, None)

    with pytest.raises(AccessError):
        update_project(pid, tm1_uid, {"name": "Project X"})

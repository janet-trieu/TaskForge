'''
Blackbox testing of Project Master Feature
'''

import pytest
from src.projects import *
from src.proj_master import *
from src.test_helpers import *
from src.helper import *
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
#                   Test for create_project                #
############################################################
def test_create_project_use_default_vals():

    print(pm_uid)
    # test for project creation
    pid = create_project(pm_uid, "Project0", "Creating Project0 for testing", None, None, None, None)

    assert pid == 0

    # reset database
    reset_projects()

def test_create_project_every_args():
    
    # test for project creation
    pid = create_project(pm_uid, "Project1", "Creating Project1 for testing", "In Progress", "2023-12-31", 5, "test1.jpg")

    assert pid == 0

    # reset database
    reset_projects()

def test_create_multiple_projects():

    # test for project1 creation
    pid = create_project(pm_uid, "Project1", "Creating Project1 for testing", None, None, None, None)
    
    assert pid == 0

    # test for project2 creation
    pid = create_project(pm_uid, "Project2", "Creating Project2 for testing", None, None, None, None)

    assert pid == 1

    reset_projects()

def test_create_project_invalid_uid():

    # test for project creation with invalid input
    with pytest.raises(InputError):
        create_project("Invalid", "Project1", "Creating Project1 for testing", None, None, None, None)

    reset_projects()

def test_create_project_invalid_uid_type():

    # test for project creation with invalid input
    with pytest.raises(InputError):
        create_project(-1, "Project1", "Creating Project1 for testing", None, None, None, None)

    reset_projects()

def test_create_project_invalid_name_type():

    # test for project creation with invalid input
    with pytest.raises(InputError):
        create_project(pm_uid, 1, "Creating Project1 for testing", None, None, None, None)

    reset_projects()

def test_create_project_empty_name():

    # test for project creation with invalid input
    with pytest.raises(InputError):
        create_project(pm_uid, "", "Creating Project1 for testing", None, None, None, None)

    reset_projects()

def test_create_project_invalid_name_length():

    # test for project creation with invalid input
    with pytest.raises(InputError):
        create_project(pm_uid, "A"*51, "Creating Project1 for testing", None, None, None, None)

    reset_projects()

def test_create_project_empty_description():

    # test for project creation with invalid input
    with pytest.raises(InputError):
        create_project(pm_uid, "Project1", "", None, None, None, None)

    reset_projects()

def test_create_project_invalid_description_type():

    # test for project creation with invalid input
    with pytest.raises(InputError):
        create_project(pm_uid, "Project1", 1, None, None, None, None)

    reset_projects()

def test_create_project_invalid_description_length():

    # test for project creation with invalid input
    with pytest.raises(InputError):
        create_project(pm_uid, "Project1", "A"*1001, None, None, None, None)

    reset_projects()

def test_create_project_invalid_status():

    with pytest.raises(InputError):
        create_project(pm_uid, "Project1", "Creating Project1 for testing", "None", None, None, None)

    reset_projects()

def test_create_project_invalid_status_type():

    with pytest.raises(InputError):
        create_project(0, "Project1", "Creating Project1 for testing", -1, None, None, None)

    reset_projects()

def test_create_project_invalid_team_strength():

    with pytest.raises(InputError):
        create_project(pm_uid, "Project1", "Creating Project1 for testing", None, None, -1, None)

    reset_projects()

def test_create_project_invalid_team_strength_type():

    with pytest.raises(InputError):
        create_project(pm_uid, "Project1", "Creating Project1 for testing", None, None, "None", None)

    reset_projects()

#TO-DO: test for invalid picture input

############################################################
#           Test for revive_completed_project              #
############################################################

def test_revive_completed_project_not_proj_master():
    
    incorrect_uid = tm1_uid

    pid = create_project(pm_uid, "Project 123", "description", "Completed", None, None, None)

    with pytest.raises(AccessError):
        revive_completed_project(pid, incorrect_uid, "In Review")

    reset_projects()

def test_revive_completed_project_invalid_pid():

    invalid_pid = -1

    pid = create_project(pm_uid, "Project 123", "description", "Completed", None, None, None)

    with pytest.raises(InputError):
        revive_completed_project(invalid_pid, pm_uid, "In Progress")

    reset_projects()

def test_revive_completed_project():

    pid = create_project(pm_uid, "Project 123", "description", "Completed", None, None, None)

    proj_ref = db.collection("projects").document(str(pid))

    assert proj_ref.get().get("status") == "Completed"

    # revive completed project back into "In Progress"
    revive_completed_project(pid, pm_uid, "In Progress")

    assert proj_ref.get().get("status") == "In Progress"

    reset_projects()

def test_revive_non_completed_project():


    pid = create_project(pm_uid, "Project X", "description", "In Progress", None, None, None)

    proj_ref = db.collection("projects").document(str(pid))

    proj_status = proj_ref.get().get("status")

    assert proj_status == "In Progress"

    with pytest.raises(InputError):
        revive_completed_project(pid, pm_uid, "In Review")

    reset_projects()

############################################################
#             Test for remove_project_member               #
############################################################

def test_remove_project_member_not_proj_master():

    incorrect_uid = tm1_uid

    pid = create_project(pm_uid, "Project X", "description", "Completed", None, None, None)

    add_tm_to_project(pid, tm1_uid)
    uid_to_be_removed = tm1_uid

    with pytest.raises(AccessError):
        remove_project_member(pid, incorrect_uid, uid_to_be_removed)

    reset_projects()

def test_remove_project_member_invalid_pid():

    pid = create_project(pm_uid, "Project X", "description", "Completed", None, None, None)

    uid_to_be_removed = tm1_uid
    invalid_pid = -1

    with pytest.raises(InputError):
        remove_project_member(invalid_pid, pm_uid, uid_to_be_removed)

    reset_projects()

def test_remove_project_member():
    '''
    Assumption: project already has members
    '''

    pid = create_project(pm_uid, "Project X", "description", "Completed", None, None, None)

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

    print(project_members)
    assert tm1_uid not in project_members

    reset_projects()

def test_remove_invalid_project_member():

    pid = create_project(pm_uid, "Project X", "description", "Completed", None, None, None)

    uid_to_be_removed = tm1_uid

    with pytest.raises(InputError):
        remove_project_member(pid, pm_uid, uid_to_be_removed)

    reset_projects()

############################################################
#               Test for invite_to_project                 #
############################################################

def test_invite_to_project_not_proj_master():

    receiver_uids = []

    incorrect_uid = tm3_uid

    pid = create_project(pm_uid, "Project X", "description", "Completed", None, None, None)

    receiver_uid = tm1_uid

    receiver_uids.append(receiver_uid)

    with pytest.raises(AccessError):
        invite_to_project(pid, incorrect_uid, receiver_uids)

    reset_projects()

def test_invite_to_project():
    
    receiver_uids = []

    sender_uid = pm_uid

    pid = create_project(sender_uid, "Project X", "description", "Completed", None, None, None)

    receiver_uids.append(tm1_uid)

    res = invite_to_project(pid, sender_uid, receiver_uids)

    assert res == {
        tm1_uid: ["testingtm1@gmail.com", "Hi Task Master1, Project Master is inviting you to this project: Project X", "Please follow the link below to accept or reject this request: https://will_be_added.soon"]
    }
        
    reset_projects()

def test_multiple_invite_to_project():

    receiver_uids = []

    sender_uid = pm_uid

    pid = create_project(sender_uid, "Project X", "description", "Completed", None, None, None)

    receiver_uids.append(tm1_uid)
    receiver_uids.append(tm2_uid)
    receiver_uids.append(tm3_uid)

    res = invite_to_project(pid, sender_uid, receiver_uids)

    assert res == {
        tm1_uid: ["testingtm1@gmail.com", "Hi Task Master1, Project Master is inviting you to this project: Project X", "Please follow the link below to accept or reject this request: https://will_be_added.soon"],
        tm2_uid: ["testingtm2@gmail.com", "Hi Task Master2, Project Master is inviting you to this project: Project X", "Please follow the link below to accept or reject this request: https://will_be_added.soon"],
        tm3_uid: ["testingtm3@gmail.com", "Hi Task Master3, Project Master is inviting you to this project: Project X", "Please follow the link below to accept or reject this request: https://will_be_added.soon"]
    }

    reset_projects()

def test_invite_to_invalid_project():

    receiver_uids = []

    sender_uid = pm_uid

    pid = create_project(sender_uid, "Project X", "description", "Completed", None, None, None)

    receiver_uid = tm1_uid

    receiver_uids.append(receiver_uid)

    incorrect_pid = -1

    with pytest.raises(InputError):
        invite_to_project(incorrect_pid, sender_uid, receiver_uids)

    reset_projects()

def test_invite_invalid_receiver_uid():

    receiver_uids = []

    sender_uid = pm_uid

    pid = create_project(sender_uid, "Project X", "description", "Completed", None, None, None)

    receiver_uid = "fbWQa7QApSXhhx4usHOllqjuhRW2"

    receiver_uids.append(receiver_uid)

    with pytest.raises(InputError):
        invite_to_project(pid, sender_uid, receiver_uids)

    reset_projects()

def test_invite_uid_already_in_project():

    receiver_uids = []

    sender_uid = pm_uid

    pid = create_project(sender_uid, "Project X", "description", "Completed", None, None, None)

    receiver_uid = tm1_uid

    receiver_uids.append(receiver_uid)

    add_tm_to_project(pid, tm1_uid)

    with pytest.raises(InputError):    
        invite_to_project(pid, sender_uid, receiver_uids)

    reset_projects()

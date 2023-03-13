'''
Blackbox testing of Project Master Feature
'''

import pytest
from src.projects import *
from src.proj_master import *
from test_helpers import *

############################################################
#                   Test for create_project                #
############################################################

# initial variables for the users 
proj_master = auth.get_user_by_email("project.master@gmail.com")
task_master1 = auth.get_user_by_email("tm1@gmail.com")
task_master2 = auth.get_user_by_email("tm2@gmail.com")
task_master3 = auth.get_user_by_email("tm3@gmail.com")

def test_create_project_use_default_vals():

    reset_project_count()

    # test for project creation
    pid = create_project(proj_master.uid, "Project0", "Creating Project0 for testing", None, None, None, None)

    assert pid == 0

    # reset database
    reset_projects()

def test_create_project_every_args():

    reset_project_count()

    # test for project creation
    pid = create_project(proj_master.uid, "Project1", "Creating Project1 for testing", "In Progress", "2023-12-31", 5, "test1.jpg")

    assert pid == 0

    # reset database
    reset_projects()

def test_create_multiple_projects():

    reset_project_count()

    # test for project1 creation
    pid = create_project(proj_master.uid, "Project1", "Creating Project1 for testing", None, None, None, None)
    
    assert pid == 0

    # test for project2 creation
    pid = create_project(proj_master.uid, "Project2", "Creating Project2 for testing", None, None, None, None)

    assert pid == 1

    reset_projects()

def test_create_project_invalid_uid():

    reset_project_count()

    # test for project creation with invalid input
    with pytest.raises(ValueError):
        create_project("Invalid", "Project1", "Creating Project1 for testing", None, None, None, None)

    reset_projects()

def test_create_project_invalid_uid_type():

    reset_project_count()

    # test for project creation with invalid input
    with pytest.raises(TypeError):
        create_project(-1, "Project1", "Creating Project1 for testing", None, None, None, None)

    reset_projects()

def test_create_project_invalid_name_type():

    reset_project_count()

    # test for project creation with invalid input
    with pytest.raises(TypeError):
        create_project(proj_master.uid, 1, "Creating Project1 for testing", None, None, None, None)

    reset_projects()

def test_create_project_empty_name():

    reset_project_count()

    # test for project creation with invalid input
    with pytest.raises(ValueError):
        create_project(proj_master.uid, "", "Creating Project1 for testing", None, None, None, None)

    reset_projects()

def test_create_project_invalid_name_length():

    reset_project_count()

    # test for project creation with invalid input
    with pytest.raises(ValueError):
        create_project(proj_master.uid, "A"*51, "Creating Project1 for testing", None, None, None, None)

    reset_projects()

def test_create_project_empty_description():

    reset_project_count()

    # test for project creation with invalid input
    with pytest.raises(ValueError):
        create_project(proj_master.uid, "Project1", "", None, None, None, None)

    reset_projects()

def test_create_project_invalid_description_type():

    reset_project_count()

    # test for project creation with invalid input
    with pytest.raises(TypeError):
        create_project(proj_master.uid, "Project1", 1, None, None, None, None)

    reset_projects()

def test_create_project_invalid_description_length():

    reset_project_count()

    # test for project creation with invalid input
    with pytest.raises(ValueError):
        create_project(proj_master.uid, "Project1", "A"*1001, None, None, None, None)

    reset_projects()

def test_create_project_invalid_status():

    reset_project_count()

    with pytest.raises(ValueError):
        create_project(proj_master.uid, "Project1", "Creating Project1 for testing", "None", None, None, None)

    reset_projects()

def test_create_project_invalid_status_type():

    reset_project_count()

    with pytest.raises(TypeError):
        create_project(0, "Project1", "Creating Project1 for testing", -1, None, None, None)

    reset_projects()

def test_create_project_invalid_team_strength():

    reset_project_count()

    with pytest.raises(ValueError):
        create_project(proj_master.uid, "Project1", "Creating Project1 for testing", None, None, -1, None)

    reset_projects()

def test_create_project_invalid_team_strength_type():

    reset_project_count()

    with pytest.raises(TypeError):
        create_project(proj_master.uid, "Project1", "Creating Project1 for testing", None, None, "None", None)

    reset_projects()

#TO-DO: test for invalid picture input

############################################################
#           Test for revive_completed_project              #
############################################################

def test_revive_completed_project_not_proj_master():
    
    reset_project_count()

    incorrect_uid = task_master1.uid

    pid = create_project(proj_master.uid, "Project 123", "description", "Completed", None, None, None)
    res = revive_completed_project(pid, incorrect_uid, "In Review")

    assert not res == 0

    reset_projects()

def test_revive_completed_project_invalid_pid():
    reset_project_count()

    pid = -1
    res = revive_completed_project(pid, proj_master.uid, "In Progress")

    assert not res == 0

    reset_projects()

def test_revive_completed_project():

    reset_project_count()

    pid = create_project(proj_master.uid, "Project 123", "description", "Completed", None, None, None)

    proj_ref = db.collection("projects_test").document(str(pid))

    assert proj_ref.get().get("status") == "Completed"

    # revive completed project back into "In Progress"
    revive_completed_project(pid, proj_master.uid, "In Progress")

    assert proj_ref.get().get("status") == "In Progress"

    reset_projects()

def test_revive_non_completed_project():

    reset_project_count()

    pid = create_project(proj_master.uid, "Project X", "description", "In Progress", None, None, None)

    proj_ref = db.collection("projects_test").document(str(pid))

    proj_status = proj_ref.get().get("status")

    assert proj_status == "In Progress"

    res = revive_completed_project(pid, proj_master.uid, "In Review")

    assert not res == 0

    reset_projects()

############################################################
#             Test for remove_project_member               #
############################################################

def test_remove_project_member_not_proj_master():

    reset_project_count()

    incorrect_uid = task_master1.uid

    pid = create_project(proj_master.uid, "Project X", "description", "Completed", None, None, None)

    add_tm_to_project(pid, task_master1.uid)
    uid_to_be_removed = task_master1.uid

    res = remove_project_member(pid, incorrect_uid, uid_to_be_removed)

    assert not res == 0

    reset_projects()

def test_remove_project_member_invalid_pid():

    reset_project_count()

    pid = create_project(proj_master.uid, "Project X", "description", "Completed", None, None, None)

    uid_to_be_removed = task_master1.uid
    invalid_pid = -1

    res = remove_project_member(invalid_pid, proj_master.uid, uid_to_be_removed)

    assert not res == 0

    reset_projects()

def test_remove_project_member():
    '''
    Assumption: project already has members
    '''

    reset_project_count()

    pid = create_project(proj_master.uid, "Project X", "description", "Completed", None, None, None)

    proj_ref = db.collection("projects_test").document(str(pid))
    project_members = proj_ref.get().get("project_members")

    uid_to_be_removed = task_master1.uid

    add_tm_to_project(pid, task_master1.uid)
    add_tm_to_project(pid, task_master2.uid)
    add_tm_to_project(pid, task_master3.uid)

    assert proj_master.uid == proj_ref.get().get("uid")
    res = remove_project_member(pid, proj_master.uid, uid_to_be_removed)

    assert res == 0

    proj_ref = db.collection("projects_test").document(str(pid))
    project_members = proj_ref.get().get("project_members")

    print(project_members)
    assert task_master1.uid not in project_members

    reset_projects()

def test_remove_invalid_project_member():

    reset_project_count()

    pid = create_project(proj_master.uid, "Project X", "description", "Completed", None, None, None)

    uid_to_be_removed = task_master1.uid

    # remove_project_member only returns 0 after successful removal of a project member
    res = remove_project_member(pid, proj_master.uid, uid_to_be_removed)

    assert not res == 0

    reset_projects()

############################################################
#               Test for invite_to_project                 #
############################################################

def test_invite_to_project_not_proj_master():

    reset_project_count()

    incorrect_uid = task_master3.uid

    pid = create_project(proj_master.uid, "Project X", "description", "Completed", None, None, None)

    receiver_uid = task_master1.uid

    res = invite_to_project(pid, incorrect_uid, receiver_uid)

    assert not res == 0

    reset_projects()

def test_invite_to_project():
    
    reset_project_count()

    sender_uid = proj_master.uid

    pid = create_project(sender_uid, "Project X", "description", "Completed", None, None, None)

    receiver_uid = task_master1.uid

    res = invite_to_project(pid, sender_uid, receiver_uid)

    assert res == ("tm1@gmail.com", "Hi TM 1, Project Master is inviting you to this project: Project X", "Please follow the link below to accept or reject this request: https://will_be_added.soon")

    reset_projects()

def test_invite_to_invalid_project():

    reset_project_count()

    sender_uid = proj_master.uid

    pid = create_project(sender_uid, "Project X", "description", "Completed", None, None, None)

    receiver_uid = task_master1.uid

    incorrect_pid = -1

    res = invite_to_project(incorrect_pid, sender_uid, receiver_uid)

    assert not res == 0

    reset_projects()

def test_invite_invalid_receiver_uid():

    reset_project_count()

    sender_uid = proj_master.uid

    pid = create_project(sender_uid, "Project X", "description", "Completed", None, None, None)

    receiver_uid = "invalid"

    with pytest.raises(auth.UserNotFoundError):
        invite_to_project(pid, sender_uid, receiver_uid)

    reset_projects()

def test_invite_uid_already_in_project():

    reset_project_count()

    sender_uid = proj_master.uid

    pid = create_project(sender_uid, "Project X", "description", "Completed", None, None, None)

    receiver_uid = task_master1.uid

    add_tm_to_project(pid, task_master1.uid)

    res = invite_to_project(pid, sender_uid, receiver_uid)

    assert not res == 0

    reset_projects()

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

def test_create_project_use_default_vals():

    reset_project_count()

    # test for project creation
    pid = create_project(0, "Project0", "Creating Project0 for testing", None, None, None, None)

    assert pid == 0

    # reset database
    reset_projects()

def test_create_project_every_args():

    reset_project_count()

    # test for project creation
    pid = create_project(0, "Project1", "Creating Project1 for testing", "In Progress", "2023-12-31", 5, "test1.jpg")

    assert pid == 0

    # reset database
    reset_projects()

def test_create_multiple_projects():

    reset_project_count()

    # test for project1 creation
    pid = create_project(0, "Project1", "Creating Project1 for testing", None, None, None, None)
    
    assert pid == 0

    # test for project2 creation
    pid = create_project(0, "Project2", "Creating Project2 for testing", None, None, None, None)

    assert pid == 1

    reset_projects()

def test_create_project_invalid_uid():

    reset_project_count()

    # test for project creation with invalid input
    with pytest.raises(ValueError):
        create_project(-1, "Project1", "Creating Project1 for testing", None, None, None, None)

    reset_projects()

def test_create_project_invalid_uid_type():

    reset_project_count()

    # test for project creation with invalid input
    with pytest.raises(TypeError):
        create_project("1", "Project1", "Creating Project1 for testing", None, None, None, None)

    reset_projects()

def test_create_project_invalid_name_type():

    reset_project_count()

    # test for project creation with invalid input
    with pytest.raises(TypeError):
        create_project(0, 1, "Creating Project1 for testing", None, None, None, None)

    reset_projects()

def test_create_project_empty_name():

    reset_project_count()

    # test for project creation with invalid input
    with pytest.raises(ValueError):
        create_project(0, "", "Creating Project1 for testing", None, None, None, None)

    reset_projects()

def test_create_project_invalid_name_length():

    reset_project_count()

    # test for project creation with invalid input
    with pytest.raises(ValueError):
        create_project(0, "A"*51, "Creating Project1 for testing", None, None, None, None)

    reset_projects()

def test_create_project_empty_description():

    reset_project_count()

    # test for project creation with invalid input
    with pytest.raises(ValueError):
        create_project(0, "Project1", "", None, None, None, None)

    reset_projects()

def test_create_project_invalid_description_type():

    reset_project_count()

    # test for project creation with invalid input
    with pytest.raises(TypeError):
        create_project(0, "Project1", 1, None, None, None, None)

    reset_projects()

def test_create_project_invalid_description_length():

    reset_project_count()

    # test for project creation with invalid input
    with pytest.raises(ValueError):
        create_project(0, "Project1", "A"*1001, None, None, None, None)

    reset_projects()

def test_create_project_invalid_status():

    reset_project_count()

    with pytest.raises(ValueError):
        create_project(0, "Project1", "Creating Project1 for testing", "None", None, None, None)

    reset_projects()

def test_create_project_invalid_status_type():

    reset_project_count()

    with pytest.raises(TypeError):
        create_project(0, "Project1", "Creating Project1 for testing", -1, None, None, None)

    reset_projects()

def test_create_project_invalid_team_strength():

    reset_project_count()

    with pytest.raises(ValueError):
        create_project(0, "Project1", "Creating Project1 for testing", None, None, -1, None)

    reset_projects()

def test_create_project_invalid_team_strength_type():

    reset_project_count()

    with pytest.raises(TypeError):
        create_project(0, "Project1", "Creating Project1 for testing", None, None, "None", None)

    reset_projects()

#TO-DO: test for invalid picture input

############################################################
#           Test for revive_completed_project              #
############################################################

def test_revive_completed_project_not_proj_master():
    
    reset_project_count()

    incorrect_uid = -1

    pid = create_project(0, "Project 123", "description", "Completed", None, None, None)
    res = revive_completed_project(pid, incorrect_uid, "In Review")

    assert not res == 0

    reset_projects()

def test_revive_completed_project_invalid_pid():
    reset_project_count()

    pid = -1
    res = revive_completed_project(pid, 0, "In Progress")

    assert not res == 0

    reset_projects()

def test_revive_completed_project():

    reset_project_count()

    pid = create_project(0, "Project 123", "description", "Completed", None, None, None)

    proj_ref = db.collection("projects_test").document(str(pid))
    print(f"THIS IS STATUS == {proj_ref.get().get('status')}")
    assert proj_ref.get().get("status") == "Completed"

    # revive completed project back into "In Progress"
    revive_completed_project(pid, proj_ref.get().get("uid"), "In Progress")

    proj_ref = db.collection("projects_test").document(str(pid))
    print(f"THIS IS STATUS == {proj_ref.get().get('status')}")
    assert proj_ref.get().get("status") == "In Progress"

    reset_projects()

def test_revive_non_completed_project():

    reset_project_count()

    pid = create_project(0, "Project X", "description", "In Progress", None, None, None)

    proj_ref = db.collection("projects_test").document(str(pid))

    proj_status = proj_ref.get().get("status")

    assert proj_status == "In Progress"

    res = revive_completed_project(pid, 0, "In Review")

    assert not res == 0

    reset_projects()

############################################################
#             Test for remove_project_member               #
############################################################

def test_remove_project_member_not_proj_master():

    reset_project_count()

    incorrect_uid = -1

    pid = create_project(0, "Project X", "description", "Completed", None, None, None)

    add_tm_to_project(pid, 1)
    uid_to_be_removed = 1

    res = remove_project_member(pid, incorrect_uid, uid_to_be_removed)

    assert not res == 0

    reset_projects()

def test_remove_project_member_invalid_pid():

    reset_project_count()

    pid = create_project(0, "Project X", "description", "Completed", None, None, None)

    proj_ref = db.collection("projects_test").document(str(pid))


    uid_to_be_removed = 1
    invalid_pid = -1

    res = remove_project_member(invalid_pid, proj_ref.get().get("uid"), uid_to_be_removed)

    assert not res == 0

    reset_projects()

def test_remove_project_member():
    '''
    Assumption: project already has members
    '''

    reset_project_count()

    pid = create_project(0, "Project X", "description", "Completed", None, None, None)

    proj_ref = db.collection("projects_test").document(str(pid))
    project_members = proj_ref.get().get("project_members")

    uid_to_be_removed = 1

    add_tm_to_project(pid, 1)
    add_tm_to_project(pid, 2)
    add_tm_to_project(pid, 3)

    remove_project_member(pid, proj_ref.get().get("uid"), uid_to_be_removed)

    proj_ref = db.collection("projects_test").document(str(pid))
    project_members = proj_ref.get().get("project_members")

    assert project_members == [0, 2, 3]

    reset_projects()

def test_remove_invalid_project_member():

    reset_project_count()

    pid = create_project(0, "Project X", "description", "Completed", None, None, None)

    proj_ref = db.collection("projects_test").document(str(pid))

    uid_to_be_removed = 5

    # remove_project_member only returns 0 after successful removal of a project member
    res = remove_project_member(pid, proj_ref.get().get("uid"), uid_to_be_removed)

    assert not res == 0

    reset_projects()

############################################################
#               Test for invite_to_project                 #
############################################################

def test_create_project_not_proj_master():
    pass

def test_invite_to_project():
    
    pass

def test_invite_to_invalid_project():

    pass

def test_invite_invalid_uid():

    pass

def test_invite_uid_already_in_project():

    pass


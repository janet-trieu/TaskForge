'''
Blackbox testing of Project Master Feature
'''

import pytest
from src.projects import *
from src.proj_master import *

# def test_user_is_proj_master():
#     uid0 = 0
#     uid1 = 1

#     pid = create_project(uid0, "Project 123", "description", "Completed", None, None, None)


def test_create_project_use_default_vals():

    # test for project creation
    uid = 1
    name = "Project0"
    description = "Creating Project0 for testing"
    status = None
    due_date = None
    team_strength = None
    picture = None
    result = create_project(uid, name, description, status, due_date, team_strength, picture)

    assert result == 0

    # # reset database
    # db.collection("projects_test").document("0").delete()

def test_create_project_every_args():

    # test for project creation
    uid = 1
    name = "Project1"
    description = "Creating Project1 for testing"
    status = "In Progress"
    due_date = "2023-12-31"
    team_strength = 5
    picture = "test1.jpg"

    result = create_project(uid, name, description, status, due_date, team_strength, picture)

    assert result == 0

'''
Below is waiting to merge in Janet's changes to global counters
'''
# def test_create_multiple_projects():

#     # test for project1 creation
#     uid = 0
#     name = "Project1"
#     description = "Creating Project1 for testing"
#     status = None
#     due_date = None
#     team_strength = None
#     picture = None

#     result = create_project(uid, name, description, status, due_date, team_strength, picture)

#     assert result == 0

#     # test for project2 creation
#     uid = 0
#     name = "Project1"
#     description = "Creating Project1 for testing"
#     status = None
#     due_date = None
#     team_strength = None
#     picture = None

#     result = create_project(uid, name, description, status, due_date, team_strength, picture)

#     assert result == 1

def test_create_project_invalid_uid():

    # test for project creation with invalid input
    uid = -1
    name = "Project1"
    description = "description"
    status = "Not Started"
    due_date = None
    team_strength = None
    picture = None

    with pytest.raises(ValueError):
        create_project(uid, name, description, status, due_date, team_strength, picture)

def test_create_project_invalid_uid_type():

    # test for project creation with invalid input
    uid = "1"
    name = "Project1"
    description = "description"
    status = "Not Started"
    due_date = None
    team_strength = None
    picture = None

    with pytest.raises(TypeError):
        create_project(uid, name, description, status, due_date, team_strength, picture)

def test_create_project_invalid_name_type():

    # test for project creation with invalid input
    uid = 0
    name = 1
    description = "description"
    status = "Not Started"
    due_date = None
    team_strength = None
    picture = None

    with pytest.raises(TypeError):
        create_project(uid, name, description, status, due_date, team_strength, picture)

def test_create_project_invalid_name():

    # test for project creation with invalid input
    uid = 0
    name = ""
    description = "description"
    status = "Not Started"
    due_date = None
    team_strength = None
    picture = None

    with pytest.raises(ValueError):
        create_project(uid, name, description, status, due_date, team_strength, picture)

def test_create_project_invalid_name_length():

    # test for project creation with invalid input
    uid = 0
    name = "A"*51
    description = "description"
    status = "Not Started"
    due_date = None
    team_strength = None
    picture = None

    with pytest.raises(ValueError):
        create_project(uid, name, description, status, due_date, team_strength, picture)

def test_create_project_invalid_description():

    # test for project creation with invalid input
    uid = 0
    name = "Project0"
    description = ""
    status = "Not Started"
    due_date = None
    team_strength = None
    picture = None

    with pytest.raises(ValueError):
        create_project(uid, name, description, status, due_date, team_strength, picture)

def test_create_project_invalid_description_length():

    # test for project creation with invalid input
    uid = 0
    name = "Project0"
    description = "A"*1001
    status = "Not Started"
    due_date = None
    team_strength = None
    picture = None

    with pytest.raises(ValueError):
        create_project(uid, name, description, status, due_date, team_strength, picture)

def test_create_project_invalid_description_type():

    # test for project creation with invalid input
    uid = 0
    name = "Project0"
    description = 0
    status = "Not Started"
    due_date = None
    team_strength = None
    picture = None

    with pytest.raises(TypeError):
        create_project(uid, name, description, status, due_date, team_strength, picture)

def test_create_project_invalid_status():

    uid = 0
    name = "Project 1"
    description = "description"
    status = "NotStarted"
    due_date = None
    team_strength = None
    picture = None

    with pytest.raises(ValueError):
        create_project(uid, name, description, status, due_date, team_strength, picture)

def test_create_project_invalid_status_type():

    uid = 0
    name = "Project1"
    description = "description"
    status = 0
    due_date = None
    team_strength = None
    picture = None

    with pytest.raises(TypeError):
        create_project(uid, name, description, status, due_date, team_strength, picture)

def test_create_project_invalid_team_strength():

    uid = 0
    name = "Project1"
    description = "description"
    status = "Not Started"
    due_date = None
    team_strength = -1
    picture = None

    with pytest.raises(ValueError):
        create_project(uid, name, description, status, due_date, team_strength, picture)

def test_create_project_invalid_team_strength_type():

    uid = 0
    name = "Project1"
    description = "description"
    status = "Not Started"
    due_date = None
    team_strength = "1"
    picture = None

    with pytest.raises(TypeError):
        create_project(uid, name, description, status, due_date, team_strength, picture)

#TO-DO: test for invalid picture input

def test_revive_completed_project():
    '''
    project = create_project(args)  # create_project returns the project id (pid)

    # set project's status to complete

    revive_completed_project(pid, uid)
    
    '''
    pid = create_project(0, "Project 123", "description", "Completed", None, None, None)

    pid = 0
    proj_ref = db.collection("projects_test").document(str(pid))
    assert proj_ref.get().get("status") == "Completed"

    # revive completed project back into "In Progress"
    revive_completed_project(pid, proj_ref.get().get("uid"),"In Progress")

    proj_ref = db.collection("projects_test").document(str(pid))
    assert proj_ref.get().get("status") == "In Progress"

def test_revive_non_completed_projecct():
    pid = create_project(0, "Project X", "description", "In Progress", None, None, None)
    pid = 0

    with pytest.raises(ValueError):
        revive_completed_project(pid, 0, "In Progress")

def test_remove_project_member():
    '''
    Assumption: project already has members
    '''
    pid = create_project(0, "Project X", "description", "Completed", None, None, None)
    pid = 0

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

def test_remove_invalid_project_member():
    pid = create_project(0, "Project X", "description", "Completed", None, None, None)
    pid = 0

    proj_ref = db.collection("projects_test").document(str(pid))

    uid_to_be_removed = 5

    # remove_project_member only returns 0 after successful removal of a project member
    res = remove_project_member(pid, proj_ref.get().get("uid"), uid_to_be_removed)

    assert not res == 0


def test_invite_to_project():
    
    pass


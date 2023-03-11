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
    uid = 0
    name = "Project0"
    description = "Creating Project0 for testing"
    status = None
    due_date = None
    team_strength = None
    picture = None
    result = create_project(uid, name, description, status, due_date, team_strength, picture)

    assert result == 0

    # reset database
    reset_projects()

def test_create_project_every_args():

    reset_project_count()

    # test for project creation
    uid = 0
    name = "Project1"
    description = "Creating Project1 for testing"
    status = "In Progress"
    due_date = "2023-12-31"
    team_strength = 5
    picture = "test1.jpg"

    result = create_project(uid, name, description, status, due_date, team_strength, picture)

    assert result == 0

    # reset database
    reset_projects()

def test_create_multiple_projects():

    reset_project_count()

    # test for project1 creation
    uid = 0
    name = "Project1"
    description = "Creating Project1 for testing"
    status = None
    due_date = None
    team_strength = None
    picture = None

    result = create_project(uid, name, description, status, due_date, team_strength, picture)
    
    assert result == 0

    # test for project2 creation
    uid = 0
    name = "Project2"
    description = "Creating Project2 for testing"
    status = None
    due_date = None
    team_strength = None
    picture = None

    result = create_project(uid, name, description, status, due_date, team_strength, picture)

    assert result == 1

    reset_projects()

def test_create_project_invalid_uid():

    reset_project_count()

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

    reset_projects()

def test_create_project_invalid_uid_type():

    reset_project_count()

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

    reset_projects()

def test_create_project_invalid_name_type():

    reset_project_count()

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

    reset_projects()

def test_create_project_invalid_name():

    reset_project_count()

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

    reset_projects()

def test_create_project_invalid_name_length():

    reset_project_count()

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

    reset_projects()

def test_create_project_invalid_description():

    reset_project_count()

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

    reset_projects()

def test_create_project_invalid_description_length():

    reset_project_count()

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

    reset_projects()

def test_create_project_invalid_description_type():

    reset_project_count()

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

    reset_projects()

def test_create_project_invalid_status():

    reset_project_count()

    uid = 0
    name = "Project 1"
    description = "description"
    status = "NotStarted"
    due_date = None
    team_strength = None
    picture = None

    with pytest.raises(ValueError):
        create_project(uid, name, description, status, due_date, team_strength, picture)

    reset_projects()

def test_create_project_invalid_status_type():

    reset_project_count()

    uid = 0
    name = "Project1"
    description = "description"
    status = 0
    due_date = None
    team_strength = None
    picture = None

    with pytest.raises(TypeError):
        create_project(uid, name, description, status, due_date, team_strength, picture)

    reset_projects()

def test_create_project_invalid_team_strength():

    reset_project_count()

    uid = 0
    name = "Project1"
    description = "description"
    status = "Not Started"
    due_date = None
    team_strength = -1
    picture = None

    with pytest.raises(ValueError):
        create_project(uid, name, description, status, due_date, team_strength, picture)

    reset_projects()

def test_create_project_invalid_team_strength_type():

    reset_project_count()

    uid = 0
    name = "Project1"
    description = "description"
    status = "Not Started"
    due_date = None
    team_strength = "1"
    picture = None

    with pytest.raises(TypeError):
        create_project(uid, name, description, status, due_date, team_strength, picture)

    reset_projects()

#TO-DO: test for invalid picture input

############################################################
#           Test for revive_completed_project              #
############################################################

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

def test_remove_project_member_invalid_pid():

    reset_project_count()

    pid = create_project(0, "Project X", "description", "Completed", None, None, None)

    proj_ref = db.collection("projects_test").document(str(pid))
    project_members = proj_ref.get().get("project_members")

    uid_to_be_removed = 1

    add_tm_to_project(pid, 1)
    add_tm_to_project(pid, 2)
    add_tm_to_project(pid, 3)

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
def test_invite_to_project():
    
    pass


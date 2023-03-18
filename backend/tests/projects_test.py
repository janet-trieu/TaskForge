'''
Unit test file for Project Management feature
'''
import pytest
from src.projects import *
from src.proj_master import *
from src.test_helpers import *
from src.helper import *
from src.projects import *

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

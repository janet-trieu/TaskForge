import pytest
from firebase_admin import auth
from src.test_helpers import *
from src.profile_page import *
from src.proj_master import *
from src.projects import *
from src.helper import *
from src.taskboard import *
from src.achievement import *

try:
    pm_uid = create_user_email("achievements.pm@gmail.com", "admin123", "Project Master")
    tm0_uid = create_user_email("achievements.tm0@gmail.com", "taskmaster0", "Task Master0")
    tm1_uid = create_user_email("achievements.tm1@gmail.com", "taskmaster1", "Task Master1")
    tm2_uid = create_user_email("achievements.tm2@gmail.com", "taskmaster2", "Task Master2")
    tm3_uid = create_user_email("achievements.tm3@gmail.com", "taskmaster3", "Task Master3")
    tm4_uid = create_user_email("achievements.tm4@gmail.com", "taskmaster4", "Task Master4")
except auth.EmailAlreadyExistsError:
    pass
pm_uid = auth.get_user_by_email("achievements.pm@gmail.com").uid
tm0_uid = auth.get_user_by_email("achievements.tm0@gmail.com").uid
tm1_uid = auth.get_user_by_email("achievements.tm1@gmail.com").uid
tm2_uid = auth.get_user_by_email("achievements.tm2@gmail.com").uid
tm3_uid = auth.get_user_by_email("achievements.tm3@gmail.com").uid
tm4_uid = auth.get_user_by_email("achievements.tm4@gmail.com").uid

############################################################
#                  Test for get_achievements               #
############################################################

def test_get_1():
    pid = create_project(pm_uid, "Project0", "Creating Project0 for testing", None, None, None)

    tid = create_task(pm_uid, pid, "", [pm_uid], "Task0", "description", "", None, None, "Not Started")

    #TODO finish this test, update task status to complete, 
    '''
    res = check_achievement("task_completion", pm_uid)
    assert res == True

    doc.get_user_ref(pm_uid)
    assert 1 in doc.get("achievements")
    '''

def test_get_2_and_16():

    pid = create_project(pm_uid, "Project0", "Creating Project0 for testing", None, None, None)

    res = check_achievement("project_completion", pm_uid)

    assert res == False

    doc = get_user_ref(pm_uid)
    assert 2 not in doc.get("achievements")
    assert 16 not in doc.get("achievements")

    update_project(pid, pm_uid, {"status": "Completed"})

    res = check_achievement("project_completion", pm_uid)

    assert res == True

    doc = get_user_ref(pm_uid)
    assert 2 in doc.get("achievements")
    assert 16 in doc.get("achievements")

# waiting for update_task
def test_get_3():
    pass

# waiting for update_task
def test_get_4():
    pass

def test_get_5_and_6():
    pid1 = create_project(pm_uid, "Project1", "Creating Project1 for testing", None, None, None)
    pid2 = create_project(pm_uid, "Project2", "Creating Project2 for testing", None, None, None)
    pid3 = create_project(pm_uid, "Project3", "Creating Project3 for testing", None, None, None)
    pid4 = create_project(pm_uid, "Project4", "Creating Project4 for testing", None, None, None)
    pid5 = create_project(pm_uid, "Project5", "Creating Project5 for testing", None, None, None)

    update_project(pid1, pm_uid, {"status": "Completed"})
    update_project(pid2, pm_uid, {"status": "Completed"})
    update_project(pid3, pm_uid, {"status": "Completed"})
    update_project(pid4, pm_uid, {"status": "Completed"})

    check_achievement("project_completion", pm_uid)

    doc = get_user_ref(pm_uid)
    assert 5 not in doc.get("achievements")

    update_project(pid5, pm_uid, {"status": "Completed"})

    check_achievement("project_completion", pm_uid)

    doc = get_user_ref(pm_uid)
    assert 5 in doc.get("achievements")

    pid6 = create_project(pm_uid, "Project6", "Creating Project6 for testing", None, None, None)
    pid7 = create_project(pm_uid, "Project7", "Creating Project7 for testing", None, None, None)
    pid8 = create_project(pm_uid, "Project8", "Creating Project8 for testing", None, None, None)
    pid9 = create_project(pm_uid, "Project9", "Creating Project9 for testing", None, None, None)
    pid10 = create_project(pm_uid, "Project10", "Creating Project10 for testing", None, None, None)

    update_project(pid6, pm_uid, {"status": "Completed"})
    update_project(pid7, pm_uid, {"status": "Completed"})
    update_project(pid8, pm_uid, {"status": "Completed"})
    update_project(pid9, pm_uid, {"status": "Completed"})

    check_achievement("project_completion", pm_uid)

    doc = get_user_ref(pm_uid)
    assert 6 not in doc.get("achievements")

    update_project(pid10, pm_uid, {"status": "Completed"})

    check_achievement("project_completion", pm_uid)

    doc = get_user_ref(pm_uid)
    assert 6 in doc.get("achievements")

def test_get_7():

    nid = notification_connection_request(tm0_uid, pm_uid)
    connection_request_respond(tm0_uid, nid, True)
    nid = notification_connection_request(tm1_uid, pm_uid)
    connection_request_respond(tm1_uid, nid, True)
    nid = notification_connection_request(tm2_uid, pm_uid)
    connection_request_respond(tm2_uid, nid, True)
    nid = notification_connection_request(tm3_uid, pm_uid)
    connection_request_respond(tm3_uid, nid, True)

    res = check_achievement("connection", pm_uid)
    assert res == False

    doc = get_user_ref(pm_uid)
    assert 7 not in doc.get("achievements")

    nid = notification_connection_request(tm4_uid, pm_uid)
    connection_request_respond(tm4_uid, nid, True)

    res = check_achievement("connection", pm_uid)
    assert res == True

    doc = get_user_ref(pm_uid)
    assert 7 in doc.get("achievements")

#TODO wait for reputation
def test_get_8():
    pass

#TODO wait for reputation
def test_get_9():
    pass

#TODO wait for reputation
def test_get_10():
    pass

#TODO wait for reputation
def test_get_11():
    pass

#TODO wait for reputation
def test_get_12():
    pass

#TODO wait for reputation
def test_get_13():
    pass

def test_get_14():
    pid = create_project(pm_uid, "Project0", "Creating Project0 for testing", None, None, None)

    tid1 = create_task(pm_uid, pid, "", [pm_uid], "Task1", "description", "", None, None, "Not Started")
    tid2 = create_task(pm_uid, pid, "", [pm_uid], "Task2", "description", "", None, None, "Not Started")
    tid3 = create_task(pm_uid, pid, "", [pm_uid], "Task3", "description", "", None, None, "Not Started")
    tid4 = create_task(pm_uid, pid, "", [pm_uid], "Task4", "description", "", None, None, "Not Started")
    tid5 = create_task(pm_uid, pid, "", [pm_uid], "Task5", "description", "", None, None, "Not Started")
    tid6 = create_task(pm_uid, pid, "", [pm_uid], "Task6", "description", "", None, None, "Not Started")
    tid7 = create_task(pm_uid, pid, "", [pm_uid], "Task7", "description", "", None, None, "Not Started")

    res = check_achievement("task_assigned", pm_uid)
    assert res == False

    doc = get_user_ref(pm_uid)
    assert 14 not in doc.get("achievements")
    
    tid8 = create_task(pm_uid, pid, "", [pm_uid], "Task8", "description", "", None, None, "Not Started")

    res = check_achievement("task_assigned", pm_uid)
    assert res == True

    doc = get_user_ref(pm_uid)
    assert 14 in doc.get("achievements")

#TODO wait for reputation
def test_get_15():
    pass

############################################################
#                 Test for view_achievements               #
############################################################

def test_view_my_achievements():
    pass

def test_view_notmy_achievements():
    pass

def test_view_no_achievements():
    pass

def test_view_invalid_uid():
    pass

def test_view_not_connected():
    pass

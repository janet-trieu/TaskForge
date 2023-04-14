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
'''
def test_task_complete_3():

    pid = create_project(pm_uid, "Project0", "Creating Project0 for testing", None, None, None)

    add_tm_to_project(pid, tm0_uid)

    tid1 = create_task(tm0_uid, pid, "", [tm0_uid], "Task0", "description", "", None, None, "Not Started")
    tid2 = create_task(tm0_uid, pid, "", [tm0_uid], "Task1", "description", "", None, None, "Not Started")
    tid3 = create_task(tm0_uid, pid, "", [tm0_uid], "Task2", "description", "", None, None, "Not Started")

    change_task_status(tm0_uid, tid1, "Completed")
    change_task_status(tm0_uid, tid2, "Completed")
    change_task_status(tm0_uid, tid3, "Completed")

    achievements = get_user_achievements(tm0_uid)

    assert achievements[0]["aid"] == 0

def test_task_complete_5():

    pid = create_project(pm_uid, "Project0", "Creating Project0 for testing", None, None, None)

    add_tm_to_project(pid, tm1_uid)

    tid1 = create_task(tm1_uid, pid, "", [tm1_uid], "Task1", "description", "", None, None, "Not Started")
    tid2 = create_task(tm1_uid, pid, "", [tm1_uid], "Task2", "description", "", None, None, "Not Started")
    tid3 = create_task(tm1_uid, pid, "", [tm1_uid], "Task3", "description", "", None, None, "Not Started")
    tid4 = create_task(tm1_uid, pid, "", [tm1_uid], "Task4", "description", "", None, None, "Not Started")
    tid5 = create_task(tm1_uid, pid, "", [tm1_uid], "Task5", "description", "", None, None, "Not Started")

    change_task_status(tm1_uid, tid1, "Completed")
    change_task_status(tm1_uid, tid2, "Completed")
    change_task_status(tm1_uid, tid3, "Completed")
    change_task_status(tm1_uid, tid4, "Completed")
    change_task_status(tm1_uid, tid5, "Completed")

    achievements = get_user_achievements(tm1_uid)

    assert achievements[1]["aid"] == 1

def test_proj_complete_3():

    pid1 = create_project(pm_uid, "Project1", "Creating Project1 for testing", None, None, None)
    pid2 = create_project(pm_uid, "Project2", "Creating Project2 for testing", None, None, None)
    pid3 = create_project(pm_uid, "Project3", "Creating Project3 for testing", None, None, None)

    update_project(pid1, pm_uid, {"status": "Completed"})
    update_project(pid2, pm_uid, {"status": "Completed"})
    update_project(pid3, pm_uid, {"status": "Completed"})

    achievements = get_user_achievements(pm_uid)

    assert achievements[0]["aid"] == 2

def test_proj_complete_5():

    pid1 = create_project(pm_uid, "Project1", "Creating Project1 for testing", None, None, None)
    pid2 = create_project(pm_uid, "Project2", "Creating Project2 for testing", None, None, None)
    pid3 = create_project(pm_uid, "Project3", "Creating Project3 for testing", None, None, None)
    pid4 = create_project(pm_uid, "Project4", "Creating Project4 for testing", None, None, None)
    pid5 = create_project(pm_uid, "Project5", "Creating Project5 for testing", None, None, None)

    update_project(pid1, pm_uid, {"status": "Completed"})
    update_project(pid2, pm_uid, {"status": "Completed"})
    update_project(pid3, pm_uid, {"status": "Completed"})
    update_project(pid4, pm_uid, {"status": "Completed"})
    update_project(pid5, pm_uid, {"status": "Completed"})

    achievements = get_user_achievements(pm_uid)

    assert achievements[1]["aid"] == 3
'''

def test_connection_num():
    tm0_email = get_email(tm0_uid)
    tm1_email = get_email(tm1_uid)
    tm2_email = get_email(tm2_uid)

    nid = notification_connection_request(tm0_email, pm_uid)
    connection_request_respond(tm0_uid, nid, True)
    nid = notification_connection_request(tm1_email, pm_uid)
    connection_request_respond(tm1_uid, nid, True)
    nid = notification_connection_request(tm2_email, pm_uid)
    connection_request_respond(tm2_uid, nid, True)

    achievements = get_user_achievements(pm_uid)

    assert achievements[0]["aid"] == 4

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

'''
Unit test file for Achievements
'''

import pytest
from firebase_admin import auth

from src.test_helpers import *
from src.projmaster import *
from src.tasks import *
from src.achievement import *
from src.reputation import *

# test set up
try:
    pm_uid = create_user_email("achievements.pm@gmail.com", "admin123", "Project Master")
    pm1_uid = create_user_email("achievements.pm1@gmail.com", "admin123", "Project Master1")
    pm2_uid = create_user_email("achievements.pm2@gmail.com", "admin123", "Project Master2")
    tm0_uid = create_user_email("achievements.tm0@gmail.com", "taskmaster0", "Task Master0")
    tm1_uid = create_user_email("achievements.tm1@gmail.com", "taskmaster1", "Task Master1")
    tm2_uid = create_user_email("achievements.tm2@gmail.com", "taskmaster2", "Task Master2")
    tm3_uid = create_user_email("achievements.tm3@gmail.com", "taskmaster3", "Task Master3")
    tm4_uid = create_user_email("achievements.tm4@gmail.com", "taskmaster4", "Task Master4")
except auth.EmailAlreadyExistsError:
    pass
pm_uid = auth.get_user_by_email("achievements.pm@gmail.com").uid
pm1_uid = auth.get_user_by_email("achievements.pm1@gmail.com").uid
pm2_uid = auth.get_user_by_email("achievements.pm2@gmail.com").uid
tm0_uid = auth.get_user_by_email("achievements.tm0@gmail.com").uid
tm1_uid = auth.get_user_by_email("achievements.tm1@gmail.com").uid
tm2_uid = auth.get_user_by_email("achievements.tm2@gmail.com").uid
tm3_uid = auth.get_user_by_email("achievements.tm3@gmail.com").uid
tm4_uid = auth.get_user_by_email("achievements.tm4@gmail.com").uid

############################################################
#                  Test for get_achievements               #
############################################################

def test_task_complete_3():

    pid = create_project(pm_uid, "Project0", "Creating Project0 for testing", None, None)

    add_tm_to_project(pid, tm0_uid)

    tid1 = create_task(tm0_uid, pid, "", [], "Task0", "description", "", None, None, "Not Started")
    tid2 = create_task(tm0_uid, pid, "", [], "Task1", "description", "", None, None, "Not Started")
    tid3 = create_task(tm0_uid, pid, "", [], "Task2", "description", "", None, None, "Not Started")

    change_task_status(tm0_uid, tid1["tid"], "Completed")
    change_task_status(tm0_uid, tid2["tid"], "Completed")
    change_task_status(tm0_uid, tid3["tid"], "Completed")

    achievements = get_user_achievements(tm0_uid)

    assert achievements[0]["aid"] == 0

def test_task_complete_5():

    pid = create_project(pm_uid, "Project0", "Creating Project0 for testing", None, None)

    add_tm_to_project(pid, tm1_uid)

    tid1 = create_task(tm1_uid, pid, "", [], "Task1", "description", "", None, None, "Not Started")
    tid2 = create_task(tm1_uid, pid, "", [], "Task2", "description", "", None, None, "Not Started")
    tid3 = create_task(tm1_uid, pid, "", [], "Task3", "description", "", None, None, "Not Started")
    tid4 = create_task(tm1_uid, pid, "", [], "Task4", "description", "", None, None, "Not Started")
    tid5 = create_task(tm1_uid, pid, "", [], "Task5", "description", "", None, None, "Not Started")

    change_task_status(tm1_uid, tid1["tid"], "Completed")
    change_task_status(tm1_uid, tid2["tid"], "Completed")
    change_task_status(tm1_uid, tid3["tid"], "Completed")
    change_task_status(tm1_uid, tid4["tid"], "Completed")
    change_task_status(tm1_uid, tid5["tid"], "Completed")

    achievements = get_user_achievements(tm1_uid)

    assert achievements[1]["aid"] == 1

def test_proj_complete_3():

    pid1 = create_project(pm_uid, "Project1", "Creating Project1 for testing", None, None)
    pid2 = create_project(pm_uid, "Project2", "Creating Project2 for testing", None, None)
    pid3 = create_project(pm_uid, "Project3", "Creating Project3 for testing", None, None)

    update_project(pid1, pm_uid, {"status": "Completed"})
    update_project(pid2, pm_uid, {"status": "Completed"})
    update_project(pid3, pm_uid, {"status": "Completed"})

    achievements = get_user_achievements(pm_uid)

    # check 2nd achievement as user probably got the lone wolf achievement first
    assert achievements[1]["aid"] == 2

def test_proj_complete_5():

    pid1 = create_project(pm1_uid, "Project1", "Creating Project1 for testing", None, None)
    pid2 = create_project(pm1_uid, "Project2", "Creating Project2 for testing", None, None)
    pid3 = create_project(pm1_uid, "Project3", "Creating Project3 for testing", None, None)
    pid4 = create_project(pm1_uid, "Project4", "Creating Project4 for testing", None, None)
    pid5 = create_project(pm1_uid, "Project5", "Creating Project5 for testing", None, None)

    update_project(pid1, pm1_uid, {"status": "Completed"})
    update_project(pid2, pm1_uid, {"status": "Completed"})
    update_project(pid3, pm1_uid, {"status": "Completed"})
    update_project(pid4, pm1_uid, {"status": "Completed"})
    update_project(pid5, pm1_uid, {"status": "Completed"})

    achievements = get_user_achievements(pm1_uid)

    # check 3rd achievement as user probably got the lone wolf achievement, and then intermediate project master 2nd
    assert achievements[2]["aid"] == 3

def test_connection_num():
    tm0_email = get_email(tm0_uid)
    tm1_email = get_email(tm1_uid)
    tm2_email = get_email(tm2_uid)

    try:
        nid = notification_connection_request(tm0_email, pm_uid)
        connection_request_respond(tm0_uid, nid, True)
        nid = notification_connection_request(tm1_email, pm_uid)
        connection_request_respond(tm1_uid, nid, True)
        nid = notification_connection_request(tm2_email, pm_uid)
        connection_request_respond(tm2_uid, nid, True)
    except AccessError:
        pass
    
    check_achievement("connection", pm_uid)

    achievements = get_user_achievements(pm_uid)

    assert achievements[2]["aid"] == 4

def test_task_assign_num():

    pid = create_project(pm_uid, "Project0", "Creating Project0 for testing", None, None)

    add_tm_to_project(pid, tm1_uid)
    add_tm_to_project(pid, tm2_uid)

    tid1 = create_task(tm2_uid, pid, "", [], "Task1", "description", "", None, None, "Not Started")
    tid2 = create_task(tm2_uid, pid, "", [], "Task2", "description", "", None, None, "Not Started")
    tid3 = create_task(tm2_uid, pid, "", [], "Task3", "description", "", None, None, "Not Started")
    tid4 = create_task(tm2_uid, pid, "", [], "Task4", "description", "", None, None, "Not Started")
    tid5 = create_task(tm2_uid, pid, "", [], "Task5", "description", "", None, None, "Not Started")
    tid6 = create_task(tm2_uid, pid, "", [], "Task6", "description", "", None, None, "Not Started")
    tid7 = create_task(tm2_uid, pid, "", [], "Task7", "description", "", None, None, "Not Started")
    tid8 = create_task(tm1_uid, pid, "", [], "Task8", "description", "", None, None, "Not Started")

    tm1_email = get_email(tm1_uid)
    tm2_email = get_email(tm2_uid)

    assign_task(tm1_uid, tid8["tid"], [tm1_email, tm2_email])

    achievements = get_user_achievements(tm2_uid)

    assert achievements[0]["aid"] == 5

def test_lone_wolf():

    pid = create_project(pm2_uid, "Project0", "Creating Project0 for testing", None, None)

    update_project(pid, pm2_uid, {"status": "Completed"})

    achievements = get_user_achievements(pm2_uid)

    assert achievements[0]["aid"] == 6

def test_reputation_num():
    pid = create_project(pm2_uid, "Project0", "Creating Project0 for testing", None, None)

    add_tm_to_project(pid, tm0_uid)
    add_tm_to_project(pid, tm1_uid)
    add_tm_to_project(pid, tm2_uid)

    update_project(pid, pm2_uid, {"status": "Completed"})

    write_review(pm2_uid, tm0_uid, pid, "5", "5", "5", "Very Good")
    write_review(pm2_uid, tm1_uid, pid, "5", "5", "5", "Very Good")
    write_review(pm2_uid, tm2_uid, pid, "5", "5", "5", "Very Good")

    achievements = get_user_achievements(pm2_uid)

    assert achievements[1]["aid"] == 7

############################################################
#                 Test for view_achievements               #
############################################################

def test_view_achievements():

    pm_uid = create_test_user("achievememts.pm123", 5)

    give_achievement(pm_uid, 0)

    res = view_achievement(pm_uid)
    assert res[0]["aid"] == 0

def test_view_notmy_achievements():

    pm_uid = create_test_user("achievememts.pm123", 5)

    try:
        tm0_email = get_email(tm0_uid)
        nid = notification_connection_request(tm0_email, pm_uid)
        connection_request_respond(tm0_uid, nid, True)
    except AccessError:
        pass

    achievements = get_user_achievements(pm_uid)

    res = view_connected_tm_achievement(tm0_uid, pm_uid)

    assert achievements == res

def test_view_not_connected():

    with pytest.raises(AccessError):
        view_connected_tm_achievement(pm_uid, tm4_uid)

def test_view_no_achievements():
    res = view_achievement(tm4_uid)

    assert res == []

def test_view_visibility_off():

    pm_uid = create_test_user("achievememts.pm123", 6)

    try:
        tm0_email = get_email(tm0_uid)
        nid = notification_connection_request(tm0_email, pm_uid)
        connection_request_respond(tm0_uid, nid, True)
    except AccessError:
        pass

    toggle_achievement_visibility(pm_uid, True)

    res = view_connected_tm_achievement(tm0_uid, pm_uid)

    assert res == []

############################################################
#                Test for share_achievements               #
############################################################

def test_share_achievement():

    pm_uid = create_test_user("achievements.pm1234", 5)

    tm0_email = get_email(tm0_uid)
    try:
        nid = notification_connection_request(tm0_email, pm_uid)
        connection_request_respond(tm0_uid, nid, True)
    except AccessError:
        pass

    give_achievement(pm_uid, 0)

    share_achievement(pm_uid, [tm0_uid], 0)

    doc_data = db.collection('notifications').document(tm0_uid).get().to_dict()
    actual_notification = doc_data.get('achievement_shared0')

    assert actual_notification.get('notification_msg') == "User User5 has earned the Intermediate Task Master achievement."
    assert actual_notification.get('type') == 'achievement_shared'
    assert actual_notification.get('nid') == 'achievement_shared0'

def test_share_not_connected():
    give_achievement(pm_uid, 0)

    with pytest.raises(InputError):
        share_achievement(pm_uid, [tm4_uid], 0)

def test_share_not_got_achievement():
    
    with pytest.raises(InputError):
        share_achievement(tm4_uid, [tm1_uid], 7)

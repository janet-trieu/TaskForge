import pytest
from firebase_admin import auth
from src.test_helpers import *
from src.proj_master import *
from src.taskboard import *
from src.achievement import *
from src.reputation import *

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

def test_task_assign_num():

    pid = create_project(pm_uid, "Project0", "Creating Project0 for testing", None, None, None)

    add_tm_to_project(pid, tm2_uid)
    add_tm_to_project(pid, tm3_uid)

    tid1 = create_task(tm3_uid, pid, "", [tm3_uid], "Task1", "description", "", None, None, "Not Started")
    tid2 = create_task(tm3_uid, pid, "", [tm3_uid], "Task2", "description", "", None, None, "Not Started")
    tid3 = create_task(tm3_uid, pid, "", [tm3_uid], "Task3", "description", "", None, None, "Not Started")
    tid4 = create_task(tm3_uid, pid, "", [tm3_uid], "Task4", "description", "", None, None, "Not Started")
    tid5 = create_task(tm3_uid, pid, "", [tm3_uid], "Task5", "description", "", None, None, "Not Started")
    tid6 = create_task(tm3_uid, pid, "", [tm3_uid], "Task6", "description", "", None, None, "Not Started")
    tid7 = create_task(tm3_uid, pid, "", [tm3_uid], "Task7", "description", "", None, None, "Not Started")
    tid8 = create_task(tm2_uid, pid, "", [tm2_uid], "Task8", "description", "", None, None, "Not Started")
    assign_task(tm2_uid, tid8, [tm2_uid, tm3_uid])

    achievements = get_user_achievements(tm3_uid)

    assert achievements[0]["aid"] == 5

def test_lone_wolf():

    pid = create_project(pm_uid, "Project0", "Creating Project0 for testing", None, None, None)

    update_project(pid, pm_uid, {"status": "Completed"})

    achievements = get_user_achievements(pm_uid)
    print(achievements)

    assert achievements[0]["aid"] == 6

def test_reputation_num():
    pid = create_project(pm_uid, "Project0", "Creating Project0 for testing", None, None, None)

    add_tm_to_project(pid, tm0_uid)
    add_tm_to_project(pid, tm1_uid)
    add_tm_to_project(pid, tm2_uid)

    update_project(pid, pm_uid, {"status": "Completed"})

    write_review(pm_uid, tm0_uid, pid, "5", "5", "5", "Very Good")
    write_review(pm_uid, tm1_uid, pid, "5", "5", "5", "Very Good")
    write_review(pm_uid, tm2_uid, pid, "5", "5", "5", "Very Good")

    achievements = get_user_achievements(pm_uid)

    assert achievements[0]["aid"] == 7

############################################################
#                 Test for view_achievements               #
############################################################

def test_view_my_achievements():

    pid = create_project(pm_uid, "Project0", "Creating Project0 for testing", None, None, None)

    update_project(pid, pm_uid, {"status": "Completed"})

    # lone wolf should be in achievements
    achievements = get_user_achievements(pm_uid)

    res = view_achievement(pm_uid)

    assert achievements == res
'''

def test_view_multiple_achievements():

    pid = create_project(pm_uid, "Project Achievements", "Creating Project0 for testing", None, None, None)

    tid1 = create_task(pm_uid, pid, "", [pm_uid], "Task1", "description", "", None, None, "Not Started")
    tid2 = create_task(pm_uid, pid, "", [pm_uid], "Task2", "description", "", None, None, "Not Started")
    tid3 = create_task(pm_uid, pid, "", [pm_uid], "Task3", "description", "", None, None, "Not Started")
    tid4 = create_task(pm_uid, pid, "", [pm_uid], "Task4", "description", "", None, None, "Not Started")
    tid5 = create_task(pm_uid, pid, "", [pm_uid], "Task5", "description", "", None, None, "Not Started")
    tid6 = create_task(pm_uid, pid, "", [pm_uid], "Task6", "description", "", None, None, "Not Started")
    tid7 = create_task(pm_uid, pid, "", [pm_uid], "Task7", "description", "", None, None, "Not Started")
    tid8 = create_task(pm_uid, pid, "", [pm_uid], "Task8", "description", "", None, None, "Not Started")

    # octopus should be achieved now
    achievements = get_user_achievements(pm_uid)
    assert achievements[0]["aid"] == 5

    update_project(pid, pm_uid, {"status": "Completed"})

    # lone wolf should be achieved now, and should be ordered first
    res = view_achievement(pm_uid)
    print(res)
    assert res[0]["aid"] == 6
    assert res[1]["aid"] == 5

'''
def test_view_notmy_achievements():

    pid = create_project(pm_uid, "Project0", "Creating Project0 for testing", None, None, None)

    update_project(pid, pm_uid, {"status": "Completed"})

    user_ref = db.collection("users").document(pm_uid).get()
    if tm0_uid not in user_ref.get("connections"):
        tm0_email = get_email(tm0_uid)
        nid = notification_connection_request(tm0_email, pm_uid)
        connection_request_respond(tm0_uid, nid, True)

    # lone wolf should be in achievements
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

    pid = create_project(pm_uid, "Project0", "Creating Project0 for testing", None, None, None)

    update_project(pid, pm_uid, {"status": "Completed"})

    user_ref = db.collection("users").document(pm_uid).get()
    if tm0_uid not in user_ref.get("connections"):
        tm0_email = get_email(tm0_uid)
        nid = notification_connection_request(tm0_email, pm_uid)
        connection_request_respond(tm0_uid, nid, True)

    toggle_achievement_visibility(pm_uid, 0)

    res = view_connected_tm_achievement(tm0_uid, pm_uid)

    assert res == []

############################################################
#                Test for share_achievements               #
############################################################

def test_share_achievement():

    user_ref = db.collection("users").document(pm_uid).get()
    if tm0_uid not in user_ref.get("connections"):
        tm0_email = get_email(tm0_uid)
        nid = notification_connection_request(tm0_email, pm_uid)
        connection_request_respond(tm0_uid, nid, True)

    give_achievement(pm_uid, 0)

    share_achievement(pm_uid, [tm0_uid], 0)

    doc_data = db.collection('notifications').document(tm0_uid).get().to_dict()
    actual_notification = doc_data.get('achievement_shared0')

    assert actual_notification.get('notification_msg') == "Project Master has earned the Intermediate Task Master achievement."
    assert actual_notification.get('type') == 'achievement_shared'
    assert actual_notification.get('nid') == 'achievement_shared0'

def test_share_not_connected():
    give_achievement(pm_uid, 0)

    with pytest.raises(InputError):
        share_achievement(pm_uid, [tm4_uid], 0)

def test_share_not_got_achievement():
    
    with pytest.raises(InputError):
        share_achievement(pm_uid, [tm1_uid], 7)
'''
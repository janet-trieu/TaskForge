import pytest
from firebase_admin import auth
from src.test_helpers import *
from src.profile_page import *
from src.projmaster import *
from src.projects import *
from src.helper import *
from src.taskboard import *
from src.achievement import *
import requests


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

port = 8000
url = f"http://localhost:{port}/"

def test_view_achievements():

    pid = create_project(pm_uid, "Project0", "Creating Project0 for testing", None, None, None)

    add_tm_to_project(pid, tm0_uid)

    tid1 = create_task(tm0_uid, pid, "", [tm0_uid], "Task0", "description", "", None, None, "Not Started")
    tid2 = create_task(tm0_uid, pid, "", [tm0_uid], "Task1", "description", "", None, None, "Not Started")
    tid3 = create_task(tm0_uid, pid, "", [tm0_uid], "Task2", "description", "", None, None, "Not Started")

    change_task_status(tm0_uid, tid1, "Completed")
    change_task_status(tm0_uid, tid2, "Completed")
    change_task_status(tm0_uid, tid3, "Completed")

    achievements = get_user_achievements(tm0_uid)

    header = {'Authorization': tm0_uid}
    view_resp = requests.get(url + "achievements/view/my", headers=header)

    assert view_resp.status_code == 200

    view_json = view_resp.json()

    assert achievements == view_json

def test_view_achievements_notmy():

    pid = create_project(pm_uid, "Project0", "Creating Project0 for testing", None, None, None)

    update_project(pid, pm_uid, {"status": "Completed"})

    user_ref = db.collection("users").document(pm_uid).get()
    if tm0_uid not in user_ref.get("connections"):
        tm0_email = get_email(tm0_uid)
        nid = notification_connection_request(tm0_email, pm_uid)
        connection_request_respond(tm0_uid, nid, True)

    # lone wolf should be in achievements
    achievements = get_user_achievements(pm_uid)

    header = {'Authorization': tm0_uid}
    params = {"conn_uid": pm_uid}
    view_resp = requests.get(url + "achievements/view/notmy", headers=header, params=params)

    assert view_resp.status_code == 200

    view_json = view_resp.json()

    assert achievements == view_json

def test_view_hidden():

    pid = create_project(pm_uid, "Project0", "Creating Project0 for testing", None, None, None)

    update_project(pid, pm_uid, {"status": "Completed"})

    user_ref = db.collection("users").document(pm_uid).get()
    if tm0_uid not in user_ref.get("connections"):
        tm0_email = get_email(tm0_uid)
        nid = notification_connection_request(tm0_email, pm_uid)
        connection_request_respond(tm0_uid, nid, True)

    header = {'Authorization': pm_uid}
    toggle_resp = requests.post(url + "achievements/toggle_visibility", headers=header, json={
        "action": 0
    })

    assert toggle_resp.status_code == 200

    header = {'Authorization': tm0_uid}
    params = {"conn_uid": pm_uid}
    view_resp = requests.get(url + "achievements/view/notmy", headers=header, params=params)

    assert view_resp.status_code == 200

    view_json = view_resp.json()

    assert view_json == []


def test_share_achievement():

    user_ref = db.collection("users").document(pm_uid).get()
    if tm0_uid not in user_ref.get("connections"):
        tm0_email = get_email(tm0_uid)
        nid = notification_connection_request(tm0_email, pm_uid)
        connection_request_respond(tm0_uid, nid, True)

    give_achievement(pm_uid, 0)

    header = {'Authorization': pm_uid}
    share_resp = requests.post(url + "achievements/share", headers=header, json={
        "receiver_uids": [tm0_uid],
        "aid": 0
    })

    assert share_resp.status_code == 200

def test_share_achievement_not_connected():

    give_achievement(pm_uid, 0)

    header = {'Authorization': pm_uid}
    share_resp = requests.post(url + "achievements/share", headers=header, json={
        "receiver_uids": [tm4_uid],
        "aid": 0
    })

    assert share_resp.status_code == 400

def test_share_achievement_not_got_achievement():

    give_achievement(pm_uid, 0)

    header = {'Authorization': pm_uid}
    share_resp = requests.post(url + "achievements/share", headers=header, json={
        "receiver_uids": [tm0_uid],
        "aid": 7
    })

    assert share_resp.status_code == 400

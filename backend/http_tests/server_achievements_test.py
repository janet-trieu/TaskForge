'''
Test file for Flask http testing of achievement
'''

import pytest
import requests
from firebase_admin import auth

from src.test_helpers import *
from src.profile_page import *
from src.projmaster import *
from src.projects import *
from src.helper import *
from src.tasks import *
from src.achievement import *

# test set up
try:
    pm_uid = create_user_email("achievements.pm9@gmail.com", "admin123", "Project Master")
    tm0_uid = create_user_email("achievements.tm10@gmail.com", "taskmaster0", "Task Master0")
    tm4_uid = create_user_email("achievements.tm11@gmail.com", "taskmaster4", "Task Master4")
except auth.EmailAlreadyExistsError:
    pass
pm_uid = auth.get_user_by_email("achievements.pm9@gmail.com").uid
tm0_uid = auth.get_user_by_email("achievements.tm10@gmail.com").uid
tm4_uid = auth.get_user_by_email("achievements.tm11@gmail.com").uid

port = 8000
url = f"http://localhost:{port}/"

############################################################
#                  Test for view_achievement               #
############################################################

def test_view_achievements():

    pid = create_project(pm_uid, "Project0", "Creating Project0 for testing", None, None)

    update_project(pid, pm_uid, {"status": "Completed"})

    achievements = get_user_achievements(pm_uid)

    header = {'Authorization': pm_uid}
    view_resp = requests.get(url + "achievements/view/my", headers=header)

    assert view_resp.status_code == 200

    view_json = view_resp.json()

    assert achievements == view_json

def test_view_achievements_notmy():

    try:
        tm0_email = get_email(tm0_uid)
        nid = notification_connection_request(tm0_email, pm_uid)
        connection_request_respond(tm0_uid, nid, True)
    except AccessError:
        pass

    # lone wolf should be in achievements
    achievements = get_user_achievements(pm_uid)

    header = {'Authorization': tm0_uid}
    params = {"conn_uid": pm_uid}
    view_resp = requests.get(url + "achievements/view/notmy", headers=header, params=params)

    assert view_resp.status_code == 200

    view_json = view_resp.json()

    assert achievements == view_json

def test_view_hidden():

    try:
        tm0_email = get_email(tm0_uid)
        nid = notification_connection_request(tm0_email, pm_uid)
        connection_request_respond(tm0_uid, nid, True)
    except AccessError:
        pass

    header = {'Authorization': pm_uid}
    toggle_resp = requests.post(url + "achievements/toggle_visibility", headers=header, json={
        "action": True
    })

    assert toggle_resp.status_code == 200
    assert check_achievement_visibility(pm_uid) == True

    header = {'Authorization': tm0_uid}
    params = {"conn_uid": pm_uid}
    view_resp = requests.get(url + "achievements/view/notmy", headers=header, params=params)

    assert view_resp.status_code == 200

    view_json = view_resp.json()

    assert view_json == []

############################################################
#                 Test for share_achievement               #
############################################################

def test_share_achievement():

    tm0_email = get_email(tm0_uid)
    try:
        nid = notification_connection_request(tm0_email, pm_uid)
        connection_request_respond(tm0_uid, nid, True)
    except AccessError:
        pass

    # lone wolf should already be given
    give_achievement(pm_uid, 0)

    header = {'Authorization': pm_uid}
    share_resp = requests.post(url + "achievements/share", headers=header, json={
        "receiver_emails": [tm0_email],
        "aid": 0
    })

    assert share_resp.status_code == 200

def test_share_achievement_not_connected():

    tm4_email = get_email(tm4_uid)
    header = {'Authorization': pm_uid}
    share_resp = requests.post(url + "achievements/share", headers=header, json={
        "receiver_emails": [tm4_email],
        "aid": 0
    })

    assert share_resp.status_code == 400

def test_share_achievement_not_got_achievement():

    tm0_email = get_email(tm0_uid)
    header = {'Authorization': pm_uid}
    share_resp = requests.post(url + "achievements/share", headers=header, json={
        "receiver_emails": [tm0_email],
        "aid": 7
    })

    assert share_resp.status_code == 400

import pytest

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth

from src.profile_page import *
from src.notifications import *
from src.proj_master import *
from src.global_counters import *

from src.test_helpers import *

# ============ SET UP ============ #
db = firestore.client()

try:
    create_user_email("notificationtest0@gmail.com", "password123", "John Doe")
    create_user_email("notificationtest1@gmail.com", "password123", "Jane Doe")
    create_user_email("notificationtest2@gmail.com", "password123", "Richard Roe")
except auth.EmailAlreadyExistsError:
    pass

user_id0 = auth.get_user_by_email("notificationtest0@gmail.com").uid
user_id1 = auth.get_user_by_email("notificationtest1@gmail.com").uid
user_id2 = auth.get_user_by_email("notificationtest2@gmail.com").uid

# ============ TESTS ============ #
def test_welcome_notification():
    '''
    Test to ensure create_user_email() adds a welcome notification in the database
    '''
    doc_data = db.collection('notifications').document(user_id0).get().to_dict()
    actual_notification = doc_data.get('welcome')

    assert actual_notification.get('has_read') == False
    assert actual_notification.get('notification_msg') == "Welcome to TaskForge, John Doe. You can view future notifications here!"
    assert isinstance(actual_notification.get('time_sent'), datetime)
    
def test_project_invite_notification():
    '''
    Test to ensure invite_to_project() adds invite notifications in the database
    '''

    pid_expected = create_project(user_id0, "Project N", "Description", None, None, None)
    receiver_uids = [user_id1, user_id2]
    invite_to_project(pid_expected, user_id0, receiver_uids)

    # Assert user 1 has invite notification data #
    doc_data = db.collection('notifications').document(user_id1).get().to_dict()
    actual_notification = doc_data.get('project_invite0')

    assert actual_notification.get('has_read') == False
    assert actual_notification.get('notification_msg') == "John Doe has invited you to join Project N."
    assert actual_notification.get('pid') == pid_expected
    assert isinstance(actual_notification.get('time_sent'), datetime)
    assert actual_notification.get('type') == 'project_invite'
    assert actual_notification.get('uid_sender') == user_id0
    assert actual_notification.get('accept_msg') == "You accepted John Doe's project invitation."
    assert actual_notification.get('decline_msg') == "You declined John Doe's project invitation."
    assert actual_notification.get('nid') == 'project_invite0'

    # Assert user 2 has invite notification data; skip some data #
    doc_data = db.collection('notifications').document(user_id2).get().to_dict()
    actual_notification = doc_data.get('project_invite0')

    assert actual_notification.get('notification_msg') == "John Doe has invited you to join Project N."
    assert actual_notification.get('pid') == pid_expected
    assert actual_notification.get('uid_sender') == user_id0
    assert actual_notification.get('nid') == 'project_invite0'

    reset_projects()

# COMMENTED OUT TESTS THAT ARE WAITING FOR IT'S PARENT FUNCTION TO BE IMPLEMENTED

""" 
def test_sorted_notifications():
    # Ensure get_notifications returns a descending order
    sorted_notifications = get_notifications(user_id0)

    # Assert the current notification timestamp is greater or equal to the next sorted notification
    for i in range(len(sorted_notifications) - 1):
        assert sorted_notifications[i]['time_sent'] >= sorted_notifications[i+1]['time_sent']

def test_clear_all_notifications():
    clear_all_notifications(user_id0)

    doc_data = db.collection('notifications').document(user_id0).get().to_dict()

    assert doc_data == {}

def test_clear_notification():
    notification_connection_request(user_id0, user_id1)
    notification_achievement(user_id0, achievement_str='night_owl')

    notf_list = get_notifications(user_id0)
    
    assert len(notf_list) == 2

    # clear achievement0 - most recent notification
    clear_notification(user_id0, notf_list[0])

    notf_list = get_notifications(user_id0)

    assert len(notf_list) == 1
    assert notf_list[0]['nid'] == 'connection_request0'
    assert notf_list[0]['uid_sender'] == 'NotifyUser1'
    assert notf_list[0]['notification_msg'] == 'Jane Doe has requested to connect.'

def test_no_dupe_nid():
    clear_all_notifications(user_id0)

    notification_comment(user_id0, user_id1, pid_expected, tid_expected)
    notification_comment(user_id0, user_id1, pid_expected, tid_expected)
    notification_comment(user_id0, user_id1, pid_expected, tid_expected)

    # Clear 2nd notification
    notf_list = get_notifications(user_id0)
    clear_notification(user_id0, notf_list[1])

    # 'comment0', 'comment2' still exist. making length = 2
    # without dupe check, the next comment would have the nid 'comment2'
    # with dupe check, the next comment would have the nid 'comment3' instead
    notification_comment(user_id0, user_id1, pid_expected, tid_expected)
    notf_list = get_notifications(user_id0)
    assert notf_list[0]['nid'] == 'comment3' """
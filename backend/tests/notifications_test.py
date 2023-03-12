'''
TODO
- !!! Currently cannot test with needed functions, added dummy data directly to db 
    - once more stuff gets implement i can make these tests alot more nicer
- remember to remove direct calls once these have been implemented to ensure they work along side with respective functions
'''
import pytest

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth

from src.notifications import *

# ============ SET UP ============ #
# Use a service account.
db = firestore.client()

# ============ HELPERS ============ #
user_id0 = 'NotifyUser0'
user_id1 = 'NotifyUser1'

pid_expected = 7357
tid_expected = 1010
rid_expected = 400

def setup():
    db.collection('users').document(user_id0).set({'display_name':'John Doe'})
    db.collection('users').document(user_id1).set({'display_name':'Jane Doe'})
    db.collection('projects').document(str(pid_expected)).set({'name':'Project Notification !!! NOTIFICATION TEST'})
    db.collection('tasks').document(str(tid_expected)).set({'name':'Task Notification !!! NOTIFICATION TEST'})
    db.collection('achievements').document('night_owl').set({'name':'Night Owl !!! NOTIFICATION TEST'})
    db.collection('reviews').document(str(rid_expected)).set({'uid':'notifytestid1'})

def remove_test_data():
    pass

# ============ TESTS ============ #
def test_welcome_notification():
    notification_welcome(user_id0)

    doc_data = db.collection('notifications').document(user_id0).get().to_dict()
    actual_notification = doc_data.get('welcome')

    assert actual_notification.get('has_read') == False
    assert actual_notification.get('notification_msg') == "Welcome to TaskForge, John Doe. You can view future notifications here!"
    assert isinstance(actual_notification.get('time_sent'), datetime)

def test_connection_request_notification():
    notification_connection_request(user_id0, user_id1)

    doc_data = db.collection('notifications').document(user_id0).get().to_dict()
    actual_notification = doc_data.get('connection_request0')

    assert actual_notification.get('has_read') == False
    assert actual_notification.get('notification_msg') == "Jane Doe has requested to connect."
    assert isinstance(actual_notification.get('time_sent'), datetime)
    assert actual_notification.get('type') == 'connection_request'
    assert actual_notification.get('uid_sender') == 'NotifyUser1'
    assert actual_notification.get('accept_msg') == "You accepted Jane Doe's connection request."
    assert actual_notification.get('decline_msg') == "You declined Jane Doe's connection request."

def test_project_invite_notification():
    notification_project_invite(user_id0, user_id1, pid_expected)

    doc_data = db.collection('notifications').document(user_id0).get().to_dict()
    actual_notification = doc_data.get('project_invite0')

    assert actual_notification.get('has_read') == False
    assert actual_notification.get('notification_msg') == "Jane Doe has invited you to join Project Notification !!! NOTIFICATION TEST."
    assert actual_notification.get('pid') == pid_expected
    assert isinstance(actual_notification.get('time_sent'), datetime)
    assert actual_notification.get('type') == 'project_invite'
    assert actual_notification.get('uid_sender') == 'NotifyUser1'
    assert actual_notification.get('accept_msg') == "You accepted Jane Doe's project invitation."
    assert actual_notification.get('decline_msg') == "You declined Jane Doe's project invitation."

def test_assigned_task_notification():
    notification_assigned_task(user_id0, pid_expected, tid_expected)

    doc_data = db.collection('notifications').document(user_id0).get().to_dict()
    actual_notification = doc_data.get('assigned_task0')

    assert actual_notification.get('has_read') == False
    assert actual_notification.get('notification_msg') == "You have been assigned Task Notification !!! NOTIFICATION TEST in Project Notification !!! NOTIFICATION TEST."
    assert actual_notification.get('pid') == pid_expected
    assert actual_notification.get('tid') == tid_expected
    assert isinstance(actual_notification.get('time_sent'), datetime)
    assert actual_notification.get('type') == 'assigned_task'

def test_comment_notification():
    notification_comment(user_id0, user_id1, pid_expected, tid_expected)

    doc_data = db.collection('notifications').document(user_id0).get().to_dict()
    actual_notification = doc_data.get('comment0')

    assert actual_notification.get('has_read') == False
    assert actual_notification.get('notification_msg') == "Jane Doe has commented in Task Notification !!! NOTIFICATION TEST in Project Notification !!! NOTIFICATION TEST."
    assert actual_notification.get('pid') == pid_expected
    assert actual_notification.get('tid') == tid_expected
    assert isinstance(actual_notification.get('time_sent'), datetime)
    assert actual_notification.get('type') == 'comment'
    assert actual_notification.get('uid_sender') == 'NotifyUser1'

def test_deadline_notification():
    notification_deadline(user_id0, pid_expected, tid_expected)

    doc_data = db.collection('notifications').document(user_id0).get().to_dict()
    actual_notification = doc_data.get('deadline0')

    assert actual_notification.get('has_read') == False
    assert actual_notification.get('notification_msg') == "Task Notification !!! NOTIFICATION TEST from Project Notification !!! NOTIFICATION TEST is due soon."
    assert actual_notification.get('pid') == pid_expected
    assert actual_notification.get('tid') == tid_expected
    assert isinstance(actual_notification.get('time_sent'), datetime)
    assert actual_notification.get('type') == 'deadline'

def test_review_notification():
    notification_review(user_id0, user_id1, rid_expected)

    doc_data = db.collection('notifications').document(user_id0).get().to_dict()
    actual_notification = doc_data.get('review0')

    assert actual_notification.get('has_read') == False
    assert actual_notification.get('notification_msg') == "Jane Doe has reviewed you."
    assert actual_notification.get('rid') == rid_expected
    assert isinstance(actual_notification.get('time_sent'), datetime)
    assert actual_notification.get('type') == 'review'
    assert actual_notification.get('uid_sender') == 'NotifyUser1'

def test_achievement_notification():
    notification_achievement(user_id0, achievement_str='night_owl')

    doc_data = db.collection('notifications').document(user_id0).get().to_dict()
    actual_notification = doc_data.get('achievement0')

    assert actual_notification.get('achievement') == 'night_owl'
    assert actual_notification.get('has_read') == False
    assert actual_notification.get('notification_msg') == "You have earned the Night Owl !!! NOTIFICATION TEST achievement."
    assert isinstance(actual_notification.get('time_sent'), datetime)
    assert actual_notification.get('type') == 'achievement'

def test_leave_request_notification():
    notification_leave_request(user_id0, user_id1, pid_expected)

    doc_data = db.collection('notifications').document(user_id0).get().to_dict()
    actual_notification = doc_data.get('leave_request0')

    assert actual_notification.get('has_read') == False
    assert actual_notification.get('notification_msg') == "Jane Doe has requested to leave Project Notification !!! NOTIFICATION TEST."
    assert actual_notification.get('pid') == pid_expected
    assert isinstance(actual_notification.get('time_sent'), datetime)
    assert actual_notification.get('type') == 'leave_request'
    assert actual_notification.get('uid_sender') == 'NotifyUser1'
    assert actual_notification.get('accept_msg') == "You accepted Jane Doe's project leave."
    assert actual_notification.get('decline_msg') == "You declined Jane Doe's project leave."
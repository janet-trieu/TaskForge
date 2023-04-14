import pytest

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth

from src.profile_page import *
from src.notifications import *
from src.proj_master import *
from src.global_counters import *
from src.projects import *
from src.taskboard import *

from src.test_helpers import *

# ============ SET UP ============ #
db = firestore.client()

# Create users #
try:
    user_id0 = create_user_email("notificationtest0@gmail.com", "password123", "John Doe")
    user_id1 = create_user_email("notificationtest1@gmail.com", "password123", "Jane Doe")
except auth.EmailAlreadyExistsError:
    pass

user_id0 = auth.get_user_by_email("notificationtest0@gmail.com").uid
user_id1 = auth.get_user_by_email("notificationtest1@gmail.com").uid

# Connect users #
try:
    nid1 = notification_connection_request("notificationtest1@gmail.com", user_id0)
    connection_request_respond(user_id1, nid1, True)
except AccessError:
    pass

# Create project #
try:
    pid = create_project(user_id0, "Project Notification", "Description", None, None, None)
    invite_to_project(pid, user_id0, [user_id1])
except:
    pid = get_pid('Project Notification')
    pass

# ============ TESTS ============ #
# SPRINT 1 #
def test_sorted_notifications():
    '''
    Test to ensure get_notifications() returns notifications in descending time order
    '''
    sorted_notifications = get_notifications(user_id0)

    # Assert the current notification timestamp is greater or equal to the next sorted notification
    for i in range(len(sorted_notifications) - 1):
        assert sorted_notifications[i]['time_sent'] >= sorted_notifications[i+1]['time_sent']

def test_welcome_notification():
    '''
    Test to ensure create_user_email() adds a welcome notification in the database
    '''
    doc_data = db.collection('notifications').document(user_id0).get().to_dict()
    actual_notification = doc_data.get('welcome')

    assert actual_notification.get('has_read') == False
    assert actual_notification.get('notification_msg') == "Welcome to TaskForge, John Doe. You can view future notifications here!"
    
def test_project_invite_notification():
    '''
    Test to ensure invite_to_project() adds invite notifications in the database
    '''

    # Assert user 1 has invite notification data #
    doc_data = db.collection('notifications').document(user_id1).get().to_dict()
    actual_notification = doc_data.get('project_invite0')

    assert actual_notification.get('notification_msg') == "John Doe has invited you to join Project Notification."
    assert actual_notification.get('pid') == pid
    assert actual_notification.get('type') == 'project_invite'
    assert actual_notification.get('uid_sender') == user_id0
    assert actual_notification.get('nid') == 'project_invite0'

# SPRINT 2 #
def test_comment_notification():
    try:
        respond_project_invitation(pid, user_id1, True)
    except:
        pass

    tid = create_task(user_id0, pid, None, [user_id0], "Comment Notify Test", "Description", "1679749200", None, None, "Not Started")
    comment_task(user_id1, tid, "Comment Notification")
    nid = 'comment0'

    # Assert user 0 has comment notification data
    doc_data = db.collection('notifications').document(user_id0).get().to_dict()
    actual_notification = doc_data.get(nid)

    assert actual_notification.get('has_read') == False
    assert actual_notification.get('notification_msg') == "Jane Doe has commented in Comment Notify Test in Project Notification."
    assert actual_notification.get('pid') == pid
    assert actual_notification.get('tid') == tid
    assert actual_notification.get('type') == 'comment'
    assert actual_notification.get('uid_sender') == user_id1
    assert actual_notification.get('nid') == nid

def test_assigned_task_notification():
    try:
        respond_project_invitation(pid, user_id1, True)
    except:
        pass

    tid = create_task(user_id0, pid, None, [user_id0], "Assign Notify Test", "Description", "1679749200", None, None, "Not Started")
    assign_task(user_id0, tid, [user_id1])
    nid = 'assigned_task0'
    
    # Assert user 1 has comment notification data
    doc_data = db.collection('notifications').document(user_id1).get().to_dict()
    actual_notification = doc_data.get(nid)

    assert actual_notification.get('has_read') == False
    assert actual_notification.get('notification_msg') == "You have been assigned Assign Notify Test in Project Notification."
    assert actual_notification.get('pid') == pid
    assert actual_notification.get('tid') == tid
    assert actual_notification.get('type') == 'assigned_task'
    assert actual_notification.get('nid') == nid

def test_leave_request_notification():
    try:
        respond_project_invitation(pid, user_id1, True)
    except:
        pass

    request_leave_project(pid, user_id1, "Testing purposes :]")
    nid = 'leave_request0'

    # Assert user 1 has comment notification data
    doc_data = db.collection('notifications').document(user_id0).get().to_dict()
    actual_notification = doc_data.get(nid)

    assert actual_notification.get('has_read') == False
    assert actual_notification.get('notification_msg') == "Jane Doe has requested to leave Project Notification."
    assert actual_notification.get('pid') == pid
    assert actual_notification.get('type') == 'leave_request'
    assert actual_notification.get('uid_sender') == user_id1
    assert actual_notification.get('nid') == nid

# SPRINT 3 #
def test_review_notification():
    pass

def test_achievement_notification():
    pass
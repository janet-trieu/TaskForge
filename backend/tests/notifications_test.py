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
reset_database() # Ensure database is clear for testing

try:
    create_user_email("notificationtest0@gmail.com", "password123", "John Doe")
    create_user_email("notificationtest1@gmail.com", "password123", "Jane Doe")
    create_user_email("notificationtest2@gmail.com", "password123", "Richard Roe")
except auth.EmailAlreadyExistsError:
    pass

user_id0 = auth.get_user_by_email("notificationtest0@gmail.com").uid
user_id1 = auth.get_user_by_email("notificationtest1@gmail.com").uid
user_id2 = auth.get_user_by_email("notificationtest2@gmail.com").uid

pid_expected = create_project(user_id0, "Project N", "Description", None, None, None)

# ============ HELPERS ============ #
def remove_test_data():
    # Reset database, call at bottom of last test
    delete_user(user_id0)
    delete_user(user_id1)
    delete_user(user_id2)
    reset_database()

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
    remove_test_data()
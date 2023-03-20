import pytest
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from src.connections import connection_request_respond, get_connection_requests, get_connected_taskmasters
from src.error import *
from src.helper import *
from src.profile_page import *
from src.notifications import *
from src.global_counters import *
from src.test_helpers import delete_user, reset_database

try:
    uid1 = create_user_email("conn1@gmail.com", "conn112312321", "conn1123123")
    uid2 = create_user_email("conn2@gmail.com", "conn241241241", "conn2123123132")
    uid3 = create_user_email("conn3@gmail.com", "conn241241212341", "conn2123123131232")
except auth.EmailAlreadyExistsError:
    pass

uid1 = auth.get_user_by_email("conn1@gmail.com").uid
uid2 = auth.get_user_by_email("conn2@gmail.com").uid
uid3 = auth.get_user_by_email("conn3@gmail.com").uid




def test_uid_type_connection_request_respond():
    try:
        connection_request_respond(1, 2, True)
    except InputError:
        pass
        

#uid1 sending a request to uid2
def test_success_connection_request_respond_deny():
    assert(not is_connected(uid1, uid2))
    assert(not is_connected(uid2, uid1))
    nid = notification_connection_request(uid2, uid1)

    connection_request_respond(uid2, nid, False)
    assert(not is_connected(uid1, uid2))
    assert(not is_connected(uid2, uid1))

#uid1 sending a request to uid2
def test_success_connection_request_respond_accept():
    assert(not is_connected(uid1, uid2))
    assert(not is_connected(uid2, uid1))
    nid = notification_connection_request(uid2, uid1)

    connection_request_respond(uid2, nid, True)
    assert(is_connected(uid1, uid2))
    assert(is_connected(uid2, uid1))
    

def test_uid_type_get_connection_requests():
    try:
        get_connection_requests(1)
    except InputError:
        pass

def test_get_connection_requests():
    notification_connection_request(uid3, uid1)
    notification_connection_request(uid3, uid2)
    
    result = get_connection_requests(uid3)
    assert(len(result) == 2)
    assert(result[0].get('type') == 'connection_request')
    assert(result[0].get('uid_sender') == uid1)
    assert(result[1].get('type') == 'connection_request')
    assert(result[1].get('uid_sender') == uid2)


def test_uid_type_get_connected_taskmasters():
    try:
        get_connected_taskmasters(1)
    except InputError:
        pass
        
def test_get_connected_taskmasters():
    notification_connection_request(uid3, uid1)
    notification_connection_request(uid3, uid2)
    connection_request_respond(uid3, 'connection_request0', True)
    connection_request_respond(uid3, 'connection_request1', True)
    
    result = get_connected_taskmasters(uid3)
    assert(len(result) == 2)
    assert(uid1 in result)
    assert(uid2 in result)
    
def test_clean_up():
    try:
        delete_user(uid1)
        delete_user(uid2)
        delete_user(uid3)
    except:
        pass

@pytest.mark.run_last
def test_reset_database():
    reset_database()
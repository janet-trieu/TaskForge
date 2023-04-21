'''
Unit test file for Connections feature
'''

from src.connections import *
from src.error import *
from src.helper import *
from src.profile_page import *
from src.notifications import *
from src.global_counters import *
from src.test_helpers import *

# test set up
try:
    uid1 = create_user_email("conn1@gmail.com", "conn112312321", "conn1123123")
    uid2 = create_user_email("conn2@gmail.com", "conn241241241", "conn2123123132")
    uid3 = create_user_email("conn3@gmail.com", "conn241241212341", "conn2123123131232")
    uid4 = create_user_email("conn4@gmail.com", "con42312321", "co4123123")
    uid5 = create_user_email("conn5@gmail.com", "con52312321", "co5123123")
except auth.EmailAlreadyExistsError:
    pass

uid1 = auth.get_user_by_email("conn1@gmail.com").uid
uid2 = auth.get_user_by_email("conn2@gmail.com").uid
uid3 = auth.get_user_by_email("conn3@gmail.com").uid
uid4 = auth.get_user_by_email("conn4@gmail.com").uid
uid5 = auth.get_user_by_email("conn5@gmail.com").uid

# main tests

def test_uid_type_connection_request_respond():
    try:
        connection_request_respond(1, 2, True)
    except InputError:
        pass
        
#uid1 sending a request to uid2
def test_success_connection_request_respond_deny():
    assert(not is_connected(uid1, uid2))
    assert(not is_connected(uid2, uid1))
    user2_email = get_email(uid2)
    nid = notification_connection_request(user2_email, uid1)

    connection_request_respond(uid2, nid, False)
    assert(not is_connected(uid1, uid2))
    assert(not is_connected(uid2, uid1))

#uid1 sending a request to uid2
def test_success_connection_request_respond_accept():
    assert(not is_connected(uid1, uid2))
    assert(not is_connected(uid2, uid1))
    user2_email = get_email(uid2)
    nid = notification_connection_request(user2_email, uid1)

    connection_request_respond(uid2, nid, True)
    assert(is_connected(uid1, uid2))
    assert(is_connected(uid2, uid1))

def test_uid_type_get_connection_requests():
    try:
        get_connection_requests(1)
    except InputError:
        pass

def test_get_connection_requests():
    user3_email = get_email(uid3)
    notification_connection_request(user3_email, uid1)
    notification_connection_request(user3_email, uid2)
    
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
    user3_email = get_email(uid3)
    notification_connection_request(user3_email, uid1)
    notification_connection_request(user3_email, uid2)
    connection_request_respond(uid3, 'connection_request0', True)
    connection_request_respond(uid3, 'connection_request1', True)
    
    result = get_connected_taskmasters(uid3)
    assert(len(result) == 2)
    assert(uid1 in result[0].get("uid"))
    assert(uid2 in result[1].get("uid"))
    
def test_remove_connected_taskmaster():
    assert(is_connected(uid1, uid2))
    assert(is_connected(uid2, uid1))
    remove_connected_taskmaster(uid1, uid2)
    assert(not is_connected(uid1, uid2))
    assert(not is_connected(uid2, uid1))
    
#uid1 is connected to uid3 but not uid2
def test_search_taskmaster():
    assert(is_connected(uid1, uid3))
    assert(not is_connected(uid1, uid2))
    result = search_taskmasters(uid1, "conn")
    assert(len(result) == 4)
    assert(result[0]["uid"] == uid3)
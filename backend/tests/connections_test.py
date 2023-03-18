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



@pytest.fixture(name="uids")
def fixture_uid():
    '''
    Create users for data
    '''
    #create_user_email("conn1@gmail.com", "conntest1", "conntest1")
    #create_user_email("conn2@gmail.com", "conntest2", "conntest2")
    #create_user_email("conn3@gmail.com", "conntest3", "conntest3")
    #uid1 = auth.get_user_by_email("conn1@gmail.com").uid
    #uid2 = auth.get_user_by_email("conn2@gmail.com").uid
    #uid3 = auth.get_user_by_email("conn3@gmail.com").uid
    #return [uid1, uid2, uid3]



def test_uid_type_connection_request_respond():
    try:
        connection_request_respond(1, 2, True)
    except InputError:
        pass
        

#uid1 sending a request to uid2
def test_success_connection_request_respond_deny(uids):
    #uid1, uid2, uid3 = uids
    #clear_all_notifications(uid2)
    assert(not is_connected('cvFHViM13NdczRaThWhIGDiqUZO2', 'tdqpOmI5iDaOCkKBWyjNUVWHAID2'))
    assert(not is_connected('tdqpOmI5iDaOCkKBWyjNUVWHAID2', 'cvFHViM13NdczRaThWhIGDiqUZO2'))
    notification_connection_request('tdqpOmI5iDaOCkKBWyjNUVWHAID2', 'cvFHViM13NdczRaThWhIGDiqUZO2')

    connection_request_respond('tdqpOmI5iDaOCkKBWyjNUVWHAID2', 'connection_request0', False)
    assert(not is_connected('cvFHViM13NdczRaThWhIGDiqUZO2', 'tdqpOmI5iDaOCkKBWyjNUVWHAID2'))
    assert(not is_connected('tdqpOmI5iDaOCkKBWyjNUVWHAID2', 'cvFHViM13NdczRaThWhIGDiqUZO2'))

#uid1 sending a request to uid2
def test_success_connection_request_respond_accept(uids):
    #uid1, uid2, uid3 = uids
    #clear_all_notifications(uid2)
    assert(not is_connected('cvFHViM13NdczRaThWhIGDiqUZO2', 'tdqpOmI5iDaOCkKBWyjNUVWHAID2'))
    assert(not is_connected('tdqpOmI5iDaOCkKBWyjNUVWHAID2', 'cvFHViM13NdczRaThWhIGDiqUZO2'))
    notification_connection_request('tdqpOmI5iDaOCkKBWyjNUVWHAID2', 'cvFHViM13NdczRaThWhIGDiqUZO2')

    connection_request_respond('tdqpOmI5iDaOCkKBWyjNUVWHAID2', 'connection_request0', True)
    assert(is_connected('cvFHViM13NdczRaThWhIGDiqUZO2', 'tdqpOmI5iDaOCkKBWyjNUVWHAID2'))
    assert(is_connected('tdqpOmI5iDaOCkKBWyjNUVWHAID2', 'cvFHViM13NdczRaThWhIGDiqUZO2'))
"""

def test_uid_type_get_connection_requests():
    try:
        get_connection_requests(1)
    except InputError:
        pass

def test_get_connection_requests(uids):
    uid1, uid2, uid3 = uids
    #clear_all_notifications(uid3)
    notification_connection_request(uid3, uid1)
    notification_connection_request(uid3, uid2)
    
    result = get_connection_requests(uid3)
    assert(result.len() == 2)
    assert(result[0].get('notification_type') == 'connection_request')
    assert(result[0].get('uid_sender') == uid1)
    assert(result[1].get('notification_type') == 'connection_request')
    assert(result[1].get('uid_sender') == uid2)


def test_uid_type_get_connected_taskmasters():
    try:
        get_connected_taskmasters(1)
    except InputError:
        pass
        
def test_get_connected_taskmasters(uids):
    uid1, uid2, uid3 = uids
    #clear_all_notifications(uid3)
    notification_connection_request(uid3, uid1)
    notification_connection_request(uid3, uid2)
    connection_request_respond(uid3, 'connection_request0', True)
    connection_request_respond(uid3, 'connection_request1', True)
    
    result = get_connected_taskmasters(uid3)
    assert(result.len() == 2)
    assert(uid1 in result)
    assert(uid2 in result)
    
"""
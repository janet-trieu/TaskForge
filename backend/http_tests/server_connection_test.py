'''
Test file for Flask http testing of connection management
'''
import pytest
import requests
from src.test_helpers import *
from src.helper import *
from src.profile_page import *

port = 8000
url = f"http://localhost:{port}/"

try:
    uid1 = create_user_email("conn1@gmail.com", "conn112312321", "conn1123123")
    uid2 = create_user_email("conn2@gmail.com", "conn241241241", "conn2123123132")
    uid3 = create_user_email("conn3@gmail.com", "conn241241212341", "conn2123123131232")
except auth.EmailAlreadyExistsError:
    pass

uid1 = auth.get_user_by_email("conn1@gmail.com").uid
uid2 = auth.get_user_by_email("conn2@gmail.com").uid
uid3 = auth.get_user_by_email("conn3@gmail.com").uid

def test_connection_request_respond_failure():
    """
    Giving an int instead of a string
    """
    json_dict = {'uid': uid2, 'uid_sender': uid1}
    resp = requests.post(url + '/notification/connection/request', json=json_dict)
    
    assert resp.status_code == 200
    
    json_dict = {'uid': 1, 'nid': 2, 'response' : 1}
    resp = requests.post(url + '/connections/request_respond', json=json_dict)

    assert resp.status_code == 400
    

def test_connection_request_respond_decline_success():
    """
    Successfully declining a connection request
    """
    headers_dict = {'Authorization': uid2}
    json_dict = {'uid': uid2, 'uid_sender': uid1}
    resp = requests.post(url + '/notification/connection/request', headers=headers_dict, json=json_dict)
    
    assert resp.status_code == 200
    nid = resp.json()
    
    json_dict = {'uid': uid2, 'nid': nid, 'response' : False}
    resp = requests.post(url + '/connections/request_respond', headers=headers_dict, json=json_dict)

    assert resp.status_code == 200

def test_connection_request_respond_accept_success():
    """
    Successfully accepting a connection request
    """
    headers_dict = {'Authorization': uid2}
    json_dict = {'uid': uid2, 'uid_sender': uid1}
    resp = requests.post(url + '/notification/connection/request', headers=headers_dict, json=json_dict)
    
    assert resp.status_code == 200
    nid = resp.json()
    
    json_dict = {'uid': uid2, 'nid': nid, 'response' : True}
    resp = requests.post(url + '/connections/request_respond', headers=headers_dict, json=json_dict)

    assert resp.status_code == 200

def test_get_connection_requests_failure():
    """
    Giving an int instead of a string
    """
    headers_dict = {'Authorization': uid3}
    json_dict = {'uid': uid3, 'uid_sender': uid1}
    resp = requests.post(url + '/notification/connection/request', headers=headers_dict, json=json_dict)
    
    assert resp.status_code == 200
    json_dict = {'uid': 1}
    resp = requests.post(url + '/connections/get_connection_requests', json=json_dict)

    assert resp.status_code == 400

def test_get_connection_requests_success():
    """
    Successfully getting a connection request list
    """
    headers_dict = {'Authorization': uid3}
    json_dict = {'uid': uid3, 'uid_sender': uid1}
    resp = requests.post(url + '/notification/connection/request', headers=headers_dict, json=json_dict)
    
    assert resp.status_code == 200
    
    resp = requests.post(url + '/connections/get_connection_requests', headers=headers_dict)

    assert resp.status_code == 200

def test_connected_taskmasters_failure():
    """
    Giving an int instead of a string
    """
    json_dict = {'uid': 1}
    resp = requests.post(url + '/connections/get_connected_taskmasters', json=json_dict)

    assert resp.status_code == 400

def test_connected_taskmasters_success():
    """
    Successfully getting a connected tm list
    """
    headers_dict = {'Authorization': uid3}
    json_dict = {'uid': uid3, 'uid_sender': uid2}
    resp = requests.post(url + '/notification/connection/request', headers=headers_dict, json=json_dict)
    
    assert resp.status_code == 200
    nid = resp.json()
    
    json_dict = {'uid': uid3, 'nid': nid, 'response' : True}
    resp = requests.post(url + '/connections/request_respond', headers=headers_dict, json=json_dict)

    assert resp.status_code == 200
    
    json_dict = {'uid': uid3}
    resp = requests.post(url + '/connections/get_connected_taskmasters', headers=headers_dict, json=json_dict)
    
    assert resp.status_code == 200

def test_clean_up():
    try:
        delete_user(uid1)
        delete_user(uid2)
        delete_user(uid3)
    except:
        pass
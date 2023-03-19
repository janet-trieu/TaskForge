import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests

from src.profile_page import *
from src.helper import *
 
url = 'http://127.0.0.1:5000'

try:
    admin_uid = create_user_email("admin@gmail.com", "admin123", "Admin Admin")
    user_uid = create_user_email("admintest.tm1@gmail.com", "taskmaster1", "Task Master1")
    create_admin(admin_uid)
except:
    print("admin and user already created")
else:
    admin_uid = auth.get_user_by_email("admin@gmail.com").uid
    user_uid = auth.get_user_by_email("admintest.tm1@gmail.com").uid

def test_give_admin_success():
    """
    Successfully giving admin to another user
    """
    headers_dict = {'Authorization': user_uid}
    json_dict = {'uid_admin': admin_uid}
    resp = requests.post(url + '/admin/give_admin', headers=headers_dict, json=json_dict)

    assert resp.status_code == 200

def test_give_admin_failure():
    """
    Giving an int instead of a string
    """
    headers_dict = {'Authorization': 'aye'}
    json_dict = {'uid_admin': 'hi'}
    resp = requests.post(url + '/admin/give_admin', headers=headers_dict, json=json_dict)

    assert resp.status_code == 400

def test_ban_user_success():
    """
    Successfully banning user by an admin
    """
    headers_dict = {'Authorization': user_uid}
    json_dict = {'uid_admin': admin_uid}
    resp = requests.post(url + '/admin/ban_user', headers=headers_dict, json=json_dict)

    assert resp.status_code == 200
    
def test_ban_user_failure():
    """
    Giving an int instead of a string
    """
    headers_dict = {'Authorization': '1'}
    json_dict = {'uid_admin': 0}
    resp = requests.post(url + '/admin/ban_user', headers=headers_dict, json=json_dict)

    assert resp.status_code == 400
    
def test_unban_user_success():
    """
    Successfully unbanning user by an admin
    """
    headers_dict = {'Authorization': user_uid}
    json_dict = {'uid_admin': admin_uid}
    resp = requests.post(url + '/admin/unban_user', headers=headers_dict, json=json_dict)

    assert resp.status_code == 200
    
def test_unban_user_failure():
    """
    Giving an int instead of a string
    """
    headers_dict = {'Authorization': '1'}
    json_dict = {'uid_admin': 0}
    resp = requests.post(url + '/admin/unban_user', headers=headers_dict, json=json_dict)

    assert resp.status_code == 400

def test_remove_user_success():
    """
    Successfully removing user by an admin
    """
    headers_dict = {'Authorization': user_uid}
    json_dict = {'uid_admin': admin_uid}
    resp = requests.post(url + '/admin/remove_user', headers=headers_dict, json=json_dict)

    assert resp.status_code == 200
   
def test_remove_user_failure():
    """
    Giving an int instead of a string
    """
    headers_dict = {'Authorization': '1'}
    json_dict = {'uid_admin': 0}
    resp = requests.post(url + '/admin/remove_user', headers=headers_dict, json=json_dict)

    assert resp.status_code == 400
   
def test_readd_user_success():
    """
    Successfully readding user by an admin
    """
    headers_dict = {'Authorization': user_uid}
    json_dict = {'uid_admin': admin_uid}
    resp = requests.post(url + '/admin/readd_user', headers=headers_dict, json=json_dict)

    assert resp.status_code == 200
    
def test_readd_user_failure():
    """
    Giving an int instead of a string
    """
    headers_dict = {'Authorization': '1'}
    json_dict = {'uid_admin': 0}
    resp = requests.post(url + '/admin/readd_user', headers=headers_dict, json=json_dict)

    assert resp.status_code == 400
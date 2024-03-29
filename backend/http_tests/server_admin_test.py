'''
Test file for Flask http testing of admin
'''

import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests

from src.profile_page import *
from src.helper import *
from src.test_helpers import reset_database

# test set up
port = 8000
url = f'http://127.0.0.1/%7Bport%7D'

try:
    admin_uid = create_user_email("admin@gmail.com", "admin123", "Admin Admin")
    user_uid = create_user_email("admintest.tm1@gmail.com", "taskmaster1", "Task Master1")
    create_admin(admin_uid)
except:
    print("admin and user already created")
else:
    admin_uid = auth.get_user_by_email("admin@gmail.com").uid
    user_uid = auth.get_user_by_email("admintest.tm1@gmail.com").uid

# main tests

def test_give_admin_success():
    """
    Successfully giving admin to another user
    """
    headers_dict = {'Authorization': admin_uid}
    json_dict = {'uid_user': get_email(user_uid)}
    resp = requests.post(url + '/admin/give_admin', headers=headers_dict, json=json_dict)

    assert resp.status_code == 200

def test_ban_user_success():
    """
    Successfully banning user by an admin
    """
    headers_dict = {'Authorization': admin_uid}
    json_dict = {'uid_user': get_email(user_uid)}
    resp = requests.post(url + '/admin/ban_user', headers=headers_dict, json=json_dict)

    assert resp.status_code == 200

def test_unban_user_success():
    """
    Successfully unbanning user by an admin
    """
    headers_dict = {'Authorization': admin_uid}
    json_dict = {'uid_user': get_email(user_uid)}
    resp = requests.post(url + '/admin/unban_user', headers=headers_dict, json=json_dict)

    assert resp.status_code == 200

def test_remove_user_success():
    """
    Successfully removing user by an admin
    """
    headers_dict = {'Authorization': admin_uid}
    json_dict = {'uid_user': get_email(user_uid)}
    resp = requests.post(url + '/admin/remove_user', headers=headers_dict, json=json_dict)

    assert resp.status_code == 200
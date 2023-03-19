import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
from src.authentication import *
from src.test_helpers import *
 
url = 'http://127.0.0.1:5000'

try:
    create_user_email("profiletest0@gmail.com", "password123", "Profile Doe")
except auth.EmailAlreadyExistsError:
    pass

user_id = auth.get_user_by_email("profiletest0@gmail.com").uid

def test_user_details_success():
    """
    Successfully accessing a user's details
    """
    json_dict = {'Authorization': user_id}
    resp = requests.get(url + '/profile/details', headers=json_dict)

    assert resp.status_code == 200

def test_user_details_failure():
    """
    Failing to access a user's details as they do not exist
    """
    json_dict = {'Authorization': user_id}
    resp = requests.get(url + '/profile/details', headers=json_dict)

    assert resp.status_code == 400


def test_update_profile_success():
    """
    Succeeding to update a user's details
    """
    headers_dict = {'Authorization': user_id}
    json_dict = {'email': 'ilovedabin@gmail.com', 'role': "duck engineer", 'photo_url': "https://t0.gstatic.com/licensed-image?q=tbn:ANd9GcSoPravXdZRihoO83Kd7TwlZBik03ZXlDZvBYx5ZyotO_RWKE7d_G_nFxBTjPE1yTILP7qUl2Q_rtbLUsk"}
    resp = requests.put(url + '/profile/update', headers=headers_dict, json=json_dict)

    assert resp.status_code == 200

def test_update_profile_failure():
    """
    Failing to  update a user's details with an invalid email
    However, should still update rest of the details
    """
    headers_dict = {'Authorization': user_id}
    json_dict = {'email': 'ilovedabin', 'role': "balls engineer", 'photo_url': ""}
    resp = requests.put(url + '/profile/update', headers=headers_dict, json=json_dict)

    assert resp.status_code == 200

def test_get_tasks_success():
    """
    Succeeding in getting a user's tasks
    """
    json_dict = {'Authorization': user_id}
    resp = requests.get(url + '/profile/tasks', headers=json_dict)

    assert resp.status_code == 200

def test_get_tasks_success():
    """
    Failing in getting a user's tasks
    """
    json_dict = {'Authorization': user_id}
    resp = requests.get(url + '/profile/tasks', headers=json_dict)

    assert resp.status_code == 400

# Reset database
delete_user(user_id)
reset_database()
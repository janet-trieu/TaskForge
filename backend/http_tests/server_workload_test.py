'''
Test file for Flask http testing of workload + supply and demand
'''
import requests
from src.taskboard import create_task
from src.proj_master import create_project
from src.test_helpers import *
from src.helper import *
from src.profile_page import *
from datetime import datetime, timedelta

port = 8000
url = f"http://localhost:{port}/"

try:
    uid = create_user_email("workload@gmail.com", "workload112312321", "workload1123123")
except auth.EmailAlreadyExistsError:
    pass

uid = auth.get_user_by_email("workload@gmail.com").uid
pid = create_project(uid, "Project 123", "description", None, None, None)
tid = create_task(uid, pid, None, [get_email(uid)], "", "", datetime.now() + timedelta(minutes=100), 2, "Low", "In Progress")

def test_get_user_workload():
    headers_dict = {'Authorization': uid}
    resp = requests.get(url + '/workload/get_user_workload', headers=headers_dict)

    assert resp.status_code == 200
    
def test_update_user_availability():
    headers_dict = {'Authorization': uid}
    json_dict = {'availability' : 4}
    resp = requests.post(url + '/workload/update_user_availability', headers=headers_dict, json=json_dict)
    assert resp.status_code == 200
    
def test_workload_get_availability():
    headers_dict = {'Authorization': uid}
    resp = requests.get(url + '/workload/get_availability', headers=headers_dict)
    assert resp.status_code == 200
    
def test_workload_get_availability_ratio():
    headers_dict = {'Authorization': uid}
    resp = requests.get(url + '/workload/get_availability_ratio', headers=headers_dict)
    assert resp.status_code == 200
    
def test_workload_calculate_supply_demand():
    headers_dict = {'Authorization': uid}
    resp = requests.get(url + '/workload/calculate_supply_demand', headers=headers_dict)
    assert resp.status_code == 200
    
def test_workload_get_supply_demand():
    headers_dict = {'Authorization': uid}
    resp = requests.get(url + '/workload/get_supply_demand', headers=headers_dict)
    assert resp.status_code == 200

def test_reset():
    reset_database()
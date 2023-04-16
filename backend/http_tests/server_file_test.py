import pytest
import requests
from src.test_helpers import *
from src.helper import *
from src.profile_page import *
from src.notifications import *
from src.connections import *
from src.proj_master import *
from src.taskboard import *


port = 8000
url = f"http://localhost:{port}/"

try:
    uid = create_user_email("file1@gmail.com", "123124515151", "FILEMAN123321")
except auth.EmailAlreadyExistsError:
    pass
uid = auth.get_user_by_email("file1@gmail.com").uid
pid = create_project(uid, "Project 123", "description", None, None, None)
eid = create_epic(uid, pid, 'title', 'desc', '#fcba03')
tid = create_task(uid, pid, eid, [], 'title', 'descr', 0, 0, "", "Not Started")

def test_file_upload():
    header = {'Authorization': uid}
    file = {'file': open('http_tests/test.jpg', 'rb')}
    resp = requests.post(url + "/upload_file1", headers=header, files=file)
    assert(resp.status_code == 200)
    
    json_dict = {'file':'http_tests/test.jpg', 'destination_name': 'test.jpg', 'tid':tid}
    resp = requests.post(url + "/upload_file2", headers=header, json=json_dict)
    assert(resp.status_code == 200)
    
def test_get_file_link():
    header = {'Authorization': uid}
    
    json_dict = {'fileName': '20/test.jpg'}
    resp = requests.get(url + "get_file_link", headers=header, json=json_dict)
    
    assert(resp.status_code == 200)
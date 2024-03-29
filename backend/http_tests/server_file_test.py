'''
Test file for Flask http testing of connection management
'''

import pytest
import requests

from src.test_helpers import *
from src.helper import *
from src.profile_page import *
from src.notifications import *
from src.connections import *
from src.projmaster import *
from src.tasks import *

# test set up
port = 8000
url = f"http://localhost:{port}/"

try:
    uid = create_user_email("file1@gmail.com", "file123541521541", "file12325452151")
except auth.EmailAlreadyExistsError:
    pass

uid = auth.get_user_by_email("file1@gmail.com").uid
pid = create_project(uid, "file1proj 123", "file1", None, None)
tid = create_task(uid, pid, None, [uid], 'file1', 'file1', 0, 0, "", "Not Started")

# main tests 

def test_file_upload():
    header = {'Authorization': uid}
    file = {'file': open('test.jpg', 'rb')}
    resp = requests.post(url + "/upload_file1", headers=header, files=file)
    assert(resp.status_code == 200)
    
    json_dict = {'file':'test.jpg', 'destination_name': 'test.jpg', 'tid':tid}
    resp = requests.post(url + "/upload_file2", headers=header, json=json_dict)
    assert(resp.status_code == 200)
    
def test_get_file_link():
    header = {'Authorization': uid}
    
    params = {'tid': tid, 'fileName': 'test.jpg'}
    resp = requests.get(url + "/get_file_link", headers=header, params=params)
    
    assert(resp.status_code == 200)
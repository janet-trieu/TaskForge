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
    uid = create_user_email("file1@gmail.com", "123124515151", "FILEMAN")
except auth.EmailAlreadyExistsError:
    pass
uid = auth.get_user_by_email("file1@gmail.com").uid


def test_file_upload():
    header = {'Authorization': uid}
    
    pid = create_project(uid, "Project 123", "description", None, None, None)
    eid = create_epic(uid, pid, 'title', 'desc', '#fcba03')
    tid = create_task(uid, pid, eid, [], 'title', 'descr', 0, 0, "", "Not Started")
    
    header = {'Authorization': uid}
    params = {'file': 'http_tests/test.jpg', 'destination_name': 'test.jpg', 'tid':tid}
    resp = requests.get(url + "upload_file", headers=header, params=params)
    assert(resp.status_code == 200)
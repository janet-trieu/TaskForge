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
    
    params = {'title': 'proj', 'description': 'desc'}
    resp = requests.get(url + "projects/create", headers=header, params=params)
    pid = resp.json()
    
    params = {'pid': pid, 'title':'tit', 'description': 'desc', 'color': '#fcba03'}
    resp = requests.get(url + "epic/create", headers=header, params=params)
    eid = resp.json()
    
    params = {'pid': pid, 'eid':eid, 'title':'tit', 'description': 'desc'}
    resp = requests.get(url + "task/create", headers=header, params=params)
    tid = resp.json()
    
    
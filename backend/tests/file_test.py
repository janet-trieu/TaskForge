import pytest
import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin import firestore

# from src.profile_page import *
from src.admin import *
from src.error import *
from src.helper import *
from src.proj_master import *
from src.taskboard import *


try:
    uid = create_user_email("file1@gmail.com", "FILENIAWFNOI", "filedude")
except:
    pass
else:
    uid = auth.get_user_by_email("file1@gmail.com").uid




def test_file_upload():
    
    pid = create_project(uid, "Project 123", "description", None, None, None)
    eid = create_epic(uid, pid, 'title', 'desc', '#fcba03')
    tid = create_task(uid, pid, eid, [], 'title', 'descr', 0, 0, "", "Not Started")
    
    upload_file(uid, 'tests/test.jpg', 'test.jpg', tid)
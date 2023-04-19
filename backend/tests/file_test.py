import pytest
import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin import firestore

# from src.profile_page import *
from src.admin import *
from src.error import *
from src.helper import *
from src.projmaster import *
from src.taskboard import *


try:
    uid = create_user_email("file1@gmail.com", "FILENIAWFNOI", "filedude")
except auth.EmailAlreadyExistsError:
    pass
uid = auth.get_user_by_email("file1@gmail.com").uid


pid = create_project(uid, "Project 123", "description", None, None)
eid = create_epic(uid, pid, 'title', 'desc', '#fcba03')
tid = create_task(uid, pid, eid, [uid], 'FILE', 'FILE', 0, 0, "", "Not Started")

def test_file_upload(): 
    upload_file(uid, 'tests/test.jpg', 'test.jpg', tid)
    
def test_get_file_link():
    get_file_link(uid, tid, 'test.jpg')
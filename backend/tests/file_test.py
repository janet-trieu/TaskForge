'''
Unit test file for File related functionality for Task Management feature
'''

'''
import pytest
from firebase_admin import auth

from src.admin import *
from src.error import *
from src.helper import *
from src.projmaster import *
from src.tasks import *
from src.epics import *

# test set up
try:
    uid = create_user_email("file1@gmail.com", "FILENIAWFNOI", "filedude")
except auth.EmailAlreadyExistsError:
    pass
uid = auth.get_user_by_email("file1@gmail.com").uid

pid = create_project(uid, "Project 123", "description", None, None, None)
eid = create_epic(uid, pid, 'title', 'desc', '#fcba03')
tid = create_task(uid, pid, eid, [uid], 'FILE', 'FILE', 0, 0, "", "Not Started")

# main tests

def test_file_upload(): 
    upload_file(uid, 'test.jpg', 'test.jpg', tid)
    
def test_get_file_link():
    get_file_link(uid, tid, 'test.jpg')
'''
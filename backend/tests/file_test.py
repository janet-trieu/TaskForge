'''
Unit test file for File related functionality for Task Management feature
'''
from firebase_admin import auth


from src.profile_page import *
from src.admin import *
from src.error import *
from src.helper import *
from src.projmaster import *
from src.taskboard import *
from src.tasks import *
from src.epics import *


try:
    uid = create_user_email("file21@gmail.com", "FILENIAWFNOI", "filedude")
except auth.EmailAlreadyExistsError:
    pass
uid = auth.get_user_by_email("file21@gmail.com").uid


pid = create_project(uid, "Project 123", "description", None, None)
tid = create_task(uid, pid, None, [], '', '', 0, 0, "", "Not Started")

def test_file_upload(): 
    upload_file(uid, 'test.jpg', 'test.jpg', tid)
    
def test_get_file_link():
    get_file_link(uid, tid, 'test.jpg')
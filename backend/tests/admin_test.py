'''
Unit test file for Admin feature
'''

from firebase_admin import  auth
from src.projmaster import create_project
from src.tasks import create_task
from src.subtasks import create_subtask
from src.test_helpers import reset_database

from src.admin import *
from src.error import *
from src.helper import *

# test set up
try:
    admin_uid = create_user_email("admin21@gmail.com", "admin121233", "Admin Ad123min")

    user_uid = create_user_email("admintest.tm12@gmail.com", "taskmaster1", "Task Master1")
except auth.EmailAlreadyExistsError:
    pass

admin_uid = auth.get_user_by_email("admin21@gmail.com").uid
user_uid = auth.get_user_by_email("admintest.tm12@gmail.com").uid
make_admin(admin_uid)

# main tests

def test_give_admin_type():
    try:
        give_admin(1, 2)
    except InputError:
        pass

def test_give_admin():
    user_ref = db.collection("users").document(user_uid)
    user_ref.update({'is_admin': False})
    
    assert(is_admin(admin_uid))
    assert(not is_admin(user_uid))
    give_admin(admin_uid, user_uid)
    assert(is_admin(user_uid))

def test_give_admin_to_admin():
    assert(is_admin(admin_uid))
    assert(is_admin(user_uid))
    try:
        give_admin(admin_uid, user_uid)
    except InputError:
        pass
    assert(is_admin(user_uid))

def test_ban_user_type():
    try:
        ban_user(1, 2)
    except InputError:
        pass

def test_ban_user():
    assert(is_admin(admin_uid))
    assert(not is_banned(user_uid))
    
    ban_user(admin_uid, user_uid)
    assert(is_banned(user_uid))

def test_ban_banned_user():
    assert(is_admin(admin_uid))
    assert(is_banned(user_uid))
    
    try:
        ban_user(admin_uid, user_uid)
    except InputError:
        pass
    assert(is_banned(user_uid))

def test_unban_user_type():
    try:
        unban_user(1, 2)
    except InputError:
        pass

#user is still banned from last test
def test_unban_user():
    assert(is_admin(admin_uid))
    assert(is_banned(user_uid))
    
    unban_user(admin_uid, user_uid)
    assert(not is_banned(user_uid))

def test_unban_notbanned_user():
    assert(is_admin(admin_uid))
    assert(not is_banned(user_uid))
    
    try:
        unban_user(admin_uid, user_uid)
    except InputError:
        pass
    assert(not is_banned(admin_uid))

def test_remove_usertype():
    try:
        remove_user(1, 2)
    except InputError:
        pass

def test_remove_user():
    assert(is_admin(admin_uid))
    pid = create_project(user_uid, "Project 123", "description", None, None)
    tid = create_task(user_uid, pid, None, [get_email(user_uid)], "", "", 0, 0, "Low", "Not Started")
    stid = create_subtask(user_uid, tid, pid, [user_uid], "", "", 0, 0, "Low", "Not Started")
    remove_user(admin_uid, user_uid)
    try:
        check_valid_uid(user_uid)
    except InputError:
        pass
    
    try:
        check_user_in_project(user_uid, pid)
    except InputError:
        pass

    try:
        check_user_in_task(user_uid, tid)
    except InputError:
        pass
    
    try:
        check_user_in_subtask(user_uid, tid, stid)
    except InputError:
        pass

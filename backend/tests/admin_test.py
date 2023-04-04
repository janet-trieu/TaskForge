import pytest
import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin import firestore
from src.proj_master import create_project

# from src.profile_page import *
from src.admin import *
from src.error import *
from src.helper import *

try:
    admin_uid = create_user_email("admin1@gmail.com", "admin121233", "Admin Ad123min")
    user_uid = create_user_email("admintest.tm1@gmail.com", "taskmaster1", "Task Master1")
    create_admin(admin_uid)
except:
    print("admin and user already created")
else:
    admin_uid = auth.get_user_by_email("admin1@gmail.com").uid
    user_uid = auth.get_user_by_email("admintest.tm1@gmail.com").uid

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

#@pytest.mark.order4
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
#@pytest.mark.order5
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
    create_project(user_uid, "Project 123", "description", None, None, None)
    remove_user(admin_uid, user_uid)
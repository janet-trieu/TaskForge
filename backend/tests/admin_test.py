import firebase_admin
from firebase_admin import auth
from src.admin import *
from src.helper import *



def test_give_admin():
    
    admin = get_user_by_uid('compgpt3900@gmail.com')
    user = get_user_by_uid(uid_user)
    assert(admin.is_admin)
    assert(not user.is_admin)
    
    result = give_admin(uid_admin, uid_user)
    assert(result == 0)
    assert(user.is_admin)
    
def test_give_admin_to_admin(uid_admin, uid_user):
    pass
    
def test_ban_user(uid_admin, uid_user):
    pass
    
def test_ban_banned_user(uid_admin, uid_user):
    pass
    
def test_unban_user(uid_admin, uid_user):
    pass
    
def test_unban_notbanned_user(uid_admin, uid_user):
    pass
    
def test_remove_user(uid_admin, uid_user):
    pass
    
def test_remove_removed_user(uid_admin, uid_user):
    pass
    
def test_readd_removed_user(uid_admin, uid_user):
    pass

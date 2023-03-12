import pytest
import firebase_admin
from firebase_admin import auth
from src.admin import *
from src.helper import *

#Assuming that 2 users already exist, the first one is root admin and 2nd one is just a normal user
#each test should somewhat reset for the next test
@pytest.mark.order1
def test_give_admin():
    admin = get_user_by_email('compgpt3900@gmail.com')
    user = get_user_by_uid(1)
    assert(admin.get('is_admin'))
    assert(not user.get('is_admin'))
    
    give_admin(admin.get('uid'), user.get('uid'))
    assert(user.is_admin)

@pytest.mark.order2
def test_give_admin_to_admin():
    admin = get_user_by_email('compgpt3900@gmail.com')
    assert(admin.get('is_admin'))
    
    give_admin(admin.get('uid'), admin.get('uid'))
    assert(admin.is_admin)

@pytest.mark.order3
def test_ban_user():
    admin = get_user_by_email('compgpt3900@gmail.com')
    user = get_user_by_uid(1)
    assert(admin.get('is_admin'))
    assert(not user.get('is_banned'))
    
    ban_user(admin.get('uid'), user.get('uid'))
    assert(user.is_banned)

@pytest.mark.order4
def test_ban_banned_user():
    admin = get_user_by_email('compgpt3900@gmail.com')
    user = get_user_by_uid(1)
    assert(admin.get('is_admin'))
    
    ban_user(admin.get('uid'), user.get('uid'))
    assert(user.is_banned)
    
    ban_user(admin.get('uid'), user.get('uid'))
    assert(user.is_banned)


#user is still banned from last test
@pytest.mark.order5
def test_unban_user():
    admin = get_user_by_email('compgpt3900@gmail.com')
    user = get_user_by_uid(1)
    assert(admin.get('is_admin'))
    assert(user.get('is_banned'))
    
    unban_user(admin.get('uid'), user.get('uid'))
    assert(not user.is_banned)

@pytest.mark.order6
def test_unban_notbanned_user():
    admin = get_user_by_email('compgpt3900@gmail.com')
    user = get_user_by_uid(1)
    assert(admin.get('is_admin'))
    assert(not user.get('is_banned'))
    
    unban_user(admin.get('uid'), user.get('uid'))
    assert(not user.is_banned)

@pytest.mark.order7
def test_remove_user():
    admin = get_user_by_email('compgpt3900@gmail.com')
    user = get_user_by_uid(1)
    assert(admin.get('is_admin'))
    assert(not user.get('is_removed'))
    
    remove_user(admin.get('uid'), user.get('uid'))
    assert(user.is_removed)


#user still removed
@pytest.mark.order8
def test_remove_removed_user():
    admin = get_user_by_email('compgpt3900@gmail.com')
    user = get_user_by_uid(1)
    assert(admin.get('is_admin'))
    assert(user.get('is_removed'))
    
    remove_user(admin.get('uid'), user.get('uid'))
    assert(user.is_removed)
    
    remove_user(admin.get('uid'), user.get('uid'))
    assert(user.is_removed)
   
@pytest.mark.order9
def test_readd_removed_user():
    admin = get_user_by_email('compgpt3900@gmail.com')
    user = get_user_by_uid(1)
    assert(admin.get('is_admin'))
    assert(user.get('is_removed'))
    
    readd_user(admin.get('uid'), user.get('uid'))
    assert(not user.is_removed)

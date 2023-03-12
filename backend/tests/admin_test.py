import pytest
import firebase_admin
from firebase_admin import auth
from src.admin import *
from src.helper import *
from src.profile import *


# Set up
# Use a service account.
cred = credentials.Certificate('taskforge-9aea9-firebase-adminsdk-xaffr-8157d1424f.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

#Assuming that 2 users already exist, the first one is root admin and 2nd one is just a normal user
#each test should somewhat reset for the next test
@pytest.mark.order1
def test_give_admin():
    assert(is_admin(0))
    assert(not is_admin(1))
    give_admin(0, 1)

@pytest.mark.order2
def test_give_admin_to_admin():
    assert(is_admin(0))
    assert(is_admin(1))
    
    give_admin(0, 1)
    assert(is_admin(1))

@pytest.mark.order3
def test_ban_user():
    assert(is_admin(0))
    assert(not is_banned(1))
    
    ban_user(0, 1)
    assert(is_banned(1))

@pytest.mark.order4
def test_ban_banned_user():
    assert(is_admin(0))
    assert(is_banned(1))
    
    ban_user(0, 1)
    assert(is_banned(1))


#user is still banned from last test
@pytest.mark.order5
def test_unban_user():
    assert(is_admin(0))
    assert(is_banned(1))
    
    unban_user(0, 1)
    assert(not is_banned(1))

@pytest.mark.order6
def test_unban_notbanned_user():
    assert(is_admin(0))
    assert(not is_banned(1))
    
    unban_user(0, 1)
    assert(not is_banned(1))


@pytest.mark.order7
def test_remove_user():
    assert(is_admin(0))
    assert(not is_removed(1))
    
    remove_user(0, 1)
    assert(is_removed(1))


#user still removed
@pytest.mark.order8
def test_remove_removed_user():
    assert(is_admin(0))
    assert(is_removed(1))
    
    remove_user(0, 1)
    assert(is_removed(1))


#user still removed from last test
@pytest.mark.order9
def test_readd_removed_user():
    assert(is_admin(0))
    assert(is_removed(1))
    
    readd_user(0, 1)
    assert(not is_removed(1))

@pytest.mark.order10
def test_readd_normal_user():
    assert(is_admin(0))
    assert(not is_removed(1))
    
    readd_user(0, 1)
    assert(not is_removed(1))
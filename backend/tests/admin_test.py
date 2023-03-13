import pytest
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from src.profile import is_admin, is_banned, is_removed
from src.admin import give_admin, ban_user, unban_user,  remove_user, readd_user

#Assuming that 2 users already exist, the first one is root admin and 2nd one is just a normal user
#each test should somewhat reset for the next test
#@pytest.mark.order1

def test_give_admin_type():
    try:
        give_admin(1, 2)
    except TypeError:
        pass

def test_give_admin():
    assert(is_admin('sklzNex5udNeOd65uvsuGAYBNkH2'))
    assert(not is_admin('xyzabc123'))
    give_admin('sklzNex5udNeOd65uvsuGAYBNkH2', 'xyzabc123')
    assert(is_admin('xyzabc123'))


#@pytest.mark.order2
def test_give_admin_to_admin():
    assert(is_admin('sklzNex5udNeOd65uvsuGAYBNkH2'))
    assert(is_admin('xyzabc123'))
    try:
        give_admin('sklzNex5udNeOd65uvsuGAYBNkH2', 'xyzabc123')
    except ValueError:
        pass
    assert(is_admin('xyzabc123'))


def test_ban_user_type():
    try:
        ban_user(1, 2)
    except TypeError:
        pass

#@pytest.mark.order3
def test_ban_user():
    assert(is_admin('sklzNex5udNeOd65uvsuGAYBNkH2'))
    assert(not is_banned('xyzabc123'))
    
    ban_user('sklzNex5udNeOd65uvsuGAYBNkH2', 'xyzabc123')
    assert(is_banned('xyzabc123'))

#@pytest.mark.order4
def test_ban_banned_user():
    assert(is_admin('sklzNex5udNeOd65uvsuGAYBNkH2'))
    assert(is_banned('xyzabc123'))
    
    try:
        ban_user('sklzNex5udNeOd65uvsuGAYBNkH2', 'xyzabc123')
    except ValueError:
        pass
    assert(is_banned('xyzabc123'))



def test_unban_user_type():
    try:
        unban_user(1, 2)
    except TypeError:
        pass

#user is still banned from last test
#@pytest.mark.order5
def test_unban_user():
    assert(is_admin('sklzNex5udNeOd65uvsuGAYBNkH2'))
    assert(is_banned('xyzabc123'))
    
    unban_user('sklzNex5udNeOd65uvsuGAYBNkH2', 'xyzabc123')
    assert(not is_banned('xyzabc123'))

#@pytest.mark.order6
def test_unban_notbanned_user():
    assert(is_admin('sklzNex5udNeOd65uvsuGAYBNkH2'))
    assert(not is_banned('xyzabc123'))
    
    try:
        unban_user('sklzNex5udNeOd65uvsuGAYBNkH2', 'xyzabc123')
    except ValueError:
        pass
    assert(not is_banned('xyzabc123'))


def test_remove_usertype():
    try:
        remove_user(1, 2)
    except TypeError:
        pass

#@pytest.mark.order7
def test_remove_user():
    assert(is_admin('sklzNex5udNeOd65uvsuGAYBNkH2'))
    assert(not is_removed('xyzabc123'))
    
    remove_user('sklzNex5udNeOd65uvsuGAYBNkH2', 'xyzabc123')
    assert(is_removed('xyzabc123'))


#user still removed
#@pytest.mark.order8
def test_remove_removed_user():
    assert(is_admin('sklzNex5udNeOd65uvsuGAYBNkH2'))
    assert(is_removed('xyzabc123'))
    
    try:
        remove_user('sklzNex5udNeOd65uvsuGAYBNkH2', 'xyzabc123')
    except ValueError:
        pass
    assert(is_removed('xyzabc123'))


def test_readd_user_type():
    try:
        readd_user(1, 2)
    except TypeError:
        pass

#user still removed from last test
#@pytest.mark.order9
def test_readd_removed_user():
    assert(is_admin('sklzNex5udNeOd65uvsuGAYBNkH2'))
    assert(is_removed('xyzabc123'))
    
    readd_user('sklzNex5udNeOd65uvsuGAYBNkH2', 'xyzabc123')
    assert(not is_removed('xyzabc123'))

#@pytest.mark.order10
def test_readd_normal_user():
    assert(is_admin('sklzNex5udNeOd65uvsuGAYBNkH2'))
    assert(not is_removed('xyzabc123'))
    
    try:
        readd_user('sklzNex5udNeOd65uvsuGAYBNkH2', 'xyzabc123')
    except ValueError:
        pass
    assert(not is_removed('xyzabc123'))
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from profile import *
from global_counters import *
from helper import *

def give_admin(uid_admin, uid_user):
    tuid = get_curr_tid()
    
    if (uid_admin is not int or uid_user is not int): raise TypeError('uids are ints')
    if (uid_admin > tuid or uid_user > tuid): raise ValueError('uid invalid')
    if (is_banned(uid_admin)): raise ValueError('You are banned')
    if (is_banned(uid_user)): raise ValueError('Cannot make a banned user an admin')
    if (not is_admin(uid_admin)): raise ValueError('You are not an admin')
    if (is_admin(uid_user)): raise ValueError('User is already an admin')
    
    user_ref = db.collection("users").document(uid_user)
    user_ref.update({'is_admin': True})
        
    

def ban_user(uid_admin, uid_user):
    tuid = get_curr_tid()
    
    if (uid_admin is not int or uid_user is not int): raise TypeError('uids are ints')
    if (uid_admin > tuid or uid_user > tuid): raise ValueError('uid invalid')
    if (is_banned(uid_admin)): raise ValueError('You are banned')
    if (not is_admin(uid_admin)): raise ValueError('You are not an admin')
    if (is_banned(uid_user)): raise ValueError('User is already banned')
    
    user_ref = db.collection("users").document(uid_user)
    user_ref.update({'is_banned': True})
    
def unban_user(uid_admin, uid_user):
    tuid = get_curr_tid()
    
    if (uid_admin is not int or uid_user is not int): raise TypeError('uids are ints')
    if (uid_admin > tuid or uid_user > tuid): raise ValueError('uid invalid')
    if (is_banned(uid_admin)): raise ValueError('You are banned')
    if (not is_admin(uid_admin)): raise ValueError('You are not an admin')
    if (not is_banned(uid_user)): raise ValueError('User is not banned')
    
    user_ref = db.collection("users").document(uid_user)
    user_ref.update({'is_banned': False})


def remove_user(uid_admin, uid_user):
    tuid = get_curr_tid()
    
    if (uid_admin is not int or uid_user is not int): raise TypeError('uids are ints')
    if (uid_admin > tuid or uid_user > tuid): raise ValueError('uid invalid')
    if (is_banned(uid_admin)): raise ValueError('You are banned')
    if (not is_admin(uid_admin)): raise ValueError('You are not an admin')
    if (is_removed(uid_user)): raise ValueError('User is already removed')
    
    user_ref = db.collection("users").document(uid_user)
    user_ref.update({'is_removed': True})

def readd_user(uid_admin, uid_user):
    tuid = get_curr_tid()
    
    if (uid_admin is not int or uid_user is not int): raise TypeError('uids are ints')
    if (uid_admin > tuid or uid_user > tuid): raise ValueError('uid invalid')
    if (is_banned(uid_admin)): raise ValueError('You are banned')
    if (not is_admin(uid_admin)): raise ValueError('You are not an admin')
    if (not is_removed(uid_user)): raise ValueError('User is not removed')
    
    user_ref = db.collection("users").document(uid_user)
    user_ref.update({'is_removed': False})
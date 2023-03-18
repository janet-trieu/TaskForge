import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from profile_page import is_banned, is_admin, is_removed, get_user_ref
from global_counters import *
import sys
from error import InputError, AccessError
'''
Feature: Admin
Functionalities:
    - give_admin
    - ban_user
    - unban_user
    - remove_user
    - readd_user
'''


'''
Takes 2 users, 1st being an admin, 2nd one not, and makes 2nd user an admin
Args:
    - uid_admin(string): uid of the admin giving admin status
    - uid_user(string): uid of user who will be given admin status
'''
def give_admin(uid_admin, uid_user): 
    if (not isinstance(uid_admin, str) or not isinstance(uid_user, str)): raise InputError('uids should be strings')
    if (not get_user_ref(uid_admin) or not get_user_ref(uid_user)): raise InputError('uid invalid')
    if (is_banned(uid_admin)): raise AccessError('You are banned')
    if (is_banned(uid_user)): raise InputError('Cannot make a banned user an admin')
    if (not is_admin(uid_admin)): raise InputError('You are not an admin')
    if (is_admin(uid_user)): raise InputError('User is already an admin')
    
    user_ref = db.collection("users").document(uid_user)
    user_ref.update({'is_admin': True})
    return {}

        
    
'''
Admin bans a user/admin
Args:
    - uid_admin(string): uid of the admin banning user
    - uid_user(string): uid of user who will be banned
'''
def ban_user(uid_admin, uid_user):  
    if (not isinstance(uid_admin, str) or not isinstance(uid_user, str)): raise InputError('uids are strings')
    if (not get_user_ref(uid_admin) or not get_user_ref(uid_user)): raise InputError('uid invalid')
    if (is_banned(uid_admin)): raise AccessError('You are banned')
    if (not is_admin(uid_admin)): raise InputError('You are not an admin')
    if (is_banned(uid_user)): raise InputError('User is already banned')
    
    user_ref = db.collection("users").document(uid_user)
    user_ref.update({'is_banned': True})
    return {}


'''
Admin removes a ban from a banned user
Args:
    - uid_admin(string): uid of the admin unbanning banned user
    - uid_user(string): uid of user who will be unbanned
'''
def unban_user(uid_admin, uid_user): 
    if (not isinstance(uid_admin, str) or not isinstance(uid_user, str)): raise InputError('uids are strings')
    if (not get_user_ref(uid_admin) or not get_user_ref(uid_user)): raise InputError('uid invalid')
    if (is_banned(uid_admin)): raise AccessError('You are banned')
    if (not is_admin(uid_admin)): raise InputError('You are not an admin')
    if (not is_banned(uid_user)): raise InputError('User is not banned')
    
    user_ref = db.collection("users").document(uid_user)
    user_ref.update({'is_banned': False})
    return {}



'''
Similar to ban, but removal is used for very long inactivity or other reasons
Args:
    - uid_admin(string): uid of the admin removing a user
    - uid_user(string): uid of user who will be removed
'''
def remove_user(uid_admin, uid_user):
    if (not isinstance(uid_admin, str) or not isinstance(uid_user, str)): raise InputError('uids are strings')
    if (not get_user_ref(uid_admin) or not get_user_ref(uid_user)): raise InputError('uid invalid')
    if (is_banned(uid_admin)): raise AccessError('You are banned')
    if (not is_admin(uid_admin)): raise InputError('You are not an admin')
    if (is_removed(uid_user)): raise InputError('User is already removed')
    
    user_ref = db.collection("users").document(uid_user)
    user_ref.update({'is_removed': True})
    return {}


'''
Undoes a removal
Args:
    - uid_admin(string): uid of the admin readding user
    - uid_user(string): uid of user who will be readded
'''
def readd_user(uid_admin, uid_user):
    if (not isinstance(uid_admin, str) or not isinstance(uid_user, str)): raise InputError('uids are strings')
    if (not get_user_ref(uid_admin) or not get_user_ref(uid_user)): raise InputError('uid invalid')
    if (is_banned(uid_admin)): raise AccessError('You are banned')
    if (not is_admin(uid_admin)): raise InputError('You are not an admin')
    if (not is_removed(uid_user)): raise InputError('User is not removed')
    
    user_ref = db.collection("users").document(uid_user)
    user_ref.update({'is_removed': False})
    return {}
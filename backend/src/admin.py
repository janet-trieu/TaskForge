import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from src.profile import is_banned, is_admin, is_removed, get_user_ref
from src.global_counters import *

def give_admin(uid_admin, uid_user): 
    if (not isinstance(uid_admin, str) or not isinstance(uid_user, str)): raise TypeError('uids are strings')
    if (not get_user_ref(uid_admin) or not get_user_ref(uid_user)): raise ValueError('uid invalid')
    if (is_banned(uid_admin)): raise ValueError('You are banned')
    if (is_banned(uid_user)): raise ValueError('Cannot make a banned user an admin')
    if (not is_admin(uid_admin)): raise ValueError('You are not an admin')
    if (is_admin(uid_user)): raise ValueError('User is already an admin')
    
    user_ref = db.collection('users').where("uid", "==", uid_user).stream()
    for doc in user_ref:
        doc_name = doc.id
    
    user_ref = db.collection("users").document(doc_name)
    user_ref.update({'is_admin': True})
        
    

def ban_user(uid_admin, uid_user):  
    if (not isinstance(uid_admin, str) or not isinstance(uid_user, str)): raise TypeError('uids are strings')
    if (not get_user_ref(uid_admin) or not get_user_ref(uid_user)): raise ValueError('uid invalid')
    if (is_banned(uid_admin)): raise ValueError('You are banned')
    if (not is_admin(uid_admin)): raise ValueError('You are not an admin')
    if (is_banned(uid_user)): raise ValueError('User is already banned')
    
    user_ref = db.collection('users').where("uid", "==", uid_user).stream()
    for doc in user_ref:
        doc_name = doc.id
    
    user_ref = db.collection("users").document(doc_name)
    user_ref.update({'is_banned': True})
    
def unban_user(uid_admin, uid_user): 
    if (not isinstance(uid_admin, str) or not isinstance(uid_user, str)): raise TypeError('uids are strings')
    if (not get_user_ref(uid_admin) or not get_user_ref(uid_user)): raise ValueError('uid invalid')
    if (is_banned(uid_admin)): raise ValueError('You are banned')
    if (not is_admin(uid_admin)): raise ValueError('You are not an admin')
    if (not is_banned(uid_user)): raise ValueError('User is not banned')
    
    user_ref = db.collection('users').where("uid", "==", uid_user).stream()
    for doc in user_ref:
        doc_name = doc.id
    
    user_ref = db.collection("users").document(doc_name)
    user_ref.update({'is_banned': False})


def remove_user(uid_admin, uid_user):
    if (not isinstance(uid_admin, str) or not isinstance(uid_user, str)): raise TypeError('uids are strings')
    if (not get_user_ref(uid_admin) or not get_user_ref(uid_user)): raise ValueError('uid invalid')
    if (is_banned(uid_admin)): raise ValueError('You are banned')
    if (not is_admin(uid_admin)): raise ValueError('You are not an admin')
    if (is_removed(uid_user)): raise ValueError('User is already removed')
    
    user_ref = db.collection('users').where("uid", "==", uid_user).stream()
    for doc in user_ref:
        doc_name = doc.id
    
    user_ref = db.collection("users").document(doc_name)
    user_ref.update({'is_removed': True})

def readd_user(uid_admin, uid_user):
    if (not isinstance(uid_admin, str) or not isinstance(uid_user, str)): raise TypeError('uids are strings')
    if (not get_user_ref(uid_admin) or not get_user_ref(uid_user)): raise ValueError('uid invalid')
    if (is_banned(uid_admin)): raise ValueError('You are banned')
    if (not is_admin(uid_admin)): raise ValueError('You are not an admin')
    if (not is_removed(uid_user)): raise ValueError('User is not removed')
    
    user_ref = db.collection('users').where("uid", "==", uid_user).stream()
    for doc in user_ref:
        doc_name = doc.id
    
    user_ref = db.collection("users").document(doc_name)
    user_ref.update({'is_removed': False})
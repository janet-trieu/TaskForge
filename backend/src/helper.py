from firebase_admin import firestore, auth

from .error import *
from .global_counters import *

db = firestore.client()

# ============ HELPERS ============ #

############################################################
#                      Error Checking                      #
############################################################
def check_valid_uid(uid):
    if not isinstance(uid, str):
        raise InputError('uid needs to be a string')

    doc = db.collection('users').document(uid).get()
    if not doc.exists:
        raise InputError(f'uid {uid} does not exist in database')

def check_valid_pid(pid):
    if not isinstance(pid, int):
        raise InputError('pid needs to be an int')

    doc = db.collection("projects").document(str(pid)).get()
    if not doc.exists:
        raise InputError(f'pid {pid} does not exist in database')

def check_valid_tid(tid):
    if not isinstance(tid, int):
        raise InputError('tid needs to be an int')
    
    doc = db.collection('tasks').document(str(tid)).get()
    if not doc.exists:
        raise InputError(f'tid {tid} does not exist in database')

def check_valid_rid(rid):
    if not isinstance(rid, int):
        raise InputError('rid needs to be an int')
    
    doc = db.collection('reviews').document(str(rid)).get()
    if not doc.exists:
        raise InputError(f'rid {rid} does not exist in database')

def check_valid_achievement(achievement_str):
    if not isinstance(achievement_str, str):
        raise InputError('achievement_str needs to be a string')
    
    doc = db.collection('achievements').document(achievement_str).get()
    if not doc.exists:
        raise InputError(f'achievement_str {achievement_str} does not exist in database')
    
def does_nid_exists(uid, nid):
    doc_ref = db.collection('notifications').document(uid)

    # Check if field name exists in document
    if (doc_ref.get().to_dict() is None): return False
    if nid in doc_ref.get().to_dict():
        return True
    else:
        return False
    
############################################################
#                          Getters                         #
############################################################
def get_display_name(uid):
    check_valid_uid(uid)
    name = auth.get_user(uid).display_name
    return name

def get_project_name(pid):
    check_valid_pid(pid)
    name = db.collection("projects").document(str(pid)).get().get('name')
    return name

def get_task_name(tid):
    check_valid_tid(tid)
    name = db.collection('tasks').document(str(tid)).get().get('name')
    return name

def get_achievement_name(achievement_str):
    check_valid_achievement(achievement_str)
    name = db.collection('achievements').document(achievement_str).get().get('name')
    return name

############################################################
#                       Create Users                       #
############################################################
def create_admin(uid):
    data = {
        'is_admin': True,
        'is_banned': False,
        'is_removed': False
    }

    db.collection('users').document(uid).set(data)
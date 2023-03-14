import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

db = firestore.client()

# ============ HELPERS ============ #

def check_valid_uid(uid):
    if not isinstance(uid, str):
        raise TypeError('uid needs to be a string')

    doc = db.collection('users').document(uid).get()
    if not doc.exists:
        raise ValueError(f'uid {uid} does not exist in database')

def check_valid_pid(pid):
    if not isinstance(pid, int):
        raise TypeError('pid needs to be an int')

    doc = db.collection('projects').document(str(pid)).get()
    if not doc.exists:
        raise ValueError(f'pid {pid} does not exist in database')

def check_valid_tid(tid):
    if not isinstance(tid, int):
        raise TypeError('tid needs to be an int')
    
    doc = db.collection('tasks').document(str(tid)).get()
    if not doc.exists:
        raise ValueError(f'tid {tid} does not exist in database')

def check_valid_rid(rid):
    if not isinstance(rid, int):
        raise TypeError('rid needs to be an int')
    
    doc = db.collection('reviews').document(str(rid)).get()
    if not doc.exists:
        raise ValueError(f'rid {rid} does not exist in database')

def check_valid_achievement(achievement_str):
    if not isinstance(achievement_str, str):
        raise TypeError('achievement_str needs to be a string')
    
    doc = db.collection('achievements').document(achievement_str).get()
    if not doc.exists:
        raise ValueError(f'achievement_str {achievement_str} does not exist in database')
    
def get_display_name(uid):
    check_valid_uid(uid)
    name = db.collection('users').document(uid).get().get('display_name')
    return name

def get_project_name(pid):
    check_valid_pid(pid)
    name = db.collection('projects').document(str(pid)).get().get('name')
    return name

def get_task_name(tid):
    check_valid_tid(tid)
    name = db.collection('tasks').document(str(tid)).get().get('name')
    return name

def get_achievement_name(achievement_str):
    check_valid_achievement(achievement_str)
    name = db.collection('achievements').document(achievement_str).get().get('name')
    return name
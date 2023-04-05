from firebase_admin import firestore, auth

from .error import *
from .global_counters import *
from firebase_admin import storage

db = firestore.client()

# ============ HELPERS ============ #

############################################################
#                      Error Checking                      #
############################################################
def check_valid_uid(uid):
    if not isinstance(uid, str):
        raise InputError('uid needs to be a string')
    
    # Auth DB
    try:
        auth.get_user(uid)
    except:
        raise InputError(f'User {uid} does not exist in Authentication database')
    # Firestore DB
    doc = db.collection('users').document(uid).get()
    if not doc.exists:
        raise InputError(f'User {uid} does not exist in Firestore database')

def check_valid_eid(eid):
    if not isinstance(eid, int):
        raise InputError('eid needs to be an int')

    doc = db.collection('epics').document(str(eid)).get()
    if not doc.exists:
        raise InputError(f'eid {eid} does not exist in database')
    
def check_epic_in_project(eid, pid):
    check_valid_eid(eid)
    check_valid_pid(pid)
    epics = db.collection('projects').document(str(pid)).get().get("epics")
    if eid not in epics:
        raise InputError(f'eid {eid} does not exist in project {pid}')

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
    
def check_valid_stid(stid):
    if not isinstance(stid, int):
        raise InputError('tid needs to be an int')
    
    doc = db.collection('subtasks').document(str(stid)).get()
    if not doc.exists:
        raise InputError(f'stid {stid} does not exist in database')

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
    
def check_user_in_project(uid, pid):
    check_valid_uid(uid)
    check_valid_pid(pid)
    doc = db.collection("projects").document(str(pid)).get()
    project_members = doc.get("project_members")
    if uid not in project_members:
        raise InputError(f'UID {uid} does not belong in project {pid}')
    
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
    
############################################################
#                       Storage                            #
############################################################
def storage_upload_file(fileName, destination_name):
    bucket = storage.bucket()
    blob = bucket.blob(destination_name)
    blob.upload_from_filename(fileName)
    blob.make_public()

def storage_download_file(fileName, destination_name): 
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.download_to_filename(destination_name)

def storage_delete_file(fileName):
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.delete()

############################################################
#                    Sorting Functions                     #
############################################################

def sort_tasks(tasks):
    unflagged_list = []
    flagged_list = []

    for task in tasks:
        if task["flagged"]:
            flagged_list.append(task)
        else:
            unflagged_list.append(task)
    
    def sortFunc(e):
        if e["deadline"]:
            return e["deadline"]
        else:
            return "No deadline"
    
    flagged_list.sort(key=sortFunc)
    unflagged_list.sort(key=sortFunc)

    return_list = flagged_list + unflagged_list

    return return_list

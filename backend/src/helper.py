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
    if str(eid) == "None":
        return
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

def check_connected(uid1, uid2):
    user_ref = db.collection('users').document(str(uid1))
    connected = user_ref.get().get("connections")
    if (uid2 not in connected):
        raise InputError(f'You are not connected to this taskmaster')

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

def check_user_in_task(uid, tid):
    check_valid_uid(uid)
    check_valid_tid(tid)
    doc = db.collection("tasks").document(str(tid)).get()
    assignees = doc.get("assignees")
    if uid not in assignees:
        raise InputError(f'UID {uid} does not belong in task {tid}')

def check_user_in_subtask(uid, tid, stid):
    check_valid_uid(uid)
    check_valid_tid(tid)
    check_valid_stid(stid)
    doc = db.collection("subtasks").document(str(stid)).get()
    assignees = doc.get("assignees")
    if uid not in assignees:
        raise InputError(f'UID {uid} does not belong in task {stid}')

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
    name = db.collection('tasks').document(str(tid)).get().get('title')
    return name

def get_achievement_name(achievement_str):
    check_valid_achievement(achievement_str)
    name = db.collection('achievements').document(achievement_str).get().get('name')
    return name

def get_pid(project_str):
    for doc in db.collection('projects').stream():
        if doc.to_dict().get('name') == project_str:
            return doc.id
    raise AccessError

def get_achievement(aid):
    '''
    Given an aid, return the achievement

    Arguments:
     - aid (achievement id)

    Returns:
     - achievement
    '''

    achievement = db.collection("achievements").document(str(aid)).get().to_dict()

    return achievement

### ========= get total number of reviews written ========= ###
def get_number_of_reviews_written(uid):
    """
    Gets the total nubmer of reviews written
    
    Args:  
        uid (str): uid of the user

    Returns:
        an int correlating to the nubmer of reviews written
    """
    check_valid_uid(uid)

    return int(db.collection("users").document(str(uid)).get().get("reputation").get("total_reviews_written"))

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
    blob.upload_from_filename(f'src/{fileName}')
    blob.make_public()
    return blob.public_url

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


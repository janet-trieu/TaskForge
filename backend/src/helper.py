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
    blob.upload_from_filename(fileName)
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

def get_default_profile_img():
    return 'data:image/png;base64,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'


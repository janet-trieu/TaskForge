from firebase_admin import firestore, auth
from .global_counters import *
from .profile_page import *

db = firestore.client()

############################################################
#                   Helpers for create user                #
############################################################

def create_test_user(test_type, num):
    try:
        uid = create_user_email(f"{test_type}.user{num}@gmail.com", "PaSsWoRd123", f"User User{num}")
    except auth.EmailAlreadyExistsError:
        pass
    uid = auth.get_user_by_email(f"{test_type}.user{num}@gmail.com").uid

    return uid

############################################################
#                 Helpers for Project Master               #
############################################################

def add_tm_to_project(pid, new_uid):
    proj_ref = db.collection("projects").document(str(pid))
    project_members = proj_ref.get().get("project_members")

    user_ref = db.collection("users").document(str(new_uid))

    if not new_uid in project_members:
        project_members.append(new_uid)

    proj_ref.update({
        "project_members": project_members
    })

    user_projects = user_ref.get().get("projects")
    if not pid in user_projects:
        user_projects.append(pid)

    user_ref.update({"projects": user_projects})

############################################################
#                    Helpers for Projects                  #
############################################################

def get_notif_ref_proj_invite(pid, uid):
    doc = db.collection('notifications').document(uid).get().to_dict()

    for key, val in doc.items():
        if val.get("pid") == pid and "project_invite" in key:
            ret = val
    
    return ret

############################################################
#                      Reset Database                      #
############################################################

### ========= Delete User ========= ###
def delete_user(uid):
    """
    Deletes User from auth and firestore database

    Args:
        uid (str): uid of the user that can be found in auth database

    Returns:
        None
    """
    try:
        auth.delete_user(uid)
        # tuid = get_user_ref(uid).get("tuid")
        db.collection("users").document(str(uid)).delete()
        db.collection('notifications').document(uid).delete()
        # TODO: Remove user data from following stuff, if we need to:
        # REMOVE user from projects
        # REMOVE user from connections
        # REMOVE user from assigned tasks
        # REMOVE user from reviews
        # REMOVE user from achievements
        # REMOVE other data that isnt listed here that should be removed
    except:
        print("uid does not correspond to a current user")

def reset_projects():
    project_count = get_curr_pid()

    for i in range(0, project_count):
        db.collection("projects").document(str(i)).delete()

    counter_ref = db.collection("counters").document("total_projects")

    counter_ref.update({"pid": 0})

def reset_database():
    '''
    Purges firestore & auth database completely and resets global counters
    '''
    # ==== AUTH DATABASE ==== #
    # USER deletion
    all_users = auth.list_users()
    for user in all_users.users:
        auth.delete_user(user.uid)

    # ==== FIRESTORE DATABASE ==== #
    # USERS deletion
    for user_doc_ref in db.collection('users').list_documents():
        user_doc_ref.delete()

    # NOTIFICATIONS deletion
    for notf_doc_ref in db.collection('notifications').list_documents():
        notf_doc_ref.delete()

    # PROJECTS deletion
    for proj_doc_ref in db.collection('projects').list_documents():
        proj_doc_ref.delete()

    # TASKS deletion
    for tasks_doc_ref in db.collection('tasks').list_documents():
        tasks_doc_ref.delete()

    # SUBTASKS deletion
    for subtasks_doc_ref in db.collection('subtasks').list_documents():
        subtasks_doc_ref.delete()

    # EPICS deletion
    for epics_doc_ref in db.collection('epics').list_documents():
        epics_doc_ref.delete()

    # Reset counters
    init_eid()
    init_pid()
    init_stid()
    init_tid()
    init_tuid()
from firebase_admin import firestore, auth
from .global_counters import *

db = firestore.client()

############################################################
#                 Helpers for Project Master               #
############################################################

def add_tm_to_project(pid, new_uid):
    proj_ref = db.collection("projects").document(str(pid))
    project_members = proj_ref.get().get("project_members")

    if not new_uid in project_members:
        project_members.append(new_uid)

    proj_ref.update({
        "project_members": project_members
    })

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

    # TODO: Add more if you have created more collections!

    # Reset counters
    init_tuid()
    init_pid()
    init_eid()
    init_tid()
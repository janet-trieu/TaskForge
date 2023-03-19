from firebase_admin import firestore, auth
from .global_counters import *
from .profile_page import *

db = firestore.client()

############################################################
#                 Helpers for Project Master               #
############################################################

# def create_project_master():
#     proj_master = auth.create_user(
#         email = "project.master@gmail.com",
#         password = "password123",
#         display_name = "Project Master"
#     )

#     return proj_master

# def create_not_project_master(email, password, display_name):

#     task_master = auth.create_user(
#         email = email,
#         password = password,
#         display_name = display_name
#     )

#     return task_master

# def reset_projects():
#     project_count = get_curr_pid()

#     for i in range(0, project_count):
#         db.collection("projects").document(str(i)).delete()

#     counter_ref = db.collection("counters").document("total_projects")

#     counter_ref.update({"pid": 0})

# def reset_project_count():
#     counter_ref = db.collection("counters").document("total_projects")

#     counter_ref.update({"pid": 0})

def add_tm_to_project(pid, new_uid):
    proj_ref = db.collection("projects").document(str(pid))
    project_members = proj_ref.get().get("project_members")

    if not new_uid in project_members:
        project_members.append(new_uid)

    proj_ref.update({
        "project_members": project_members
    })

### ========= Delete User ========= ###
"""
Deletes User from auth and firestore database

Args:
    uid (str): uid of the user that can be found in auth database

Returns:
    None
"""
def delete_user(uid):
    try:
        auth.delete_user(uid)
        # tuid = get_user_ref(uid).get("tuid")
        db.collection("users").document(str(uid)).delete()
        db.collection('notifications').document(uid).delete()
    except:
        print("uid does not correspond to a current user")

############################################################
#                      Reset Database                      #
############################################################

def reset_projects():
    project_count = get_curr_pid()

    for i in range(0, project_count):
        db.collection("projects").document(str(i)).delete()

    counter_ref = db.collection("counters").document("total_projects")

    counter_ref.update({"pid": 0})

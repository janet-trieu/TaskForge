from firebase_admin import firestore
from src.global_counters import *

db = firestore.client()

############################################################
#                 Helpers for Project Master               #
############################################################

def reset_projects():
    project_count = get_curr_pid()

    for i in range(0, project_count):
        db.collection("projects_test").document(str(i)).delete()

def reset_project_count():
    counter_ref = db.collection("counters").document("project")

    counter_ref.update({"pid": 0})

def add_tm_to_project(pid, new_uid):
    proj_ref = db.collection("projects_test").document(str(pid))
    project_members = proj_ref.get().get("project_members")

    if not new_uid in project_members:
        project_members.append(new_uid)

    proj_ref.update({
        "project_members": project_members
    })
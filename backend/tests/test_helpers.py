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

def is_user_project_master(uid):
    pass
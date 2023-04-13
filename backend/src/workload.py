from .helper import *
from datetime import datetime


def get_workload(uid):
    check_valid_uid(uid)
    workload = 0
    curr_time = datetime.now()
    SEVEN_DAYS = 604800 #7 days worth of seconds
    user_ref = db.collection('users').document(uid)
    tids = user_ref.get().get("tasks")
    for tid in tids:
        task_ref = db.collection('tasks').document(tid)
        
        status = task_ref.get().get("status")
        if (status != "In Progress" or status != "Testing/Reviewing"): continue
        
        due_date = task_ref.get().get("deadline")
        if (due_date - curr_time > SEVEN_DAYS): continue
        
        task_wl = task_ref.get().get("workload")
        if (isinstance(task_wl, int)):
            workload += task_wl

    return workload
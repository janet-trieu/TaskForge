# Imports
from firebase_admin import firestore
from firebase_admin import auth

from .global_counters import *
from .classes import Epic, Task, Subtask
from .error import *
from .notifications import *
from .helper import *
from .profile_page import *
from .taskboard import get_task_ref, insert_tasklist
import re
import time

### ========= Get User Assigned Tasks ========= ###
def get_user_assigned_task(uid, show_completed):
    """
    Retrieves the user's assigned tasks with a boolean that will either retrieve all
    assigned tasks or non-completed tasks

    Args:
        uid (str): id of the user requesting all their assigned tasks
        show_completed (boolean): boolean on whether completed tasks will be shown

    Returns:
        a dict of tasks with the headings "Not Started", "In Progress", "Blocked", "In Review/Testing",
        or "Completed". Task details include: id, title, project_name, epic, deadline, priority, status, assignees
    """
    check_valid_uid(uid)

    tasks = db.collection("users").document(uid).get().get("tasks")
    task_list = []
    if show_completed == True:
        for task in tasks:
            task_ref = get_task_ref(task)
            pid = task_ref.get("pid")
            eid = task_ref.get("eid")
            task_details = {
                "tid": task,
                "title": task_ref.get("title"),
                "project_name": db.collection("projects").document(str(pid)).get().get("name"),
                "pid": pid,
                "description": task_ref.get("description"),
                "deadline": task_ref.get("deadline"),
                "priority": task_ref.get("priority"),
                "status": task_ref.get("status"),
                "assignees": task_ref.get("assignees"),
                "flagged": task_ref.get("flagged")
            }
            if eid == "" or eid == None:
                task_details['epic'] = "None"
            else:
                task_details['epic'] = db.collection("epics").document(str(eid)).get().get("title")
            task_list = insert_tasklist(task_list, task_details)
    elif show_completed == False:
        for task in tasks:
            task_ref = get_task_ref(task)
            pid = task_ref.get("pid")
            eid = task_ref.get("eid")
            if task_ref.get("status") != "Completed":
                task_details = {
                    "tid": task,
                    "title": task_ref.get("title"),
                    "project_name": db.collection("projects").document(str(pid)).get().get("name"),
                    "pid": pid,
                    "description": task_ref.get("description"),
                    "deadline": task_ref.get("deadline"),
                    "priority": task_ref.get("priority"),
                    "status": task_ref.get("status"),
                    "assignees": task_ref.get("assignees"),
                    "flagged": task_ref.get("flagged")
                }
                if eid == "" or eid == None:
                    task_details['epic'] = "None"
                else:
                    task_details['epic'] = db.collection("epics").document(str(eid)).get().get("title")
                task_list = insert_tasklist(task_list, task_details)
    return task_list

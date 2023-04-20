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
from datetime import datetime

### ========= Get User Assigned Tasks ========= ###
def get_user_assigned_task(uid, show_completed):
    """
    Retrieves the user's assigned tasks with a boolean that will either retrieve all
    assigned tasks or non-completed tasks

    Args:
        uid (str): id of the user requesting all their assigned tasks
        show_completed (boolean): boolean on whether completed tasks will be shown

    Returns:
        a dict of tasks with the Task details include: id, title, project_name, epic, deadline, priority, status, assignees
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

def search_tasklist(uid, query_tid, query_title, query_description, query_deadline):
    """
    Searches the user's tasklist and retrieves task that match the combination of queries

    Args:
        uid (str): id of the user's task that are being searched
        query_tid (int): id of the task
        query_title(str): str of the title of the task
        query_description (str): str of the description query of the task
        query_deadline (int): int of the deadline

    Returns:
        a dict of tasks with the Task details include: id, title, project_name, epic, deadline, priority, status, assignees
        task must match the combination of queries
    """
    check_valid_uid(uid)
    tasks = db.collection("users").document(uid).get().get("tasks")

    task_list = []
    for task in tasks:
        task_ref = get_task_ref(task)
        pid = task_ref.get("pid")
        eid = task_ref.get("eid")
        task_details = {
            "tid": task,
            "title": task_ref.get("title"),
            "project_name": db.collection("projects").document(str(pid)).get().get("name"),
            "deadline": task_ref.get("deadline"),
            "priority": task_ref.get("priority"),
            "status": task_ref.get("status"),
            "assignees": task_ref.get("assignees"),
            "flagged": task_ref.get("flagged"),
            "description": task_ref.get("description")
        }
        if eid == "" or eid == None:
            task_details['epic'] = "None"
        else:
            task_details['epic'] = db.collection("epics").document(str(eid)).get().get("title")

        if ((query_tid == "" or int(query_tid) == int(task)) and (query_title == "" or query_title.lower() in task_ref.get("title"))
                                                        and (query_description == "" or query_description.lower() in task_ref.get("description"))
                                                        and (query_deadline == "" or query_deadline == task_ref.get("deadline"))):
            task_list = insert_tasklist(task_list, task_details)
    return task_list
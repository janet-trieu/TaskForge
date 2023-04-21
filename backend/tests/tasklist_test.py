import pytest

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth

from src.error import *
from src.profile_page import *
from src.notifications import *
from src.global_counters import *
from src.taskboard import *
from src.projmaster import *
from src.test_helpers import add_tm_to_project
from src.tasklist import get_user_assigned_task
from src.epics import create_epic, delete_epic
from src.tasks import create_task, get_task_details, delete_task

# ============ SET UP ============ #
db = firestore.client()

# Create new users
try:
    uid1 = create_user_email("taskboardtest1@gmail.com", "password123", "user1")
    uid2 = create_user_email("taskboardtest2@gmail.com", "password123", "user2")
    uid3 = create_user_email("taskboardtest3@gmail.com", "password123", "user3")
except auth.EmailAlreadyExistsError:
    pass

# Users may already exist

uid1 = auth.get_user_by_email("taskboardtest1@gmail.com").uid
uid2 = auth.get_user_by_email("taskboardtest2@gmail.com").uid
uid3 = auth.get_user_by_email("taskboardtest3@gmail.com").uid

pid1 = create_project(str(uid1), "boobs", "butts", None, None)
pid2 = create_project(str(uid1), "booties", "butts", None, None)

def test_get_assigned_tasklist_show_completed():
    eid1 = create_epic(str(uid1), pid1, "Epic1", "Epic1 Description", "#ffa28e")

    task1 = create_task(str(uid1), pid1, eid1, ["taskboardtest1@gmail.com"], "Task1", "Task1 Description", "", None, None, "Not Started")
    tid1 = task1.get("tid")
    task1_details = get_task_details(uid1, tid1)
    assert task1_details == {"tid": tid1, "pid": pid1, "eid": eid1, "assignees": [uid1], "subtasks": [], "title": "Task1", "description": "Task1 Description",
                     "deadline": "", "workload": 0, "priority": None, "status": "Not Started", "comments": [], "flagged": False, "completed": "", "files": None}
    assigned_list = get_user_assigned_task(uid1, True)
    assert assigned_list == [{'tid': tid1, 'title': 'Task1', 'project_name': 'boobs', 'deadline': '', 'priority': None, 
                              'status': 'Not Started', 'assignees': [uid1], 'epic': 'Epic1', 'flagged': False, "description": "Task1 Description", "pid": pid1}]

                                            
    delete_task(uid1, tid1)
    delete_epic(uid1, eid1)

def test_get_assigned_task_list_show_completed_two_projects():
    eid1 = create_epic(str(uid1), pid1, "Epic1", "Epic1 Description", "#ffa28e")
    task1 = create_task(str(uid1), pid1, eid1, ["taskboardtest1@gmail.com"], "Task1", "Task1 Description", "", None, None, "Not Started")
    tid1 = task1.get("tid")
    task1_details = get_task_details(uid1, tid1)
    assert task1_details == {"tid": tid1, "pid": pid1, "eid": eid1, "assignees": [uid1], "subtasks": [], "title": "Task1", "description": "Task1 Description",
                     "deadline": "", "workload": 0, "priority": None, "status": "Not Started", "comments": [], "flagged": False, "completed": "", "files": None}
    
    eid2 = create_epic(str(uid1), pid2, "Epic1", "Epic1 Description", "#ffa28e")
    task2 = create_task(str(uid1), pid2, eid2, ["taskboardtest1@gmail.com"], "Task1", "Task1 Description", "", None, None, "Not Started")
    tid2 = task2.get("tid")
    task2_details = get_task_details(uid1, tid2)
    assert task2_details == {"tid": tid2, "pid": pid2, "eid": eid2, "assignees": [uid1], "subtasks": [], "title": "Task1", "description": "Task1 Description",
                     "deadline": "", "workload": 0, "priority": None, "status": "Not Started", "comments": [], "flagged": False, "completed": "", "files": None}
    assigned_list = get_user_assigned_task(uid1, True)

    assert assigned_list == [{'tid': tid1, 'title': 'Task1', 'project_name': 'boobs', 'deadline': '', 'priority': None, 
                              'status': 'Not Started', 'assignees': [uid1], 'epic': 'Epic1', 'flagged': False, "description": "Task1 Description", "pid": pid1}, 
                              {'tid': tid2, 'title': 'Task1', 'project_name': 'booties', 'deadline': '', 'priority': None, 
                               'status': 'Not Started', 'assignees': [uid1], 'epic': 'Epic1', 'flagged': False, "description": "Task1 Description", "pid": pid2}]

    delete_task(uid1, tid1)
    delete_epic(uid1, eid1)
    delete_task(uid1, tid2)
    delete_epic(uid1, eid2)
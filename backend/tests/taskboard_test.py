import pytest

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth
import datetime

from src.error import *
from src.profile_page import *
from src.notifications import *
from src.global_counters import *
from src.taskboard import *
from src.epics import create_epic, get_epic_details, delete_epic
from src.tasks import create_task, get_task_details, delete_task, assign_task, flag_task
from src.projmaster import *
from src.test_helpers import add_tm_to_project

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

def test_create_epic():
    eid1 = create_epic(str(uid1), pid1, "Epic1", "Epic1 Description", "#ffa28e")
    epic = get_epic_details(uid1, eid1)
    assert epic == {"eid": eid1, "pid": pid1, "tasks": [], "title": "Epic1", "description": "Epic1 Description", "colour": "#ffa28e"}
    delete_epic(uid1, eid1)

def test_create_task():
    eid1 = create_epic(str(uid1), pid1, "Epic1", "Epic1 Description", "#ffa28e")

    task1 = create_task(str(uid1), pid1, eid1, ["taskboardtest1@gmail.com"], "Task1", "Task1 Description", "1679749200", None, None, "Not Started")
    tid1 = task1.get("tid")
    task1 = get_task_details(uid1, tid1)
    assert task1 == {"tid": tid1, "pid": pid1, "eid": eid1, "assignees": [uid1], "subtasks": [], "title": "Task1", "description": "Task1 Description",
                     "deadline": "1679749200", "workload": 0, "priority": None, "status": "Not Started", "comments": [], "flagged": False, "completed": "", "files": None}
    delete_task(uid1, tid1)
    delete_epic(uid1, eid1)

def test_assign_task():
    eid1 = create_epic(str(uid1), pid1, "Epic1", "Epic1 Description", "#ffa28e")

    task1 = create_task(str(uid1), pid1, eid1, ["taskboardtest1@gmail.com"], "Task1", "Task1 Description", "1679749200", None, None, "Not Started")
    tid1 = task1.get("tid")
    task1 = get_task_details(uid1, tid1)
    assert task1 == {"tid": tid1, "pid": pid1, "eid": eid1, "assignees": [uid1], "subtasks": [], "title": "Task1", "description": "Task1 Description",
                     "deadline": "1679749200", "workload": 0, "priority": None, "status": "Not Started", "comments": [], "flagged": False, "completed": "", "files": None}
    add_tm_to_project(pid1, uid2)
    assign_task(uid1, tid1, ["taskboardtest2@gmail.com"])
    task1 = get_task_details(uid1, tid1)
    assert task1 == {"tid": tid1, "pid": pid1, "eid": eid1, "assignees": [uid2], "subtasks": [], "title": "Task1", "description": "Task1 Description",
                     "deadline": "1679749200", "workload": 0, "priority": None, "status": "Not Started", "comments": [], "flagged": False, "completed": "", "files": None}
    delete_task(uid1, tid1)
    delete_epic(uid1, eid1)

def test_show_taskboard():
    eid1 = create_epic(str(uid1), pid1, "Epic1", "Epic1 Description", "#ffa28e")

    task1 = create_task(str(uid1), pid1, eid1, ["taskboardtest1@gmail.com"], "Task1", "Task1 Description", "1679749200", None, None, "Not Started")
    tid1 = task1.get("tid")
    task1_details = get_task_details(uid1, tid1)
    assert task1_details == {"tid": tid1, "pid": pid1, "eid": eid1, "assignees": [uid1], "subtasks": [], "title": "Task1", "description": "Task1 Description",
                     "deadline": "1679749200", "workload": 0, "priority": None, "status": "Not Started", "comments": [], "flagged": False, "completed": "", "files": None}
    taskboard = get_taskboard(uid1, pid1, True)
    assert taskboard == {'Not Started': [{'tid': tid1, 'title': 'Task1', 'deadline': '1679749200', 'priority': None, 
                                          'status': 'Not Started', 'assignees': [uid1], 'epic': 'Epic1', 'flagged': False, "assignee_emails": ["taskboardtest1@gmail.com"], "comments": [], 'description': 'Task1 Description','eid': eid1, "files": [], "subtasks": [], "workload": 0}], 'In Progress': [], 'Blocked': [], 'In Review/Testing': [], 'Completed': []}
    delete_task(uid1, tid1)
    delete_epic(uid1, eid1)    

def test_show_taskboard_one_flag():
    eid1 = create_epic(str(uid1), pid1, "Epic1", "Epic1 Description", "#ffa28e")
    task1 = create_task(str(uid1), pid1, eid1, ["taskboardtest1@gmail.com"], "Task1", "Task1 Description", "", None, None, "Not Started")
    tid1 = task1.get("tid")
    task1_details = get_task_details(uid1, tid1)
    assert task1_details == {"tid": tid1, "pid": pid1, "eid": eid1, "assignees": [uid1], "subtasks": [], "title": "Task1", "description": "Task1 Description",
                     "deadline": "", "workload": 0, "priority": None, "status": "Not Started", "comments": [], "flagged": False, "completed": "", "files": None}
    task2 = create_task(str(uid1), pid1, eid1, ["taskboardtest1@gmail.com"], "Task2", "Task2 Description", "", None, None, "Not Started")
    tid2 = task2.get("tid")
    flag_task(uid1, tid2, True)
    task2_details = get_task_details(uid1, tid2)
    assert task2_details == {"tid": tid2, "pid": pid1, "eid": eid1, "assignees": [uid1], "subtasks": [], "title": "Task2", "description": "Task2 Description",
                     "deadline": "", "workload": 0, "priority": None, "status": "Not Started", "comments": [], "flagged": True, "completed": "", "files": None}
    taskboard = get_taskboard(uid1, pid1, True)
    assert taskboard == {'Not Started': [{'tid': tid2, 'title': 'Task2', 'deadline': "", 'priority': None,
                                          'status': 'Not Started', 'assignees': [uid1], 'epic': 'Epic1', 'flagged': True, "assignee_emails": ["taskboardtest1@gmail.com"], "comments": [], 'description': 'Task2 Description','eid': eid1, "files": [], "subtasks": [], "workload": 0}, {'tid': tid1, 'title': 'Task1', 'deadline': "", 'priority': None,  'status': 'Not Started', 'assignees': [uid1], 'epic': 'Epic1', 'flagged': False, "assignee_emails": ["taskboardtest1@gmail.com"], "comments": [], 'description': 'Task1 Description','eid': eid1, "files": [], "subtasks": [], "workload": 0}], 'In Progress': [], 'Blocked': [], 'In Review/Testing': [], 'Completed': []}
    delete_task(uid1, tid1)
    delete_task(uid1, tid2)
    delete_epic(uid1, eid1)    
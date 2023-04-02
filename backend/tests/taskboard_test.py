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
from src.proj_master import *
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

pid1 = create_project(str(uid1), "boobs", "butts", "", None, "")

def test_create_epic():
    eid1 = create_epic(str(uid1), pid1, "Epic1", "Epic1 Description", "#ffa28e")
    epic = get_epic_details(uid1, eid1)
    assert epic == {"eid": eid1, "pid": pid1, "tasks": [], "title": "Epic1", "description": "Epic1 Description", "colour": "#ffa28e"}
    delete_epic(uid1, eid1)

def test_create_task():
    eid1 = create_epic(str(uid1), pid1, "Epic1", "Epic1 Description", "#ffa28e")

    tid1 = create_task(str(uid1), pid1, eid1, [uid1], "Task1", "Task1 Description", "1679749200", None, None, "Not Started")
    task1 = get_task_details(uid1, tid1)
    assert task1 == {"tid": tid1, "pid": pid1, "eid": eid1, "assignees": [uid1], "subtasks": [], "title": "Task1", "description": "Task1 Description",
                     "deadline": "1679749200", "workload": None, "priority": None, "status": "Not Started", "comments": [], "flagged": False, "completed": ""}
    delete_task(uid1, tid1)
    delete_epic(uid1, eid1)

def test_assign_task():
    eid1 = create_epic(str(uid1), pid1, "Epic1", "Epic1 Description", "#ffa28e")

    tid1 = create_task(str(uid1), pid1, eid1, [uid1], "Task1", "Task1 Description", "1679749200", None, None, "Not Started")
    task1 = get_task_details(uid1, tid1)
    assert task1 == {"tid": tid1, "pid": pid1, "eid": eid1, "assignees": [uid1], "subtasks": [], "title": "Task1", "description": "Task1 Description",
                     "deadline": "1679749200", "workload": None, "priority": None, "status": "Not Started", "comments": [], "flagged": False, "completed": ""}
    add_tm_to_project(pid1, uid2)
    assign_task(uid1, tid1, [uid2])
    task1 = get_task_details(uid1, tid1)
    assert task1 == {"tid": tid1, "pid": pid1, "eid": eid1, "assignees": [uid2], "subtasks": [], "title": "Task1", "description": "Task1 Description",
                     "deadline": "1679749200", "workload": None, "priority": None, "status": "Not Started", "comments": [], "flagged": False, "completed": ""}
    delete_task(uid1, tid1)
    delete_epic(uid1, eid1)

def test_show_taskboard():
    eid1 = create_epic(str(uid1), pid1, "Epic1", "Epic1 Description", "#ffa28e")

    tid1 = create_task(str(uid1), pid1, eid1, [uid1], "Task1", "Task1 Description", "1679749200", None, None, "Not Started")
    task1 = get_task_details(uid1, tid1)
    assert task1 == {"tid": tid1, "pid": pid1, "eid": eid1, "assignees": [uid1], "subtasks": [], "title": "Task1", "description": "Task1 Description",
                     "deadline": "1679749200", "workload": None, "priority": None, "status": "Not Started", "comments": [], "flagged": False, "completed": ""}
    taskboard = get_taskboard(uid1, pid1, True)
    assert taskboard == {'Not Started': [{'tid': tid1, 'title': 'Task1', 'deadline': '1679749200', 'priority': None, 
                                          'status': 'Not Started', 'assignees': [uid1], 'epic': 'Epic1'}], 
                                          'In Progress': [], 'Blocked': [], 'In Review/Testing': [], 'Completed': []}
    delete_task(uid1, tid1)
    delete_epic(uid1, eid1)    
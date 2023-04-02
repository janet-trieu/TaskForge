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
from src.tasklist import get_user_assigned_task

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
pid2 = create_project(str(uid1), "bootie", "butts", "", None, "")

def test_get_assigned_tasklist_show_completed():
    eid1 = create_epic(str(uid1), pid1, "Epic1", "Epic1 Description", "#ffa28e")

    tid1 = create_task(str(uid1), pid1, eid1, [uid1], "Task1", "Task1 Description", "1679749200", None, None, "Not Started")
    task1 = get_task_details(uid1, tid1)
    assert task1 == {"tid": tid1, "pid": pid1, "eid": eid1, "assignees": [uid1], "subtasks": [], "title": "Task1", "description": "Task1 Description",
                     "deadline": "1679749200", "workload": None, "priority": None, "status": "Not Started", "comments": [], "flagged": False, "completed": ""}
    assigned_list = get_user_assigned_task(uid1, True)
    print(assigned_list)
    assert assigned_list == [{'tid': tid1, 'title': 'Task1', 'project_name': 'boobs', 'deadline': '1679749200', 'priority': None, 
                              'status': 'Not Started', 'assignees': [uid1], 'epic': 'Epic1'}]

                                            
    delete_task(uid1, tid1)
    delete_epic(uid1, eid1)

def test_get_assigned_task_list_show_completed_two_projects():
    eid1 = create_epic(str(uid1), pid1, "Epic1", "Epic1 Description", "#ffa28e")
    tid1 = create_task(str(uid1), pid1, eid1, [uid1], "Task1", "Task1 Description", "1679749200", None, None, "Not Started")
    task1 = get_task_details(uid1, tid1)
    assert task1 == {"tid": tid1, "pid": pid1, "eid": eid1, "assignees": [uid1], "subtasks": [], "title": "Task1", "description": "Task1 Description",
                     "deadline": "1679749200", "workload": None, "priority": None, "status": "Not Started", "comments": [], "flagged": False, "completed": ""}
    
    eid2 = create_epic(str(uid1), pid2, "Epic1", "Epic1 Description", "#ffa28e")
    tid2 = create_task(str(uid1), pid2, eid2, [uid1], "Task1", "Task1 Description", "1679749201", None, None, "Not Started")
    task2 = get_task_details(uid1, tid2)
    assert task2 == {"tid": tid2, "pid": pid2, "eid": eid2, "assignees": [uid1], "subtasks": [], "title": "Task1", "description": "Task1 Description",
                     "deadline": "1679749201", "workload": None, "priority": None, "status": "Not Started", "comments": [], "flagged": False, "completed": ""}
    assigned_list = get_user_assigned_task(uid1, True)
    print(assigned_list)

    assert assigned_list == [{'tid': tid1, 'title': 'Task1', 'project_name': 'boobs', 'deadline': '1679749200', 'priority': None, 
                              'status': 'Not Started', 'assignees': [uid1], 'epic': 'Epic1'}, 
                              {'tid': tid2, 'title': 'Task1', 'project_name': 'bootie', 'deadline': '1679749201', 'priority': None, 
                               'status': 'Not Started', 'assignees': [uid1], 'epic': 'Epic1'}]

    delete_task(uid1, tid1)
    delete_epic(uid1, eid1)
    delete_task(uid1, tid2)
    delete_epic(uid1, eid2)

def test_get_assigned_list_not_completed():
    eid1 = create_epic(str(uid1), pid1, "Epic1", "Epic1 Description", "#ffa28e")
    tid1 = create_task(str(uid1), pid1, eid1, [uid1], "Task1", "Task1 Description", "1679749200", None, None, "Completed")
    assigned_list = get_user_assigned_task(uid1, False)
    
    assert assigned_list == []
    delete_task(uid1, tid1)
    delete_epic(uid1, eid1)
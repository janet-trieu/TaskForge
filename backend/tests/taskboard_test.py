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
    eid1 = create_epic(str(uid1), pid1, "Women", "kill all men", "")
    epic = get_epic_details(uid1, eid1)
    delete_epic(uid1, eid1)
    return

def test_create_task():
    eid1 = create_epic(str(uid1), pid1, "Women", "kill all men", "")
    epic = get_epic_details(uid1, eid1)
    tid1 = create_task(str(uid1), pid1, eid1, [uid1], "booties", "bootilicious", "1679749200", None, None, "Not Started")
    print(tid1)
import pytest

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth

from src.error import *
from src.helper import *
from src.profile_page import *
from src.notifications import *
from src.global_counters import *
from src.taskboard import *

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

uid1 = auth.get_user_by_email("taskboardtest1@gmail.com")
uid2 = auth.get_user_by_email("taskboardtest2@gmail.com")
uid3 = auth.get_user_by_email("taskboardtest3@gmail.com")
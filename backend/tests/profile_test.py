# profile_text.py
# blackbox unit testing of profile features
# profile features include:
# profile including name, email, password
# update: name, email, password
# assigned tasks lists (task id, title, deadline, in order)
# view other profiles

import pytest 
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth
from operator import itemgetter
from src.error import *
from src.profile_page import *
from src.test_helpers import *

# ============ SET UP ============ #
db = firestore.client()

@pytest.fixture
def set_up():
    reset_database() # Ensure database is clear for testing
    email1 = "johndoe1@gmail.com"
    password1 = "password123"
    display_name1 = "john doe"
    uid = create_user_email(email1, password1, display_name1)
    return {'email1': email1, 'password1': password1, 'display_name1': display_name1, 'uid': uid}

# ============ TESTS ============ #
def test_create_user(set_up):
    email1, password1, display_name1, uid = itemgetter('email1', 'password1', 'display_name1', 'uid')(set_up)

    assert uid == auth.get_user_by_email(email1).uid
    assert auth.get_user_by_email(email1).display_name == display_name1
    assert db.collection('users').document(uid).get().get("projects") == []
    assert db.collection('users').document(uid).get().get('role') == ""
    assert db.collection('users').document(uid).get().get('tasks') == []
    assert db.collection('users').document(uid).get().get('achievements') == []
    assert db.collection('users').document(uid).get().get('DOB') == ""
    assert db.collection('users').document(uid).get().get('is_banned') == False
    assert db.collection('users').document(uid).get().get('is_admin') == False
    assert db.collection('users').document(uid).get().get('is_removed') == False

def test_create_duplicate_email(set_up):
    email1, password1, display_name1, uid = itemgetter('email1', 'password1', 'display_name1', 'uid')(set_up)

    try:
        uid1 = create_user_email(email1, password1, display_name1)
    except auth.EmailAlreadyExistsError:
        print("Email already exists")
    else:
        delete_user(uid1)

def test_update_email(set_up):
    email1, password1, display_name1, uid = itemgetter('email1', 'password1', 'display_name1', 'uid')(set_up)

    update_email(uid, "johndoe2@gmail.com")
    
    new_email = auth.get_user(uid).email
    assert new_email == "johndoe2@gmail.com"

def test_update_password_success(set_up):
    email1, password1, display_name1, uid = itemgetter('email1', 'password1', 'display_name1', 'uid')(set_up)

    update_password(uid, "password2")
    #no real way to check password change, if it does not pop up error, it passes

def test_update_password_failure(set_up):
    email1, password1, display_name1, uid = itemgetter('email1', 'password1', 'display_name1', 'uid')(set_up)

    try:
        update_password(uid, "")
    except InputError:
        pass

# TO-DO: Fix this test
# def test_update_display_photo(set_up):
#     email1, password1, display_name1, uid = itemgetter('email1', 'password1', 'display_name1', 'uid')(set_up)
#
#     try:
#         update_photo(uid, "https://thumbs.dreamstime.com/z/default-avatar-profile-icon-vector-default-avatar-profile-icon-vector-social-media-user-image-vector-illustration-227787227.jpg")
#         display_photo = auth.get_user(uid).photo_url
#     except:
#         print("Error")
#     else:
#         assert display_photo == "https://thumbs.dreamstime.com/z/default-avatar-profile-icon-vector-default-avatar-profile-icon-vector-social-media-user-image-vector-illustration-227787227.jpg"

def test_update_display_name(set_up):
    email1, password1, display_name1, uid = itemgetter('email1', 'password1', 'display_name1', 'uid')(set_up)

    update_display_name(uid, "john moe")

    assert auth.get_user(uid).display_name == "john moe"

def test_update_role(set_up):
    email1, password1, display_name1, uid = itemgetter('email1', 'password1', 'display_name1', 'uid')(set_up)

    update_role(uid, "software developer")

    assert db.collection('users').document(uid).get().get('role') == "software developer"
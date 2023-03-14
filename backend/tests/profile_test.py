
# profile_text.py
# blackbox unit testing of profile features
# profile features include:
# profile including name, email, password
# update: name, email, password
# assigned tasks lists (task id, title, deadline, in order)
# view other profiles

#import pytest 
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth
from src.profile import *

# Set up
db = firestore.client()

# ============ HELPERS ============ #
email1 = "johndoe1@gmail.com"
password1 = "password123"
display_name1 = "john doe"

def test_create_user():
    uid = create_user_email(email1, password1, display_name1)

    assert uid == auth.get_user_by_email(email1).uid
    assert auth.get_user_by_email(email1).display_name == display_name1
    assert db.collection('users').document(uid).get().get('projects') == []
    assert db.collection('users').document(uid).get().get('role') == ""
    assert db.collection('users').document(uid).get().get('tasks') == []
    assert db.collection('users').document(uid).get().get('achievements') == []
    assert db.collection('users').document(uid).get().get('DOB') == ""
    assert db.collection('users').document(uid).get().get('is_banned') == False
    assert db.collection('users').document(uid).get().get('is_admin') == False
    assert db.collection('users').document(uid).get().get('is_removed') == False

    delete_user(uid)

def test_create_duplicate_email():
    uid = create_user_email(email1, password1, display_name1)
    try:
        uid = create_user_email(email1, password1, display_name1)
    except auth.EmailAlreadyExistsError:
        pass
    delete_user(uid)

def test_update_email():
    uid = create_user_email(email1, password1, display_name1)
    update_email(uid, "johndoe2@gmail.com")
    
    assert auth.get_user(uid).email == "johndoe2@gmail.com"
    delete_user(uid)

def test_update_password_success():
    uid = create_user_email(email1, password1, display_name1)
    
    update_password(uid, "password2")
    #no real way to check password change, if it does not pop up error, it passes
    delete_user(uid)

def test_update_password_failure():
    uid = create_user_email(email1, password1, display_name1)
    try:
        update_password(uid, "")
    except ValueError:
        pass
    delete_user(uid)

def test_update_display_photo():
    uid = create_user_email(email1, password1, display_name1)

    update_photo(uid, "google.com")
    assert auth.get_user(uid).photo_url == "google.com"
    delete_user(uid)

def test_update_display_name():
    uid = create_user_email(email1, password1, display_name1)

    update_display_name(uid, "john moe")

    assert auth.get_user(uid).display_name == "john moe"
    delete_user(uid)

def test_update_role():
    uid = create_user_email(email1, password1, display_name1)

    update_role(uid, "software developer")

    assert db.collection('users').document(uid).get().get('role') == "software developer"
    delete_user(uid)
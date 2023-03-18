# Imports
from firebase_admin import firestore
from firebase_admin import auth

from .global_counters import *
from .classes import User
from .error import *
from .notifications import *

db = firestore.client()

### ========= Functions ========= ###
### ========= Create User ========= ###
def create_user_email(email, password, display_name):
    try:
        user = auth.create_user(
            email = email,
            password = password,
            display_name = display_name
        )
    except auth.EmailAlreadyExistsError:
        print("Email already exists")
    except InputError:
        if display_name == "":
            print("Display name must not be empty")
        if len(password) < 6:
            print("Password must be at least 6 characters long")
        else:
            print("Invalid email address")
    else:   
        create_user_firestore(user.uid)
        update_tuid()
        print('Sucessfully created new user: {0}'.format(user.uid))
        return user.uid

### ========= Delete User ========= ###
def delete_user(uid):
    try:
        auth.delete_user(uid)
        # tuid = get_user_ref(uid).get("tuid")
        db.collection("users").document(str(uid)).delete()
        db.collection('notifications').document(uid).delete()
    except:
        print("uid does not correspond to a current user")
### ========= Updaters ========= ###
### ========= Update email ========= ###
def update_email(uid, new_email):
    # if old email is same as new email, change nothing
    if new_email == get_email(uid):
        return
    try:
        user = auth.update_user(
            uid,
            email = new_email
        )
        print('Sucessfully updated user: {0}'.format(user.uid))
    except InputError:
        print('Invalid email address')

### ========= Update Display Name ========= ###
def update_display_name(uid, new_display_name):
    if new_display_name == "":
        raise InputError("Display name must not be empty")
    else:
        user = auth.update_user(
            uid,
            display_name = new_display_name
        )
        print('Sucessfully updated user: {0}'.format(user.uid))

### ========= Update Password ========= ###
def update_password(uid, new_password):
    if len(new_password) < 6:
        raise InputError("Password must be at least 6 characters long")
    else:
        user = auth.update_user(
            uid,
            display_name = new_password
        )
        print('Sucessfully updated user: {0}'.format(user.uid))

### ========= Update photo ========= ###
def update_photo(uid, new_photo_url):
    # user_ref = db.collection("users").document(uid)
    # user_ref.update({"picture": new_photo_url})
    try:
        user = auth.get_user(uid)
        user = auth.update_user({"photo_url": new_photo_url})
    except:
        print("Error occurred in trying to update user photo")
        print(f"UID: {uid} | new_photo_url: {new_photo_url}")
        print(f"this is user: {user.display_name}")
    else:
        print('Sucessfully updated user: {0}'.format(uid))

### ========= Update Role ========= ###
def update_role(uid, new_role):
    user_ref = db.collection("users").document(uid)
    user_ref.update({"role": new_role})

### ========= Update DOB ========= ###
def update_DOB(uid, new_DOB):
    user_ref = db.collection("users").document(uid)
    user_ref.update({"DOB": new_DOB})

### ========= Getters ========= ###
### ========= get tuid ========= ###
def get_tuid(uid):
    return get_user_ref(uid).get("tuid")

### ========= Get display name ========= ###
def get_display_name(uid):
    return auth.get_user(uid).display_name

### ========= Get photo ========= ###
def get_photo(uid):
    return get_user_ref(uid).get("picture")

### ========= Get email ========= ###
def get_email(uid):
    return auth.get_user(uid).email

### ========= Get Role ========= ###
def get_projects(uid):    
    return get_user_ref(uid).get("role")

### ========= Get DOB ========= ###
def get_DOB(uid):    
    return get_user_ref(uid).get("DOB")

### ========= Get Projects ========= ###
def get_projects(uid):    
    return get_user_ref(uid).get("projects")

### ========= Get Tasks ========= ###
def get_tasks(uid):
    return get_user_ref(uid).get("tasks")

### ========= is admin ========= ###
def is_admin(uid):
    return get_user_ref(uid).get("is_admin")

### ========= is banned ========= ###
def is_banned(uid):
    return get_user_ref(uid).get("is_banned")
    
### ========= is removed ========= ###
def is_removed(uid):
    return get_user_ref(uid).get("is_removed")

### ========= get uid fromemail ========= ###
def get_uid_from_email(email):
    return auth.get_user_by_email(email).uid

### ========= Helper Functions ========= ###
### ========= Create User in Firestore Database ========= ###
def create_user_firestore(uid):
    users_ref = db.collection("users")
    value = get_curr_tuid()
    user = User(uid, value, "", "", "", False, False, False, [], [], [], [])
    
    users_ref.document(uid).set(user.to_dict())

    # Add welcome notification to new user
    notification_welcome(uid)

### ========= get user ref ========= ###
def get_user_ref(uid):
    return db.collection('users').document(uid).get()

### ========= is valid user ========= ###
def is_valid_user(uid):
    try:
        auth.get_user(uid)
    except auth.UserNotFoundError:
        return False
    else:
        return True
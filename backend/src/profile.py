# Imports
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth
from global_counters import *
from classes import *

tu_doc = db.collection("counters").document("total_user")
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
    except ValueError:
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

### ========= Update email ========= ###
def update_email(uid, new_email):
    try:
        user = auth.update_user(
            uid,
            display_name = new_email
        )
        print('Sucessfully updated user: {0}'.format(user.uid))
    except ValueError:
        print('Invalid email address')

### ========= Update Display Name ========= ###
def update_display_name(uid, new_display_name):
    if new_display_name == "":
        raise ValueError("Display name must not be empty")
    else:
        user = auth.update_user(
            uid,
            display_name = new_display_name
        )
        print('Sucessfully updated user: {0}'.format(user.uid))

### ========= Update Password ========= ###
def update_password(uid, new_password):
    if len(new_password) < 6:
        raise ValueError("Password must be at least 6 characters long")
    else:
        user = auth.update_user(
            uid,
            display_name = new_password
        )
        print('Sucessfully updated user: {0}'.format(user.uid))

### ========= Get display name ========= ###
def get_display_name(uid):
    return auth.get_user(uid).display_name

### ========= Get email ========= ###
def get_email(uid):
    return auth.get_user(uid).email

### ========= Get Projects ========= ###
def get_projects(uid):
    user_ref = db.collection("users").document(uid)
    return user_ref.get().get("projects")

### ========= Get Projects ========= ###
def get_tasks(uid):
    user_ref = db.collection("users").document(uid)
    return user_ref.get().get("tasks")

### ========= Helper Functions ========= ###
### ========= Create User in Firestore Database ========= ###
def create_user_firestore(uid):
    users_ref = db.collection("users")
    value = get_curr_tuid()
    user = User(value, uid, False, False, [], [], [])
    
    users_ref.document(str(value)).set(user.to_dict())

#create_user_email("ilovehotstinkymenunderwear@gmail.com", "helloitsmeyourworstnightmarewetsocks", "bleh")
update_display_name("Jgq6jSlxHkYS5gx48REykwCAA0Q2", "bob the builder")
print(get_display_name("Jgq6jSlxHkYS5gx48REykwCAA0Q2"))
print(get_projects("Jgq6jSlxHkYS5gx48REykwCAA0Q2"))
print(get_tasks("Jgq6jSlxHkYS5gx48REykwCAA0Q2"))
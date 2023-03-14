# Imports
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth
from src.global_counters import get_curr_tuid
from src.classes import User


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
        return user.uid

### ========= Delete User ========= ###
def delete_user(uid):
    try:
        auth.delete_user(uid)
        tuid = get_user_ref(uid).get("tuid")
        db.collection("users").document(str(tuid)).delete()
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

### ========= Update photo ========= ###
def update_photo(uid, new_photo_url):
    try:
        user = auth.update_user(
            uid,
            photo_url = new_photo_url
        )
        print('Sucessfully updated user: {0}'.format(user.uid))
    except:  
        print('Unsuccesful photo change')

### ========= Update Role ========= ###
def update_display_name(uid, new_role):
    user_ref = db.collection("users").document(str(get_tuid(uid)))
    user_ref.update({"role": new_role})

### ========= Update DOB ========= ###
def update_DOB(uid, new_DOB):
    user_ref = db.collection("users").document(str(get_tuid(uid)))
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
    return auth.get_user(uid).photo_url

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
    user = User(value, uid, "", "", False, False, False, [], [], [])
    
    users_ref.document(str(value)).set(user.to_dict())

### ========= get user ref ========= ###
def get_user_ref(uid):
    user_ref = db.collection('users').where("uid", "==", uid).stream()
    return list(user_ref)[0].to_dict()
 

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
"""
Creates a User and initialises them into the auth and firestore database.

Args:
    email (str): email of the user
    password (str): password of the user
    display_name (str): display name of the user

Returns:
    str: uid of the user

Raises:
    InputError: an error occured due to the input given from the user
        - Empty display_name
        - Password less than 6 characters
        - Email address is invalid or already taken
"""
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
"""
Deletes User from auth and firestore database

Args:
    uid (str): uid of the user that can be found in auth database

Returns:
    None
"""
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
"""
Updates email of the user identified by Uid in auth database

Args:
    uid (str): uid of the user that can be found in auth database
    new_email (str): new email of the user

Returns:
    None

Raises:
    InputError: The new email address is an invalid email or the email
    address has already been taken 
"""
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
"""
Updates display name of the user identified by Uid in auth database

Args:
    uid (str): uid of the user that can be found in auth database
    new_display_name (str): new display name of the user

Returns:
    None

Raises:
    InputError: The display name is empty
"""
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
"""
Updates password of the user identified by Uid in auth database

Args:
    uid (str): uid of the user that can be found in auth database
    new_password (str): new pasword of the user

Returns:
    None

Raises:
    InputError: The new password is invalid as it is shorter than 6
    characters long
"""
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
"""
Updates photo of the user identified by Uid in auth database

Args:
    uid (str): uid of the user that can be found in auth database
    new_photo_url (str): new photo url of the user

Returns:
    None
"""
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
"""
Updates role of the user identified by Uid in firestore database

Args:
    uid (str): uid of the user that can be found in auth database
    new_role (str): new email of the user

Returns:
    None
"""
def update_role(uid, new_role):
    user_ref = db.collection("users").document(uid)
    user_ref.update({"role": new_role})

### ========= Update DOB ========= ###
"""
Updates Date of Birth of the user identified by Uid in firestore database

Args:
    uid (str): uid of the user that can be found in auth database
    new_DOB (str): new email of the user

Returns:
    None
"""
def update_DOB(uid, new_DOB):
    user_ref = db.collection("users").document(uid)
    user_ref.update({"DOB": new_DOB})

### ========= Getters ========= ###
### ========= get tuid ========= ###
"""
Gets tuid of the User from firestore database

Args:
    uid (str): uid of the user that can be found in auth and firestore database

Returns:
    An int corresponding to the tuid of the user from the firestore. The tuid is
    integer of how many users have been created before the user, in other words, the 
    integer identifier of each user.
"""
def get_tuid(uid):
    return get_user_ref(uid).get("tuid")

### ========= Get display name ========= ###
"""
Gets display name of the User from auth database

Args:
    uid (str): uid of the user that can be found in auth and firestore database

Returns:
    A string corresponding with the display name of the user
    found in auth database
"""
def get_display_name(uid):
    return auth.get_user(uid).display_name

### ========= Get photo ========= ###
"""
Gets photo of the User from auth database

Args:
    uid (str): uid of the user that can be found in auth and firestore database

Returns:
    A string that corresponds to the url link of the photo image
    of the user found in the auth database
"""
def get_photo(uid):
    return get_user_ref(uid).get("picture")

### ========= Get email ========= ###
"""
Gets email of the User from auth database

Args:
    uid (str): uid of the user that can be found in auth and firestore database

Returns:
    A string that corresponds to the email address of the user
"""
def get_email(uid):
    return auth.get_user(uid).email

### ========= Get Role ========= ###
"""
Gets role of the User from firestore database

Args:
    uid (str): uid of the user that can be found in auth and firestore database

Returns:
    A string that corresponds to the role of the user
"""
def get_role(uid):    
    return get_user_ref(uid).get("role")

### ========= Get DOB ========= ###
"""
Gets date of birth of the User from firestore database

Args:
    uid (str): uid of the user that can be found in auth and firestore database

Returns:
    A string that corresponds to the date of birth of the user found in firestore database
"""
def get_DOB(uid):    
    return get_user_ref(uid).get("DOB")

### ========= Get Projects ========= ###
"""
Gets projects of the User from firestore database

Args:
    uid (str): uid of the user that can be found in auth and firestore database

Returns:
    A list of project ids that the user is involved in.
"""
def get_projects(uid):    
    return get_user_ref(uid).get("projects")

### ========= Get Tasks ========= ###
"""
Gets tasks of the User from firestore database

Args:
    uid (str): uid of the user that can be found in auth and firestore database

Returns:
    A list of task ids that the user has been assigned too
"""
def get_tasks(uid):
    return get_user_ref(uid).get("tasks")

### ========= is admin ========= ###
"""
Gets is_admin of the User from auth database

Args:
    uid (str): uid of the user that can be found in auth and firestore database

Returns:
    A Boolean that corresponds to the user's administrator privileges. True for administrator and False
    for normal user.
"""
def is_admin(uid):
    return get_user_ref(uid).get("is_admin")

### ========= is banned ========= ###
"""
Gets is_banned of the User from firestore database

Args:
    uid (str): uid of the user that can be found in auth and firestore database

Returns:
    A Boolean that corresponds to the user's ban status. True for user has been banned and False
    for normal user that should be able to access Task Forge.
"""
def is_banned(uid):
    return get_user_ref(uid).get("is_banned")
    
### ========= is removed ========= ###
"""
Gets is_removed of the User from firestore database

Args:
    uid (str): uid of the user that can be found in auth and firestore database

Returns:
    A Boolean that corresponds to the user's removed status. True for user has been removed and False
    for normal user that should be able to access Task Forge.
"""
def is_removed(uid):
    return get_user_ref(uid).get("is_removed")

### ========= get uid fromemail ========= ###
"""
Gets uid of the User from auth database using email of the user

Args:
    email (str): email of the user that can be found in auth database

Returns:
    A string corresponding with the UID of the user found in the auth and firestore database
"""
def get_uid_from_email(email):
    return auth.get_user_by_email(email).uid

### ========= Helper Functions ========= ###
### ========= Create User in Firestore Database ========= ###
"""
Initialises the user into firestore database and adds notifications to the user

Args:
    uid (str): uid of the user that can be found in auth and firestore database

Returns:
    None
"""
def create_user_firestore(uid):
    users_ref = db.collection("users")
    value = get_curr_tuid()
    user = User(uid, value, "", "", "", False, False, False, [], [], [])
    
    users_ref.document(uid).set(user.to_dict())

    # Add welcome notification to new user
    notification_welcome(uid)

### ========= get user ref ========= ###
"""
Gets user reference of the User from firestore database

Args:
    uid (str): uid of the user that can be found in auth and firestore database

Returns:
    A User document from firestore that corresponds to the UID given. 
"""
def get_user_ref(uid):
    return db.collection('users').document(uid).get()

### ========= is valid user ========= ###
"""
Checks whether a user is a valid user

Args:
    uid (str): uid of the user that can be found in auth and firestore database

Returns:
    A Boolean. True for the UID corresponds with a real user. False for a UID that does
    not exist
"""
def is_valid_user(uid):
    try:
        auth.get_user(uid)
    except auth.UserNotFoundError:
        return False
    else:
        return True
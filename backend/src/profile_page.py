# Imports
from firebase_admin import firestore
from firebase_admin import auth
from .classes import User

from .global_counters import *
from .classes import *
from .error import *
from .notifications import *

db = firestore.client()

### ========= Functions ========= ###
### ========= Create User ========= ###
def create_user_email(email, password, display_name):
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

### ========= Updaters ========= ###
### ========= Update email ========= ###
def update_email(uid, new_email):
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
    """
    Updates photo of the user identified by Uid in auth database

    Args:
        uid (str): uid of the user that can be found in auth database
        new_photo_url (str): new photo url of the user

    Returns:
        None
    """
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
    """
    Updates role of the user identified by Uid in firestore database

    Args:
        uid (str): uid of the user that can be found in auth database
        new_role (str): new email of the user

    Returns:
        None
    """
    user_ref = db.collection("users").document(uid)
    user_ref.update({"role": new_role})

### ========= Update DOB ========= ###
def update_DOB(uid, new_DOB):
    """
    Updates Date of Birth of the user identified by Uid in firestore database

    Args:
        uid (str): uid of the user that can be found in auth database
        new_DOB (str): new email of the user

    Returns:
        None
    """
    user_ref = db.collection("users").document(uid)
    user_ref.update({"DOB": new_DOB})

### ========= Getters ========= ###
### ========= get tuid ========= ###
def get_tuid(uid):
    """
    Gets tuid of the User from firestore database

    Args:
        uid (str): uid of the user that can be found in auth and firestore database

    Returns:
        An int corresponding to the tuid of the user from the firestore. The tuid is
        integer of how many users have been created before the user, in other words, the 
        integer identifier of each user.
    """
    return get_user_ref(uid).get("tuid")

### ========= Get display name ========= ###
def get_display_name(uid):
    """
    Gets display name of the User from auth database

    Args:
        uid (str): uid of the user that can be found in auth and firestore database

    Returns:
        A string corresponding with the display name of the user
        found in auth database
    """
    return auth.get_user(uid).display_name

### ========= Get photo ========= ###
def get_photo(uid):
    """
    Gets photo of the User from auth database

    Args:
        uid (str): uid of the user that can be found in auth and firestore database

    Returns:
        A string that corresponds to the url link of the photo image
        of the user found in the auth database
    """
    return get_user_ref(uid).get("picture")

### ========= Get email ========= ###
def get_email(uid):
    """
    Gets email of the User from auth database

    Args:
        uid (str): uid of the user that can be found in auth and firestore database

    Returns:
        A string that corresponds to the email address of the user
    """
    return auth.get_user(uid).email

### ========= Get Role ========= ###
def get_role(uid):  
    """
    Gets role of the User from firestore database

    Args:
        uid (str): uid of the user that can be found in auth and firestore database

    Returns:
        A string that corresponds to the role of the user
    """
    return get_user_ref(uid).get("role")

### ========= Get DOB ========= ###
def get_DOB(uid): 
    """
    Gets date of birth of the User from firestore database

    Args:
        uid (str): uid of the user that can be found in auth and firestore database

    Returns:
        A string that corresponds to the date of birth of the user found in firestore database
    """   
    return get_user_ref(uid).get("DOB")

### ========= Get Projects ========= ###
def get_projects(uid): 
    """
    Gets projects of the User from firestore database

    Args:
        uid (str): uid of the user that can be found in auth and firestore database

    Returns:
        A list of project ids that the user is involved in.
    """   
    return get_user_ref(uid).get("projects")

### ========= Get Tasks ========= ###
def get_tasks(uid):
    """
    Gets tasks of the User from firestore database

    Args:
        uid (str): uid of the user that can be found in auth and firestore database

    Returns:
        A list of task ids that the user has been assigned too
    """
    return get_user_ref(uid).get("tasks")

### ========= Get Connected TMs ========= ###
def get_connection_list(uid):
    """
    Gets the list of connected TMs uid of the User from firestore database

    Args:
        uid (str): uid of the user that can be found in auth and firestore database

    Returns:
        A list of uids that the user is connected with
    """
    return get_user_ref(uid).get("connections")

### ========= is admin ========= ###
def is_admin(uid):
    """
    Gets is_admin of the User from auth database

    Args:
        uid (str): uid of the user that can be found in auth and firestore database

    Returns:
        A Boolean that corresponds to the user's administrator privileges. True for administrator and False
        for normal user.
    """
    return get_user_ref(uid).get("is_admin")

### ========= is banned ========= ###
def is_banned(uid):
    """
    Gets is_banned of the User from firestore database

    Args:
        uid (str): uid of the user that can be found in auth and firestore database

    Returns:
        A Boolean that corresponds to the user's ban status. True for user has been banned and False
        for normal user that should be able to access Task Forge.
    """
    return get_user_ref(uid).get("is_banned")
    
### ========= is removed ========= ###
def is_removed(uid):
    """
    Gets is_removed of the User from firestore database

    Args:
        uid (str): uid of the user that can be found in auth and firestore database

    Returns:
        A Boolean that corresponds to the user's removed status. True for user has been removed and False
        for normal user that should be able to access Task Forge.
    """
    return get_user_ref(uid).get("is_removed")

### ========= get uid fromemail ========= ###
def get_uid_from_email(email):
    """
    Gets uid of the User from auth database using email of the user

    Args:
        email (str): email of the user that can be found in auth database

    Returns:
        A string corresponding with the UID of the user found in the auth and firestore database
    """
    return auth.get_user_by_email(email).uid

### ========= Helper Functions ========= ###
### ========= Create User in Firestore Database ========= ###
def create_user_firestore(uid):
    """
    Initialises the user into firestore database and adds notifications to the user

    Args:
        uid (str): uid of the user that can be found in auth and firestore database

    Returns:
        None
    """
    
    users_ref = db.collection("users")
    value = get_curr_tuid()
    reputation = {
        'reviews': [],
        'avg_communication': [],
        'avg_time_management': [],
        'avg_task_quality': [],
        'avg': [],
        'visibility': True
    }
    user = User(uid, value, "", "", "", False, False, False, [], [], [], [], [], [], reputation)
    
    print(users_ref.document(uid).set(user.to_dict()))

    # Add welcome notification to new user
    notification_welcome(uid)

### ========= get user ref ========= ###
def get_user_ref(uid):
    """
    Gets user reference of the User from firestore database

    Args:
        uid (str): uid of the user that can be found in auth and firestore database

    Returns:
        A User document from firestore that corresponds to the UID given. 
    """
    return db.collection('users').document(str(uid)).get()

### ========= is valid user ========= ###
def is_valid_user(uid):
    """
    Checks whether a user is a valid user

    Args:
        uid (str): uid of the user that can be found in auth and firestore database

    Returns:
        A Boolean. True for the UID corresponds with a real user. False for a UID that does
        not exist
    """
    try:
        auth.get_user(uid)
    except auth.UserNotFoundError:
        return False
    else:
        return True
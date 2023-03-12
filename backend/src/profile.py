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

### ========= Helper Functions ========= ###
### ========= Create User in Firestore Database ========= ###

def create_user_firestore(uid):
    users_ref = db.collection("users")
    value = get_curr_tuid()
    user = User(value ,uid, False, False, [], [], [])
    
    users_ref.document(str(value)).set(user.to_dict())

create_user_email("ilovehotstinkymenunderwear@gmail.com", "helloitsmeyourworstnightmarewetsocks", "bleh")
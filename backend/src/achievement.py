'''
Feature: Achievements

Functionalities:
 - check_achievement()
 - view_achievements()
 - tba
'''
from .helper import *
from .profile_page import *

def check_achievement(a_type, uid):
    '''
    Check to see if an achievement is able to be acquired
    If requirements are met, grant the achievement to the user
     - This will append the achievement id in the user's doc

    Arguments:
     - a_type (a string value to decipher the type of achievement)
     - uid (user id)

    Returns:
     - True, if achievement is granted
     - False, if not

    Raises:
     - InputError for any incorrect values
    '''
    
    check_valid_uid(uid)

    user_db = db.collection("users").get()
    # print(f"this is user_db: {user_db}")
    # print(f"this is user_db type: {type(user_db)}")

    achievements = get_achievements_uid(uid)

    if a_type == "user_creation":
        if len(user_db) > 1:
            return False
        else:
            achievements.append(0)
            update_achievements(uid, achievements)

    elif a_type == "task_completion":
        pass
    elif a_type == "project_completion":
        pass
    elif a_type == "connection":
        pass
    elif a_type == "task_assigned":
        pass
    elif a_type == "reputation":
        pass
    else:
        raise InputError(f"ERROR: Invalid achievement type specified {a_type}")

    return True

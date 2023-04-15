'''
Feature: Achievements

Functionalities:
 - check_achievement()
 - view_achievements()
 - tba
'''
from .helper import *
from .classes import *
from .notifications import *

import time

def add_achievements():
    '''
    Function to add the achievements to firestore db
    '''
    achievements = {
        0: {
            "aid": 0,
            "title": "Intermediate Task Master",
            "description": "Complete at least 3 assigned tasks",
            "time_acquired": ""
        },
        1: {
            "aid": 1,
            "title": "Advanced Task Master",
            "description": "Complete at least 5 assigned tasks",
            "time_acquired": ""
        },
        2: {
            "aid": 2,
            "title": "Intermediate Project Master",
            "description": "Complete at least 3 projects",
            "time_acquired": ""
        },
        3: {
            "aid": 3,
            "title": "Advanced Project Master",
            "description": "Complete at least 5 projects",
            "time_acquired": ""
        },
        4: {
            "aid": 4,
            "title": "I am bnoc",
            "description": "Have at least 3 connections",
            "time_acquired": ""
        },
        5: {
            "aid": 5,
            "title": "I am Octopus",
            "description": "Have more than 8 tasks assigned at one time",
            "time_acquired": ""
        },
        6: {
            "aid": 6,
            "title": "Woof Woof Lone Wolf",
            "description": "Complete a project with only yourself",
            "time_acquired": ""
        },
        7: {
            "aid": 7,
            "title": "I also leave google restaurant reviews",
            "description": "Leave at least 3 unique reputation reviews",
            "time_acquired": ""
        }
    }

    for key, val in achievements.items():
        db.collection("achievements").document(str(key)).set(val)

def reset_time_acquired(aid):
    '''
    Given an aid, reset the time acquired to ""

    Arguments:
     - aid (achievement id)

    Returns:
     - None
    '''

    achievement = db.collection("achievements").document(str(aid)).get().to_dict()

    achievement.update({"time_acquired": ""})

def give_achievement(uid, aid):
    '''
    Updates the achievements list of the user identified by Uid in firestore database

    Args:
        uid (str): uid of the user that can be found in auth database
        aid (int): aid of the new achievement acquired

    Returns:
        None
    '''
    user_ref = db.collection("users").document(uid)

    new_achievement = get_achievement(aid)
    new_achievement.update({"time_acquired": time.time()})

    user_achievements = user_ref.get().get("achievements")
    user_achievements.append(new_achievement)

    user_ref.update({"achievements": user_achievements})

    notification_achievement(uid, aid)

    reset_time_acquired(aid)

def check_user_has_achievement(uid, aid):
    '''
    Check if the user has already gotten a specific achievement

    Args:
     - uid (str): uid of the user that can be found in auth database
     - aid (int): aid of the achievement to be checked

    Returns:
     - True, if the achievement has already been achieved
     - False, if otherwise
    '''

    curr_achievements = db.collection("users").document(uid).get().get("achievements")
    for ach in curr_achievements:
        if aid == ach["aid"]:
            return True
    return False

def check_lone_wolf(uid):
    '''
    Specific helper to check if a user can get the lone wolf achievement
    - checks if the user has completed a project by themself

    Args:
     - uid (str): uid of the user that can be found in auth database

    Returns:
     - True, if the achievement can be given
     - False, if otherwise
    '''
    user_ref = db.collection("users").document(uid).get()

    for pid in user_ref.get("projects"):
        proj_ref = get_project(pid)
        if len(proj_ref.get("project_members")) == 1 and proj_ref.get("status") == "Completed":
            return True

    return False

def list_unachieved(uid):
    '''
    Specific helper to return a list of achievement ids the user has not achieved

    Args:
     - uid (str): uid of the user that can be found in auth database

    Returns:
     - list of aids that hasnt been achieved
    '''
    achievements = db.collection("users").document(uid).get().get("achievements")
    has_got = []
    for ach in achievements:
        has_got.append(ach["aid"])

    not_got = []
    for i in range(0, 8):
        if i not in has_got:
            not_got.append(i)

    return not_got

def check_achievement(a_type, uid):
    '''
    Check to see if an achievement is able to be acquired
    If requirements are met, grant the achievement to the user
     - This will append the achievement id in the user's doc

    Arguments:
     - a_type (a string value to decipher the type of achievement)
     - uid (user id)

    Returns:
     - 0, if achievement is granted
     - 1 or err if not

    Raises:
     - InputError for any incorrect values
    '''

    # user_ref = get_user_ref(uid)
    user_ref = db.collection("users").document(uid).get()

    if a_type == "task_completion":
        n_tasks = user_ref.get("num_tasks_completed")
        if n_tasks >= 3 and check_user_has_achievement(uid, 0) == False:
            give_achievement(uid, 0)
        elif n_tasks >= 5 and check_user_has_achievement(uid, 1) == False:
            give_achievement(uid, 1)
        else:
            return 1
    elif a_type == "project_completion":
        n_projs = user_ref.get("num_projs_completed")
        if n_projs >= 3 and check_user_has_achievement(uid, 2) == False:
            give_achievement(uid, 2)
        elif n_projs >= 5 and check_user_has_achievement(uid, 3) == False:
            give_achievement(uid, 3)
        elif check_lone_wolf(uid) == True and check_user_has_achievement(uid, 6) == False:
            give_achievement(uid, 6)
        else:
            return 1
    elif a_type == "connection":
        n_conns = len(db.collection("users").document(uid).get().get("connections"))
        if n_conns >= 3 and check_user_has_achievement(uid, 4) == False:
            give_achievement(uid, 4)
        else:
            return 1
    elif a_type == "task_assigned":
        n_assigned = len(db.collection("users").document(uid).get().get("tasks"))
        if n_assigned >= 8 and check_user_has_achievement(uid, 5) == False:
            give_achievement(uid, 5)
        else:
            return 1
    elif a_type == "reputation":
        n_reviews = get_number_of_reviews_written(uid)
        if n_reviews >= 3 and check_user_has_achievement(uid, 7) == False:
            give_achievement(uid, 7)
        else:
            return 1
    else:
        raise InputError(f"ERROR: Invalid achievement type specified {a_type}")

    return 0

def view_achievement(uid):
    '''
    View the list of achievements

    Arguments:
     - uid (user id)

    Returns:
     - list of achievements

    Raises:
     - None
    '''

    check_valid_uid(uid)

    curr_achievements = db.collection("users").document(uid).get().get("achievements")

    return curr_achievements

def view_connected_tm_achievement(uid, conn_uid):
    '''
    View a connected Task Master's achievements
    If the two users are connected and their visibility setting doesn't forbid, view achievements

    Arguments:
     - uid (user id)
     - conn_uid (uid to view their achievements)

    Returns:
     - list of achievements
     - err

    Raises:
     - AccessError if uid is not connected  
    '''
    user_ref = db.collection("users").document(uid).get()

    if conn_uid not in user_ref.get("connections"):
        raise AccessError("ERROR: uid is not connected")

    conn_user_ref = db.collection("users").document(conn_uid).get()
    hidden = conn_user_ref.get("hide_achievements")
    if hidden == True:
        return []

    curr_achievements = db.collection("users").document(conn_uid).get().get("achievements")

    return curr_achievements

def toggle_achievement_visibility(uid, action):
    '''
    Toggle on, or off the visibility of the user's achievements
     - if on, the achievements are only visible to the user

    Arguments:
     - uid (user id)
     - action (int, 0 to toggle on, 1 to toggle off)

    Returns:
     - None

    Raises:
     - InputError if attempt to toggle on when visibility if already on (True), or otherwise same for off
    '''
    user_ref = db.collection("users").document(uid)

    hidden = user_ref.get().get("hide_achievements")

    if action == 0 and hidden == True:
        raise InputError("ERROR: Visibility is already toggled ON")
    elif action == 1 and hidden == False:
        raise InputError("ERROR: Visibility is already toggled OFF")
    
    if action == 0:
        user_ref.update({"hide_achievements": True})
    elif action == 1:
        user_ref.update({"hide_achievements": False})

def share_achievement(uid, receiver_uids, aid):
    '''
    Share an achievements a user has gotten, to other connected TMs
     - this is done through sending a notification to them

    Arguments:
     - uid (user id)
     - receiver_uids (uids to send)
     - aid (aid to be shared)

    Returns:
     - 0 for success
     - err

    Raises:
     - 
    '''
    user_ref = db.collection("users").document(uid)

    if aid in list_unachieved(uid):
        raise InputError("ERROR: Cannot share an achievement you have not gotten")
         
    for id in receiver_uids:
        if id not in user_ref.get().get("connections"):
            raise InputError("ERROR: Cannot share to a TM you are not connected with")

        notification_achievement_share(uid, id, aid)
    
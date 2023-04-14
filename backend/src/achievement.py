'''
Feature: Achievements

Functionalities:
 - check_achievement()
 - view_achievements()
 - tba
'''
from .helper import *
from .profile_page import *
from .classes import *
import time

def add_achievements():

    achievements = {
        0: {
            "aid": 0,
            "title": "Intermediate Task Master",
            "description": "Complete at least 3 assigned tasks",
            "icon": "abc",
            "time_acquired": ""
        },
        1: {
            "aid": 1,
            "title": "Advanced Task Master",
            "description": "Complete at least 5 assigned tasks",
            "icon": "abc",
            "time_acquired": ""
        },
        2: {
            "aid": 2,
            "title": "Intermediate Project Master",
            "description": "Complete at least 3 projects",
            "icon": "abc",
            "time_acquired": ""
        },
        3: {
            "aid": 3,
            "title": "Advanced Project Master",
            "description": "Complete at least 5 projects",
            "icon": "abc",
            "time_acquired": ""
        },
        4: {
            "aid": 4,
            "title": "I am bnoc",
            "description": "Have at least 3 connections",
            "icon": "abc",
            "time_acquired": ""
        },
        5: {
            "aid": 5,
            "title": "I also leave google restaurant reviews",
            "description": "Leave at least 3 unique reputation reviews",
            "icon": "abc",
            "time_acquired": ""
        },
        6: {
            "aid": 6,
            "title": "I am Octopus",
            "description": "Have more than 8 tasks assigned at one time",
            "icon": "abc",
            "time_acquired": ""
        },
        7: {
            "aid": 7,
            "title": "Woof Woof Lone Wolf",
            "description": "Complete a project with only yourself",
            "icon": "abc",
            "time_acquired": ""
        }
    }

    for key, val in achievements.items():
        db.collection("achievements").document(str(key)).set(val)

def get_achievement(aid):

    achievement = db.collection("achievements").document(str(aid)).get().to_dict()

    achievement.update({"time_acquired": time.time()})

    return achievement

def reset_time_acquired(aid):

    achievement = db.collection("achievements").document(str(aid)).get().to_dict()

    achievement.update({"time_acquired": ""})

    return achievement

def give_achievement(uid, aid):
    """
    Updates the achievements list of the user identified by Uid in firestore database

    Args:
        uid (str): uid of the user that can be found in auth database
        aid (int): aid of the new achievement acquired

    Returns:
        None
    """
    user_ref = db.collection("users").document(uid)

    new_achievement = get_achievement(aid)

    user_achievements = user_ref.get().get("achievements")
    user_achievements.append(new_achievement)

    user_ref.update({"achievements": user_achievements})

    reset_time_acquired(aid)

def check_user_has_achievement(uid, aid):
    curr_achievements = get_user_achievements(uid)
    for ach in curr_achievements:
        if aid == ach["aid"]:
            return True
    return False

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

    user_ref = get_user_ref(uid)

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
        else:
            return 1
    elif a_type == "connection":
        n_conns = len(get_connection_list(uid))
        print(n_conns)
        if n_conns >= 3 and check_user_has_achievement(uid, 4) == False:
            give_achievement(uid, 4)
        else:
            return 1
    elif a_type == "task_assigned":
        pass
    elif a_type == "reputation":
        pass
    else:
        raise InputError(f"ERROR: Invalid achievement type specified {a_type}")

    return 0

'''
Feature: Achievements

Functionalities:
 - check_achievement()
 - view_achievements()
 - tba
'''
from .helper import *
from .profile_page import *
import time

def add_achievements():

    achievements = {
        0: {
            "aid": 0,
            "title": "Almost Admin",
            "description": "The very first user",
            "icon": "abc",
            "time_acquired": ""
        },
        1: {
            "aid": 1,
            "title": "TBA",
            "description": "First Task Master to complete a task",
            "icon": "abc",
            "time_acquired": ""
        },
        2: {
            "aid": 2,
            "title": "TBA",
            "description": "First Project Master to complete a project",
            "icon": "abc",
            "time_acquired": ""
        },
        3: {
            "aid": 3,
            "title": "Intermediate Task Master",
            "description": "Complete at least 10 assigned tasks",
            "icon": "abc",
            "time_acquired": ""
        },
        4: {
            "aid": 4,
            "title": "Advanced Task Master",
            "description": "Complete at least 20 assigned tasks",
            "icon": "abc",
            "time_acquired": ""
        },
        5: {
            "aid": 5,
            "title": "Intermediate Project Master",
            "description": "Complete at least 5 projects",
            "icon": "abc",
            "time_acquired": ""
        },
        6: {
            "aid": 6,
            "title": "Advanced Project Master",
            "description": "Complete at least 10 projects",
            "icon": "abc",
            "time_acquired": ""
        },
        7: {
            "aid": 7,
            "title": "I am bnoc",
            "description": "Have at least 5 connections",
            "icon": "abc",
            "time_acquired": ""
        },
        8: {
            "aid": 8,
            "title": "I also leave google restaurant reviews",
            "description": "Leave at least 10 unique reputation reviews",
            "icon": "abc",
            "time_acquired": ""
        },
        9: {
            "aid": 9,
            "title": "Problem Solver",
            "description": "Reputation of teamwork and communication over 4/5",
            "icon": "abc",
            "time_acquired": ""
        },
        10: {
            "aid": 10,
            "title": "Fast as Lightning",
            "description": "Complete a task within the first half of deadline",
            "icon": "abc",
            "time_acquired": ""
        },
        11: {
            "aid": 11,
            "title": "There is no 'I' in team",
            "description": "Reputation of teamwork over 4.5/5",
            "icon": "abc",
            "time_acquired": ""
        },
        12: {
            "aid": 12,
            "title": "Megaphone",
            "description": "Reputation of communication over 4.5/5",
            "icon": "abc",
            "time_acquired": ""
        },
        13: {
            "aid": 13,
            "title": "Michelangelo.. is that mE?",
            "description": "Reputation of quality over 4.5/5",
            "icon": "abc",
            "time_acquired": ""
        },
        14: {
            "aid": 14,
            "title": "I am Octopus",
            "description": "Have more than 8 tasks assigned at one time",
            "icon": "abc",
            "time_acquired": ""
        },
        15: {
            "aid": 15,
            "title": "Look at me, I'm StackOverflow Now",
            "description": "Overall Reputation over 4.5/5",
            "icon": "abc",
            "time_acquired": ""
        },
        16: {
            "aid": 16,
            "title": "Woof Woof Lone Wolf",
            "description": "Complete a project with only yourself",
            "icon": "abc",
            "time_acquired": ""
        }
    }

    for key,val in achievements.items():
        db.collection("achievements").document(str(key)).set(val)

def get_achievement(aid):
    return db.collection("achievements").document(str(aid)).to_dict()

def update_time_acquired(aid):
    achievement = get_achievement(aid)

    achievement.update({"time_acquired": time.time()})

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

    achievements = get_achievements_list(uid)

    if a_type == "user_creation":
        if len(user_db) > 1:
            return False
        else:
            achievement = get_achievement(0)
            update_time_acquired(0)

            achievements.append(achievements)
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

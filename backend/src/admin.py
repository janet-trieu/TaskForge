from .profile_page import *
from .error import *
from firebase_admin import auth
'''
Feature: Admin
Functionalities:
    - give_admin
    - ban_user
    - unban_user
    - remove_user
    - readd_user
'''


def give_admin(uid_admin, uid_user):
    '''
    Takes 2 users, 1st being an admin, 2nd one not, and makes 2nd user an admin
    Args:
        - uid_admin(string): uid of the admin giving admin status
        - uid_user(string): uid of user who will be given admin status
    '''
    if (not isinstance(uid_admin, str) or not isinstance(uid_user, str)): raise InputError('uids should be strings')
    if (not get_user_ref(uid_admin) or not get_user_ref(uid_user)): raise InputError('uid invalid')
    if (is_banned(uid_admin)): raise AccessError('You are banned')
    if (is_banned(uid_user)): raise InputError('Cannot make a banned user an admin')
    if (not is_admin(uid_admin)): raise InputError('You are not an admin')
    if (is_admin(uid_user)): raise InputError('User is already an admin')
    
    user_ref = db.collection("users").document(uid_user)
    user_ref.update({'is_admin': True})
    return {}
    

def ban_user(uid_admin, uid_user):
    '''
    Admin bans a user/admin
    Args:
        - uid_admin(string): uid of the admin banning user
        - uid_user(string): uid of user who will be banned
    '''
    if (not isinstance(uid_admin, str) or not isinstance(uid_user, str)): raise InputError('uids are strings')
    if (not get_user_ref(uid_admin) or not get_user_ref(uid_user)): raise InputError('uid invalid')
    if (is_banned(uid_admin)): raise AccessError('You are banned')
    if (not is_admin(uid_admin)): raise InputError('You are not an admin')
    if (is_banned(uid_user)): raise InputError('User is already banned')
    
    user_ref = db.collection("users").document(uid_user)
    user_ref.update({'is_banned': True})
    #auth.update_user(uid_user, disabled=True)
    return {}


def unban_user(uid_admin, uid_user):
    '''
    Admin removes a ban from a banned user
    Args:
        - uid_admin(string): uid of the admin unbanning banned user
        - uid_user(string): uid of user who will be unbanned
    '''
    if (not isinstance(uid_admin, str) or not isinstance(uid_user, str)): raise InputError('uids are strings')
    if (not get_user_ref(uid_admin) or not get_user_ref(uid_user)): raise InputError('uid invalid')
    if (is_banned(uid_admin)): raise AccessError('You are banned')
    if (not is_admin(uid_admin)): raise InputError('You are not an admin')
    if (not is_banned(uid_user)): raise InputError('User is not banned')
    
    user_ref = db.collection("users").document(uid_user)
    user_ref.update({'is_banned': False})
    #auth.update_user(uid_user, disabled=False)
    return {}


def remove_user(uid_admin, uid_user):
    '''
    Similar to ban, but removal is used for very long inactivity or other reasons
    User is deleted along with task assignee, subtask assignee and project member
    Args:
        - uid_admin(string): uid of the admin removing a user
        - uid_user(string): uid of user who will be removed
    '''
    if (not isinstance(uid_admin, str) or not isinstance(uid_user, str)): raise InputError('uids are strings')
    if (not get_user_ref(uid_admin) or not get_user_ref(uid_user)): raise InputError('uid invalid')
    if (is_banned(uid_admin)): raise AccessError('You are banned')
    if (not is_admin(uid_admin)): raise InputError('You are not an admin')
    
    #delete from auth db
    auth.delete_user(uid_user)
    
    #delete user field
    db.collection('users').document(uid_user).delete()
    
    #delete notifications of users
    db.collection('notifications').document(uid_user).delete()
    
    
    #remove from projects
    projs = db.collection('users').document(uid_user).get().get("projects")
    if (projs is not None):
        for proj in projs:
            proj_mems = db.collection('projects').document(proj).get().get('project_members')
            proj_mems.remove(uid_user)
            if (proj_mems == ""):
                db.collection('projects').document(proj).delete()
            db.collection("project").document(uid_user).update({"project_members": proj_mems})
        
    #remove from tasks
    tasks = db.collection('users').document(uid_user).get().get("tasks")
    if (tasks is not None):
        for task in tasks:
            assignees = db.collection('tasks').document(task).get().get('assignees')
            assignees.remove(uid_user)
            db.collection("tasks").document(uid_user).update({"assignees": assignees})
    
    #remove from subtasks
    subtasks = db.collection('users').document(uid_user).get().get("subtasks")
    if (subtasks is not None):
        for subtask in subtasks:
            assignees = db.collection('subtasks').document(subtask).get().get('assignees')
            assignees.remove(uid_user)
            db.collection("subtasks").document(uid_user).update({"assignees": assignees})
    
    return {}

from .profile_page import *
from .error import *
'''
Feature: Admin
Functionalities:
    - give_admin
    - ban_user
    - unban_user
    - remove_user
    - readd_user
'''

'''
Takes 2 users, 1st being an admin, 2nd one not, and makes 2nd user an admin
Args:
    - uid_admin(string): uid of the admin giving admin status
    - uid_user(string): uid of user who will be given admin status
'''
def give_admin(uid_admin, uid_user): 
    if (not isinstance(uid_admin, str) or not isinstance(uid_user, str)): raise InputError('uids should be strings')
    if (not get_user_ref(uid_admin) or not get_user_ref(uid_user)): raise InputError('uid invalid')
    if (is_banned(uid_admin)): raise AccessError('You are banned')
    if (is_banned(uid_user)): raise InputError('Cannot make a banned user an admin')
    if (not is_admin(uid_admin)): raise InputError('You are not an admin')
    if (is_admin(uid_user)): raise InputError('User is already an admin')
    
    user_ref = db.collection("users").document(uid_user)
    user_ref.update({'is_admin': True})
    return {}
    
'''
Admin bans a user/admin
Args:
    - uid_admin(string): uid of the admin banning user
    - uid_user(string): uid of user who will be banned
'''
def ban_user(uid_admin, uid_user):  
    if (not isinstance(uid_admin, str) or not isinstance(uid_user, str)): raise InputError('uids are strings')
    if (not get_user_ref(uid_admin) or not get_user_ref(uid_user)): raise InputError('uid invalid')
    if (is_banned(uid_admin)): raise AccessError('You are banned')
    if (not is_admin(uid_admin)): raise InputError('You are not an admin')
    if (is_banned(uid_user)): raise InputError('User is already banned')
    
    user_ref = db.collection("users").document(uid_user)
    user_ref.update({'is_banned': True})
    return {}

'''
Admin removes a ban from a banned user
Args:
    - uid_admin(string): uid of the admin unbanning banned user
    - uid_user(string): uid of user who will be unbanned
'''
def unban_user(uid_admin, uid_user): 
    if (not isinstance(uid_admin, str) or not isinstance(uid_user, str)): raise InputError('uids are strings')
    if (not get_user_ref(uid_admin) or not get_user_ref(uid_user)): raise InputError('uid invalid')
    if (is_banned(uid_admin)): raise AccessError('You are banned')
    if (not is_admin(uid_admin)): raise InputError('You are not an admin')
    if (not is_banned(uid_user)): raise InputError('User is not banned')
    
    user_ref = db.collection("users").document(uid_user)
    user_ref.update({'is_banned': False})
    return {}

'''
Similar to ban, but removal is used for very long inactivity or other reasons
Args:
    - uid_admin(string): uid of the admin removing a user
    - uid_user(string): uid of user who will be removed
'''
def remove_user(uid_admin, uid_user):
    if (not isinstance(uid_admin, str) or not isinstance(uid_user, str)): raise InputError('uids are strings')
    if (not get_user_ref(uid_admin) or not get_user_ref(uid_user)): raise InputError('uid invalid')
    if (is_banned(uid_admin)): raise AccessError('You are banned')
    if (not is_admin(uid_admin)): raise InputError('You are not an admin')
    if (is_removed(uid_user)): raise InputError('User is already removed')
    
    #delete user field
    user_ref = db.collection('users').document(uid_user)
    user_ref.update({uid_user: firestore.DELETE_FIELD})
    
    #delete notifications of users
    user_ref = db.collection('notifications').document(uid_user)
    user_ref.update({uid_user: firestore.DELETE_FIELD})
    
    #remove from projects
    projs = db.collection('users').document(uid_user).get().get("projects")
    for proj in projs:
        proj_mems = db.collection('projects').document(proj).get().get('project_members')
        proj_mems.remove(uid_user)
        db.collection("project").document(uid_user).update({"project_members": proj_mems})
        
    #remove from tasks
    tasks = db.collection('users').document(uid_user).get().get("tasks")
    for task in tasks:
        assignees = db.collection('tasks').document(task).get().get('assignees')
        assignees.remove(uid_user)
        db.collection("tasks").document(uid_user).update({"assignees": assignees})
        
    return {}

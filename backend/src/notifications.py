'''
Feature: Notifications
Functionalities:
 - get_uid_from_email2()
 - create_nid()
 - is_connected()
 - get_notifications()
 - clear_notification()
 - clear_all_notifications()
 - notification_welcome()
 - notification_connection_request()
 - notification_project_invite()
 - notification_assigned_task()
 - notification_comment()
 - notification_review()
 - notification_achievement()
 - notification_achievement_share()
 - notification_leave_request()
 - notification_accepted_request()
 - notification_denied_request()
'''
from firebase_admin import firestore, auth
from datetime import datetime
from .error import *
from .helper import *

db = firestore.client()

# ============ HELPERS ============ #
def get_uid_from_email2(email):
    """
    Gets uid of the User from auth database using email of the user
    Args:
        email (str): email of the user that can be found in auth database
    Returns:
        A string corresponding with the UID of the user found in the auth and firestore database
    """
    return auth.get_user_by_email(email).uid

def create_nid(uid, type):
    '''
    Creates notification ID based on the type and how many currently exists
    Args:
        uid (str): User ID
        type (str): Notification type
    Returns:
        nid (str): Notification ID
    '''
    doc_dict = db.collection('notifications').document(uid).get().to_dict()
    if (doc_dict is None):
        count = 0
    else:
        count = sum(type in key for key in doc_dict.keys()) # sum of existing notifications of same type
    nid = f'{type}{count}'
    
    # If nid exists, increment count and update nid and check again until unique
    while does_nid_exists(uid, nid):
        count += 1
        nid = f'{type}{count}'

    return nid

def is_connected(uid1, uid2):
    '''
    Helper to check if two users are connected
    Args:
        uid1 (str): User ID of first user
        uid2 (str): User ID of second user
    Returns:
        (boolean): If users are connected
    Assume uids have already been checked as existing
    '''
    connections = db.collection('users').document(uid1).get().to_dict().get('connections')
    if (connections is None): return False
    if (uid2 in connections): return True
    return False
    
# ============ FUNCTIONS ============ #
def get_notifications(uid):
    '''
    Get the user's notifications in descending time order.
    Args:
        uid (string): User getting notifications
    Returns:
        sorted_notifications (list): List of dictionaries of user's notifications sorted by descending timestamps
    '''
    check_valid_uid(uid)

    notf_data = db.collection('notifications').document(str(uid)).get().to_dict()

    # Sort notification dictionaries by time_sent in descending order
    sorted_notifications = sorted(notf_data.values(), key=lambda x: x['time_sent'], reverse=True)

    return sorted_notifications

def clear_notification(uid, nid):
    '''
    Clears a user's specific notification
    Args:
        uid (string): User with notification to delete
        nid (string): Notification ID of notification being deleted
    '''
    check_valid_uid(uid)
    doc_ref = db.collection('notifications').document(uid)
    doc_ref.update({
        nid: firestore.DELETE_FIELD
    })

def clear_all_notifications(uid):
    '''
    Clears all the user's notification
    Args:
        uid (string): User with notifications to delete
    '''
    check_valid_uid(uid)
    notf_data = db.collection('notifications').document(uid)
    notf_data.set({}) #set to nothing

def notification_welcome(uid):
    '''
    Welcome message to new user.
    Args:
        uid (string): User being notified
    Returns:
        nid (string): Notification ID of newly created notification
    ASSUMPTION that this function is called ONCE per user.
    '''
    nid = 'welcome'
    name = get_display_name(uid)

    notification = {
        'welcome' : {
            "has_read": False,
            "notification_msg": f"Welcome to TaskForge, {name}. You can view future notifications here!",
            "time_sent": str(datetime.now()),
            "type": nid,
            "nid": nid
        }
    }

    db.collection("notifications").document(uid).set(notification)
    return nid

def notification_connection_request(user_email, uid_sender):
    '''
    Creates and adds notification when a user requests to connect another user.
    Args:
        user_email (string): Email of user being notified
        uid_sender (string): User who requests to connect
    Returns:
        nid (string): Notification ID of newly created notification
    '''
    uid = auth.get_user_by_email(user_email).uid # get uid of requestee by email
    if (uid == uid_sender): raise AccessError('Cant connect to yourself')
    check_valid_uid(uid_sender)

    if (is_connected(uid, uid_sender)): raise AccessError('Already connected')

    notification_type = 'connection_request'
    nid = create_nid(uid, notification_type) # create notification ID
    sender_name = auth.get_user(uid_sender).display_name

    notification = {
        nid : {
            "has_read": False,
            "notification_msg": f"{sender_name} has requested to connect.",
            "time_sent": str(datetime.now()),
            "type": notification_type,
            "uid_sender": uid_sender,
            "nid": nid
        }
    }

    db.collection("notifications").document(str(uid)).update(notification)

    return nid

def notification_project_invite(uid, uid_sender, pid):
    '''
    Creates and adds notification when a user invites another user to a project.
    Args:
        uid (string): User being notified
        uid_sender (string): User that is inviting to the project
        pid (int): Project being invited to
    Returns:
        nid (string): Notification ID of newly created notification
    ASSUMPTION that the user sending is in project + user receiving is not in project + do not have an existing request (+ possibly need to be connected?)
    '''

    notification_type = 'project_invite'
    nid = create_nid(uid, notification_type) # create notification ID
    sender_name =  auth.get_user(uid_sender).display_name
    project_name = db.collection("projects").document(str(pid)).get().get('name')

    notification = {
        nid : {
            "has_read": False,
            "notification_msg": f"{sender_name} has invited you to join {project_name}.",
            "pid": pid,
            "time_sent": str(datetime.now()),
            "type": notification_type,
            "uid_sender": uid_sender,
            "response": False,
            "nid": nid
        }
    }

    db.collection("notifications").document(uid).update(notification)
    return nid

def notification_assigned_task(uid, pid, tid):
    '''
    Creates and adds notification when a user is assigned a task in a project.
    Args:
        uid (string): User being notified
        pid (int): Project the task is located in
        tid (int): Task being assigned
    Returns:
        nid (string): Notification ID of newly created notification
    ASSUMPTION that the user is in project + task is in project
    '''

    notification_type = 'assigned_task'
    nid = create_nid(uid, notification_type) # create notification ID
    project_name = db.collection("projects").document(str(pid)).get().get('name')
    task_name = get_task_name(tid)

    notification = {
        nid : {
            "has_read": False,
            "notification_msg": f"You have been assigned {task_name} in {project_name}.",
            "pid": pid,
            "tid": tid,
            "time_sent": str(datetime.now()),
            "type": notification_type,
            "nid": nid
        }
    }

    db.collection("notifications").document(uid).update(notification)
    return nid

def notification_comment(uid, uid_sender, pid, tid):
    '''
    Creates and adds notification when a comment is added to a user's assigned task in a project.
    Args:
        uid (string): User being notified
        uid_sender (string): User who commented
        pid (int): Project the task is in
        tid (int): Task that was commented in
    Returns:
        nid (string): Notification ID of newly created notification
    ASSUMPTION that the user is in the project + task is in the project + user was assigned the task
    '''

    notification_type = 'comment'
    nid = create_nid(uid, notification_type) # create notification ID
    sender_name = get_display_name(uid_sender)
    project_name = get_project_name(pid)
    task_name = get_task_name(tid)

    notification = {
        nid : {
            "has_read": False,
            "notification_msg": f"{sender_name} has commented in {task_name} in {project_name}.",
            "pid": pid,
            "tid": tid,
            "time_sent": str(datetime.now()),
            "type": notification_type,
            "uid_sender": uid_sender,
            "nid": nid
        }
    }

    db.collection("notifications").document(uid).update(notification)
    return nid

def notification_review(uid, uid_sender):
    '''
    Creates and adds notification when a review is added to a user's profile.
    Args:
        uid (string): User being notified
        uid_sender (string): User who made review
    Returns:
        nid (string): Notification ID of newly created notification
    ASSUMPTION that the users are connected(?)
    '''

    notification_type = 'review'
    nid = create_nid(uid, notification_type) # create notification ID
    sender_name = get_display_name(uid_sender)

    notification = {
        nid : {
            "has_read": False,
            "notification_msg": f"{sender_name} has reviewed you.",
            "time_sent": str(datetime.now()),
            "type": notification_type,
            "uid_sender": uid_sender,
            "nid": nid
        }
    }

    db.collection("notifications").document(uid).update(notification)
    return nid

def notification_achievement(uid, aid):
    '''
    Creates and adds notification when an achievement has been completed.
    Args:
        uid (string): User being notified
        aid (int): Achievement that has been completed
    Returns:
        nid (string): Notification ID of newly created notification
    ASSUMPTION that the achievement has been fulfilled
    '''

    notification_type = 'achievement'
    nid = create_nid(uid, notification_type) # create notification ID
    achievement = get_achievement(aid)
    title = achievement.get("title")

    notification = {
        nid : {
            "achievement": title,
            "aid": aid,
            "has_read": False,
            "notification_msg": f"You have earned the {title} achievement.",
            "time_sent": str(datetime.now()),
            "type": notification_type,
            "nid": nid
        }
    }

    db.collection("notifications").document(uid).update(notification)
    return nid

def notification_achievement_share(uid, receiver_uid, aid):
    '''
    Shares the achievement that has been achieved
    Args:
        uid (string): User being notified
        aid (int): Achievement that has been completed
    Returns:
        nid (string): Notification ID of newly created notification
    ASSUMPTION that the achievement has been fulfilled
    '''

    notification_type = 'achievement_shared'
    nid = create_nid(uid, notification_type) # create notification ID
    achievement = get_achievement(aid)
    title = achievement.get("title")
    achiever_name = auth.get_user(uid).display_name

    notification = {
        nid : {
            "achievement": title,
            "aid": aid,
            "has_read": False,
            "notification_msg": f"{achiever_name} has earned the {title} achievement.",
            "time_sent": str(datetime.now()),
            "type": notification_type,
            "nid": nid
        }
    }

    db.collection("notifications").document(receiver_uid).update(notification)
    return nid

def notification_leave_request(uid, uid_sender, pid):
    '''
    Creates and adds notification when a user requests to leave a project to the project master.
    Args:
        uid (string): The project master
        uid_sender (string): User sending leave request
        pid (int): Project being left
    Returns:
        nid (string): Notification ID of newly created notification
    ASSUMPTION that the users are in project + user notified is project master
    '''

    notification_type = 'leave_request'
    nid = create_nid(uid, notification_type) # create notification ID
    sender_name = get_display_name(uid_sender)
    project_name = get_project_name(pid)

    notification = {
        nid : {
            "has_read": False,
            "notification_msg": f"{sender_name} has requested to leave {project_name}.",
            "pid": pid,
            "time_sent": str(datetime.now()),
            "type": notification_type,
            "uid_sender": uid_sender,
            "nid": nid
        }
    }

    db.collection("notifications").document(uid).update(notification)
    return nid

def notification_accepted_request(uid, uid_sender):
    '''
    Creates and add notification when a user's request was accepted.
    This is non-specific for simplicity sake can refer to:
        -connection request, project invite, leave request
    Args:
        uid (string): User being notified and who sent the request
        uid_sender (string): User who has responded to the request
    Returns:
        nid (string): Notification ID of newly created notification
    ASSUMPTION that the user has sent a request + respondee has accepted
    '''
    notification_type = 'accepted_request'
    nid = create_nid(uid, notification_type) # create notification ID
    sender_name = get_display_name(uid_sender)

    notification = {
        nid : {
            "has_read": False,
            "notification_msg": f"{sender_name} has accepted your request.",
            "time_sent": str(datetime.now()),
            "type": notification_type,
            "uid_sender": uid_sender,
            "nid": nid
        }
    }

    from .achievement import check_achievement
    check_achievement("connection", uid)

    db.collection("notifications").document(uid).update(notification)
    return nid

def notification_denied_request(uid, uid_sender):
    '''
    Creates and add notification when a user's request was denied.
    This is non-specific for simplicity sake can refer to:
        -connection request, project invite, leave request
    Args:
        uid (string): User being notified and who sent the request
        uid_sender (string): User who has responded to the request
    Returns:
        nid (string): Notification ID of newly created notification
    ASSUMPTION that the user has sent a request + respondee has denied
    '''
    notification_type = 'denied_request'
    nid = create_nid(uid, notification_type) # create notification ID
    sender_name = get_display_name(uid_sender)

    notification = {
        nid : {
            "has_read": False,
            "notification_msg": f"{sender_name} has denied your request.",
            "time_sent": str(datetime.now()),
            "type": notification_type,
            "uid_sender": uid_sender,
            "nid": nid
        }
    }

    db.collection("notifications").document(uid).update(notification)
    return nid
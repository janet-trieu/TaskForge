'''
Frontend notes: 
- unread indicator + tab
- clicking on the notification makes it read - change has_read to True
- responding to responsive notifications makes it read - change has_read to True
- responsive notifications have special message fields when the user 'accepts' or 'declines'
    - so we dont have to worry about deleting the notification and the user remembers what they responded
    - e.g. user presses accept to connection request. the notification text is changed from 'notification_msg' to 'accept_msg'
TODO notes:
- When task, reviews, achievements are implemented - this may need to be updated to suit the databases of them :)
- ASSUMPTION should be covered by the function the notfiication is called in
'''
from firebase_admin import firestore
from datetime import datetime

from src.helper import *

db = firestore.client()

# ============ HELPERS ============ #

def does_nid_exists(uid, nid):
    doc_ref = db.collection('notifications').document(uid)

    # Check if field name exists in document
    if nid in doc_ref.get().to_dict():
        return True
    else:
        return False

def create_nid(uid, type):
    doc_dict = db.collection('notifications').document(uid).get().to_dict()
    count = sum(type in key for key in doc_dict.keys()) # sum of existing notifications of same type
    nid = f'{type}{count}'
    
    # If nid exists, increment count and update nid and check again until unique
    while does_nid_exists(uid, nid):
        count += 1
        nid = f'{type}{count}'

    return nid

# ============ FUNCTIONS ============ #
def get_notifications(uid):
    '''
    Get the user's notifications in descending time order.
    Args:
        uid (string): User getting notifications
    Returns:
        sorted_notifications (list): List of user's notifications sorted by descending timestamps
    '''
    check_valid_uid

    notf_data = db.collection('notifications').document(uid).get().to_dict()

    # Sort notification dictionaries by time_sent in descending order
    sorted_notifications = sorted(notf_data.values(), key=lambda x: x['time_sent'], reverse=True)

    return sorted_notifications

def notification_welcome(uid):
    '''
    Welcome message to new user.
    Args:
        uid (string): User being notified
    ASSUMPTION that this function is called ONCE per user.
    '''
    check_valid_uid(uid)

    name = get_display_name(uid)

    notification = {
        'welcome' : {
            "has_read": False,
            "notification_msg": f"Welcome to TaskForge, {name}. You can view future notifications here!",
            "time_sent": datetime.now(),
            "nid": 'welcome'
        }
    }

    db.collection("notifications").document(uid).set(notification)

def notification_connection_request(uid, uid_sender):
    '''
    Creates and adds notification when a user requests to connect another user.
    Args:
        uid (string): User being notified
        uid_sender (string): User who requests to connect
    ASSUMPTION that the users are not connected + do not have an existing request
    '''
    check_valid_uid(uid)
    check_valid_uid(uid_sender)

    notification_type = 'connection_request'
    nid = create_nid(uid, notification_type) # create notification ID
    sender_name = get_display_name(uid_sender)

    notification = {
        nid : {
            "has_read": False,
            "notification_msg": f"{sender_name} has requested to connect.",
            "time_sent": datetime.now(),
            "type": notification_type,
            "uid_sender": uid_sender,
            "accept_msg": f"You accepted {sender_name}'s connection request.",
            "decline_msg": f"You declined {sender_name}'s connection request.",
            "nid": nid
        }
    }

    db.collection("notifications").document(uid).update(notification)

def notification_project_invite(uid, uid_sender, pid):
    '''
    Creates and adds notification when a user invites another user to a project.
    Args:
        uid (string): User being notified
        uid_sender (string): User that is inviting to the project
        pid (int): Project being invited to
    ASSUMPTION that the user sending is in project + user receiving is not in project + do not have an existing request (+ possibly need to be connected?)
    '''
    check_valid_uid(uid)
    check_valid_uid(uid_sender)
    check_valid_pid(pid)

    notification_type = 'project_invite'
    nid = create_nid(uid, notification_type) # create notification ID
    sender_name = get_display_name(uid_sender)
    project_name = get_project_name(pid)

    notification = {
        nid : {
            "has_read": False,
            "notification_msg": f"{sender_name} has invited you to join {project_name}.",
            "pid": pid,
            "time_sent": datetime.now(),
            "type": notification_type,
            "uid_sender": uid_sender,
            "accept_msg": f"You accepted {sender_name}'s project invitation.",
            "decline_msg": f"You declined {sender_name}'s project invitation.",
            "nid": nid
        }
    }

    db.collection("notifications").document(uid).update(notification)

def notification_assigned_task(uid, pid, tid):
    '''
    Creates and adds notification when a user is assigned a task in a project.
    Args:
        uid (string): User being notified
        pid (int): Project the task is located in
        tid (int): Task being assigned
    ASSUMPTION that the user is in project + task is in project
    '''
    check_valid_uid(uid)
    check_valid_pid(pid)
    check_valid_tid(tid)

    notification_type = 'assigned_task'
    nid = create_nid(uid, notification_type) # create notification ID
    project_name = get_project_name(pid)
    task_name = get_task_name(tid)

    notification = {
        nid : {
            "has_read": False,
            "notification_msg": f"You have been assigned {task_name} in {project_name}.",
            "pid": pid,
            "tid": tid,
            "time_sent": datetime.now(),
            "type": notification_type,
            "nid": nid
        }
    }

    db.collection("notifications").document(uid).update(notification)

def notification_comment(uid, uid_sender, pid, tid):
    '''
    Creates and adds notification when a comment is added to a user's assigned task in a project.
    Args:
        uid (string): User being notified
        uid_sender (string): User who commented
        pid (int): Project the task is in
        tid (int): Task that was commented in
    ASSUMPTION that the user is in the project + task is in the project + user was assigned the task
    '''
    check_valid_uid(uid)
    check_valid_uid(uid_sender)
    check_valid_pid(pid)
    check_valid_tid(tid)

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
            "time_sent": datetime.now(),
            "type": notification_type,
            "uid_sender": uid_sender,
            "nid": nid
        }
    }

    db.collection("notifications").document(uid).update(notification)

def notification_deadline(uid, pid, tid):
    '''
    Creates and adds notification when an assigned task's deadline is coming up.
    Args:
        uid (string): User being notified
        pid (int): Project the task is in
        tid (int): Task that is due soon
    ASSUMPTION that the user is in the project + task is in project + task assigned to user
    '''
    check_valid_uid(uid)
    check_valid_pid(pid)
    check_valid_tid(tid)

    notification_type = 'deadline'
    nid = create_nid(uid, notification_type) # create notification ID
    project_name = get_project_name(pid)
    task_name = get_task_name(tid)

    notification = {
        nid : {
            "has_read": False,
            "notification_msg": f"{task_name} from {project_name} is due soon.",
            "pid": pid,
            "tid": tid,
            "time_sent": datetime.now(),
            "type": notification_type,
            "nid": nid
        }
    }

    db.collection("notifications").document(uid).update(notification)

def notification_review(uid, uid_sender, rid):
    '''
    Creates and adds notification when a review is added to a user's profile.
    Args:
        uid (string): User being notified
        uid_sender (string): User who made review
        rid (int): Review created
    ASSUMPTION that the users are connected(?)
    '''
    check_valid_uid(uid)
    check_valid_uid(uid_sender)
    check_valid_rid(rid)

    notification_type = 'review'
    nid = create_nid(uid, notification_type) # create notification ID
    sender_name = get_display_name(uid_sender)

    notification = {
        nid : {
            "has_read": False,
            "notification_msg": f"{sender_name} has reviewed you.",
            "rid": rid,
            "time_sent": datetime.now(),
            "type": notification_type,
            "uid_sender": uid_sender,
            "nid": nid
        }
    }

    db.collection("notifications").document(uid).update(notification)

def notification_achievement(uid, achievement_str):
    '''
    Creates and adds notification when an achievement has been completed.
    Args:
        uid (string): User being notified
        achievement_str (string): Achievement that has been completed
    ASSUMPTION that the achievement has been fulfilled
    '''
    check_valid_uid(uid)
    check_valid_achievement(achievement_str)

    notification_type = 'achievement'
    nid = create_nid(uid, notification_type) # create notification ID
    achievement_name = get_achievement_name(achievement_str)

    notification = {
        nid : {
            "achievement": achievement_str,
            "has_read": False,
            "notification_msg": f"You have earned the {achievement_name} achievement.",
            "time_sent": datetime.now(),
            "type": notification_type,
            "nid": nid
        }
    }

    db.collection("notifications").document(uid).update(notification)

def notification_leave_request(uid, uid_sender, pid):
    '''
    Creates and adds notification when a user requests to leave a project to the project master.
    Args:
        uid (string): User being notified
        uid_sender (string): User sending leave request
        pid (int): Project being left
    ASSUMPTION that the users are in project + user notified is project master
    '''
    check_valid_uid(uid)
    check_valid_uid(uid_sender)
    check_valid_pid(pid)

    notification_type = 'leave_request'
    nid = create_nid(uid, notification_type) # create notification ID
    sender_name = get_display_name(uid_sender)
    project_name = get_project_name(pid)

    notification = {
        nid : {
            "has_read": False,
            "notification_msg": f"{sender_name} has requested to leave {project_name}.",
            "pid": pid,
            "time_sent": datetime.now(),
            "type": notification_type,
            "uid_sender": uid_sender,
            "accept_msg": f"You accepted {sender_name}'s project leave.",
            "decline_msg": f"You declined {sender_name}'s project leave.",
            "nid": nid
        }
    }

    db.collection("notifications").document(uid).update(notification)

def get_notifications(uid):
    '''
    Get the user's notifications in descending time order.
    Args:
        uid (string): User getting notifications
    Returns:
        sorted_notifications (list): List of dictionaries of user's notifications sorted by descending timestamps
    '''
    check_valid_uid

    notf_data = db.collection('notifications').document(uid).get().to_dict()

    # Sort notification dictionaries by time_sent in descending order
    sorted_notifications = sorted(notf_data.values(), key=lambda x: x['time_sent'], reverse=True)

    return sorted_notifications

def clear_notification(uid, notf_dict):
    '''
    Clears all the user's notification
    Args:
        uid (string): User getting notifications
        notf_dict (dictionary): Dictionary of notification data
    '''
    check_valid_uid(uid)
    nid = notf_dict['nid']
    doc_ref = db.collection('notifications').document(uid)
    doc_ref.update({
        nid: firestore.DELETE_FIELD
    })

def clear_all_notifications(uid):
    '''
    Clears all the user's notification
    Args:
        uid (string): User getting notifications
    '''
    check_valid_uid(uid)
    notf_data = db.collection('notifications').document(uid)
    notf_data.set({}) #set to nothing

if __name__ == "__main__":
    # im just gonna keep this here cause i like to test and not keep writing data again and again hehe
    """ db.collection('users').document('notifytestid').set({'display_name':'John Doe'})
    db.collection('users').document('notifytestid1').set({'display_name':'Jane Doe'})
    db.collection('achievements').document('night_owl').set({'name':'Night Owl !!! NOTIFICATION TEST'})
    db.collection('projects').document('1337').set({'name':'Project Notification !!! NOTIFICATION TEST'})
    db.collection('tasks').document('1337').set({'name':'Task Notification !!! NOTIFICATION TEST'})
    db.collection('reviews').document('1337').set({'uid':'notifytestid1'})
    notification_welcome('notifytestid')
    notification_connection_request('notifytestid', 'notifytestid1')
    notification_project_invite('notifytestid', 'notifytestid1', 1337)
    notification_assigned_task('notifytestid', 1337, 1337)
    notification_comment('notifytestid', 'notifytestid1', 1337, 1337)
    notification_deadline('notifytestid', 1337, 1337)
    notification_review('notifytestid', 'notifytestid1', 1337)
    notification_achievement('notifytestid', 'night_owl')
    notification_leave_request('notifytestid', 'notifytestid1', 1337)
    clear_all_notifications('notifytestid')
    #checking if nid is unique when deleted a specific notification
    notification_achievement('notifytestid', 'night_owl')
    notification_achievement('notifytestid', 'night_owl')
    notification_achievement('notifytestid', 'night_owl')
    notflist = get_notifications('notifytestid')
    clear_notification('notifytestid', notflist[1])
    notification_achievement('notifytestid', 'night_owl')
    clear_notification('notifytestid', notflist[1])
    notification_achievement('notifytestid', 'night_owl') """
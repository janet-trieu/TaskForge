'''
Feature: Connections
Functionalities:
 - connection_request_respond(uid, nid, response)
 - get_connection_requests(uid)
 - get_connected_taskmasters(uid)
 - remove_connected_taskmaster(uid, uid_remove)
 - remove_connected_taskmaster(uid, uid_remove)
 - search_taskmasters(uid, search_string)
'''

from google.cloud.firestore_v1.transforms import DELETE_FIELD, ArrayUnion

from .error import *
from .helper import *
from .profile_page import *
from .notifications import *

def connection_request_respond(uid, nid, response):
    '''
    Accepts or Declines a connection request from another taskmaster
    Args:
        - uid (string): User responding to request
        - nid (nid): Identification of notification
        - response (bool): Accept or Declining the request
    '''
    check_valid_uid(uid)
    if (not does_nid_exists(uid, nid)): raise InputError('Notification invalid')
    if (not isinstance(response, bool)): raise InputError('Response should be bool')
    
    #delete notification
    nid_ref = db.collection('notifications').document(uid)
    uid_sender = nid_ref.get().get(nid).get('uid_sender')
    db.collection('notifications').document(uid).update({nid:DELETE_FIELD})
    if response == True:
        notification_accepted_request(uid_sender, uid)
    else:
        notification_denied_request(uid_sender, uid)
        return {}
    #add each other to each connection list
    u_ref = db.collection('users').document(uid)
    u_ref.update({'connections' : ArrayUnion([uid_sender])})
    u_ref = db.collection('users').document(uid_sender)
    u_ref.update({'connections' : ArrayUnion([uid])})
    db.collection('notifications').document(uid).update({nid:DELETE_FIELD})

    return {}
    
def get_connection_requests(uid):
    '''
    Gets a list of connection requests to a certain user
    Args:
        - uid (string): User for whom the list is being made
    Returns:
        - conn_list (list of dicts): Notification dicts of type connection_request
    '''
    check_valid_uid(uid)
    conn_list = []
    notis = db.collection('notifications').document(uid).get().to_dict()
    for noti in notis:
        if (notis.get(noti).get('type') == 'connection_request'):
            conn_list.append(notis.get(noti))
    return conn_list

def get_connected_taskmasters(uid):
    '''
    Gets a list of connection taskmasters to user
    Args:
        - uid (string): User for whom the list is being made
    Returns:
        - connections (list of dictionaries): Users who are connected to current user
    '''
    check_valid_uid(uid)
    user_ref = db.collection('users').document(uid)
    connection_uids = user_ref.get().get('connections')

    connections = []

    for uid in connection_uids:
        connected_tm_data = {
            'uid': uid,
            'photo_url': get_photo(uid),
            'display_name': get_display_name(uid),
            'role': get_role(uid)
        }
        connections.append(connected_tm_data)
    
    return connections
    
def remove_connected_taskmaster(uid, uid_remove):
    """
    'Unfriends' 2 taskmasters
    Removes each other from their connections list
    Args:
        - uid (string): User invoking the command
        - uid_remove (string): User who is being removed
    Returns:
        - Nothing
    """
    check_valid_uid(uid)
    check_valid_uid(uid_remove)
    check_connected(uid, uid_remove)
    
    connections1 = db.collection('users').document(str(uid)).get().get('connections')
    connections1.remove(uid_remove)
    db.collection("users").document(str(uid)).update({"connections": connections1})
    
    connections2 = db.collection('users').document(str(uid_remove)).get().get('connections')
    connections2.remove(uid)
    db.collection("users").document(str(uid_remove)).update({"connections": connections2})

def search_taskmasters(uid, search_string):
    """
    Searches all taskmasters by display name and email
    Args:
        - uid (string): User who is searching
        - string (string): String to search by
    Returns:
        - Taskmasters (List of Users)
    """
    check_valid_uid(uid)
    if (search_string == ""): raise InputError('Must give proper string to search by')
    
    matches = []
    search_string = search_string.lower()
    users = db.collection('users').stream()
    for user in users:
        user_dict = user.to_dict()
        if (uid == user_dict["uid"]): continue
        display_name = get_display_name(user_dict["uid"]).lower()
        email = get_email(user_dict["uid"]).lower()
        if (search_string in display_name or search_string in email):
            matches.append(user_dict)
    
    #sort so that connected tms are at start of list
    sorted1 = []
    sorted2 = []
    for user in matches:
        if (is_connected(uid, user["uid"])):
            sorted1.append(user)
        else:
            sorted2.append(user)
    return sorted1 + sorted2 #connected tms first

from google.cloud.firestore_v1.transforms import DELETE_FIELD, ArrayUnion

from .error import *
from .helper import *

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
    
    nid_ref = db.collection('notifications').document(uid)
    uid_sender = nid_ref.get().get(nid).get('uid_sender')
    db.collection('notifications').document(uid).update({nid:DELETE_FIELD})
    if (not response): return {}
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
        - conn_list (list of Strings): Users who have connected
    '''
    check_valid_uid(uid)
    user_ref = db.collection('users').document(uid)
    return user_ref.get().get('connections')
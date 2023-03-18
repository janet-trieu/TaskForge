from .global_counters import *
from .error import InputError
from .helper import check_valid_uid
from .notifications import does_nid_exists
from .profile_page import is_valid_user
import firestore

def connection_request_respond(uid, nid, response):
    check_valid_uid(uid)
    if (not does_nid_exists(nid)): raise InputError('Notification invalid')
    if (not isinstance(response, bool)): raise InputError('Response should be bool')
    
    nid_ref = db.collections('notifications').document(nid)
    uid_sender = nid_ref.get().get('uid_sender')
    db.collections('notifications').document(nid).delete()
    if (not response): return
    u_ref = db.collections('users').document(uid)
    u_ref.update({'connections' : firestore.ArrayUnion([uid_sender])})
    u_ref = db.collections('users').document(uid_sender)
    u_ref.update({'connections' : firestore.ArrayUnion([uid])})
    
def get_connection_requests(uid):
    check_valid_uid(uid)
    conn_list = []
    notis = db.collections('notifications').where('uid', '==', uid).stream()
    for noti in notis:
        result = noti.to_dict()
        if (result.get('notification_type') == 'connection_request'):
            conn_list.append(result)
    return conn_list

def get_connected_taskmasters(uid):
    check_valid_uid(uid)
    user_ref = db.collections('users').document(uid)
    return user_ref.get().get('connections')
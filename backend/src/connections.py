from .global_counters import *
from .error import InputError
from .helper import check_valid_uid
from .notifications import does_nid_exists
import firestore
from google.cloud.firestore_v1.transforms import DELETE_FIELD, ArrayUnion

def connection_request_respond(uid, nid, response):
    check_valid_uid(uid)
    if (not does_nid_exists(uid, nid)): raise InputError('Notification invalid')
    if (not isinstance(response, bool)): raise InputError('Response should be bool')
    
    nid_ref = db.collection('notifications').document(uid)
    uid_sender = nid_ref.get().get(nid).get('uid_sender')
    db.collection('notifications').document(uid).update({nid:DELETE_FIELD})
    if (not response): return
    u_ref = db.collection('users').document(uid)
    u_ref.update({'connections' : ArrayUnion([uid_sender])})
    u_ref = db.collection('users').document(uid_sender)
    u_ref.update({'connections' : ArrayUnion([uid])})
    db.collection('notifications').document(uid).update({nid:DELETE_FIELD})
    
def get_connection_requests(uid):
    check_valid_uid(uid)
    conn_list = []
    notis = db.collection('notifications').document(uid).get().to_dict()
    for noti in notis:
        if (notis.get(noti).get('type') == 'connection_request'):
            conn_list.append(notis.get(noti))
    return conn_list

def get_connected_taskmasters(uid):
    check_valid_uid(uid)
    user_ref = db.collection('users').document(uid)
    return user_ref.get().get('connections')
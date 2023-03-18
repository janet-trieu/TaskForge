from global_counters import *
import sys
from error import InputError, AccessError
from helper import *
from notifications import does_nid_exists

def connection_request_respond(uid, nid, response):
    check_valid_uid(uid)
    if (not does_nid_exists(nid)): raise InputError('Notification invalid')
    if (not isinstance(response, bool)): raise InputError('Response should be bool')
    
    
    
def get_connection_requests():
    pass

def get_connected_taskmasters():
    pass
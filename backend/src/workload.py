from .helper import *



def get_workload(uid):
    check_valid_uid(uid)
    user_ref = db.collection('users').document(uid)
    return user_ref.get().get('workload')
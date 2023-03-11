import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def get_user_by_email(email, db):
    users_ref = db.collection('users')
    users = db.collection('users').where('email', '==', email).stream()
    for user in users:
        return (user.to_dict())
        
def get_user_by_uid(uid, db):
    users_ref = db.collection('users')
    users = db.collection('users').where('uid', '==', uid).stream()
    for user in users:
        return (user.to_dict())
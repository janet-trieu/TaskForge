'''
File for authentication user-invoked reset password
'''
from firebase_admin import auth
from error import *

def get_reset_password_link(uid):

    try:
        email = auth.get_user(uid).email
    except auth.UserNotFoundError:
        return -1
    else:
        return auth.generate_password_reset_link(email, {})

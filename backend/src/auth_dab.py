'''
Temporary file for authentication user-invoked reset password
'''
from firebase_admin import auth

def get_reset_password_link(uid):

    email = auth.get_user(uid).email

    link = auth.generate_password_reset_link(email, {})

    if link == None:
        return -1

    return link

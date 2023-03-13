'''
Temporary test file for authentication user-invoked reset password
'''

from src.auth_dab import get_reset_password_link

def test_reset_password():

    user_id = "3TssNFyMXmOtTGarpRtAZ7VrOd72"

    res = get_reset_password_link(user_id)

    assert not res == -1


'''
Test file for authentication user-invoked reset password
'''
import pytest
from src.authentication import *
from src.test_helpers import *

def test_reset_password():

    user_id = "rFoLiVMvWwaahFGpQTsb9jtZKT53"

    res = get_reset_password_link(user_id)

    assert not res == -1

def test_reset_password_invalid_uid():

    user_id = "3TssNFyM70OtTGarpRtAZzVrOd72"

    # with pytest.raises(auth.UserNotFoundError):
    # with pytest.raises(AccessError):
    assert get_reset_password_link(user_id) == -1

# Reset database
# IMPORTANT: Ensure you delete auth db data with delete_user(uid) as well
reset_firestore_database()
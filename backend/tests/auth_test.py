'''
Test file for authentication user-invoked reset password
'''
import pytest
from src.authentication import *
from src.profile_page import *
from src.test_helpers import reset_database

try:
    create_user_email("authtest0@gmail.com", "password123", "Auth Doe")
except auth.EmailAlreadyExistsError:
    pass

user_id = auth.get_user_by_email("authtest0@gmail.com").uid

def test_reset_password():

    res = get_reset_password_link(user_id)

    assert not res == -1

def test_reset_password_invalid_uid():

    invalid_user_id = "invalid uid"

    # with pytest.raises(auth.UserNotFoundError):
    # with pytest.raises(AccessError):
    assert get_reset_password_link(invalid_user_id) == -1

@pytest.mark.run_last
def test_reset_database():
    reset_database()
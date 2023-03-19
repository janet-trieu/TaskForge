'''
Test file for authentication user-invoked reset password
'''
import pytest
from src.authentication import *
from src.test_helpers import *

# ============ SET UP ============ #
reset_database() # Ensure database is clear for testing

try:
    create_user_email("authtest0@gmail.com", "password123", "Auth Doe")
except auth.EmailAlreadyExistsError:
    pass

user_id = auth.get_user_by_email("authtest0@gmail.com").uid

# ============ HELPERS ============ #
def remove_test_data():
    # Reset database, call at bottom of last test
    delete_user(user_id)
    reset_database()

# ============ TESTS ============ #
def test_reset_password():

    res = get_reset_password_link(user_id)

    assert not res == -1

def test_reset_password_invalid_uid():

    invalid_user_id = "my name is invalid uid and i hate being valid"

    # with pytest.raises(auth.UserNotFoundError):
    # with pytest.raises(AccessError):
    assert get_reset_password_link(invalid_user_id) == -1

    remove_test_data()
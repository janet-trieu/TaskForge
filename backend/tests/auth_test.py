'''
Test file for authentication user-invoked reset password
'''
import pytest
from operator import itemgetter
from src.authentication import *
from src.test_helpers import *

# ============ SET UP ============ #
@pytest.fixture
def set_up():
    reset_database() # Ensure database is clear for testing
    user_id = create_user_email("authtest0@gmail.com", "password123", "Auth Doe")
    return {'user_id': user_id}

# ============ TESTS ============ #
def test_reset_password(set_up):
    user_id = itemgetter(user_id)(set_up)

    res = get_reset_password_link(user_id)

    assert not res == -1

def test_reset_password_invalid_uid(set_up):
    invalid_user_id = "my name is invalid uid and i hate being valid"

    # with pytest.raises(auth.UserNotFoundError):
    # with pytest.raises(AccessError):
    assert get_reset_password_link(invalid_user_id) == -1
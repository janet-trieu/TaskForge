import pytest

from operator import itemgetter

from src.test_helpers import *

# ============ SET UP ============ #
@pytest.fixture
def set_up():
    reset_database() # Ensure database is clear for testing
    # Create users, projects etc.
    # Return as a dictionary, using itemgetter to use return data

# ============ TESTS ============ #
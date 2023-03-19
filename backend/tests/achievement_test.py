from src.test_helpers import *

# ============ SET UP ============ #
reset_database() # Ensure database is clear for testing

# ============ HELPERS ============ #
def remove_test_data():
    # Reset database, call at bottom of last test
    # IMPORTANT: Ensure you delete auth db data with delete_user(uid) as well
    reset_database()

# ============ TESTS ============ #
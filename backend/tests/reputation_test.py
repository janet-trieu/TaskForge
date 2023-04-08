import pytest

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth

from src.error import *
from src.profile_page import *
from src.notifications import *
from src.global_counters import *
from src.reputation import *
from src.proj_master import *
from src.test_helpers import add_tm_to_project

# ============ SET UP ============ #
db = firestore.client()

# Create new users
try:
    uid1 = create_user_email("reputationtest1@gmail.com", "password123", "user1")
    uid2 = create_user_email("reputationtest2@gmail.com", "password123", "user2")
    uid3 = create_user_email("reputationtest3@gmail.com", "password123", "user3")
except auth.EmailAlreadyExistsError:
    pass

# Users may already exist

uid1 = auth.get_user_by_email("reputationtest1@gmail.com").uid
uid2 = auth.get_user_by_email("reputationtest2@gmail.com").uid
uid3 = auth.get_user_by_email("reputationtest3@gmail.com").uid

pid1 = create_project(str(uid1), "project_1", "project_1", "", None, "")
pid2 = create_project(str(uid1), "project_2", "project_2", "", None, "")
add_tm_to_project(pid1, uid2)
update_project(pid1, uid1, {"status": "Completed"})
add_tm_to_project(pid2, uid2)

# Test: Valid Review with comment
def test_valid_review_comment():
    write_review(uid1, uid2, pid1, "5", "5", "5", "Very good")
    delete_review(uid1, uid2, pid1)
    return

# Test: Valid Review with no comment
def test_valid_review_no_comment():
    write_review(uid1, uid2, pid1, "5", "5", "5", "")
    delete_review(uid1, uid2, pid1)
    return

# Test: Invalid Review, non existent Project
def test_invalid_review_no_project():
    with pytest.raises(InputError):
        write_review(uid1, uid2, 1000000, "5", "5", "5", "Very good")
    

# Test: Invalid Review, not in same project
def test_invalid_review_not_in_same_project():
    with pytest.raises(InputError):
        write_review(uid1, uid3, pid1, "5", "5", "5", "Very good")

# Test: Invalid Review, project not completed
def test_invalid_review_project_not_complete():
    with pytest.raises(InputError):
        write_review(uid1, uid2, pid2, "5", "5", "5", "Very good")

# Test: Invalid Review, non integer review
def test_invalid_review_non_integer_review():
    with pytest.raises(InputError):
        write_review(uid1, uid2, pid1, "a", "5", "5", "Very good")

# Test: Invalid Review, out of range integer reviews
def test_invalid_review_out_of_range_integer():
    with pytest.raises(InputError):
        write_review(uid1, uid2, pid1, "5", "7", "5", "Very good")

# Test: Invalid Review, same uids
def test_invalid_review_same_uid():
    with pytest.raises(InputError):
        write_review(uid1, uid1, pid1, "5", "5", "5", "Very good")

# Test: Invalid Review, non existent uids
def test_invalid_review_non_existent_uids():
    with pytest.raises(InputError):
        write_review(uid1, "bkehshskes", pid1, "5", "5", "5", "Very good")

# Test: Valid View, own view
def test_valid_view_own_view():
    write_review(uid1, uid2, pid1, "5", "5", "5", "Very good")
    reviews = view_reviews(uid1, uid1)

    delete_review(uid1, uid2, pid1)

# Test: Valid View, own view, off visibility
def test_valid_view_own_view_visibility_off():
    return

# Test: Valid View, view other, visibility on
def test_valid_view_other_visibility_on():
    return

# Test: Valid View, view other, visbiility off, show nothing
def test_valid_view_other_visibility_off():
    return

# Test: Invalid View, non existent uids
def test_invalid_view_non_existent_uid():
    return

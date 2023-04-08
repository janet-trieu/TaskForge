# Imports
from firebase_admin import firestore
from firebase_admin import auth

from .global_counters import *
from .error import *
from .notifications import *
from .helper import *
from .profile_page import *
import re
import time
from datetime import datetime, time

### ========= Write Review ========= ###
def write_review(reviewer_uid, reviewee_uid, pid, communication, time_management, task_quality, comment):
    """
    Write a review for a connected task master after the completion of a shared project
    conditions:
        - Both task masters must be in same project
        - project must be complete
        - Both task masters are different
        - One review for each project
        - Must be integers (1<=score<=5)
    
    Args:
        - Reviewer_uid (str): uid of the task master that is leaving a review
        - Reviewee_uid (str): uid of the task master that is being reviewed
        - pid (int): id of the project that is shared between the two task masters
        - communication (int): an integer out of 5 corresponding how well reviewee_uid communicated
        - time_management (int): an integer out of 5 corresponding how well reviewee_uid managed tasks
        - task_quality (int): an integer out of 5 corresponding how well reviewee_uid did tasks
        - comment (str): str for any additional comments the reviewer_uid would like to say,
    
    Returns:
        None
    """

### ========= Write Review ========= ###
def delete_review(reviewer_uid, reviewee_uid, pid):
    """
    Deletes a review

    Args:
        - reviewer_uid (str): uid of the task master that is deleting their review
        - reviewee_uid (str): uid of the task master who is having their reviews deleted
        - pid (int): int of the project that the review belongs to
    
    Returns
        None
    
    """

### ========= View Reviews ========= ###
def view_reviews(viewer_uid, viewee_uid):
    """
    View the reviews of a task master. If the viewee has their reputation visibility off,
    return nothing

    Args:
        - Viewer_uid (str): uid of the task master that is viewing reviews
        - Viewee_uid (str): uid of the task master that is being viewed
    
    Return
        A dict with the following keys:
        - Reviews (list): a list of reviews
        - Communication (float): averaged communication score
        - Time_management (float): averaged time management score
        - task_quality (float): averaged task quality score
    """

### ========= Change Visibility ========= ###
def change_review_visibility(uid, visibility):
    """
    Changes the visibility of the task master's reputation for other task masters.

    Args:
        - uid (str): uid of the task master that is changing their reputation visibility
        - visibility (boolean): the new visibility setting of the task master
    """
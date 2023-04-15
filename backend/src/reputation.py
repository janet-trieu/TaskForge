# Imports
from firebase_admin import firestore
from firebase_admin import auth

from .global_counters import *
from .error import *
from .notifications import *
from .helper import *
from .profile_page import *
from .classes import Review
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
        - Must be integers (1<=score<=5)-
    
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
    # Check if uids are valid
    check_valid_uid(reviewer_uid)
    check_valid_uid(reviewee_uid)
    # Cannot write review for yourself
    if reviewer_uid == reviewee_uid:
        raise InputError("You cannot write a review for yourself")
    # Check if project is valid
    check_valid_pid(pid)
    # Check if users are in project
    check_user_in_project(reviewer_uid, pid)
    check_user_in_project(reviewee_uid, pid)
    # Check if project is completed
    project_status = db.collection("projects").document(str(pid)).get().get("status")
    if project_status != "Completed":
        raise InputError(f"Project {pid} is not complete.")
    # Check if reviewer has already made a review for reviewee for this project
    if check_review(reviewer_uid, reviewee_uid, pid):
        raise InputError(f"You have already written a review for {reviewee_uid} in project {pid}")
    # Check if review are integers
    if not communication.isnumeric() or not time_management.isnumeric() or not task_quality.isnumeric():
        raise InputError("Only integers for review")
    # check if review are between 1 and 5 inclusive
    if not (1<= int(communication) <= 5):
        raise InputError("Communication must be 1, 2, 3, 4 or 5")
    if not (1<= int(time_management) <= 5):
        raise InputError("Time Management must be 1, 2, 3, 4 or 5")
    if not (1<= int(task_quality) <= 5):
        raise InputError("Task Quality must be 1, 2, 3, 4 or 5")
    # Check if comment is string
    if not isinstance(comment, str):
        raise InputError("Comment must be a string")

    now = datetime.now()
    now = now.strftime("%d/%m/%Y")
    
    review = Review(reviewer_uid, reviewee_uid, pid, now, communication, time_management, task_quality, comment)
    # Add review to reviewee
    reputation_docs = db.collection("users").document(str(reviewee_uid)).get().get("reputation")
    reputation_docs["reviews"].append(review.to_dict())
    db.collection("users").document(str(reviewee_uid)).update({"reputation": reputation_docs})
    # Increment number of reviews written by 1
    reviewer_doc = db.collection("users").document(str(reviewer_uid)).get().get("reputation")
    reviewer_doc["total_reviews_written"] += 1
    db.collection("users").document(str(reviewer_uid)).update({"reputation": reviewer_doc})
    # update average
    update_average(reviewee_uid)

### ========= Update Review ========= ###
def update_review(reviewer_uid, reviewee_uid, pid, communication, time_management, task_quality, comment):
    """
    Update a review for a connected task master
    conditions:
        - Both task masters must be in same project
        - project must be complete
        - Both task masters are different
        - One review for each project
        - Must be integers (1<=score<=5)-
    
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
    # Check if uids are valid
    check_valid_uid(reviewer_uid)
    check_valid_uid(reviewee_uid)
    # Cannot write review for yourself
    if reviewer_uid == reviewee_uid:
        raise InputError("You cannot write a review for yourself")
    # Check if project is valid
    check_valid_pid(pid)
    # Check if users are in project
    check_user_in_project(reviewer_uid, pid)
    check_user_in_project(reviewee_uid, pid)
    # Check if project is completed
    project_status = db.collection("projects").document(str(pid)).get().get("status")
    if project_status != "Completed":
        raise InputError(f"Project {pid} is not complete.")
    # Check if reviewer has already made a review for reviewee for this project
    if check_review(reviewer_uid, reviewee_uid, pid) == False:
        raise InputError(f"No review for {reviewee_uid} in project {pid} has been written yet")
    # Check if review are integers
    if not communication.isnumeric() or not time_management.isnumeric() or not task_quality.isnumeric():
        raise InputError("Only integers for review")
    # check if review are between 1 and 5 inclusive
    if not (1<= int(communication) <= 5):
        raise InputError("Communication must be 1, 2, 3, 4 or 5")
    if not (1<= int(time_management) <= 5):
        raise InputError("Time Management must be 1, 2, 3, 4 or 5")
    if not (1<= int(task_quality) <= 5):
        raise InputError("Task Quality must be 1, 2, 3, 4 or 5")
    # Check if comment is string
    if not isinstance(comment, str):
        raise InputError("Comment must be a string")
    
    reputation = db.collection("users").document(str(reviewee_uid)).get().get("reputation")
    reviews = reputation.get("reviews")

    i = 0
    while i < len(reviews):
        review = reviews[i]
        if review.get("pid") == pid and review.get("reviewee_uid") == reviewee_uid and review.get("reviewer_uid") == reviewer_uid:
            review["communication"] = communication
            review["time_management"] = time_management
            review["task_quality"] = task_quality
            review["comment"] = comment
            reviews[i] = review
            reputation["reviews"] = reviews
            db.collection("users").document(str(reviewee_uid)).update({"reputation": reputation})
            update_average(reviewee_uid)
            return
        i += 1

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
    check_valid_uid(reviewer_uid)
    check_valid_uid(reviewee_uid)
    check_valid_pid(pid)

    reputation = db.collection("users").document(str(reviewee_uid)).get().get("reputation")
    reviews = reputation.get("reviews")

    for review in reviews:
        if review.get("pid") == pid and review.get("reviewee_uid") == reviewee_uid and review.get("reviewer_uid") == reviewer_uid:
            reviews.remove(review)
            reputation["reviews"] = reviews
            db.collection("users").document(str(reviewee_uid)).update({"reputation": reputation})
            reviewer_doc = db.collection("users").document(str(reviewer_uid)).get().get("reputation")
            reviewer_doc["total_reviews_written"] -= 1
            db.collection("users").document(str(reviewer_uid)).update({"reputation": reviewer_doc})
            update_average(reviewee_uid)
            print("Successfully deleted review")
            return
    print("No such review found")

### ========= Update Average ========= ###
def update_average(uid):
    """
    Updates the average of the reputation of the user

    Args:
        - uid (str): uid of the user that is being updated

    returns
        None
    """
    # Check for valid uid
    check_valid_uid(uid)

    reputation_doc = db.collection("users").document(str(uid)).get().get("reputation")
    reviews = reputation_doc.get("reviews")
    avg_communication = []
    avg_time_management = []
    avg_task_quality = []
    avg = []
    i = 0
    while i < len(reviews):
        review = reviews[i]
        communication = review.get("communication")
        time_management = review.get("time_management")
        task_quality = review.get("task_quality")
        # append review if first review
        if i == 0:
            avg_communication.append(communication)
            avg_time_management.append(time_management)
            avg_task_quality.append(task_quality)
        # if there are already averages, 
        else:
            prev_avg_communication = float(avg_communication[i-1])
            prev_avg_time_management = float(avg_time_management[i-1])
            prev_avg_task_quality = float(avg_task_quality[i-1])

            avg_communication.append(str((prev_avg_communication*i+float(communication))/(i+1)))
            avg_time_management.append(str((prev_avg_time_management*i+float(time_management))/(i+1)))
            avg_task_quality.append(str((prev_avg_task_quality*i+float(task_quality))/(i+1)))
        
        curr_avg_communication = float(avg_communication[i])
        curr_avg_time_management = float(avg_time_management[i])
        curr_avg_task_quality = float(avg_task_quality[i])

        avg.append(str((curr_avg_communication + curr_avg_time_management + curr_avg_task_quality)/3))
        i += 1

    reputation_doc["avg_communication"] = avg_communication
    reputation_doc["avg_time_management"] = avg_time_management
    reputation_doc["avg_task_quality"] = avg_task_quality
    reputation_doc["avg"] = avg
    db.collection("users").document(str(uid)).update({'reputation': reputation_doc})
    
### ========= Check Review ========= ###
def check_review(reviewer_uid, reviewee_uid, pid):
    """
    Check whether reviewer has already made a review for reviewee for project pid

    Args:
        - reviewer_uid (str): uid of the reviewer
        - reviewee_uid (str): uid of the reviewee
        - pid (int): id of the project
    
    Returns:
        True if a review already exists written by reviewer_uid for the project pid. False otherwise
    """
    reviews = db.collection("users").document(str(reviewee_uid)).get().get("reputation").get("reviews")
    for review in reviews:
        if review["reviewer_uid"] == reviewer_uid and review["pid"] == pid:
            return True
    return False

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
        - avg_communication (list): averaged communication score over time
        - avg_time_management (list): averaged time management score over time
        - avg_task_quality (list): averaged task quality score over time
        - avg (list): list of averaged scores
    """
    check_valid_uid(viewer_uid)
    check_valid_uid(viewee_uid)
    visibility = db.collection("users").document(str(viewee_uid)).get().get("reputation").get("visibility")
    if viewee_uid == viewer_uid or visibility == True:
        return db.collection("users").document(str(viewee_uid)).get().get("reputation")
    else:
        return None
    
### ========= Change Visibility ========= ###
def change_review_visibility(uid, visibility):
    """
    Changes the visibility of the task master's reputation for other task masters.

    Args:
        - uid (str): uid of the task master that is changing their reputation visibility
        - visibility (boolean): the new visibility setting of the task master
    """
    check_valid_uid(uid)
    if isinstance(visibility, bool) != True:
        raise InputError(f"{visibility} is not a boolean")
    reputation_doc = db.collection("users").document(str(uid)).get().get("reputation")
    reputation_doc["visibility"] = visibility
    db.collection("users").document(str(uid)).update({"reputation": reputation_doc})

### ========= get total number of reviews written ========= ###
def get_number_of_reviews_written(uid):
    """
    Gets the total nubmer of reviews written
    
    Args:  
        uid (str): uid of the user

    Returns:
        an int correlating to the nubmer of reviews written
    """
    check_valid_uid(uid)

    return int(db.collection("users").document(str(uid)).get().get("reputation").get("total_reviews_written"))
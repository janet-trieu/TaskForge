from .helper import *
from datetime import datetime, timedelta
import pytz



def get_user_workload(uid):
    """
    Get the workload of a certain user.
    Workload is the sum of the task workloads that are in progress and due within 7 days
    Args:
        - uid (string): UID of the user we are checking
    Returns:
        - workload (int): Workload total
    """
    utc=pytz.UTC
    check_valid_uid(uid)
    workload = 0
    curr_time = utc.localize(datetime.now())
    user_ref = db.collection('users').document(uid)
    tids = user_ref.get().get("tasks")

    for tid in tids:
        task_ref = db.collection('tasks').document(str(tid))
        
        status = task_ref.get().get("status")
        if (status != "In Progress" and status != "Testing/Reviewing"): continue
        
        due_date = task_ref.get().get("deadline")
        if (curr_time + timedelta(days = 7) < due_date): continue
        
        task_wl = task_ref.get().get("workload")
        workload += task_wl

    return workload

def update_user_availability(uid, avail):
    """
    Updates availablility from 0 to 5 in increments of 0.5
    Default is 5
    Args:
        - uid (string): User being updated
        - avail (float): Number of days available over the next week
    Returns:
        - None
    """
    check_valid_uid(uid)
    nums = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
    if (avail not in nums): raise InputError("Availability should be from 0 to 5 in increments of 0.5")
    user_ref = db.collection("users").document(str(uid))
    user_ref.update({'availability': avail})

def get_availability(uid):
    """
    Gets availability of a user
    Args:
        - uid (string): User being queried
    Returns:
        - Availability (float): Number of days available over the next week
    """
    check_valid_uid(uid)
    user_ref = db.collection("users").document(str(uid))
    return user_ref.get().get("availability")
    
    
def get_availability_ratio(uid):
    """
    Get the availability ratio of a certain user.
    Availability is workload/availability. 5 Working days
    Args:
        - uid (string): UID of the user we are checking
    Returns:
        - Availability (float): Availability of user
    """
    return get_user_workload(uid) / get_availability(uid)
    
def calculate_supply_demand(pid):
    pass
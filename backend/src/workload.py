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
        if (str(curr_time + timedelta(days = 7)) < str(due_date)): continue
        task_wl = int(task_ref.get().get("workload"))
        if (task_wl is None):
            task_wl = 0
        workload += task_wl

    return workload

def update_user_availability(uid, availability):
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
    if (availability not in nums): raise InputError("Availability should be from 0 to 5 in increments of 0.5")
    user_ref = db.collection("users").document(str(uid))
    
    user_ref.update({"availability": availability})

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
    Get the availability percentage of a certain user.
    Availability is workload/availability. 5 Working days
    Args:
        - uid (string): UID of the user we are checking
    Returns:
        - percentage (number): Availability ratio of user
    """
    avail = get_availability(uid)
    if (avail == 0) : return 1
    percentage = (get_user_workload(uid) / avail) * 100
    return int(percentage)
    
def calculate_supply_demand(uid):
    check_valid_uid(uid)
    user_ref = db.collection("users").document(str(uid))
    snd = user_ref.get().get("snd")
    total_workload = 0
    total_avail = 0
    
    workload = get_user_workload(uid)
    availability = get_availability(uid)
    total_workload += workload
    total_avail += availability
        
    data = {
        "supply": total_avail,
        "demand": total_workload
    }
    
    snd.append(data)
    user_ref.update({"snd":[data]})
    return snd
    
def get_supply_and_demand(uid):
    check_valid_uid(uid)
    calculate_supply_demand(uid)
    user_ref = db.collection("users").document(str(uid))
    return user_ref.get().get("snd")
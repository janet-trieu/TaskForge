from .helper import *
from datetime import datetime, timedelta
import pytz

def get_user_workload(uid, pid):
    """
    Get the workload of a certain user.
    Workload is the sum of the task workloads that are in progress and due within 7 days
    Args:
        - uid (string): UID of the user we are checking
        - pid (string): Project we are checking workload in
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
        
        task_pid = task_ref.get().get("pid")
        if (task_pid != pid): continue
        
        status = task_ref.get().get("status")
        if (status != "In Progress" and status != "Testing/Reviewing"): continue
        
        due_date = task_ref.get().get("deadline")
        if (curr_time + timedelta(days = 7) < due_date): continue
        
        task_wl = task_ref.get().get("workload")
        workload += task_wl

    return workload

def update_user_availability(uid, pid, availability):
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
    
    avail_ref = user_ref.collection("availability").document(str(pid))
    avail_ref.set({"availability": availability})

def get_availability(uid, pid):
    """
    Gets availability of a user
    Args:
        - uid (string): User being queried
    Returns:
        - Availability (float): Number of days available over the next week
    """
    check_valid_uid(uid)
    user_ref = db.collection("users").document(str(uid))

    return user_ref.collection("availability").document(str(pid)).get().get("availability")
    
    
def get_availability_ratio(uid, pid):
    """
    Get the availability ratio of a certain user.
    Availability is workload/availability. 5 Working days
    Args:
        - uid (string): UID of the user we are checking
    Returns:
        - Availability (float): Availability of user
    """
    return get_user_workload(uid, pid) / get_availability(uid, pid)
    
def calculate_supply_demand(pid):
    check_valid_pid(pid)
    proj_ref = db.collection('projects').document(str(pid))
    snd = proj_ref.get().get("snd")
    total_workload = 0
    total_avail = 0
    users = proj_ref.get().get('project_members')
    
    for user in users:
        workload = get_user_workload(user, pid)
        availability = get_availability(user, pid)
        total_workload += workload
        total_avail += availability
        
    data = {
        "time": datetime.now(),
        "supply": total_avail,
        "demand": total_workload
    }
    
    snd.append(data)
    proj_ref.update({"snd":snd})
    return snd
    
def get_supply_and_demand(pid):
    check_valid_pid(pid)
    proj_ref = db.collection('projects').document(str(pid))
    return proj_ref.get().get("snd")
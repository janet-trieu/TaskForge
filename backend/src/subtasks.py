"""
Feature: [Task Management]
Functionalities:
    - create_subtask()
    - get_subtask_ref()
    - get_subtask_details()
    - assign_subtask()
    - delete_subtask()
    - get_all_subtasks()
    - update_subtask()
"""
from firebase_admin import firestore
from firebase_admin import auth
from .classes import Subtask
from .error import *
from .helper import *
from .profile_page import get_user_ref
import datetime
from .tasks import get_task_ref

### ========= SUBTASKS ========= ###
### ========= Create Subtask ========= ###
def create_subtask(uid, tid, pid, assignees, title, description, deadline, workload, priority, status):
    """
    Creates a subtask and initialises the subtask into firestore database

    Args:
        uid (str): uid of the user that can be found in auth database
        pid (int): pid of the project that the subtask belongs to, found in firestore database
        eid (int): an integer that corresponds to a specific epic this task belongs to
        assignees (list): a list of UIDs (str) corresponding to who is assigned to this task
        title (str): a string that corresponds to the task's title
        description (str): a string that corresponds to the task's description
        deadline (int): an int that corresponds to the unix time the task is supposed to be finished
        workload (int): an int that corresponds to the estimated number of days required to finish this task
        priority (str): a string that corresponds to the prioty of the task. It is either "High", "Moderate", or "Low"
        status (str): a string that corresponds to the task's status. It is either "Not Started", "In Progress", "Testing/Reviewing", or "Done"

    Returns:
        An int that corresponds to the id to the subtask.
    """
    # Check if user is in project
    check_user_in_project(uid, pid)
    
    subtask_ref = db.collection("subtasks")
    value = get_curr_stid()
    eid = db.collection("tasks").document(str(tid)).get().get("eid")
    subtask = Subtask(value, tid, pid, eid, assignees, title, description, deadline, workload, priority, status)
    subtask_ref.document(str(value)).set(subtask.to_dict())

    project_subtasks = db.collection("tasks").document(str(tid)).get().get("subtasks")
    task_ref = db.collection("tasks").document(str(tid))
    if (project_subtasks is None):
        project_subtasks = [value]
        task_ref.set({'subtasks': project_subtasks})
        update_stid()
        return
    project_subtasks.append(value)
    task_ref.update({'subtasks': project_subtasks})
    update_stid()

    return {
        "stid": value,
        "title": title,
        "deadline": deadline,
        "priority": priority,
        "status": status,
        "assignee_emails": assignees,
        "flagged": False,
        "description": description,
        "workload": workload
    }

### ========= Get Subtask Ref ========= ###
def get_subtask_ref(stid):
    """
    Gets a subtask reference from firestore database

    Args:
        stid (int): id of the subtask that can be found in firestore database

    Returns:
        A Subtask document from firestore that corresponds to the STID given. 
    """
    # Check if user is in project
    check_valid_stid(stid)
 
    return db.collection('subtasks').document(str(stid)).get()

### ========= Get Subtask Details ========= ###
def get_subtask_details(uid, stid):
    """
    Gets a Subtask's full details and returns in dict form

    Args:
        stid (int): id of the subtask that can be found in firestore database

    Returns:
        A dict with the full details of the task
    """
    # Check if user is in project
    check_user_in_project(uid, get_subtask_ref(stid).get("pid"))
    check_valid_stid(stid)
    doc = get_subtask_ref(stid)
    subtask = Subtask(doc.get("stid"), doc.get("tid"), doc.get("pid"), doc.get("eid"),doc.get("assignees"), doc.get("title"), 
                doc.get("description"), doc.get("deadline"), doc.get("workload"), doc.get("priority"), doc.get("status"))
    return subtask.to_dict()

### ========= Get Assign Subtask ========= ###
def assign_subtask(uid, stid, new_assignees):
    """
    Assigns new users to a subtask

    Args:
        stid (int): id of the subtask that can be found in firestore database
        new_assignees (list): a list of UIDs (str) that will become the new assignee list
    
    Returns:
        None
    """
    # Check if user is in project
    check_user_in_project(uid, get_subtask_ref(stid).get("pid"))
    # Check if all UIDs in new_assignee are valid and in the project
    pid = get_subtask_ref(stid).get("pid")
    old_assignees = get_subtask_ref(stid).get("assignees")
    for uid in new_assignees:
        check_valid_uid(uid)
        check_user_in_project(uid, pid)
    
    removed_assignees = list(set(old_assignees) - set(new_assignees))
    added_assignees = list(set(new_assignees) - set(old_assignees))

    # remove subtask from assignees that are no longer assigned
    for uid in removed_assignees:
        user = get_user_ref(uid)
        subtasks = user.get("subtasks")
        user.update({"subtasks": subtasks.remove(stid)})

    # add subtask to new assignees
    for new_uid in added_assignees:
        user = get_user_ref(new_uid)
        subtasks = user.get("subtasks")
        if (subtasks is None):
            db.collection('users').document(new_uid).update({"subtasks": [stid]})
        else:
            subtasks.append(stid)
            db.collection('users').document(new_uid).update({"subtasks": subtasks})
    db.collection('tasks').document(str(stid)).update({"assignees": new_assignees})
    return

### ========= Delete Subtask ========= ###
def delete_subtask(uid, stid):
    """
    Deletes a subtask from firestore database

    Args:
        stid (int): id of the subtask that can be found in firestore database

    Returns:
        None
    """
    pid = get_subtask_ref(stid).get("pid")
    check_user_in_project(uid, pid)
    check_valid_stid(stid)
    # Remove task from assigned users
    assignees = db.collection('tasks').document(str(stid)).get("assignees")
    for assignee in assignees:
        assigned_subtasks = db.collection('users').document(str(assignee)).get("subtasks")
        assigned_subtasks.remove(stid)
        db.collection('users').document(str(assignee)).update({"tasks": assigned_subtasks})

    #Remove from project
    project_subtasks = db.collection("projects").document(str(pid)).get().get("subtasks")
    project_subtasks.remove(stid)
    db.collection("projects").document(str(pid)).update({"subtasks": project_subtasks})

    return db.collection('subtasks').document(str(stid)).delete()

def get_all_subtasks(uid, tid):
    """
    Gets all the subtasks in a task

    Args:
        uid (str):
        tid (int):

    Returns:
        A dict
    """
    check_valid_uid(uid)
    check_valid_tid(tid)

    task_ref = get_task_ref(tid)
    subtasks = task_ref.get("subtasks")
    subtask_list = []
    for subtask in subtasks:
        subtask_list.append(get_subtask_details(uid, subtask))
    return subtask_list

def update_subtask(uid, stid, assignees, title, description, deadline, workload, priority, status):
    """
    updates subtask

    Args:
        uid (str): uid of the user updating the task
        stid (int): id of the subtask that is being updated
        eid (int): id of the new epic that is being updated
        assignees (list): list of uids that will be assigned to the task
        title (str): string of the new title
        description (str): new description
        deadline (int): unix time stamp of when the task is due
        workload (int): new workload
        priority (str): new priority
        status (str): new status   
    
    Return:
        None
    """
    pid = get_subtask_ref(stid).get("pid")
    check_user_in_project(uid, pid)

    if type(title) != str:
        raise InputError(f'title is not a string')
    else:
        db.collection("subtasks").document(str(stid)).update({'title': title})
    if type(description) != str:
        raise InputError(f'description is not a string')
    else:
        db.collection("subtasks").document(str(stid)).update({'description': description})
    if deadline and not datetime.datetime.strptime(deadline, "%d/%m/%Y"):
        raise InputError(f'deadline is not valid')
    else:
        db.collection("subtasks").document(str(stid)).update({'deadline': deadline})
    if type(workload) != int and type(workload) != str:
        raise InputError(f'workload is not valid')
    else:
        db.collection("subtasks").document(str(stid)).update({'workload': workload})
    if priority != "High" and priority != "Moderate" and     priority != "Low":
        raise InputError('priority is not valid')
    else:
        db.collection("subtasks").document(str(stid)).update({'priority': priority})
    db.collection("subtasks").document(str(stid)).update({'assignees': assignees})
    if status != "Not Started" and status != "In Progress" and status != "Blocked" and status != "In Review/Testing" and status != "Completed":
        raise InputError("Not a valid status")
    else:
        db.collection("subtasks").document(str(stid)).update({'status': status})
    return    

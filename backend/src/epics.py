"""
Feature: [Task_Management]
Functionalities:
    - create_epic()
    - get_epic_ref()
    - get_epic_details()
    - delete_epic()
    - update_epic()
"""
from firebase_admin import firestore
from firebase_admin import auth
from .classes import Epic
from .error import *
from .helper import *
import datetime
import re

### ========= EPICS ========= ###
### ========= Create Epic ========= ###
def create_epic(uid, pid, title, description, colour):
    """
    Creates an epic and initalises the epic into firestore database

    Args:
        uid (str): uid of the user that can be found in auth database
        pid (int): pid of the project that the epic belongs to, found in firestore database
        title (str): a string that corresponds to the task's title
        description (str): a string that corresponds to the task's description
        colour (str): a string that corresponds to the hexadecimal code for the colour for the epic
    
    Returns:
        An int that corresponds to the id of the epic
    """
    # Check whether UID or PID is valid and if UID is in PID
    check_user_in_project(uid, pid)

    # check for invalid value inputs:
    if len(title) >= 50:
        raise InputError("Epic name is too long. Please keep it below 50 characters.")
    if len(title) <= 0:
        raise InputError("Epic requires a name!!!")
    if len(description) >= 1000:
        raise InputError("Epic description is too long. Please keep it below 1000 characters.")
    if len(description) <= 0:
        raise InputError("Epic requies a description!!!")

    #checks if colour is a valid hex code
    match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', colour)
    if not match:
        raise InputError("Colour is not a valid hex colour")

    #Add to firestore
    epic_ref = db.collection("epics")
    value = get_curr_eid()
    epic = Epic(value, pid, [], title, description, colour)
    epic_ref.document(str(value)).set(epic.to_dict())
    # Add to project
    project_epics = db.collection("projects").document(str(pid)).get().get("epics")
    project_epics.append(value)
    db.collection("projects").document(str(pid)).update({"epics": project_epics})
    #Update eid
    update_eid()
    return value

### ========= Get Epic Ref ========= ###
def get_epic_ref(eid):
    """
    Gets an Epic reference from firestore database

    Args:
        eid (int): id of the epic that can be found in firestore database

    Returns:
        An Epic document from firestore that corresponds to the EID given. 
    """
    # Check if user is in project
    check_valid_eid(int(eid))

    return db.collection('epics').document(str(eid)).get()

### ========= Get Epic Details ========= ###
def get_epic_details(uid, eid):
    """
    Gets an Epic's full details and returns in dict form

    Args:
        eid (int): id of the epic that can be found in firestore database

    Returns:
        A dict with the full details of the epic
    """
    # Check if user is in project
    check_valid_eid(eid)
    check_user_in_project(uid, get_epic_ref(eid).get("pid"))

    doc = get_epic_ref(eid)
    epic = Epic(doc.get("eid"), doc.get("pid"), doc.get("tasks"), doc.get("title"), doc.get("description"), doc.get("colour"))
    return epic.to_dict()

### ========= Delete Epic ========= ###
def delete_epic(uid, eid):
    """
    Deletes an epic from firestore database and removes eid from every task and subtask.
    The task and subtask will still exist, but just will not belong under an epic

    Args:
        eid (int): eid of the task that can be found in firestore database

    Returns:
        None
    """
    # Check if user is in project
    check_valid_eid(eid)
    pid = get_epic_ref(eid).get("pid")
    check_user_in_project(uid, pid)
    tasks = get_epic_ref(eid).get("tasks")

    # Remove eid in every child task and subtask
    for task in tasks:
        task_doc = db.collection('tasks').document(str(task))
        subtasks = task_doc.get().get('subtasks')
        for subtask in subtasks:
            db.collection('subtasks').document(str(subtask)).update({'eid': ""})
        task_doc.update({'eid': ""})

    project_epics = db.collection("projects").document(str(pid)).get().get("epics")
    project_epics.remove(eid)
    db.collection("projects").document(str(pid)).update({"epics": project_epics})

    db.collection('epics').document(str(eid)).delete()
    return

def update_epic(uid, eid, title, description, colour):
    """
    updates epic

    Args:
        uid (str): uid of the user updating the epic
        eid (int): id of the epic that is being updated
        title (str): str of the new title
        description (str): str of the new description
        colour (str): str of the new colour

    Return:
        None
    """
    pid = get_epic_ref(eid).get("pid")
    check_user_in_project(uid, pid)
    check_epic_in_project(eid, pid)    

    if type(title) != str:
        raise InputError(f'title is not a string')
    else:
        db.collection("epics").document(str(eid)).update({'title': title})
    if type(description) != str:
        raise InputError(f'description is not a string')
    else:
        db.collection("epics").document(str(eid)).update({'description': description})
    match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', colour)
    if not match:
        raise InputError("Colour is not a valid hex colour")
    else:
        db.colection("epics").document(str(eid)).update({'colour': colour})
    return
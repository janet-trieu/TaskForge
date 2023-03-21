# Imports
from firebase_admin import firestore
from firebase_admin import auth

from .global_counters import *
from .classes import Epic, Task, Subtask
from .error import *
from .notifications import *

### ========= EPICS ========= ###
### ========= Create Epic ========= ###
def create_epic(uid, pid):
    """
    Creates an epic and initalises the epic into firestore database

    Args:
        uid (str): uid of the user that can be found in auth database
        pid (int): pid of the project that the epic belongs to, found in firestore database
    
    Returns:
        An int that corresponds to the id of the epic
    """
    epic_ref = db.collection("epics")
    value = get_curr_eid()
    epic = Epic(value, pid, [uid], [], "", "", "", "", "", "")
    epic_ref.document(value).set(epic.to_dict())

    return

### ========= Get Epic Ref ========= ###
def get_epic_ref(eid):
    """
    Gets an Epic reference from firestore database

    Args:
        eid (int): id of the epic that can be found in firestore database

    Returns:
        An Epic document from firestore that corresponds to the EID given. 
    """    
    #return db.collection('epics').document(eid).get()
    return

### ========= Delete Epic ========= ###
def delete_epic(eid):
    """
    Deletes an epic from firestore database and subsequent tasks and subtask

    Args:
        eid (int): eid of the task that can be found in firestore database

    Returns:
        None
    """
    return

### ========= TASKS ========= ###
### ========= Create Task ========= ###
def create_task(uid, pid):
    """
    Creates a task and initialises the task into firestore database

    Args:
        uid (str): uid of the user that can be found in auth database
        pid (int): pid of the project that the task belongs to, found in firestore database

    Returns:
        An int that corresponds to the id to the task.
    """
    return
### ========= Get Task Ref ========= ###
def get_task_ref(tid):
    """
    Gets a task reference from firestore database

    Args:
        tid (int): id of the task that can be found in firestore database

    Returns:
        A Task document from firestore that corresponds to the TID given. 
    """    
    #return db.collection('tasks').document(tid).get()
    return

### ========= Delete Task ========= ###
def delete_task(tid):
    """
    Deletes a task from firestore database and subsequent subtasks

    Args:
        tid (int): id of the task that can be found in firestore database

    Returns:
        None
    """
    return

### ========= SUBTASKS ========= ###
### ========= Create Subtask ========= ###
def create_subtask(uid, pid):
    """
    Creates a subtask and initialises the subtask into firestore database

    Args:
        uid (str): uid of the user that can be found in auth database
        pid (int): pid of the project that the subtask belongs to, found in firestore database

    Returns:
        An int that corresponds to the id to the subtask.
    """    
    return

### ========= Get Task Ref ========= ###
def get_subtask_ref(stid):
    """
    Gets a subtask reference from firestore database

    Args:
        stid (int): id of the subtask that can be found in firestore database

    Returns:
        A Subtask document from firestore that corresponds to the STID given. 
    """    
    #return db.collection('subtasks').document(stid).get()
    return

### ========= Delete Subtask ========= ###
def delete_subtask(stid):
    """
    Deletes a subtask from firestore database

    Args:
        stid (int): id of the subtask that can be found in firestore database

    Returns:
        None
    """
    return

create_epic("boobs", 1)
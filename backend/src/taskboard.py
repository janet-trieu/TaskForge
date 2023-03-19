# Imports
from firebase_admin import firestore
from firebase_admin import auth

from .global_counters import *
from .classes import User
from .error import *
from .notifications import *

### ========= Create Task ========= ###
def create_task(uid):
    """
    Creates a task and initialises the task into firestore database

    Args:
        uid (str): uid of the user that can be found in auth database

    Returns:
        An int that corresponds to the id to the task.
    """
    return

### ========= Delete Task ========= ###
def delete_task(tid):
    """
    Deletes a task from firestore database

    Args:
        tid (int): id of the task that can be found in firestore database

    Returns:
        None
    """
    return


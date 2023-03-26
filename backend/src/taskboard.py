# Imports
from firebase_admin import firestore
from firebase_admin import auth

from .global_counters import *
from .classes import Epic, Task, Subtask
from .error import *
from .notifications import *
from .helper import *
from .profile_page import *

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

    epic_ref = db.collection("epics")
    value = get_curr_eid()
    epic = Epic(value, pid, [], title, description, colour)
    epic_ref.document(str(value)).set(epic.to_dict())
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
    check_valid_eid(eid)

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
    return epic.to_dict

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
    check_user_in_project(uid, get_epic_ref(eid).get("pid"))
    tasks = get_epic_ref(eid).get("tasks")

    # Remove eid in every child task and subtask
    for task in tasks:
        task_doc = db.collection('tasks').document(str(task))
        subtasks = task_doc.get('subtasks')
        for subtask in subtasks:
            db.collection('subtasks').document(str(subtask)).update({'eid': ""})
        task_doc.update({'eid': ""})

    db.collection('epics').document(str(eid)).delete()
    return

### ========= TASKS ========= ###
### ========= Create Task ========= ###
def create_task(uid, pid, eid, assignees, title, description, deadline, workload, priority, status):
    """
    Creates a task and initialises the task into firestore database

    Args:
        uid (str): uid of the user that can be found in auth database
        pid (int): an integer that corresponds to a specific project this task belongs to
        eid (int): an integer that corresponds to a specific epic this task belongs to
        assignees (list): a list of UIDs (str) corresponding to who is assigned to this task
        title (str): a string that corresponds to the task's title
        description (str): a string that corresponds to the task's description
        deadline (int): an int that corresponds to the unix time the task is supposed to be finished
        workload (int): an int that corresponds to the estimated number of days required to finish this task
        priority (str): a string that corresponds to the prioty of the task. It is either "High", "Moderate", or "Low"
        status (str): a string that corresponds to the task's status. It is either "Not Started", "In Progress", "Testing/Reviewing", or "Done"

    Returns:
        An int that corresponds to the id to the task.
    """
    # Check whether UID or PID is valid and if UID is in PID
    check_user_in_project(uid, pid)

    task_ref = db.collection("tasks")
    value = get_curr_tid()
    task = Task(value, pid, eid, "", [], title, description, deadline, workload, priority, status, [], False, "")
    task_ref.document(str(value)).set(task.to_dict())

    #Assign task to assignees
    assign_task(uid, value, assignees)
    # Add task to epic
    epic_tasks = db.collection('epics').document(str(eid)).get().get("tasks")
    epic_tasks.append(value)
    db.collection('epics').document(str(eid)).update({"tasks": epic_tasks})
    # update tid
    update_tid()
    return value
### ========= Get Task Ref ========= ###
def get_task_ref(tid):
    """
    Gets a task reference from firestore database

    Args:
        tid (int): id of the task that can be found in firestore database

    Returns:
        A Task document from firestore that corresponds to the TID given. 
    """
    # Check if user is in project
    check_valid_tid(tid)
    return db.collection('tasks').document(str(tid)).get()


### ========= Get Task Details ========= ###
def get_task_details(uid, tid):
    """
    Gets a Task's full details and returns in dict form

    Args:
        tid (int): id of the task that can be found in firestore database

    Returns:
        A dict with the full details of the task
    """
    # Check if user is in project
    check_valid_tid(tid)
    check_user_in_project(uid, get_task_ref(tid).get("pid"))

    doc = get_task_ref(tid)
    task = Task(doc.get("tid"), doc.get("pid"), doc.get("eid"), doc.get("assignees"), doc.get("subtasks"), doc.get("title"), 
                doc.get("description"), doc.get("deadline"), doc.get("workload"), doc.get("priority"), doc.get("status"), doc.get("comments"),
                doc.get("flagged"), doc.get("completed"))
    return task.to_dict

### ========= Get Assign Task ========= ###
def assign_task(uid, tid, new_assignees):
    """
    Assigns new users to a task

    Args:
        uid (str): id of the user thats assigning tasks
        tid (int): id of the task that can be found in firestore database
        new_assignees (list): a list of UIDs (str) that will become the new assignee list
    
    Returns:
        None
    """
    # Check if user is in project
    check_valid_tid(tid)
    check_user_in_project(uid, get_task_ref(tid).get("pid"))
    # Check if all UIDs in new_assignee are valid and in the project
    pid = get_task_ref(tid).get("pid")
    old_assignees = get_task_ref(tid).get("assignees")
    for uid in new_assignees:
        check_valid_uid(uid)
        check_user_in_project(uid, pid)
    
    removed_assignees = list(set(old_assignees) - set(new_assignees))
    added_assignees = list(set(new_assignees) - set(old_assignees))

    # remove task from assignees that are no longer assigned
    for uid in removed_assignees:
        user = get_user_ref(uid)
        tasks = user.get("tasks")
        db.collection('users').document(new_uid).update({"tasks": tasks.remove(tid)})

    # add task to new assignees
    for new_uid in added_assignees:
        user = get_user_ref(new_uid)
        tasks = user.get("tasks")
        if (tasks is None):
            db.collection('users').document(new_uid).update({"tasks": [tid]})
        else:
            tasks.append(tid)
            db.collection('users').document(new_uid).update({"tasks": tasks})
    db.collection('tasks').document(str(tid)).update({"assignees": new_assignees})
    return

### ========= Delete Task ========= ###
def delete_task(uid, tid):
    """
    Deletes a task from firestore database and subsequent subtasks

    Args:
        tid (int): id of the task that can be found in firestore database

    Returns:
        None
    """
    # Check if user is in project
    check_valid_tid(tid)
    check_user_in_project(uid, get_task_ref(uid, tid).get("pid"))

    # Delete all subtasks under it
    task_ref = get_task_ref(tid)
    subtasks = task_ref.get('subtasks')
    for subtask in subtasks:
        delete_subtask(subtask)
    
    # Remove task from epic
    epic = get_epic_ref(task_ref.get("eid"))
    tasks = epic.get("tasks")
    tasks.remove("tid")
    epic.update({"tasks": tasks})

    # Remove task from assigned users
    assignees = db.collection('tasks').document(str(tid)).get("assignees")
    for assignee in assignees:
        assigned_tasks = db.collection('users').document(str(assignee)).get("tasks")
        assigned_tasks.remove(tid)
        db.collection('users').document(str(assignee)).update({"tasks": assigned_tasks})

    db.collection('tasks').document(str(tid)).delete()
    return 

### ========= SUBTASKS ========= ###
### ========= Create Subtask ========= ###
def create_subtask(uid, tid, pid, eid, assignees, title, description, deadline, workload, priority, status):
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
    subtask = Subtask(value, tid, pid, eid, "", title, description, deadline, workload, priority, status)
    subtask_ref.document(value).set(subtask.to_dict())

    assign_subtask(uid, value, assignees)
    update_stid()
    return value

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
 
    return db.collection('subtasks').document(stid).get()

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
                doc.get("description"), doc.get("deadline"), doc.get("workload"), doc.get("priority"), doc.get("status"),
                doc.get("comments"), doc.get("flagged"), doc.get("completed"))
    return subtask.to_dict

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
    check_user_in_project(uid, get_subtask_ref(uid, stid).get("pid"))
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
            subtasks.append(tid)
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
    check_user_in_project(uid, get_subtask_ref(stid).get("pid"))
    check_valid_stid(stid)
    # Remove task from assigned users
    assignees = db.collection('tasks').document(str(stid)).get("assignees")
    for assignee in assignees:
        assigned_subtasks = db.collection('users').document(str(assignee)).get("subtasks")
        assigned_subtasks.remove(stid)
        db.collection('users').document(str(assignee)).update({"tasks": assigned_subtasks})
    return db.collection('subtasks').document(str(stid)).delete()

### ========= Search Taskboard ========= ###
def search_taskboard(uid, pid, query):
    """
    Searches the project and returns a list of tasks that match the query

    Args:
        uid (str): id of the user requesting the search
        pid (int): id of the project that is being searched
        query (str): string of the query that will be compared to tasks

    Returns:
        A list of tasks that match the query
    """
    return

### ========= Comment Task ========= ###
def comment_task(uid, tid, comment):
    """
    Comments on a task

    Args:
        uid (str): id of the user commenting
        tid (int): id of the task that will be commented on
        comment (str): comment that will be commented

    Returns:
        None
    """
    return

### ========= Flag Task ========= ###
def flag_task(uid, tid, boolean):
    """
    Sets task flagness as boolean

    Args:
        uid (str): id of the user
    """
    
    return
# Imports
from firebase_admin import firestore
from firebase_admin import auth

from .global_counters import *
from .classes import Epic, Task, Subtask
from .error import *
from .notifications import *
from .helper import *
from .profile_page import *
import re
import time

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
        subtasks = task_doc.get('subtasks')
        for subtask in subtasks:
            db.collection('subtasks').document(str(subtask)).update({'eid': ""})
        task_doc.update({'eid': ""})

    project_epics = db.collection("projects").document(str(pid)).get().get("epics")
    project_epics.remove(eid)
    db.collection("projects").document(str(pid)).update({"epics": project_epics})

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
    #Add to project
    project_tasks = db.collection("projects").document(str(pid)).get().get("tasks")
    project_tasks.append(value)
    db.collection("projects").document(str(pid)).update({"tasks": project_tasks})
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
    return task.to_dict()

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
    for new_uid in removed_assignees:
        user = get_user_ref(new_uid)
        tasks = user.get("tasks")
        tasks.remove(tid)
        db.collection('users').document(new_uid).update({"tasks": tasks})

    # add task to new assignees
    for new_uid in added_assignees:
        user = get_user_ref(new_uid)
        tasks = user.get("tasks")
        if (tasks is None):
            db.collection('users').document(new_uid).update({"tasks": [tid]})
        else:
            tasks.append(tid)
            db.collection('users').document(new_uid).update({"tasks": tasks})
    # 
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
    pid = get_task_ref(tid).get("pid")
    check_user_in_project(uid, pid)

    # Delete all subtasks under it
    task_ref = get_task_ref(tid)
    subtasks = task_ref.get('subtasks')
    for subtask in subtasks:
        delete_subtask(subtask)
    
    # Remove task from epic
    epic = get_epic_ref(task_ref.get("eid"))
    tasks = epic.get("tasks")
    tasks.remove(tid)
    db.collection("epics").document(str(task_ref.get("eid"))).update({"tasks": tasks})

    # Remove task from assigned users
    assignees = db.collection('tasks').document(str(tid)).get().get("assignees")
    for assignee in assignees:
        assigned_tasks = db.collection('users').document(str(assignee)).get().get("tasks")
        assigned_tasks.remove(tid)
        db.collection('users').document(str(assignee)).update({"tasks": assigned_tasks})

    #Remove from projects
    project_tasks = db.collection("projects").document(str(pid)).get().get("tasks")
    project_tasks.remove(tid)
    db.collection("projects").document(str(pid)).update({"tasks": project_tasks})

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

    project_subtasks = db.collection("projects").document(str(pid)).get().get("subtasks")
    project_subtasks.append(value)
    db.collection("projects").document(str(pid)).update({"subtasks": project_subtasks})
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

#TODO
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
    check_user_in_project(uid, pid)
    project_tasks = db.collection("projects").document(str(pid)).get().get("tasks")

    tasks = {}
    #task ID, task name, description and/or deadline
    for task in project_tasks:
        task_ref = db.collection("tasks").document(str(task)).get()
        title = task_ref.get("title")
        description = task_ref.get("description")
        deadline = task_ref.get("deadline")

        if query.lower() in title.lower() or query.lower() in description.lower() or query.lower() in deadline.lower():
            tasks.append(task)

    return tasks

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
    pid = get_task_ref(tid).get("pid")
    check_user_in_project(uid, pid)
    check_valid_stid(tid)

    if len(comment) <= 0:
        raise InputError("Comment must not be empty")
    if len(comment) > 1000:
        raise InputError("Comment must not be longer than 1000 characters")
    
    data = {
        "time": time.time(),
        "uid": uid,
        "display_name": get_display_name(uid),
        "comment": comment,
    }
    comments = db.collection("tasks").document(str(tid)).get().get("comments")
    comments.append(data)
    db.collection("tasks").document(str(tid)).update({"comments": comments})

### ========= Flag Task ========= ###
def flag_task(uid, tid, boolean):
    """
    Sets task flagness as boolean

    Args:
        uid (str): id of the user
        tid (int): id of the task that will be flagged/unflagged
    """
    pid = get_task_ref(tid).get("pid")
    check_user_in_project(uid, pid)
    check_valid_stid(tid)

    db.collection("tasks").document(str(tid)).update({"flagged": boolean})

### ========= Change status ========= ###
def change_status(uid, tid, status):
    """
    Changes the status of a task

    Args:
        uid (str): id of the user
        tid (int): id of the task that will be changed
        status (str): the new status of the task
    
    Returns:
        None
    """
    pid = get_task_ref(tid).get("pid")
    check_user_in_project(uid, pid)
    check_valid_stid(tid)

    if status is not "Not Started" or status is not "In Progress" or status is not "Blocked" or status is not "In Review/Testing" or status is not "Completed":
        raise InputError("Not a valid status")
    
    if status is "Completed":
        db.collection("tasks").document(str(tid)).update({"completed": time.time()})
    else:
        db.collection("tasks").document(str(tid)).update({"completed": ""})
    db.collection("tasks").document(str(tid)).update({"status": status})

### ========= Show Non-Hidden Tasks ========= ###
def show_tasks(uid, pid, hidden):
    """
    Retrieves a list of tasks based on whether the hidden boolean is true or false.
    If true, retrieve all tasks. If false, only show non-hidden tasks.

    Args:
        uid (str): user that is requesting tasks
        pid (int): id of the project that will be accessed
        hidden (boolean): boolean that determines if the tasks will include hidden or non-hidden tasks

    Returns:
        A list of tids based on the hidden argument
    """
    task_list = []
    pid = get_task_ref(tid).get("pid")
    check_user_in_project(uid, pid)
    check_valid_stid(tid)
    curr_time = time.time()

    if hidden == True:
        return db.collection("projects").document(str(pid)).get().get("tasks")
    else:
        tasks = db.collection("projects").document(str(pid)).get().get("tasks")
        for task in tasks:
            time = db.collection("tasks").document(str(task)).get().get("completed")
            # if task has been completed and it has been more than 2 weeks since completed
            # this task is hidden
            if time.isdigit() and (curr_time - time) >= 604800 * 2:
                pass
            # this task is not hidden
            else:
                task_list.append(task)
        return task_list
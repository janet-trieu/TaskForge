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
from datetime import datetime, time
import os

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
        status (str): a string that corresponds to the task's status. It is either "Not Started", "In Progress", "In Review/Testing", or "Completed"

    Returns:
        An int that corresponds to the id to the task.
    """
    # Check whether UID or PID is valid and if UID is in PID
    check_user_in_project(uid, pid)

    task_ref = db.collection("tasks")
    value = get_curr_tid()
    # Check Status
    if status != "Not Started" and status != "In Progress" and status != "Blocked" and status != "In Review/Testing" and status != "Completed":
        raise InputError("Not a valid status")
    
    task = Task(value, pid, eid, "", [], title, description, deadline, workload, priority, "Not Started", [], [], False, "")
    task_ref.document(str(value)).set(task.to_dict())

    #Assign task to assignees
    assign_task(uid, value, assignees)

    # Add task to epic
    if eid != "":
        epic_tasks = db.collection('epics').document(str(eid)).get().get("tasks")
        epic_tasks.append(value)
        db.collection('epics').document(str(eid)).update({"tasks": epic_tasks})
    #Add to project
    project_tasks = db.collection("projects").document(str(pid)).get().get("tasks")
    project_tasks.get("Not Started").append(value)
    db.collection("projects").document(str(pid)).update({"tasks": project_tasks})

    # Not started is default but will be changed to status
    change_status(uid, value, status)
    
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
    if epic != "":
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
    status = db.collection("tasks").document(str(tid)).get().get("status")
    project_tasks.get(status).remove(tid)
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

### ========= Search Taskboard ========= ###
def search_taskboard(uid, pid, query):
    """
    Searches the project and returns a list of tasks that match the query

    Args:
        uid (str): id of the user requesting the search
        pid (int): id of the project that is being searched
        query (str): string of the query that will be compared to tasks

    Returns:
        A list of tasks and their details that match the query (in deadline order)
    """
    check_user_in_project(uid, pid)
    project_tasks = db.collection("projects").document(str(pid)).get().get("tasks")

    task_list = {}
    #task ID, task name, description and/or deadline
    for task in project_tasks:
        task_ref = get_task_ref(task)
        pid = task_ref.get("pid")
        eid = task_ref.get("eid")
        task_details = {
            "tid": task,
            "title": task_ref.get("title"),
            "deadline": task_ref.get("deadline"),
            "priority": task_ref.get("priority"),
            "status": task_ref.get("status"),
            "assignees": task_ref.get("assignees"),
            "flagged": task_ref.get("flagged")
        }
        if eid == "" or eid == None:
            task_details['epic'] = "None"
        else:
            task_details['epic'] = db.collection("epics").document(str(eid)).get().get("title")
        if query.lower() in title.lower() or query.lower() in description.lower() or query.lower() in deadline.lower():
            task_list = insert_tasklist(task_list, task_details)

    return task_list

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
    now = datetime.now()
    data = {
        "time": now.strftime("%d/%m/%Y"),
        "uid": uid,
        "display_name": get_display_name(uid),
        "comment": comment,
        "file": None
    }
    comments = db.collection("tasks").document(str(tid)).get().get("comments")
    comments.append(data)
    db.collection("tasks").document(str(tid)).update({"comments": comments})

### ========= Files ========= ###
#prefix is basically the t_id
def upload_file(uid, fileName, destination_name, tid):
    if (not get_user_ref(uid)): raise InputError('uid invalid')
    path = f"{tid}/{destination_name}"
    storage_upload_file(fileName, path)
    
    data = {
        "time": time.time(),
        "uid": uid,
        "display_name": get_display_name(uid),
        "comment": "",
        "file": path
    }
    files = db.collection("tasks").document(str(tid)).get().get("files")
    files.append(data)
    db.collection("tasks").document(str(tid)).update({"files": files})
    
def download_file(uid, fileName):
    if (not get_user_ref(uid)): raise InputError('uid invalid')
    print(f"filename is {fileName}")
    new = re.sub('.*' + '/', '', fileName)# src/
    storage_download_file(fileName, f"src/{new}")

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
    check_valid_tid(tid)

    db.collection("tasks").document(str(tid)).update({"flagged": boolean})

### ========= Change status ========= ###
def change_task_status(uid, tid, status):
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
    check_valid_tid(tid)
    old_status = db.collection("tasks").document(str(tid)).get().get("status")

    if status != "Not Started" and status != "In Progress" and status != "Blocked" and status != "In Review/Testing" and status != "Completed":
        raise InputError("Not a valid status")
    
    if status == "Completed":
        now = datetime.now()
        db.collection("tasks").document(str(tid)).update({"completed": now.strftime("%d/%m/%Y")})
    else:
        db.collection("tasks").document(str(tid)).update({"completed": ""})

    # Remove from old status in project and add to status in project
    tasks = db.collection("projects").document(str(pid)).get().get("tasks")
    tasks.get(old_status).remove(tid)
    tasks.get(status).append(tid)

    db.collection("projects").document(str(pid)).update({"tasks": tasks})
    db.collection("tasks").document(str(tid)).update({"status": status})

### ========= List of Hidden/Non-Hidden Tasks ========= ###
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
    check_user_in_project(uid, pid)
    curr_time = datetime.now()

    tasks = db.collection("projects").document(str(pid)).get().get("tasks")
    task_list.extend(tasks.get("Not Started"))
    task_list.extend(tasks.get("In Progress"))
    task_list.extend(tasks.get("Blocked"))
    task_list.extend(tasks.get("In Review/Testing"))

    if hidden == True:
        task_list.extend(tasks.get("Completed"))
        return task_list
    else:
        completed_tasks = tasks.get("Completed")
        for task in completed_tasks:
            task_time = db.collection("tasks").document(str(task)).get().get("completed")
            # if task has been completed and it has been more than a weeks since completed
            # this task is hidden
            if task_time != "":
                task_time = datetime.strptime(task_time, "%d/%m/%Y")
                difference = curr_time - task_time
            if difference.days <= 7:
                task_list.append(task)
        return task_list
    
def get_taskboard(uid, pid, hidden):
    """
    Retrieves every task in a project. Shows or does not show hidden tasks depending on whether
    hidden is True or False

    Args:
        uid (str): id of the user requesting the tasks
        pid (int): id of the project's tasks that is being requested
        hidden (boolean): boolean on whether hidden or non-hidden tasks are returned

    Returns:
        a dict of statuses with tasks details inside. Details include: 
        Task details include: id, title, epic, deadline, priority, status, assignees
        in the priority order:
        flagged with timestamp
        flagged with no timestamp
        not flagged with timestamp
        not flagged without timestamp
    """
    taskboard_list = show_tasks(uid, pid, hidden)
    task_list = {
        "Not Started": [],
        "In Progress": [],
        "Blocked": [],
        "In Review/Testing": [],
        "Completed": []
    }
    for task in taskboard_list:
        task_ref = get_task_ref(task)
        pid = task_ref.get("pid")
        eid = task_ref.get("eid")
        task_details = {
            "tid": task,
            "title": task_ref.get("title"),
            "deadline": task_ref.get("deadline"),
            "priority": task_ref.get("priority"),
            "status": task_ref.get("status"),
            "assignees": task_ref.get("assignees"),
            "flagged": task_ref.get("flagged")
        }
        if eid == "" or eid == None:
            task_details['epic'] = "None"
        else:
            task_details['epic'] = db.collection("epics").document(str(eid)).get().get("title")
        status_list = task_list[task_ref.get("status")]
        status_list = insert_tasklist(status_list, task_details)
        task_list[task_ref.get("status")] = status_list
    return task_list

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
        
def update_task(uid, tid, eid, assignees, title, description, deadline, workload, priority, status, flagged):
    """
    Updates task

    Args:
        uid (str): uid of the user updating the task
        tid (int): id of the task that is being updated
        eid (int): id of the new epic that is being updated
        assignees (list): list of uids that will be assigned to the task
        title (str): string of the new title
        description (str): new description
        deadline (int): unix time stamp of when the task is due
        workload (int): new workload
        priority (str): new priority
        status (str): new status
        flagged (boolean): new flagged

    Returns:
        None

    """
    pid = get_task_ref(tid).get("pid")
    check_user_in_project(uid, pid)
    check_epic_in_project(eid, pid)
    
    # Update epics
    old_epic = get_task_ref(tid).get("eid")
    # new epic is different
    if not old_epic == eid:
        # Update subtask epic
        subtasks = get_task_ref(tid).get("subtasks")
        for subtask in subtasks:
            db.collection("subtasks").document(str(subtask)).update({'eid': eid})
        # Update task epic
        db.collection("tasks").document(str(tid)).update({'eid': eid})
        # Update new epic to include tid
        new_epic_tasks = get_epic_ref(eid).get("tasks")
        db.collection("epics").document(str(eid)).update({'tasks': new_epic_tasks.append(tid)})
        # Remove tid from old epic
        old_epic_tasks = get_epic_ref(old_epic).get("tasks")
        old_epic_tasks.remove(tid)
        db.collection("epics").document(str(old_epic)).update({'tasks': old_epic_tasks})

    assign_task(uid, tid, assignees)

    if type(title) != str:
        raise InputError(f'title is not a string')
    else:
        db.collection("tasks").document(str(tid)).update({'title': title})
    if type(description) != str:
        raise InputError(f'description is not a string')
    else:
        db.collection("tasks").document(str(tid)).update({'description': description})
    if datetime.strptime(deadline, "%d/%m/%Y"):
        raise InputError(f'deadline is not valid')
    else:
        db.collection("tasks").document(str(tid)).update({'deadline': deadline})
    if type(workload) != int:
        raise InputError(f'workload is not valid')
    else:
        db.collection("tasks").document(str(tid)).update({'workload': workload})
    if priority != "High" or priority != "Moderate" or priority != "Low":
        raise InputError('priority is not valid')
    else:
        db.collection("tasks").document(str(tid)).update({'priority': priority})
    change_task_status(uid, tid, status)
    flag_task(uid, tid, flagged)
    return

def update_subtask(uid, stid, eid, assignees, title, description, deadline, workload, priority, status):
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
    pid = get_task_ref(stid).get("pid")
    check_user_in_project(uid, pid)
    check_epic_in_project(eid, pid)
    
    # Update epics
    old_epic = get_subtask_ref(stid).get("eid")
    # new epic is different
    if not old_epic == eid:
        # Update task epic
        db.collection("subtasks").document(str(stid)).update({'eid': eid})

    assign_subtask(uid, stid, assignees)

    if type(title) != str:
        raise InputError(f'title is not a string')
    else:
        db.collection("subtasks").document(str(stid)).update({'title': title})
    if type(description) != str:
        raise InputError(f'description is not a string')
    else:
        db.collection("subtasks").document(str(stid)).update({'description': description})
    if datetime.strptime(deadline, "%d/%m/%Y"):
        raise InputError(f'deadline is not valid')
    else:
        db.collection("subtasks").document(str(stid)).update({'deadline': deadline})
    if type(workload) != int:
        raise InputError(f'workload is not valid')
    else:
        db.collection("subtasks").document(str(stid)).update({'workload': workload})
    if priority != "High" or priority != "Moderate" or priority != "Low":
        raise InputError('priority is not valid')
    else:
        db.collection("subtasks").document(str(stid)).update({'priority': priority})
    
    if status != "Not Started" and status != "In Progress" and status != "Blocked" and status != "In Review/Testing" and status != "Completed":
        raise InputError("Not a valid status")
    else:
        db.collection("subtasks").document(str(stid)).update({'status': status})
    return    

### ========= Insert into tasklist ========= ###
def insert_tasklist(tasklist, task):
    length = len(tasklist)
    if length == 0:
        tasklist.append(task)
        return tasklist
    i = 0
    
    while i < length:
        if less_than(task, tasklist[i]):
            tasklist.insert(i, task)
            return tasklist
        i += 1
    tasklist.append(task)
    return tasklist

### ========= Less than helper ========= ###
def less_than(task_one, task_two):
    task_one_flagged = task_one['flagged']
    task_two_flagged = task_two['flagged']
    if (task_one['deadline'] == "" or task_one['deadline'] == None):
        task_one_deadline = None
    else: 
        task_one_deadline = datetime.strptime(task_one['deadline'], "%d/%m/%Y")
    if (task_two['deadline'] == "" or task_two['deadline'] == None):
        task_two_deadline = None
    else:         
        task_two_deadline = datetime.strptime(task_two['deadline'], "%d/%m/%Y")

    if ((task_one_flagged == True and task_two_flagged == True) or (task_one_flagged == False and task_two_flagged == False)):
        # Both have time stamps
        if (task_one_deadline != None and task_two_deadline != None):
            if (task_one_deadline < task_two_deadline):
                return True
            else:
                return False       
        # Indexed has a time stamp but task doesnt
        if (task_one_deadline == None and task_two_deadline != None):
            return False
        # Both do not have timestamps
        if (task_one_deadline == None and task_two_deadline == None):
            return True
        # Indexed does not have a timestamp so task should be added infront of it
        if (task_one_deadline != None and task_two_deadline == None):
            return True
    # task one isnt flagged so should be after flagged task
    elif (task_one_flagged == False and task_two_flagged == True):
        return False
    # Task one is flagged and task two isnt so task should be inserted infront
    elif (task_one_flagged == True and task_two_flagged == False):
        return True

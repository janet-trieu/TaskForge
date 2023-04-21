"""
Feature: [Task Management]
Functionalities:
    - create_task()
    - get_task_ref()
    - get_task_details()
    - assign_task()
    - delete_task()
    - comment_task()
    - upload_file()
    - get_file_link()
    - flag_task()
    - change_task_status()
    - update_task()
"""
from firebase_admin import firestore
from firebase_admin import auth
from .classes import Task
from .error import *
from .helper import *
from .profile_page import get_user_ref, get_uid_from_email, get_email, update_user_num_tasks_completed
import datetime
from .notifications import *
from .achievement import *
from .epics import get_epic_ref
from google.cloud.firestore_v1.transforms import ArrayUnion
import os

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
    
    # Check Priority
    if priority and not (priority == "High" or priority == "Moderate" or priority == "Low"):
        raise InputError('Priority is not valid')
    
    if (not isinstance(workload, (str, int))):
        workload = 0
    
    task = Task(value, pid, eid, "", [], title, description, deadline, workload, priority, "Not Started", [], [], False, "")
    task_ref.document(str(value)).set(task.to_dict())

    #Assign task to assignees
    if assignees == []:
        assignees = [get_email(uid)]
    assign_task(uid, value, assignees)
    
    # Add task to epic
    if eid != "" and eid != None:
        epic_tasks = db.collection('epics').document(str(eid)).get().get("tasks")
        epic_tasks.append(value)
        db.collection('epics').document(str(eid)).update({"tasks": epic_tasks})
    #Add to project
    project_tasks = db.collection("projects").document(str(pid)).get().get("tasks")
    project_tasks.get("Not Started").append(value)
    db.collection("projects").document(str(pid)).update({"tasks": project_tasks})

    # Not started is default but will be changed to status
    change_task_status(uid, value, status)
    
    # update tid
    update_tid()
    return {
        "tid": value,
        "title": title,
        "deadline": deadline,
        "priority": priority,
        "status": status,
        "assignees": db.collection("tasks").document(str(value)).get().get("assignees"),
        "assignee_emails": assignees,
        "flagged": False,
        "description": description,
        "workload": workload,
        "eid": eid,
        "comments": [],
        "subtasks": [],
        "files": []
    }

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
                None, doc.get("flagged"), doc.get("completed"))
    return task.to_dict()

### ========= Get Assign Task ========= ###
def assign_task(uid, tid, new_assignees):
    """
    Assigns new users to a task

    Args:
        uid (str): id of the user thats assigning tasks
        tid (int): id of the task that can be found in firestore database
        new_assignees (list): a list of emails (str) that will become the new assignee list
    
    Returns:
        None
    """
    # Check if user is in project
    check_valid_tid(tid)
    check_user_in_project(uid, get_task_ref(tid).get("pid"))
    # Check if all UIDs in new_assignee are valid and in the project
    new_assignees_uids = []
    for assignee in new_assignees:
        new_assignees_uids.append(get_uid_from_email(assignee))
    pid = get_task_ref(tid).get("pid")
    old_assignees = get_task_ref(tid).get("assignees")
    for uid in new_assignees_uids:
        check_valid_uid(uid)
        check_user_in_project(uid, pid)
    
    removed_assignees = list(set(old_assignees) - set(new_assignees_uids))
    added_assignees = list(set(new_assignees_uids) - set(old_assignees))

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
            notification_assigned_task(uid, pid, tid)
        else:
            tasks.append(tid)
            db.collection('users').document(new_uid).update({"tasks": tasks})
            notification_assigned_task(uid, pid, tid)
    #
    
    check_achievement("task_assigned", uid)

    db.collection('tasks').document(str(tid)).update({"assignees": new_assignees_uids})
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
        delete_subtask(uid, subtask)
    
    # Remove task from epic
    eid= task_ref.get("eid")
    if eid != "" and eid is not None and eid != "None":
        epic = get_epic_ref(eid)
        if epic != "":
            tasks = epic.get("tasks")
            tasks.remove(tid)
            db.collection("epics").document(str(eid)).update({"tasks": tasks})

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
    check_valid_tid(tid)

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

    # Notify comment to assigned users
    assignees = db.collection("tasks").document(str(tid)).get().get("assignees")
    for user in assignees:
        notification_comment(user, uid, pid, tid)

    return data

### ========= Files ========= ###
#prefix is basically the t_id
def upload_file(uid, fileName, destination_name, tid):
    """
    Uploads a file from a user onto storage. Info is stored in firestore
    Args:
        - uid (string): User uploading file
        - fileName (string): File being uploaded
        - destination_name (string): Option of renaming file when it is uploaded
        - tid (int): Task in which file is being uploaded
    Returns:
        - link (string): URL where file can be accessed from storage
    """
    if (not get_user_ref(uid)): raise InputError('uid invalid')
    path = f"{tid}/{destination_name}"
    link = storage_upload_file(fileName, path)
    
    data = {
        "time": datetime.now(),
        "uid": uid,
        "display_name": get_display_name(uid),
        "comment": "",
        "file": destination_name,
        "link" : link
    }
    files = db.collection("tasks").document(str(tid)).get().get("files")
    if (files is None):
        files = []
        files.append(data)
        db.collection("tasks").document(str(tid)).set({"files": files})
        return data
    files.append(data)
    db.collection("tasks").document(str(tid)).update({"files": files})
    os.remove(f"src/{destination_name}")
    return data
    
def get_file_link(uid, tid, fileName):
    """
    Retrieves link to file from storage
    Args:
        - uid (string): User requesting file
        - fileName (string): File being requested
        - tid (int): Task in which file belongs
    Returns:
        - link (string): URL where file can be accessed from storage
    """
    tidfile = f"{tid}/{fileName}"
    if (not get_user_ref(uid)): raise InputError('uid invalid')
    files = db.collection("tasks").document(str(tid)).get().get("files")
    for file in files:
        if (file["file"] == tidfile):
            return file["link"]

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
        # incremenet number of tasks completed
        update_user_num_tasks_completed(uid)
        check_achievement("task_completion", uid)
    else:
        db.collection("tasks").document(str(tid)).update({"completed": ""})

    # Remove from old status in project and add to status in project
    tasks = db.collection("projects").document(str(pid)).get().get("tasks")
    tasks.get(old_status).remove(tid)
    tasks.get(status).append(tid)

    db.collection("projects").document(str(pid)).update({"tasks": tasks})
    db.collection("tasks").document(str(tid)).update({"status": status})

def update_task(uid, tid, eid, title, description, deadline, workload, priority, status, flagged):
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
        # Update new epic to include tid if it is not none
        if eid != "None":
            new_epic_tasks = get_epic_ref(eid).get("tasks")
            if new_epic_tasks is None:
                new_epic_tasks = []
            new_epic_tasks.append(tid)
            db.collection("epics").document(str(eid)).update({'tasks': new_epic_tasks})
        # Remove tid from old epic if it is not none
        if old_epic is not None and not old_epic == "None":
            old_epic_tasks = get_epic_ref(old_epic).get("tasks")
            old_epic_tasks.remove(tid)
            db.collection("epics").document(str(old_epic)).update({'tasks': old_epic_tasks})

    if type(title) != str:
        raise InputError(f'title is not a string')
    else:
        db.collection("tasks").document(str(tid)).update({'title': title})
    if type(description) != str:
        raise InputError(f'description is not a string')
    else:
        db.collection("tasks").document(str(tid)).update({'description': description})
    if deadline and not datetime.strptime(deadline, "%d/%m/%Y"):
        raise InputError(f'deadline is not valid')
    else:
        db.collection("tasks").document(str(tid)).update({'deadline': deadline})
    if type(workload) != str:
        raise InputError(f'workload is not valid')
    else:
        db.collection("tasks").document(str(tid)).update({'workload': workload})
    if priority and not (priority == "High" or priority == "Moderate" or priority == "Low"):
        raise InputError('priority is not valid')
    else:
        db.collection("tasks").document(str(tid)).update({'priority': priority})
    change_task_status(uid, tid, status)
    flag_task(uid, tid, flagged)

    assignees = db.collection("tasks").document(str(tid)).get().get("assignees");
    assignee_emails = []
    for assignee in assignees:
        assignee_emails.append(get_email(assignee));

    return {
        "tid": tid,
        "title": title,
        "deadline": deadline,
        "priority": priority,
        "status": status,
        "assignees": assignees,
        "assignee_emails": assignee_emails,
        "flagged": flagged,
        "description": description,
        "workload": workload,
        "eid": eid,
        "epic": db.collection("epics").document(str(eid)).get().get("title"),
        "comments": [],
        "subtasks": []
    }

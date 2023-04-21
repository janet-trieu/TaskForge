"""
Feature: [Task Management]
Functionalities:
    - search_taskboard()
    - show_tasks()
    - get_taskboard()
    - insert_tasklist()
    - less_than()
"""

### ========= Imports ========= ###
from firebase_admin import firestore
from firebase_admin import auth
from .profile_page import get_email
from .tasks import get_task_ref
from .error import *
from .helper import *
import datetime
### ========= Search Taskboard ========= ###
def search_taskboard(uid, pid, query_tid, query_title, query_description, query_deadline):
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
    # For every task in project, check if title, description or deadline are the same as the query
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
        date = datetime.strptime(query_deadline, "%d/%m/%Y")
        if ((query_tid == "" or int(query_tid) == int(task)) and (query_title == "" or query_title.lower() in task_ref.get("title")
                                                        and (query_description == "" or query_description.lower() in task_ref.get("description"))
                                                        and (query_deadline == "" or query_deadline == date))):
            task_list = insert_tasklist(task_list, task_details)
    return task_list

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
    curr_time = datetime.datetime.now()

    # Add all tasks from the project into one list
    tasks = db.collection("projects").document(str(pid)).get().get("tasks")
    task_list.extend(tasks.get("Not Started"))
    task_list.extend(tasks.get("In Progress"))
    task_list.extend(tasks.get("Blocked"))
    task_list.extend(tasks.get("In Review/Testing"))

    # If hidden is true, completed is added into the list
    if hidden == True:
        task_list.extend(tasks.get("Completed"))
        return task_list
    # Otherwise, check if completed tasks have been completed for 1 week already, if so, do not add
    else:
        completed_tasks = tasks.get("Completed")
        for task in completed_tasks:
            task_time = db.collection("tasks").document(str(task)).get().get("completed")
            # if task has been completed and it has been more than a weeks since completed
            # this task is hidden
            if task_time != "":
                task_time = datetime.datetime.strptime(task_time, "%d/%m/%Y")
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
    # Grab list of tasks based on whether hidden tasks are shown or not
    taskboard_list = show_tasks(uid, pid, hidden)
    task_list = {
        "Not Started": [],
        "In Progress": [],
        "Blocked": [],
        "In Review/Testing": [],
        "Completed": []
    }
    # For every task in taskboard_list, add their details into correct order
    for task in taskboard_list:
        task_ref = get_task_ref(task)
        pid = task_ref.get("pid")
        eid = task_ref.get("eid")
        assignees = task_ref.get("assignees")
        assignee_emails = []
        for assignee in assignees:
            assignee_emails.append(get_email(assignee))
        comments = task_ref.get("comments")
        comments.sort(key=(lambda x: x["time"]), reverse=True)

        task_details = {
            "tid": task,
            "title": task_ref.get("title"),
            "deadline": task_ref.get("deadline"),
            "priority": task_ref.get("priority"),
            "status": task_ref.get("status"),
            "assignees": assignees,
            "assignee_emails": assignee_emails,
            "flagged": task_ref.get("flagged"),
            "description": task_ref.get("description"),
            "workload": task_ref.get("workload"),
            "eid": task_ref.get("eid"),
            "comments": comments,
            "subtasks": task_ref.get("subtasks"),
            "files": task_ref.get("files")
        }
        if eid == "" or eid == None:
            task_details['epic'] = "None"
        else:
            task_details['epic'] = db.collection("epics").document(str(eid)).get().get("title")
        status_list = task_list[task_ref.get("status")]
        status_list = insert_tasklist(status_list, task_details)
        task_list[task_ref.get("status")] = status_list
    return task_list

### ========= Insert into tasklist ========= ###
def insert_tasklist(tasklist, task):
    """
    Helper function to add tasks into a list based in sorted order

    Args:
        - tasklist (list): list of current task details
        - task (dict): a dictionary for a task with their details

    Returns:
        a combination of tasklist and task where task is sorted into the correct order
    """
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
    """
    Helper function that determines whether two task are less than or greater
    Correct order:
        - Flagged with deadline with earliest deadline first
        - Flagged with no deadline
        - Unflagged with deadline with earliest deadline first
        - Unflagged with no deadline

    Args:
        - task_one (dict): a dictionary of task details
        - task_two (dict): a dictionary of task details

    Returns:
        True or False depending on whether task_one should be before or after task_two
    """
    # extract flag and deadline
    task_one_flagged = task_one['flagged']
    task_two_flagged = task_two['flagged']
    if (task_one['deadline'] == "" or task_one['deadline'] == None):
        task_one_deadline = None
    else: 
        task_one_deadline = datetime.datetime.strptime(task_one['deadline'], "%d/%m/%Y")
    if (task_two['deadline'] == "" or task_two['deadline'] == None):
        task_two_deadline = None
    else:         
        task_two_deadline = datetime.datetime.strptime(task_two['deadline'], "%d/%m/%Y")

    
    if (task_one_flagged == True):
        if ((task_one_deadline is not None) and (task_two_flagged == True and task_two_deadline is not None)):
            # If flagged and deadline, check order
            if (task_one_deadline < task_two_deadline):
                return True
            else:
                return False
        # Both are flagged but task_two has a deadline
        elif ((task_one_deadline is None) and (task_two_flagged == True and task_two_deadline is not None)):
            return False
        # Both are flagged but neither have a deadline
        else:
            return True
    else:
        # task_one is flagged but task_two is not
        if (task_two_flagged == True):
            return False
        # Both are unflagged and both have deadlines
        elif (task_one_deadline is not None and task_two_deadline is not None):
            if (task_one_deadline < task_two_deadline):
                return True
            else:
                return False
        # Both are unflagged but task_one has a deadline but task_two does not
        elif (task_one_deadline is not None and task_two_deadline is None):
            return True
        else:
        # Both are unflagged but task_one does not have a deadline but task_two does
            return False
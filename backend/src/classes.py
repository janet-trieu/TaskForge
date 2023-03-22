import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class User(object):
    """
    User Class that will be stored in the firestore database

    Attributes:
        uid (str): UID of the user generated by the auth database
        tuid (int): integer id of the user, increments with each user createed
        role (str): self-described role of the user
        picture (str): url of the display photo of the user
        DOB (str): date of birth of the suer
        is_admin (boolean): admin status of the user
        is_banned (boolean): ban status of the user
        is_removed (boolean): removal status of the user
        achievements (list): list of achievements the user has obtained
        projects (list): list of project ids that the user has joined
        epics (list): list of epic ids that the user has been assigned
        tasks (list): list of tasks ids that the user has been assigned
        subtasks (list): list of subtask ids that the user has been assigned
        connections (list): list of uids of users that the User has connected to
    """
    def __init__(self, uid, tuid, role, picture, DOB, is_admin, is_banned, is_removed, achievements, projects, epics, tasks, subtasks, connections):
        self.uid = uid
        self.tuid = tuid
        self.role = role
        self.picture = picture
        self.DOB = DOB
        self.is_admin = is_admin
        self.is_banned = is_banned
        self.is_removed = is_removed
        self.achievements = achievements
        self.projects = projects
        self.epics = epics
        self.tasks = tasks
        self.subtasks = subtasks
        self.connections = connections
        
        
    def to_dict(self):
        return {
            'uid': self.uid, 
            'tuid': self.tuid,
            'role': self.role,
            'picture': self.picture,
            'DOB': self.DOB,
            'is_admin': self.is_admin,
            'is_banned': self.is_banned,
            'is_removed': self.is_removed,
            "achievements": self.achievements,
            "projects": self.projects,
            "epics": self.epics,
            "tasks": self.tasks,
            "subtasks": self.subtasks,
            "connections": self.connections
        }

class Epic():
    """
    An Epic class that will be stored in firestore.

    Attributes:
        eid (int): an integer that corresponds to a specific epic
        pid (int): an integer that corresponds to a specific project this task belongs to
        title (str): a string that corresponds to the task's title
        tasks (list): a list of tuids (int) corresponding to the subtasks belonging to this task
        description (str): a string that corresponds to the task's description
        colour (str): a string that corresponds to the hexadecimal code for the colour for the epic

    """
    def __init__(self, eid, pid, tasks, title, description, colour):
        self.eid = eid
        self.pid = pid
        self.title = title
        self.tasks = tasks
        self.description = description
        self.colour = colour

    def to_dict(self):
        return {
            'eid': self.eid,
            'pid': self.pid,
            'title': self.title,
            'tasks': self.tasks,
            'description': self.description,
            'colour': self.colour
        }    

class Task():
    """
    A Task class that will be stored in firestore.

    Attributes:
        tid (int): an integer that corresponds to a specific task
        pid (int): an integer that corresponds to a specific project this task belongs to
        eid (int): an integer that corresponds to a specific epic this task belongs to
        assignees (list): a list of UIDs (str) corresponding to who is assigned to this task
        subtasks (list): a list of tuids (int) corresponding to the subtasks belonging to this task
        title (str): a string that corresponds to the task's title
        description (str): a string that corresponds to the task's description
        deadline (int): an int that corresponds to the unix time the task is supposed to be finished
        workload (int): an int that corresponds to the estimated number of days required to finish this task
        priority (str): a string that corresponds to the prioty of the task. It is either "High", "Moderate", or "Low"
        status (str): a string that corresponds to the task's status. It is either "Not Started", "In Progress", "Testing/Reviewing", or "Done"

    """
    def __init__(self, tid, pid, eid, assignees, subtasks, title, description, deadline, workload, priority, status):
        self.tid = tid
        self.pid = pid
        self.eid = eid
        self.assignees = assignees
        self.title = title
        self.description = description
        self.deadline = deadline
        self.workload = workload
        self.priority = priority
        self.status = status
        self.subtasks = subtasks

    def to_dict(self):
        return {
            'tid': self.tid,
            'pid': self.pid,
            'eid': self.eid,
            'assignees': self.assignees,
            'subtasks': self.subtasks,
            'title': self.title,
            'description': self.description,
            'deadline': self.deadline,
            'workload': self.workload,
            'priority': self.priority,
            'status': self.status
        }

class Subtask(Board_Object):
    """
    A Subtask class that will be stored in firestore.

    Attributes:
        stid (int): an integer that corresponds to a specific subtask
        tid (int): an integer that corresponds to a specific task
        pid (int): an integer that corresponds to a specific project this task belongs to
        eid (int): an integer that corresponds to a specific epic this task belongs to
        assignees (list): a list of UIDs (str) corresponding to who is assigned to this task
        title (str): a string that corresponds to the task's title
        description (str): a string that corresponds to the task's description
        deadline (int): an int that corresponds to the unix time the task is supposed to be finished
        workload (int): an int that corresponds to the estimated number of days required to finish this task
        priority (str): a string that corresponds to the prioty of the task. It is either "High", "Moderate", or "Low"
        status (str): a string that corresponds to the task's status. It is either "Not Started", "In Progress", "Testing/Reviewing", or "Done"

    """
    def __init__(self, stid, tid, pid, eid, assignees, title, description, deadline, workload, priority, status):
        self.stid = stid
        self.tid = tid
        self.pid = pid
        self.eid = eid
        self.assignees = assignees
        self.title = title
        self.description = description
        self.deadline = deadline
        self.workload = workload
        self.priority = priority
        self.status = status

    def to_dict(self):
        return {
            'stid': self.stid,
            'tid': self.tid,
            'pid': self.pid,
            'eid': self.eid,
            'assignees': self.assignees,
            'title': self.title,
            'description': self.description,
            'deadline': self.deadline,
            'workload': self.workload,
            'priority': self.priority,
            'status': self.status
        }
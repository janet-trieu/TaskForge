'''
temp file to store the project class 
'''
class Project():
    """
    A Project class that will be stored in firestore.

    Attributes:
     - 
     - 
    """
    def __init__(self, pid, uid, name, description, status, due_date, team_strength, picture, project_members, epics, tasks, subtasks,is_pinned):
        self.pid = pid
        self.uid = uid
        self.name = name
        self.description = description
        self.status = status
        self.due_date = due_date
        self.team_strength = team_strength
        self.picture = picture
        self.project_members = project_members
        self.epics = epics
        self.tasks = tasks
        self.subtasks = tasks
        self.is_pinned = is_pinned
    
    def to_dict(self):
        return {
            "pid": self.pid,
            "uid": self.uid,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "due_date": self.due_date,
            "team_strength": self.team_strength,
            "picture": self.picture,
            "project_members": self.project_members,
            "epics": self.epics,
            "tasks": self.tasks,
            "is_pinned": self.is_pinned
        }
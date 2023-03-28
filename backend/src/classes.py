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
            tasks (list): list of tasks ids that the user has been assigned
    """
    def __init__(self, uid, tuid, role, picture, DOB, is_admin, is_banned, is_removed, achievements, projects, tasks, connections):
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
        self.tasks = tasks
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
            "tasks": self.tasks,
            "connections": self.connections
        }
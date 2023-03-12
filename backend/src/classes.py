import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class User(object):
    def __init__(self, tuid, uid, is_admin, is_banned, achievements, projects, tasks):
        self.tuid = tuid
        self.uid = uid
        self.is_admin = is_admin
        self.is_banned = is_banned
        self.achievements = achievements
        self.projects = projects
        self.tasks = tasks
        
        
    def to_dict(self):
        return {
            'tuid': self.tuid,
            'uid': self.uid, 
            'is_admin': self.is_admin,
            'is_banned': self.is_banned,
            "achievements": self.achievements,
            "projects": self.projects,
            "tasks": self.tasks
        }
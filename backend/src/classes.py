import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class User(object):
    def __init__(self, uid, tuid, role, picture, DOB, is_admin, is_banned, is_removed, achievements, projects, tasks):
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
            "tasks": self.tasks
        }
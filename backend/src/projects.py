'''
Feature: Project Management
Functionalities:
 - create_project()
 - tba
'''
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('taskforge-9aea9-firebase-adminsdk-xaffr-c80ed6513a.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

def create_project(uid, name, description, status, due_date, team_strength, picture):

    if status == None:
        status = "Not Started"
    if due_date == None:
        due_date = None
    if team_strength == None:
        team_strength = None
    if picture == None:
        picture = "bleh.png"

    pid = 0

    data = {
        "uid": uid,
        "name": name,
        "description": description,
        "status": status,
        "due_date": due_date,
        "team_strength": team_strength,
        "picture": picture,
    }

    proj_ref = db.collection("projects_test").document(str(pid)).set(data)

    return proj_ref.id

if __name__ == "__main__":
    create_project(0, "Project1", "bleh", None, None, None, None)

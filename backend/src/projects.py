'''
Feature: Project Management
Functionalities:
 - create_project()
 - tba
'''
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime, date

cred = credentials.Certificate('taskforge-9aea9-firebase-adminsdk-xaffr-c80ed6513a.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

def create_project(uid, name, description, status, due_date, team_strength, picture):

    # setting default values 
    if status == None:
        status = "Not Started"
    if due_date == None:
        due_date = None
    if team_strength == None:
        team_strength = None
    if picture == None:
        picture = "bleh.png"

    print(f"THIS IS team strength @@@@@@@@@@@@@ {team_strength}")
    print(f"THIS IS team strength @@@@@@@@@@@@@ {type(team_strength)}")

    # check for invalid type inputs:
    if not type(uid) == int:
        raise TypeError("uid has to be type of integer!!!")
    if not type(name) == str:
        raise TypeError("Project name has to be type of string!!!")
    if not type(description) == str:
        raise TypeError("Project description has to be type of string!!!")
    if not type(status) == str:
        raise TypeError("Project status has to be type of string!!!")
    # if not due_date == None:
    #     if not isinstance(due_date, date):
    #         raise TypeError("Project due date has to be type of date!!!")
    if not team_strength == None:
        if not type(team_strength) == int:
            raise TypeError("Project team strength has to be type of int!!!")
    # below will have to have more checks implemented to ensure the input is a valid picture, type of png, jpg or jpeg
    if not type(picture) == str:
        raise TypeError("Project picture has to be type of string!!!")

    # check for invalid value inputs:
    if uid < 0:
        raise ValueError("Invalid uid entered!!!")
    if len(name) >= 50:
        raise ValueError("Project name is too long. Please keep it below 50 characters.")
    if len(name) <= 0:
        raise ValueError("Project requires a name!!!")
    if len(description) >= 1000:
        raise ValueError("Project description is too long. Please keep it below 1000 characters.")
    if len(description) <= 0:
        raise ValueError("Project requies a description!!!")
    
    if not status in ("Not Started", "In Progress", "Blocked", "Completed"):
        raise ValueError("Project status is incorrect. Please choose an appropriate staus of 'Not Started', 'In Progress', 'Blocked', 'Completed'.")
    # check for due date being less than 1 day away from today
    # if due_date <= date.today().strftime('%Y-%m-%d') or due_date <:
    #     raise ValueError("Project due date cannot be less than 1 day away")
    if not team_strength == None:
        if team_strength < 0:
            raise ValueError("Team strength cannot be less than 0!!!")

    data = {
        "uid": uid,
        "name": name,
        "description": description,
        "status": status,
        "due_date": due_date,
        "team_strength": team_strength,
        "picture": picture,
        "project_members": [uid]
    }

    pid = 0

    db.collection("projects_test").document(str(pid)).set(data)
    
    return pid

def delete_project(pid, uid):

    # check for uid being a project master

    # remove the project id with given pid

    # if project successfully removed, return f"project {pid} successfully removed"
    # else, return f"project {pid} couldn't be removed"
    pass

if __name__ == "__main__":
    get_project_details(0)
    add_tm_to_project(0, 2)

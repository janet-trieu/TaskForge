'''
Feature: Global ID counters (Project, Epic, Task)

Functionalities:
    - init_?id
        > Resets ID to 0
    - get_curr_?id
        > Returns currrent amount of ID
    - update_?id
        > Increments ID
'''
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('taskforge-9aea9-firebase-adminsdk-xaffr-c80ed6513a.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

p_doc = db.collection("counters").document("project")
e_doc = db.collection("counters").document("epic")
t_doc = db.collection("counters").document("task")
tu_doc = db.collection("counters").document("toal_user")

### ========= Project ID ========= ###
def init_pid():
    data = {
        "pid": 0
    }
    
    p_doc.set(data)

def get_curr_pid():
    return p_doc.get().get("pid")

def update_pid():
    value = get_curr_pid() + 1

    p_doc.update({"pid": value})

### ========= Epic ID ========= ###
def init_eid():
    data = {
        "eid": 0
    }
    
    e_doc.set(data)

def get_curr_eid():
    return e_doc.get().get("eid")

def update_eid():
    value = get_curr_eid() + 1

    e_doc.update({"eid": value})

### ========= Task ID ========= ###
def init_tid():
    data = {
        "tid": 0
    }
    
    t_doc.set(data)

def get_curr_tid():
    return t_doc.get().get("tid")

def update_tid():
    value = get_curr_tid() + 1

    t_doc.update({"tid": value})


### ========= Total User ID ========= ###
def init_tuid():
    data = {
        "tuid": 0
    }
    
    tu_doc.set(data)

def get_curr_tuid():
    return tu_doc.get().get("tuid")

def update_tuid():
    value = get_curr_tuid() + 1

    tu_doc.update({"tuid": value})
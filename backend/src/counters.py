'''
Feature: Global ID counters (Project, Epic, Task)

Functionalities:
    - init_id
    - get_id
    - update_id
    - reset_id
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

### ========= Project ID ========= ###
def init_pid():
    data = {
        "pid": 0
    }
    
    p_doc.set(data)

def get_pid():
    return p_doc.get().get("pid")

def update_pid():
    value = get_pid() + 1

    p_doc.update({"pid": value})

### ========= Epic ID ========= ###
def init_eid():
    data = {
        "eid": 0
    }
    
    e_doc.set(data)

def get_eid():
    return e_doc.get().get("eid")

def update_eid():
    value = get_eid() + 1

    e_doc.update({"eid": value})

### ========= Task ID ========= ###
def init_tid():
    data = {
        "tid": 0
    }
    
    t_doc.set(data)

def get_tid():
    return t_doc.get().get("tid")

def update_tid():
    value = get_tid() + 1

    t_doc.update({"tid": value})

if __name__ == "__main__":
    print("===== task ID =====")
    init_tid()
    print(get_tid()) #0
    update_tid()
    print(get_tid()) #1
    update_tid()
    update_tid()
    print(get_tid()) #3
    init_tid()
    print(get_tid()) #0
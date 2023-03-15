'''
Feature: Global ID counters (Project, Epic, Task, Total User)

Functionalities:
    - init_?id
        > Resets ID to 0
    - get_curr_?id
        > Returns currrent amount of ID
    - update_?id
        > Increments ID
'''
from firebase_admin import firestore, auth

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
    tu_doc = db.collection("counters").document("total_user")
    data = {
        "tuid": 0
    }
    
    tu_doc.set(data)

def get_curr_tuid():
    tu_doc = db.collection("counters").document("total_user")
    doc = tu_doc.get()
    if not (doc.exists):
        init_tuid()
    return tu_doc.get().get("tuid")

def update_tuid():
    tu_doc = db.collection("counters").document("total_user")
    doc = tu_doc.get()
    if not (doc.exists):
        init_tuid()
    value = get_curr_tuid() + 1

    tu_doc.update({"tuid": value})
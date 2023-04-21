from firebase_admin import firestore

db = firestore.client()

p_doc = db.collection("counters").document("total_projects")
e_doc = db.collection("counters").document("total_epics")
t_doc = db.collection("counters").document("total_tasks")

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
    e_doc = db.collection("counters").document("total_epics")
    data = {
        "eid": 0
    }
    
    e_doc.set(data)

def get_curr_eid():
    e_doc = db.collection("counters").document("total_epics")
    doc = e_doc.get()
    if not (doc.exists):
        init_eid()
    return e_doc.get().get("eid")

def update_eid():
    e_doc = db.collection("counters").document("total_epics")
    doc = e_doc.get()
    if not (doc.exists):
        init_eid()
    value = get_curr_eid() + 1

    e_doc.update({"eid": value})

### ========= Task ID ========= ###
def init_tid():
    t_doc = db.collection("counters").document("total_tasks")
    data = {
        "tid": 0
    }
    
    t_doc.set(data)

def get_curr_tid():
    t_doc = db.collection("counters").document("total_tasks")
    doc = t_doc.get()
    if not (doc.exists):
        init_tid()
    return t_doc.get().get("tid")

def update_tid():
    t_doc = db.collection("counters").document("total_tasks")
    doc = t_doc.get()
    if not (doc.exists):
        init_tid()
    value = get_curr_tid() + 1

    t_doc.update({"tid": value})

### ========= Subtask ID ========= ###
def init_stid():
    st_doc = db.collection("counters").document("total_subtasks")
    data = {
        "stid": 0
    }
    
    st_doc.set(data)

def get_curr_stid():
    st_doc = db.collection("counters").document("total_subtasks")
    doc = st_doc.get()
    if not (doc.exists):
        init_stid()
    return st_doc.get().get("stid")

def update_stid():
    st_doc = db.collection("counters").document("total_subtasks")
    doc = st_doc.get()
    if not (doc.exists):
        init_stid()
    value = get_curr_stid() + 1

    st_doc.update({"stid": value})



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

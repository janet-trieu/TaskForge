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
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate({
    "type": "service_account",
    "project_id": "taskforge-9aea9",
    "private_key_id": "c54a827d6cf0fa53707e51f300a6a225c0e28634",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCmlavEfpasLsth\nOnvvLfV8+NGnlWeqtCtNVN9nJkTDJgBTAmDubnbg2PhLBiTH4fEWylfOSqMCNm+v\n0uC6Ibr6LzM1ZlytjpKvcWJ+/pKC7F5pUTHGfwyjBcHe99oZRZZZC8qFWMoGqd8c\n5hK8BtHrkm2OCyLcY2cn8aSHE6HpRvEvkPVim68YR8JVeBQo+ThhlqywpcplmUsF\nMRSaVoVHp+ELLXoEA9XlX+vdXa+22bzTxH2+H7NTNuHtkzzjKSU7iL9ujR7JB+FT\nFBNPTAuP5JvEgKplfCndUTi765g9IgQhc2IZOpUTWuxYjTKGOq2G2G759ttcWm5Y\nB50boG/XAgMBAAECggEALJ6WXZFSplf6Xdaeb5gt0wWKkoqwM8cCejorhKN5c5Pw\nLkvKztKDwQIcr2u72lYoj2QvVLAlLWiLTdr8Gp8CSBTwcHM0i8BOhfOm4EEr2Sma\nuDbpUDOjnN7j6OcWYgKDnOJNop3/rv09J65wgjCJdcHI2m0dL07oyIgu+4dErQjG\nS64/c4DwrLiO7E16tNhc+Yn53g+Qkc37dAAndB8afkRcu3shgsOmWYLFa6dCm8wY\nqBNC+v893w4ki0dx3cZGXaLwGSDBfl++1EOhpLeUT2z1jU0vynVDmmh2LvmM+ySO\nTTY/J6bUs73yE3OZdR4xuTmhAVlyU2C3eU4R2DTaEQKBgQDkfmnHaqI57i/wJx7K\n9e5qNisCcH5NRHfL6Qd+ndmHe3qBvrFXyCO6SmSLvhcepJWjKuku8rkyOOKuRGr/\nom+/MWjhkCFbde2NgO6TkBjNFdpunAEiDh1XsxrY5jrvEsC0fAd0UXrOZitUtGPE\nbQrWsNjTJmQ9osXqhsR1uhzkGwKBgQC6o2DTlVNRrEb11wQ4Rxf2XQUfPU3dEcBw\naPcbA3rw0856GwxwMv3fCZi396ggf/uGmKuLuI4hOeM20bqVUd9Xzqmvbwxgm0YA\nk+WnSt0grrJ04FtoYRjKLYlYo39PhlnSwYBmGKE7oN4wg9lwxXP9lA+eO6nlb1Wl\ntZbgPPyG9QKBgQCQdYO2+inaakaQlIsZUmcLa3fBsRGJFFKQ7qE4Yd/Xki+fu8ov\nb293JfVvjBzd2LxqToTik76Wi/R0rPjg6fewbzKZ+R+9zU8E+ZDcZmvnrXtOFv94\nYmgWvDurCdQUtkxzTz7/QUxdFacrhGjXFQGXPnO2+zzA4xox7kZjD+mYJQKBgQC6\nYn5HzlAuuAUFbXzhVt4vQiXjVK11oEy19Z0QdSFJb7w7ZNe/FK1DF6pTzhcwnZ7q\ng3yNQ/lsZQrrq/bRN7n7Tn9Wm2eY8neuDATEVJcQFGZTIdsnGhBPl7oZsu1o1ZrO\nRj+bte0OR1Cc0o9Ld2SmUD5ontzEK7M0kWvi9AScIQKBgDNHvxiWYDeB0xg+8nRU\nARoIMagv7EMQ+E722xbWe8spSqubjXmMNiHbsPhcTxKm/SXngLFMQ92mm/4vIHbk\n+WyPGCq8JurXcO3DaHmnb+b6Mm/UxKezfa0ItNcyVcdJA2nXlS7NqLkezm0tRuj4\nlbO6DO643TpkYM52jBNwMpN0\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-xaffr@taskforge-9aea9.iam.gserviceaccount.com",
    "client_id": "107639385024138930542",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-xaffr%40taskforge-9aea9.iam.gserviceaccount.com"
  })
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
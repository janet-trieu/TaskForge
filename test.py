import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth
import json


#not sure if we need this or not
firebase_config={"apiKey": "AIzaSyCODWXHzh67zRV-xq9ZFAZ4sVaqKwUq9cY",
  "authDomain": "taskforge-9aea9.firebaseapp.com",
  "databaseURL": "https://taskforge-9aea9-default-rtdb.firebaseio.com",
  "projectId": "taskforge-9aea9",
  "storageBucket": "taskforge-9aea9.appspot.com",
  "messagingSenderId": "221747524877",
  "appId": "1:221747524877:web:8785cfe8e0847bd257ec44",
  "measurementId": "G-5N1VTMSWEC"
}


# Use a service account.
cred = credentials.Certificate('taskforge-9aea9-firebase-adminsdk-xaffr-c54a827d6c.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

#writing to db
doc_ref = db.collection('users').document('how')
doc_ref.set({
    'first': 'random',
    'middle': 'Mathison',
    'last': 'Turing',
    'born': 1912
})


#reading from db
users_ref = db.collection('users')
docs = users_ref.stream()

for doc in docs:
    print(f'{doc.id} => {doc.to_dict()}')
    
    
auth.create_user(email="emaillol@gmail.com", password="gaygay")
auth.create_user(email="emaillol@gmail.com", password="gaygay")
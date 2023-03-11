import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth

cred = credentials.Certificate('taskforge-9aea9-firebase-adminsdk-xaffr-c80ed6513a.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

cred = credentials.Certificate('taskforge-9aea9-firebase-adminsdk-xaffr-c80ed6513a.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()


def create_user():

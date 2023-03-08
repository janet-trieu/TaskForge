import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth
import json
import datetime

cred = credentials.Certificate('taskforge-9aea9-firebase-adminsdk-xaffr-c54a827d6c.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

#auth.create_user(email='yoloswag@gmail.com', password='unidropout')


user = auth.get_user_by_email('yoloswag@gmail.com')
print(user.email)
print(user.uid)
print(user.disabled)
print(user.display_name)
print(user.email_verified)
print(user.phone_number)
print(user.photo_url)


user_metadata = user.user_metadata
print(user_metadata.creation_timestamp)
print(user_metadata.last_refresh_timestamp)
print(user_metadata.last_sign_in_timestamp)



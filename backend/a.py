import firebase_admin
from firebase_admin import credentials, initialize_app, storage
from google.cloud import storage
from google.oauth2 import service_account
# Init firebase with your credentials
cred = credentials.Certificate("taskforge-9aea9-firebase-adminsdk-xaffr-c80ed6513a.json")
initialize_app(cred, {'storageBucket': 'taskforge-9aea9.appspot.com'})
credentials = service_account.Credentials.from_service_account_file("taskforge-9aea9-firebase-adminsdk-xaffr-c80ed6513a.json")

def upload_file(fileName, destination_name):
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(destination_name)
    blob.make_public()
    print(f"{destination_name}", blob.public_url)
    

files = storage.Client(credentials=credentials).list_blobs(firebase_admin.storage.bucket().name) # fetch all the files in the bucket
for i in files: print('The public url is ', i.public_url)
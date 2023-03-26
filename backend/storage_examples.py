import firebase_admin
from firebase_admin import credentials, initialize_app, storage
from google.oauth2 import service_account
# Init firebase with your credentials
cred = credentials.Certificate("taskforge-9aea9-firebase-adminsdk-xaffr-c80ed6513a.json")
initialize_app(cred, {'storageBucket': 'taskforge-9aea9.appspot.com'})
credentials = service_account.Credentials.from_service_account_file("taskforge-9aea9-firebase-adminsdk-xaffr-c80ed6513a.json")

def upload_file(fileName, destination_name):
    bucket = storage.bucket()
    blob = bucket.blob(destination_name)
    blob.upload_from_filename(fileName)
    blob.make_public()
    print(f"{destination_name}", blob.public_url)


base_url = 'https://storage.googleapis.com/taskforge-9aea9.appspot.com/'

def download_file(fileName, destination_name): 
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.download_to_filename(destination_name)
    

def delete_file(fileName):
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.delete()

upload_file('antonio.jpeg', 'ant.jpeg')
upload_file('safety.docx', 'safety.docx')
download_file('safety.docx', 'safse.docx')
delete_file('safety.docx')
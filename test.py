import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import datetime

class User(object):
    def __init__(self, uid, email, display_name, is_admin, is_banned):
        self.uid = uid
        self.email = email
        self.display_name = display_name
        self.is_admin = is_admin
        self.is_banned = is_banned
        
        
    def to_dict(self):
        return {
              'uid': self.uid, 
              'email': self.email,
              'display_name': self.display_name,
              'is_admin': self.is_admin,
              'is_banned': self.is_banned
        }

class Project(object):
    def __init__(self, pid, creator, date_created):
        self.pid = pid
        self.creator = creator
        self.date_created = date_created
        
        
    def to_dict(self):
        return {
              'pid': self.pid, 
              'creator': self.creator,
              'date_created': self.date_created,
        }


class Task(object):
    def __init__(self, tid, creator, date_created):
        self.tid = tid
        self.creator = creator
        self.date_created = date_created
        
        
    def to_dict(self):
        return {
              'tid': self.tid, 
              'creator': self.creator,
              'date_created': self.date_created,
        }

# Use a service account.
cred = credentials.Certificate('taskforge-9aea9-firebase-adminsdk-xaffr-c54a827d6c.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

a = User(0, 'x1@gmail.com', 'tim', True, False)
b = User(1, 'x2@gmail.com', 'john', False, False)
c = User(2, 'x3@gmail.com', 'alex', False, False)
d = User(3, 'x4@gmail.com', 'whitney', False, False)
e = User(4, 'x5@gmail.com', 'jen', True, False)


users_ref = db.collection('users')
users_ref.document('0').set(a.to_dict())
users_ref.document('2').set(b.to_dict())
users_ref.document('3').set(c.to_dict())
users_ref.document('4').set(d.to_dict())
users_ref.document('5').set(e.to_dict())


#QUERYING THE USERS COLLECTION
users_ref = db.collection('users')
query = users_ref.where('is_admin', '==', 'True')

#docs = db.collection('users').where('is_admin', '==', True).stream()
#for doc in docs:
#    print(f'{doc.id} => {doc.to_dict()}')
    

docs = db.collection('users').where('uid', '>', 6).stream()
dict_list = []
for doc in docs:
    #dict_list.append(doc.to_dict())
    result = doc.to_dict()
    if (result == {}) : print("none")
    print(result)
#print(result.get('display_name'))


#ADDING NEW COLLECTION, PROJECTS

p0 = Project(0, 0, datetime.datetime.now())
t0 = Task(0, 0, datetime.datetime.now())

projects_ref = db.collection('projects')
projects_ref.document('0').set(p0.to_dict())


#ADDING TASKS AS A SUBCOLLECTION INSIDE OF A PROJECT DOCUMENT
p0_ref = db.collection('projects').document('0')
t0_ref = p0_ref.collection('tasks').document('0')
t0_ref.set(t0.to_dict())
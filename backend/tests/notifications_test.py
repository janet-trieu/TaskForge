'''
# 1new connection request
    # {User} has requested to connect. Accept Decline - !! remove after response !!
# 2project invitation
    # {User} has invited you to join {project}. Accept Decline - !! remove after response !!
# 3assigned a task
    # You have been assigned {task} in {project}.
# 4comment added in task
    # {User} has commented on {task} in {project}.
# 5upcoming assigned task deadline
    # {Task} is due soon. - put this up when due in 1 day
# 6new review
    # {User} has reviewed you.
# 7achievement gained
    # You have gained {achievement} achievement.
# 8request to leave
    # {User} has requested to leave {project}. Accept Decline - !! remove after response !!

# EXCEPTIONS
# - tries to accept even if already responded to connection or project req (happens when accepted via email during time)
# - User or project or task or comment does not exist
# - user is not project master for leave
'''

'''
TODO
- Update functions when implemented
    - create project
    - create task
    - send connect req
    - clear database
'''

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth

# ============ SET UP ============ #
# Use a service account.
cred = credentials.Certificate('taskforge-9aea9-firebase-adminsdk-xaffr-c54a827d6c.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

notf_ref = db.collection("notifications").stream


def setup():
    auth.create_user(uid=1, display_name='John Doe')
    auth.create_user(uid=2, display_name='Jane Doe')

    create_project() # user 1 creates project
    create_task() # user 1 creates task in project

# ============ TESTS ============ #

def test_connection_req_notification():
    setup()

    send_req() # user 1 send connection request to user 2

    #ensure connection requestion notification exists in db
    # loop through notifications database and check if match
    for notf in notf_ref:
        # if ID = user1 && prompt_ID = user2 && type == req && time == timestamp
            # end loop, notification successful
    # if not found raise error
    clear_db()

def test_project_inv_notification():
    #setup()
    #ensure project inv notification exists in db
    # loop through notifications database and check if match
    for notf in notf_ref:
        # if ID = user1 && prompt_ID = user2 && type == inv && time == timestamp && pid == pid
            # end loop, notification successful
    # if not found raise error
    #clear data
    pass

def test_assigned_notification():
    #setup()
    #ensure assigned notification exists in db
    #clear data
    pass

def test_comment_notification():
    #setup()
    #ensure comment notification exists in db
    #clear data
    pass

def test_deadline_notification():
    #setup()
    #ensure deadline notification exists in db
    #clear data
    pass

def test_review_notification():
    #setup()
    #ensure project inv notification exists in db
    #clear data
    pass

def test_achievement_notification():
    #setup()
    #ensure achievement notification exists in db
    #clear data
    pass

def test_leave_req_notification():
    #setup()
    #ensure leave req notification exists in db
    #clear data
    pass

def test_invalid_uid():
    #setup()
    # ensure notification does not exist in db
    #clear data
    pass

def test_invalid_pid():
    #setup()
    # ensure notification does not exist in db
    #clear data
    pass

def test_invalid_tid():
    #setup()
    # ensure notification does not exist in db
    #clear data
    pass

def test_invalid_achievement():
    #setup()
    # ensure notification does not exist in db
    #clear data
    pass
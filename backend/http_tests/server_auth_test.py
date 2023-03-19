'''
Test file for Flask http testing of authentication reset password (user invoked) functionality
'''
import requests
from src.authentication import *
from src.test_helpers import *

port = 5000
url = f"http://localhost:{port}/"

try:
    create_user_email("authtest0@gmail.com", "password123", "Auth Doe")
except auth.EmailAlreadyExistsError:
    pass

user_id = auth.get_user_by_email("authtest0@gmail.com").uid

def test_reset_password():

    reset_resp = requests.post(url + "authentication/reset_password", headers={
        "Authorization": user_id
    })

    assert reset_resp.status_code == 200

def test_reset_password_invalid_uid():

    invalid_user_id = "my name is invalid uid and i hate being valid"

    reset_resp = requests.post(url + "authentication/reset_password", headers={
        "Authorization": invalid_user_id
    })

    assert reset_resp.status_code == 400

# Reset database
delete_user(user_id)
reset_firestore_database()
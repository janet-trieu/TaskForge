'''
Test file for Flask http testing of authentication reset password (user invoked) functionality
'''
import requests
port = 5000
url = f"http://localhost:{port}/"

def test_reset_password():

    reset_resp = requests.post(url + "authentication/reset_password", json={
        "uid": "3TssNFyMXmOtTGarpRtAZ7VrOd72"
    })

    assert reset_resp.status_code == 200

def test_reset_password_invalid_uid():

    reset_resp = requests.post(url + "authentication/reset_password", json={
        "uid": "Xaao51rHZ9fJK6U6J0NtPixAh0k2"
    })

    assert reset_resp.status_code == 400
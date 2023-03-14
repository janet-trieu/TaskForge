import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json
import urllib


# Use this fixture to get the URL of the server. It starts the server for you,
# so you don't need to.
@pytest.fixture(name="url")
def fixture_url():
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "src/server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")
        

def test_give_admin_success(url):
    """
    Successfully giving admin to another user
    """
    json_dict = {'uid_admin': 'sklzNex5udNeOd65uvsuGAYBNkH2', 'uid_user': 'xyzabc123',}
    resp = requests.post(url + '/admin/give_admin', json=json_dict)

    payload = resp.json()

    assert payload == 0
    assert resp.status_code == 200

def test_give_admin_failure(url):
    """
    Giving an int instead of a string
    """
    json_dict = {'uid_admin': 0, 'uid_user': 1,}
    resp = requests.post(url + '/admin/give_admin', json=json_dict)

    assert resp.status_code == 400

def test_ban_user_success(url):
    """
    Successfully banning user by an admin
    """
    json_dict = {'uid_admin': 'sklzNex5udNeOd65uvsuGAYBNkH2', 'uid_user': 'xyzabc123',}
    resp = requests.post(url + '/admin/ban_user', json=json_dict)

    payload = resp.json()

    assert payload == 0
    assert resp.status_code == 200
    
def test_ban_user_failure(url):
    """
    Giving an int instead of a string
    """
    json_dict = {'uid_admin': 0, 'uid_user': 1,}
    resp = requests.post(url + '/admin/ban_user', json=json_dict)

    assert resp.status_code == 400
    
def test_unban_user_success(url):
    """
    Successfully unbanning user by an admin
    """
    json_dict = {'uid_admin': 'sklzNex5udNeOd65uvsuGAYBNkH2', 'uid_user': 'xyzabc123',}
    resp = requests.post(url + '/admin/unban_user', json=json_dict)

    payload = resp.json()

    assert payload == 0
    assert resp.status_code == 200
    
def test_unban_user_failure(url):
    """
    Giving an int instead of a string
    """
    json_dict = {'uid_admin': 0, 'uid_user': 1,}
    resp = requests.post(url + '/admin/unban_user', json=json_dict)

    assert resp.status_code == 400

def test_remove_user_success(url):
    """
    Successfully removing user by an admin
    """
    json_dict = {'uid_admin': 'sklzNex5udNeOd65uvsuGAYBNkH2', 'uid_user': 'xyzabc123',}
    resp = requests.post(url + '/admin/remove_user', json=json_dict)

    payload = resp.json()

    assert payload == 0
    assert resp.status_code == 200
   
def test_remove_user_failure(url):
    """
    Giving an int instead of a string
    """
    json_dict = {'uid_admin': 0, 'uid_user': 1,}
    resp = requests.post(url + '/admin/remove_user', json=json_dict)

    assert resp.status_code == 400
   
def test_readd_user_success(url):
    """
    Successfully readding user by an admin
    """
    json_dict = {'uid_admin': 'sklzNex5udNeOd65uvsuGAYBNkH2', 'uid_user': 'xyzabc123',}
    resp = requests.post(url + '/admin/readding_user', json=json_dict)

    payload = resp.json()

    assert payload == 0
    assert resp.status_code == 200
    
def test_readd_user_failure(url):
    """
    Giving an int instead of a string
    """
    json_dict = {'uid_admin': 0, 'uid_user': 1,}
    resp = requests.post(url + '/admin/readd_user', json=json_dict)

    assert resp.status_code == 400
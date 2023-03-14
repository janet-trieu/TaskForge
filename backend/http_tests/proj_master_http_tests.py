'''
Test file for Flask http testing of project master feature
'''
import pytest
import requests
from tests.test_helpers import *
port = 5010
url = "http://localhost:{port}/"

def test_create_project_use_default_vals():

    reset_project_count()

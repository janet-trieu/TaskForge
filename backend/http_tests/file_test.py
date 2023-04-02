import pytest
import requests
from src.test_helpers import *
from src.helper import *
from src.profile_page import *
from src.notifications import *
from src.connections import *
from src.proj_master import *

port = 8000
url = f"http://localhost:{port}/"


def test_file_upload():
    pass
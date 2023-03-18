import pytest
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from src.connections import connection_request_respond, get_connection_requests, get_connected_taskmasters
from src.error import *
from src.helper import *


def test_uid_type_connection_request_respond():
    try:
        connection_request_respond(1, 2, True)
    except InputError:
        pass

def test_success_connection_request_respond():
    pass


def test_uid_type_get_connection_requests():
    try:
        get_connection_requests(1)
    except InputError:
        pass
        
def test_uid_type_get_connected_taskmasters():
    try:
        get_connected_taskmasters(1)
    except InputError:
        pass
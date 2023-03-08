'''
Blackbox testing of Project Management Feature

*** currently only implementing create_project()
'''

import pytest
from src.projects import *
from datetime import date
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('taskforge-9aea9-firebase-adminsdk-xaffr-c80ed6513a.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

def test_create_project1():

    # test for project creation
    uid = 0
    name = "Project1"
    description = "Creating Project1 for testing"
    status = "Not Started"
    due_date = None
    team_strength = None
    picture = None
    result = create_project(uid, name, description, status, due_date, team_strength, picture)

    assert result == 0

def test_create_project2():

    # test for project creation
    uid = 0
    name = "Project2"
    description = "Creating Project2 for testing"
    status = "Completed"
    due_date = date.fromisoformat("2023-12-31")
    team_strength = 5
    picture = "test1.jpg"
    result = create_project(uid, name, description, status, due_date, team_strength, picture)

    assert result == 1

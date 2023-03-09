'''
Blackbox testing of Project Management Feature

*** currently only implementing create_project()
'''

import pytest
from datetime import datetime, date
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from src.projects import *

# cred = credentials.Certificate('taskforge-9aea9-firebase-adminsdk-xaffr-c80ed6513a.json')
# app = firebase_admin.initialize_app(cred)
# db = firestore.client()

def test_create_project_use_default_vals():

    # test for project creation
    uid = 1
    name = "Project0"
    description = "Creating Project0 for testing"
    status = None
    due_date = None
    team_strength = None
    picture = None
    result = create_project(uid, name, description, status, due_date, team_strength, picture)

    assert result == 0

    # # reset database
    # db.collection("projects_test").document("0").delete()

def test_create_project_every_args():

    # test for project creation
    uid = 1
    name = "Project1"
    description = "Creating Project1 for testing"
    status = "In Progress"
    due_date = "2023-12-31"
    team_strength = 5
    picture = "test1.jpg"

    result = create_project(uid, name, description, status, due_date, team_strength, picture)

    assert result == 0

    # # reset database
    # db.collection("projects_test").document("0").delete()

# def test_create_multiple_projects():

#     # test for project1 creation
#     uid = 0
#     name = "Project1"
#     description = "Creating Project1 for testing"
#     status = None
#     due_date = None
#     team_strength = None
#     picture = None

#     result = create_project(uid, name, description, status, due_date, team_strength, picture)

#     assert result == 0

#     # test for project2 creation
#     uid = 0
#     name = "Project1"
#     description = "Creating Project1 for testing"
#     status = None
#     due_date = None
#     team_strength = None
#     picture = None

#     result = create_project(uid, name, description, status, due_date, team_strength, picture)

#     assert result == 1

def test_create_project_invalid_uid():

    # test for project creation with invalid input
    uid = -1
    name = "Project1"
    description = "description"
    status = "Not Started"
    due_date = None
    team_strength = None
    picture = None

    with pytest.raises(ValueError):
        create_project(uid, name, description, status, due_date, team_strength, picture)

def test_create_project_invalid_uid_type():

    # test for project creation with invalid input
    uid = "1"
    name = "Project1"
    description = "description"
    status = "Not Started"
    due_date = None
    team_strength = None
    picture = None

    with pytest.raises(TypeError):
        create_project(uid, name, description, status, due_date, team_strength, picture)

def test_create_project_invalid_name_type():

    # test for project creation with invalid input
    uid = 0
    name = 1
    description = "description"
    status = "Not Started"
    due_date = None
    team_strength = None
    picture = None

    with pytest.raises(TypeError):
        create_project(uid, name, description, status, due_date, team_strength, picture)

def test_create_project_invalid_name():

    # test for project creation with invalid input
    uid = 0
    name = ""
    description = "description"
    status = "Not Started"
    due_date = None
    team_strength = None
    picture = None

    with pytest.raises(ValueError):
        create_project(uid, name, description, status, due_date, team_strength, picture)

def test_create_project_invalid_name_length():

    # test for project creation with invalid input
    uid = 0
    name = "A"*51
    description = "description"
    status = "Not Started"
    due_date = None
    team_strength = None
    picture = None

    with pytest.raises(ValueError):
        create_project(uid, name, description, status, due_date, team_strength, picture)

def test_create_project_invalid_description():

    # test for project creation with invalid input
    uid = 0
    name = "Project0"
    description = ""
    status = "Not Started"
    due_date = None
    team_strength = None
    picture = None

    with pytest.raises(ValueError):
        create_project(uid, name, description, status, due_date, team_strength, picture)

def test_create_project_invalid_description_length():

    # test for project creation with invalid input
    uid = 0
    name = "Project0"
    description = "A"*1001
    status = "Not Started"
    due_date = None
    team_strength = None
    picture = None

    with pytest.raises(ValueError):
        create_project(uid, name, description, status, due_date, team_strength, picture)

def test_create_project_invalid_description_type():

    # test for project creation with invalid input
    uid = 0
    name = "Project0"
    description = 0
    status = "Not Started"
    due_date = None
    team_strength = None
    picture = None

    with pytest.raises(TypeError):
        create_project(uid, name, description, status, due_date, team_strength, picture)

def test_create_project_invalid_status():

    uid = 0
    name = "Project 1"
    description = "description"
    status = "NotStarted"
    due_date = None
    team_strength = None
    picture = None

    with pytest.raises(ValueError):
        create_project(uid, name, description, status, due_date, team_strength, picture)

def test_create_project_invalid_status_type():

    uid = 0
    name = "Project1"
    description = "description"
    status = 0
    due_date = None
    team_strength = None
    picture = None

    with pytest.raises(TypeError):
        create_project(uid, name, description, status, due_date, team_strength, picture)

def test_create_project_invalid_team_strength():

    uid = 0
    name = "Project1"
    description = "description"
    status = "Not Started"
    due_date = None
    team_strength = -1
    picture = None

    with pytest.raises(ValueError):
        create_project(uid, name, description, status, due_date, team_strength, picture)

def test_create_project_invalid_team_strength_type():

    uid = 0
    name = "Project1"
    description = "description"
    status = "Not Started"
    due_date = None
    team_strength = "1"
    picture = None

    with pytest.raises(TypeError):
        create_project(uid, name, description, status, due_date, team_strength, picture)

# test for invalid picture input


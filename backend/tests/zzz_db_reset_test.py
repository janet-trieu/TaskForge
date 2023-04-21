'''
Dummy helper file used to reset the firestore database (both auth database and storage database)
 - was used for testing purposes
'''

from src.test_helpers import *
import pytest

def test_reset_everything():
    reset_database()
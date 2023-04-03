import pytest
from src.test_helpers import *
from src.profile_page import *
from src.proj_master import *
from src.projects import *
from src.helper import *
from src.achievement import *

def test_get_0():
    reset_database()

    pm_uid = create_user_email("achievements.pm@gmail.com", "admin123", "Project Master")
    
    res = check_achievement("user_creation", pm_uid)

    assert res == True
    assert 0 in get_achievements_uid(pm_uid)

    tm1_uid = create_user_email("achievements.tm1@gmail.com", "fuckingpassword123", "Task Master")

    res = check_achievement("user_creation", tm1_uid)

    assert res == False
    assert 0 not in get_achievements_uid(tm1_uid)

    reset_database()

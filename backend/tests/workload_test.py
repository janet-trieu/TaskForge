from src.error import *
from src.helper import *
from src.profile_page import *
from src.notifications import *
from src.global_counters import *
from src.test_helpers import *
from src.workload import *
from src.taskboard import *
from src.proj_master import *
import datetime

try:
    uid = create_user_email("workload1@gmail.com", "wl112312321", "wl1123123")
except auth.EmailAlreadyExistsError:
    pass

uid = auth.get_user_by_email("workload1@gmail.com").uid
pid = create_project(uid, "Project 123", "description", None, None, None)
 
def test_get_user_workload():
    assert(get_user_workload(uid) == 0)
    curr_time = datetime.datetime.now()
    create_task(uid, pid, None, [], "", "", curr_time + datetime.timedelta(minutes=100), 2, "Low", "In Progress")
    assert(get_user_workload(uid) == 2)
    create_task(uid, pid, None, [], "", "", curr_time + datetime.timedelta(minutes=100), 3, "Low", "In Progress")
    assert(get_user_workload(uid) == 5)
    
def test_update_availability():
    update_user_availability(uid, 4.5)
    assert(get_availability(uid) == 4.5)
    
def test_availability_ratio():
    assert(get_availability_ratio(uid) == 5/4.5)

def test_supply_and_demand():
    calculate_supply_demand(uid)
    data = get_supply_and_demand(uid)
    assert(data[0]["demand"] == 5)
    assert(data[0]["supply"] == 4.5)

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
    uid = create_user_email("wl@gmail.com", "wl112312321", "wl1123123")
except auth.EmailAlreadyExistsError:
    pass

uid = auth.get_user_by_email("wl@gmail.com").uid
pid = create_project(uid, "Project 123", "description", None, None, None)
 
def test_get_user_workload():
    assert(get_user_workload(uid, pid) == 0)
    curr_time = datetime.datetime.now()
    create_task(uid, pid, None, [uid], "", "", curr_time + datetime.timedelta(minutes=100), 2, "Low", "In Progress")
    assert(get_user_workload(uid, pid) == 2)
    create_task(uid, pid, None, [uid], "", "", curr_time + datetime.timedelta(minutes=100), 3, "Low", "In Progress")
    assert(get_user_workload(uid, pid) == 5)
    
def test_update_availability():
    update_user_availability(uid, pid, 4.5)
    assert(get_availability(uid, pid) == 4.5)
    
def test_availability_ratio():
    assert(get_availability_ratio(uid, pid) == 5/4.5)

def test_supply_and_demand():
    calculate_supply_demand(pid)
    data = get_supply_and_demand(pid)
    assert(data[0]["demand"] == 5)
    assert(data[0]["supply"] == 4.5)
    try:
        uid2 = create_user_email("wl2@gmail.com", "wl2112312321", "wl11223123")
    except auth.EmailAlreadyExistsError:
        pass
    uid2 = auth.get_user_by_email("wl2@gmail.com").uid
    add_tm_to_project(pid, uid2)
    create_task(uid2, pid, None, [uid2], "", "", datetime.datetime.now() + datetime.timedelta(minutes=100), 1, "Low", "In Progress")
    calculate_supply_demand(pid)
    data = get_supply_and_demand(pid)
    assert(data[1]["demand"] == 6)
    assert(data[1]["supply"] == 9.5)
    
    remove_project_member(pid, uid, uid2)
    calculate_supply_demand(pid)
    data = get_supply_and_demand(pid)
    assert(data[2]["demand"] == 5)
    assert(data[2]["supply"] == 4.5)
    
def atest_reset():
    reset_database()
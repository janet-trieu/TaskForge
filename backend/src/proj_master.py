'''
Feature: Project Master
Functionalities:
 - revive_completed_project()
 - remove_project_member()
 - request_leave_project()
 - invite_to_project()
'''

'''
Revives a project where its status has been set to complete,
but have be able to bring it back into progress
pid = project id
uid = user id
'''
def revive_completed_project(pid, uid):
    '''
    check whether supplied pid exists
    check whether supplied uid exists

    set project's status back into review
    '''
    pass

def remove_project_member():
    pass

# Below shouldnt be in proj_master, but keeping it here till we find somewhere more appropriate
# def reqeust_leave_project():
#     pass

def invite_to_project():
    pass
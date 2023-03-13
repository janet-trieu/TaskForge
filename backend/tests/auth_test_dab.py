'''
Temporary test file for authentication user-invoked reset password
'''
def test_reset_password():

    email = "dabin.haam@gmail.com"
    link = auth.generate_password_reset_link(email, {})

    assert not link == None


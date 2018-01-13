xiv_data = {
    'account_id': 'xxxxxx', # account_id
    'username': 'xxxxxx',   # device_id
    'password': 'xxxxxx',   # device_password
    'login_username': "xxxxxx", # user_email
    'login_password': "xxxxxx", # user_password
    'topic': "xi/blue/v1/[account_id]/d/[username]/random_values"
}
xiv_data['topic'] = "xi/blue/v1/" + xiv_data['account_id'] + "/d/" + xiv_data['username'] + "/random_values"

push_data = {
    'app_id': 'xxxxxx',
    'key': 'xxxxxx',
    'secret': 'xxxxxx',
    'cluster': 'xx',
    'ssl': True
}

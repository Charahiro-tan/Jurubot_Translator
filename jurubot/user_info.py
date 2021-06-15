import oauth_key
import requests

client_id = '0vak4vlm2cdhrpwgq1iabfs38u5h5d'

class GetUserInfo:
    def __init__(self):
        self.user_info_url = 'https://api.twitch.tv/helix/users?login={}'
        self.token         = oauth_key.token
        self.headers       = {'Authorization':'Bearer '+self.token , 'Client-Id':client_id}
    
    def get_display_name(self, user_login):
        res = requests.get(self.user_info_url.format(user_login), headers=self.headers)
        if res.status_code == 200:
            json = res.json()
            display_name = json['data'][0]['display_name']
        else:
            display_name = ''
        return display_name
    
    def get_user_id(self, user_login):
        res = requests.get(self.user_info_url.format(user_login), headers=self.headers)
        if res.status_code == 200:
            json = res.json()
            user_id = json['data'][0]['id']
        else:
            user_id = ''
        return user_id

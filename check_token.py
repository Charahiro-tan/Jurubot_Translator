import requests

client_id = '0vak4vlm2cdhrpwgq1iabfs38u5h5d'
url = 'https://id.twitch.tv/oauth2/validate'

def check_token(token):
    validate = False
    login_id = ''
    token = token.removeprefix('oauth:')
    header = {'Authorization':'OAuth {}'.format(token)}
    res = requests.get(url, headers=header)
    if res.status_code == 200:
        json = res.json()
        if json.get('client_id') == client_id:
            validate = True
            login_id = json.get('login')
    else:
        print('有効なトークンではありません。もう一度取得してみてください。')
        login_id = ''
    return validate, login_id

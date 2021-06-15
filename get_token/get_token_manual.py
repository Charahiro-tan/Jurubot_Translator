import time
import webbrowser

import pyperclip

import check_token

URL = "https://id.twitch.tv/oauth2/authorize?client_id=0vak4vlm2cdhrpwgq1iabfs38u5h5d&redirect_uri=https://twitchapps.com/tmi/&response_type=token&scope=chat:read+chat:edit"
token  = ''

# クリップボードにアクセスできるかチェック
copy = False
try:
    c = 'jurubot'
    clip = pyperclip.paste()
    pyperclip.copy(c)
    p = pyperclip.paste()
    if p == c:
        copy = True
        pyperclip(clip)
except:
    pass


# クリップボードにアクセスできたとき
if copy:
    
    print('''
トークンの取得方法(まぁまぁ手動ver.)
-------------------------------------------------------------
以下の中からどちらかを選び、"BOTのアカウント"で承認してください。
oauth:～という文字列が出てきたら、[Ctrl + C]でコピーしてください。
クリップボードを監視してるので自動的に読み込まれます。

    ''')
    while True:
        print('''
認証ページにどうやって行きますか？
(1) ブラウザで開く(多分Edge)
(2) URLをクリップボードにコピーする
(3) URLを表示する

        ''')
        num = input('番号を入力してEnterを押してください > ')
        if num == '':
            pass
        elif int(num) == 1:
            try:
                browser = webbrowser.get('windows-default')
                browser.open_new_tab(URL)
                break
            except:
                print('ブラウザが取得できませんでした')
                time.sleep(2)
        elif int(num) == 2:
            try:
                pyperclip.copy(URL)
                break
            except:
                print('クリップボードにコピーできませんでした')
                time.sleep(2)
        elif int(num) == 3:
            print('\r\n')
            print(URL)
            break
        else:
            print('もう一度入力してください')
            time.sleep(2)
        
    print('''
2分間クリップボードを監視します。
コピーした内容がそのまま読み込まれます。
oauth:はついたままコピーしてください。

コピーとペーストができることは確認してますが、もし読み込まれなかった場合は
2分経つと入力できるようになるのでそこに貼り付けてください。

    ''')
        
    sec = 0
    while sec <= 120:
        time.sleep(1)
        sec += 1
        try:
            token = pyperclip.paste()
            if token.startswith('oauth:'):
                print('トークンを取得できました')
                break
        except:
            break
    
    while not token.startswith('oauth:'):
        token = input('トークンをペースト(入力)してEnterを押してください > ')

# クリップボードにアクセスできなかったとき
else:
    print('''
トークンの取得方法(まぁまぁ手動ver.)
-------------------------------------------------------------
以下の中からどちらかを選び、"BOTのアカウント"で承認してください。
oauth:～という文字列が出てきたら、[Ctrl + C]でコピーしてください。

    ''')
    print('''
認証ページにどうやって行きますか？
(1) ブラウザで開く(多分Edge)
(2) URLを表示する

    ''')
    while True:
        num = input('番号を入力してEnterを押してください > ')
        
        if num == '':
            pass
        elif int(num) == 1:
            try:
                browser = webbrowser.get('windows-default')
                browser.open_new_tab(URL)
                break
            except:
                print('ブラウザが取得できませんでした')
                time.sleep(2)
        elif int(num) == 2:
            print('\r\n')
            print(URL)
            break
        else:
            print('もう一度入力してください')
            time.sleep(2)
    print('''
認証したら表示されたoauth:～の文字列をペーストしてください。
oauth:はついたままペーストしてください。

    ''')
    
    while not token.startswith('oauth:'):
        token = input('トークンをペースト(入力)してEnterを押してください > ')


token = token.replace('oauth:','')
print('トークンをチェック中....')
validate, login_id = check_token.check_token(token)
if validate:
    print(f'Botに使うアカウントは「{login_id}」でよろしいですか？')
    input('よろしければEnterを押してください。違う場合は一度閉じて最初からやり直してください >')
    
    with open ('oauth_key.py', mode='w') as f:
        f.write(f"token = '{token}'")
    
    print('トークンが取得できました。3秒後に終了します...')
    time.sleep(3)
    quit()
else:
    print('どうしても取得できない場合はお知らせください')
    print('3秒後に終了します....')
    time.sleep(3)
    quit()

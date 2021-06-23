import http.server as server
import time
from urllib.parse import parse_qs, urlparse

import pyperclip

import check_token

html = '''
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8" />
    <title>認証</title>
    </head>
    <script>
        if (location.hash) {
        var hash = location.hash
        var query = hash.replace("#","?")
        var url = "http://localhost/" + query
        location.replace(url)
        }
    </script>
    <body>
        <a href="https://id.twitch.tv/oauth2/authorize?client_id=0vak4vlm2cdhrpwgq1iabfs38u5h5d&redirect_uri=http://localhost&response_type=token&scope=chat:read+chat:edit">ここをクリックしてBotで使うアカウントで認証してください</a>
    </body>
    </html>
    '''

close_html ='''
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8" />
        <title>認証完了</title>
    </head>
    <body>
        ブラウザを閉じてコンソールに戻ってください。
    </body>
</html>
'''


class MyHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.query:
            token = parse_qs(parsed.query)['access_token']
            token = token[0]
            self.wfile.write(close_html.encode())
            
            print('トークンをチェック中....')
            time.sleep(1)
            validate, login_id = check_token.check_token(token)
            if validate:
                print(f'Botに使うアカウントは「{login_id}」でよろしいですか？')
                input('よろしければEnterを押してください。違う場合は一度閉じて最初からやり直してください >')
                
                with open ('oauth_key.py', mode='w') as f:
                    f.write(f"token = '{token}'")
                
                print('トークンが取得できました。')
                quit()
            else:
                print('終了します....')
                quit()
        else:
            self.wfile.write(html.encode())


if __name__ == '__main__':
    print('''
トークンの取得方法(ほぼ自動ver.)
------------------------------------------------------------------------------------------
自動取得では今実行してるPCに一時的にサーバーを建てることで取得します。
実行すると警告文が出るかもしれませんが、外部からアクセスできるサーバーではありません。
気になる方や、セキュリティソフトなどにブロックされて起動できない場合は手動取得で取得してください。
サーバーが起動したあと、http://localhost にアクセスして認証してください。

''')
    
    print('"http://localhost"をクリップボードにコピーしますか？')
    while True:
        num = input('コピーする場合は「1」しない場合は「2」を入力してEnterを押してください > ')
        
        if num == '':
            pass
        elif int(num) == 1:
            try:
                pyperclip.copy('http://localhost')
                print('クリップボードに"http://localhost"をコピーしました。')
                break
            except:
                print('クリップボードにコピーできませんでした。このままサーバーを起動します....')
                break
        elif int(num) == 2:
            break
        else:
            print('1か2を入力してください....')
    
    host = 'localhost'
    port = 80
    httpd = server.HTTPServer((host, port), MyHandler)
    print('サーバを起動しました。http://localhostにアクセスしてください。')
    try:
        httpd.serve_forever()
    except:
        quit()

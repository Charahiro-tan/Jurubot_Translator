##################################################
# 翻訳の設定
# 変更した設定は次回起動時から適用されます
##################################################
# []でくくってある項目は""でくくって,で区切ることでいくつも設定できます。

# 無視するユーザー
ignore_user = ["Nightbot","Streamelements","Moobot"]

# 翻訳する前に削除するワード。正規表現対応。
# URLや同じ言葉の繰り返しなどはデフォルトで削除してますので足りなかったら追加してください。
del_word = ["88+","８８+"]

# 無視する言語。
# 言語コードは https://cloud.google.com/translate/docs/languages 参照
ignore_lang = ["",""]

# 配信者が使用している言語。あらゆる言語がこの言語に翻訳されます。
home_lang = "ja"

# 上のhome_langで投稿された時の翻訳先
default_to_lang = "en"

# translate.googleのURLのサフィックス。日本の方ならこのままで。
url_suffix = "co.jp"

# 翻訳結果に発言者の名前を入れる場合はTrue、入れない場合はFalse
sender = True

# 上がTrueの場合に表示する名前
# "displayname" でディスプレイネーム
# "loginid" でログインID
sender_name = "displayname"

# 翻訳結果に言語情報((en → ja)みたいな)を付ける場合はTrue、付けない場合はFalse
language = True

# Google Apps Scriptで作成したAPIを使用するときはTrue、しないときはFalse
# Google Apps Scriptを使用するときは必ずReadmeを読んでください。
gas = False

# Google Apps Scriptで作成したURL
gas_url = ""
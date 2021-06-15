##################################################
# 基本設定
# 変更した設定は次回起動時から適用されます
##################################################

# 接続するチャンネル
channel   = "__Your_Channel__"

# Botのカラー 下の中から選択
# 'Red','Blue','Green','Firebrick','Coral','YellowGreen',
# 'OrengeRed','SeaGreen','GoldenRod','Chocolate','CadetBlue',
# 'DodgerBlue','HotPink','BlueViolet','SpringGreen'
bot_color = "HotPink"

# 送信するメッセージの先頭に何か付けたいときは設定
# 何もつけないときは = ""
send_message_prefix = "🐻＜"

# 送信するメッセージに/meをつける場合はTrue、つけない場合はFalse
send_me = False

# 翻訳を有効にするときはTrue、無効にしたいときはFalse
# 翻訳の設定詳細なはconfig_translator.pyでできます。
translate = True

##################################################
# メッセージタイマーの設定
##################################################
# メッセージタイマー(一定時間ごとに定型文を流す)を有効にするときはTrue、無効にするときはFalse
timer = False

# メッセージタイマーの間隔(分)
timer_interval = 15

# 流すメッセージ
timer_message = "I'm using a translator so don't hesitate to comment!"

##################################################
# 棒読みちゃんの設定
#
# 棒読みちゃんの
# 「設定→システム→アプリケーション連携→HTTP連携→ローカルHTTPサーバー機能を使う」
# がTrueになってることを確認してください。
##################################################
# メッセージを棒読みちゃんに送りたいときはTrue、無効にしたいときはFalse
bouyomi = False

# 棒読みちゃんのHTTP連携ポート(棒読みちゃんの設定→アプリケーション連携→HTTP連携→ポート番号)
bouyomi_port = 50080

# 棒読みちゃんにBotのコメントを読ませるときはTrue、読ませないときはFalse
bouyomi_bot = False

# 棒読みちゃんに読み上げさせる文章(Botのコメント用)
# 
# {bot_name}    = ボットのログインID
# {bot_disp}    = ボットのディスプレイネーム
# {sender_name} = 発言者のログインID
# {sender_disp} = 発言者のディスプレイネーム
# {msg}         = コメント
# 
# 棒読みちゃんに「(ボットの名前)さん、(コメント)」と読ませるときは
# bouyomi_bot_content = "{disp_name}さん、{message}"
# となります。
bouyomi_bot_content = "{msg}"

# 棒読みちゃんに読み上げさせる文章(受信したコメント用)
# 整形、未整形は翻訳と同じ設定になります。
#
# {sender_name}   = ログインID
# {sender_disp}   = ディスプレイネーム
# {raw_msg}       = 未整形(受信したメッセージそのまま)メッセージ
# {emote_del_msg} = 整形済(NGワードやエモートを取り除いた)メッセージ
# 
# 要領は上と同じ。
bouyomi_content = "{sender_disp}さん、 {emote_del_msg}"

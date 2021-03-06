import re

import requests
from twitchio import Message
from natsort import natsorted

import config_bot
import config_translator
import user_info
import oauth_key

del_word_def = [r"^(.)\1+$",r"ww+",r"ｗｗ+",r"^@\S*",r"https?://[\w!\?/\+\-_~=;\.,\*&@#\$%\(\)'\[\]]+"]

emotes_compiled = []
del_word_compiled = []
cheer_compiled = []


def msg_fmt(message: Message):
    msg = message.content
    
    # エモート削除
    if message.tags['emotes']:
        emotes = message.tags['emotes']
        emote_pos = re.findall('\d+-\d+', emotes)
        emote_pos = natsorted(emote_pos, reverse=True)
        for pos in emote_pos:
            pos = pos.split('-')
            msg = msg[:int(pos[0])] + msg[int(pos[1]) +2:]
    
    # 削除ワード削除
    for w in del_word_compiled:
        msg = w.sub('', msg)
    
    # BTTVエモート削除
    for w in emotes_compiled:
        msg = w.sub('', msg)
    
    # cheer削除
    if 'bits' in message.tags:
        for w in cheer_compiled:
            msg = w.sub('', msg)
    
    # 文頭、文末のスペースを削除
    msg = msg.strip()
    
    return msg

def get_emotes(streamer_id):
    global emotes_compiled
    print('BTTVエモート取得中...')
    bttv_global_url  = 'https://api.betterttv.net/3/cached/emotes/global'
    bttv_channel_url = 'https://api.betterttv.net/3/cached/users/twitch/{}'.format(streamer_id)
    ffz_global_url   = 'https://api.frankerfacez.com/v1/set/global'

    def get(url):
        try:
            res = requests.get(url)
            if res.status_code == 200:
                res_json = res.json()
            else:
                res_json = {}
        except:
            print(f'{url}からエモートが取得できませんでした....')
            res_json = {}
        return res_json
    
    
    bttv_global_json  = get(bttv_global_url)
    try:
        bttv_global_emote = [d.get('code') for d in bttv_global_json]
    except:
        bttv_global_emote = []
    
    ffz_global_json = get(ffz_global_url)
    try:
        ffz_global_emote  = [d.get('name') for d in ffz_global_json['sets']['3']['emoticons']]
    except:
        ffz_global_emote  = []
    
    bttv_channel_json = get(bttv_channel_url)
    try:
        bttv_channel_emote = [d.get('code') for d in bttv_channel_json['channelEmotes']]
        bttv_channel_sharedemote = [d.get('code') for d in bttv_channel_json['sharedEmotes']]
    except:
        bttv_channel_emote = []
        bttv_channel_sharedemote = []
    
    emotes = bttv_global_emote + bttv_channel_emote + bttv_channel_sharedemote + ffz_global_emote
    emotes_compiled = [re.compile(w) for w in emotes]
    print('BTTVエモート取得完了！')

def get_cheer(streamer_id):
    global cheer_compiled
    print('Cheerエモート取得中....')
    
    client_id = user_info.client_id
    headers = {'Authorization':f'Bearer {oauth_key.token}', 'Client-id':client_id}
    URL = 'https://api.twitch.tv/helix/bits/cheermotes?broadcaster_id={}'.format(streamer_id)
    
    res = requests.get(URL, headers=headers)
    if res.status_code == 200:
        json = res.json()
        try:
            cheer_list     = [d.get('prefix') for d in json['data']]
            cheer_list.sort(key=len, reverse=True)
            cheer_re       = [w+'\d+' for w in cheer_list]
            cheer_compiled = [re.compile(w, re.I) for w in cheer_re]
            print('Cheerエモート取得完了！')
        except:
            cheer_compiled = []
            print('Cheerエモートの取得に失敗しました‥‥')
    else:
        cheer_compiled = []
        print('Cheerエモートの取得に失敗しました‥‥')

def ignore_compile():
    global del_word_compiled
    print('無視ワード準備中...')
    # 削除ワード
    del_word_list = del_word_def + config_translator.del_word
    del_word_compiled = [re.compile(w) for w in del_word_list]
    
    get_user_info = user_info.GetUserInfo()
    _, streamer_id = get_user_info.get_user_info(config_bot.channel)
    # BTTV
    get_emotes(streamer_id)
    # Cheer
    get_cheer(streamer_id)
    print('無視ワード準備完了！')

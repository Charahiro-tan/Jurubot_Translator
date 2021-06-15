import asyncio
import re

import aiohttp
import config_translator
from async_google_trans_new import AsyncTranslator, constant

import msg_formatter


class Translate:
    def __init__(self):
        print('翻訳の準備中....')
        # 無視ユーザー、無視言語読み込み
        self.ignore_user = [w.lower() for w in config_translator.ignore_user]
        self.ignore_lang = [w.lower() for w in config_translator.ignore_lang]
        
        # 言語リスト準備
        self.lang_list = list(constant.LANGUAGES.keys())
        
        # urlサフィックスチェック&インスタンス生成
        print('GoogleTranslateのURLのサフィックスをチェック中....')
        urlsuffix_list = [re.search('translate.google.(.*)', url.strip()).group(1) for url in constant.DEFAULT_SERVICE_URLS]
        s = config_translator.url_suffix
        if s not in urlsuffix_list:
            url_suffix = 'co.jp'
        else:
            url_suffix = s
        print(f'URLサフィックス : "{url_suffix}"')
        self.gt = AsyncTranslator(url_suffix=url_suffix)
        
        # GASの準備
        if config_translator.gas:
            conn = aiohttp.TCPConnector(ttl_dns_cache=300)
            self.session = aiohttp.ClientSession(connector=conn)
        print('翻訳の準備完了！')
    
    async def translator(self, message):
        
        # メッセージが1文字以下の場合は無視
        if len(message.content) <=1:
            _ = __ = ___ =''
            return _, __, ___
        # メッセージが無視ユーザーの場合は無視
        if message.author.name.lower() in self.ignore_user:
            _ = __ = ___ =''
            return _, __, ___
        
        # 入れ替え
        user = message.author.name
        display_name = message.author.display_name
        
        # 整形
        msg = msg_formatter.msg_fmt(message)
        
        if len(msg) <= 1:
            _ = __ = ___ =''
            return _, __, ___
        
        # 言語選択
        lang_src = None
        lang_tgt = None
        
        # 先頭で言語が指定されているかチェック
        split_msg = msg.split(':')
        if len(split_msg) >= 2:
            if split_msg[0].lower() in self.lang_list:
                lang_tgt = split_msg[0]
                msg = ':'.join(split_msg[1:])
                detect_task = asyncio.create_task(self.gt.detect(msg))
                lang_src = await detect_task
                lang_src = lang_src[0]
            else:
                msg = ':'.join(split_msg[0:])
        else:
            msg = ':'.join(split_msg[0:])
        
        # 指定されていなかったとき
        if lang_tgt is None:
            detect_task = asyncio.create_task(self.gt.detect(msg))
            lang_src = await detect_task
            lang_src = lang_src[0]
            
            if lang_src.lower() in self.ignore_lang:
                _ = __ = ___ =''
                return _, __, ___
            elif lang_src == config_translator.home_lang:
                lang_tgt = config_translator.default_to_lang
            else:
                lang_tgt = config_translator.home_lang
        
        # 翻訳
        translated = ''
        gas_used = False
        
        if config_translator.gas:
            translated, gas_used = await self.gas_trans(msg, lang_tgt, lang_src)
        if not translated:
            trans_task = asyncio.create_task(self.gt.translate(msg, lang_tgt, lang_src))
            translated = await trans_task
        
        if not translated:
            _ = __ = ___ =''
            return _, __, ___
        
        # 投稿文組み立て
        send_msg = translated
        if config_translator.sender:
            if config_translator.sender_name == 'displayname':
                send_msg = send_msg + f'[by {display_name}]'
            elif config_translator.sender_name == 'loginid':
                send_msg = send_msg + f'[by {user}]'
        
        if config_translator.language:
            send_msg = send_msg + f'({lang_src} → {lang_tgt})'
        
        return send_msg, translated, gas_used
    
    async def gas_trans(self, text, lang_tgt, lang_src):
        translated_text = ''
        gas_used = False
        params = {
            'text' : text,
            'target' : lang_tgt,
            'source'  : lang_src
        }

        try:
            async with self.session.get(config_translator.gas_url, params=params, timeout=3) as res:
                if res.status == 200:
                    json = await res.json()
                    if json['code'] == 200:
                        translated_text = json['text']
                        gas_used = True
                        return translated_text, gas_used
        except:
            return translated_text, gas_used
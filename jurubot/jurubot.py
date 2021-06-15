import asyncio
import msg_formatter

from pyfiglet import Figlet
from twitchio.ext import commands

import config_bot, config_translator, oauth_key
import bouyomi, translator, user_info
import check_token


version = '1.0.0'


class Bot(commands.Bot):
    def __init__(self, token, bot_nick):
        self.ch = []
        self.ch.append(config_bot.channel)
        super().__init__(irc_token=token,
                         nick=bot_nick,
                         prefix='!',
                         initial_channels=self.ch)

        # ボットのディスプレイネームを取得
        print('ボットのディスプレイネームを取得中....')
        get_user_info = user_info.GetUserInfo()
        self.bot_disp = get_user_info.get_display_name(bot_nick)
        if not self.bot_disp:
            self.bot_disp = bot_nick
            print('ボットのディスプレイネームの取得に失敗しました...(ログインできていれば翻訳には問題ありません)')
        
        self.ignore_user = [w.lower() for w in config_translator.ignore_user]
        msg_formatter.ignore_compile()
        self.bot_nick = bot_nick
        self.translator = translator.Translate()
        self.bouyomi = bouyomi.Bouyomi()
    

    async def event_ready(self):
        channel = bot.get_channel(config_bot.channel)
        print(f'\r\n{self.bot_disp}で{config_bot.channel}に接続しました！')
        
        # 色の設定
        color_list = ['Red','Blue','Green','Firebrick','Coral','YellowGreen','OrengeRed','SeaGreen','GoldenRod','Chocolate','CadetBlue','DodgerBlue','HotPink','BlueViolet','SpringGreen']
        if config_bot.bot_color in color_list:
            color = config_bot.bot_color
        else:
            color = 'HotPink'
        await channel.colour(color)
        print(f'Botのカラーを{color}に設定しました！\r\n')
        
        if config_bot.send_me:
            await channel.send_me(f'{config_bot.send_message_prefix}Jurubot_Translator接続しました！')
        else:
            await channel.send(f'{config_bot.send_message_prefix}Jurubot_Translator接続しました！')
        
        # タイマースタート
        try:
            interval = int(config_bot.timer_interval)
            if interval != 0:
                if config_bot.timer_message:
                    while config_bot.timer:
                        if config_bot.send_me:
                            await channel.send_me(f'{config_bot.send_message_prefix}{config_bot.timer_message}')
                        else:
                            await channel.send(f'{config_bot.send_message_prefix}{config_bot.timer_message}')
                        print(f'[{channel}]({self.bot_disp}){config_bot.send_message_prefix}{config_bot.timer_message}')
                        await asyncio.sleep(interval*60)
        except:
            pass

    async def event_message(self, message):
        # Botのメッセージは無視
        if message.echo:
            # print(f'[{message.channel}]({self.bot_disp}){message.content}')
            return
        
        # コマンド処理
        if message.content.startswith('!'):
            await self.handle_commands(message)
            return
        
        # 棒読みちゃん(受信したコメント用)
        if config_bot.bouyomi:
            if message.author.name.lower() not in self.ignore_user:
                await self.bouyomi.bouyomi(message)
        print(f'[{message.author.display_name}({message.author.name})]{message.content}')
        
        
        # 翻訳&棒読みちゃん(Bot用)
        if config_bot.translate:
            send_msg, translated, gas_use = await self.translator.translator(message)
            if send_msg:
                # 棒読みちゃんが有効な時翻訳しただけのメッセージを渡す
                if config_bot.bouyomi:
                    if config_bot.bouyomi_bot:
                        await self.bouyomi.bouyomi_bot(message, translated, self.bot_disp, self.bot_nick)
                
                if config_bot.send_me:
                    await message.channel.send_me(f'{config_bot.send_message_prefix}{send_msg}')
                else:
                    await message.channel.send(f'{config_bot.send_message_prefix}{send_msg}')
                
                # GASを使っているかどうが表示したいのでここで表示する
                if gas_use:
                    send_msg = send_msg + '(GAS)'
                print(f'[{self.bot_disp}({self.bot_nick})]{config_bot.send_message_prefix}{send_msg}')

    # !ver
    @commands.command(name='ver')
    async def ver(self, ctx):
        if config_bot.send_me:
            await ctx.send_me(f'{config_bot.send_message_prefix}このBotはJurubotTranslator ver{version}です！ http://neko2.net/jurubot ')
        else:
            await ctx.send(f'{config_bot.send_message_prefix}このBotはJurubotTranslator ver{version}です！ http://neko2.net/jurubot ')
    # !lang
    @commands.command(name='lang')
    async def lang(self, ctx):
        if config_bot.send_me:
            await ctx.send_me(f'{config_bot.send_message_prefix}言語コード一覧はこちらです！ https://cloud.google.com/translate/docs/languages ')
        else:
            await ctx.send(f'{config_bot.send_message_prefix}言語コード一覧はこちらです！ https://cloud.google.com/translate/docs/languages ')

if __name__ == '__main__':
    f = Figlet(font='speed')
    jurubot_f = f.renderText('Jurubot')
    translator_f = f.renderText('Translator')
    print(jurubot_f)
    print(translator_f)
    print(f'Jurubot_Translator ver{version}\r\n')
    
    print('トークンをチェック中...')
    token = oauth_key.token
    if not token:
        print('トークンを取得してください')
        input('Enterを押すと終了します...')
        quit()
    else:
        validate, login_id = check_token.check_token(token)
        if not validate:
            input('Enterを押すと終了します....')
            quit()
    token = 'oauth:' + token
    
    bot = Bot(token, login_id)
    try:
        bot.run()
    except Exception as e:
        print(e)

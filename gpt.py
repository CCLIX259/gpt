import asyncio,time
from pyrogram import Client, filters, types,enums
from pyrogram.errors.exceptions.not_acceptable_406 import ChannelPrivate
from pyrogram.errors.exceptions.bad_request_400 import UserBannedInChannel
from pyrogram.errors.exceptions.forbidden_403 import Forbidden
from pyrogram.types import Chat
import emoji
import re


import random
api_id = 19309010
api_hash = "dfdf154157cca400bd53b00100468fa5"
app = Client("Traficmaker", api_id=api_id, api_hash=api_hash,parse_mode=enums.parse_mode.ParseMode.HTML)

bot_id = '@vitaliy_chatGPT_bot'

def contains_letter(text):
    for char in text:
        if char.isalpha() and (char.isascii() or char.isalpha()):
            return True
    return False


@app.on_message(filters.channel)
def getpost(client, message: types.Message):
    chat_id = message.chat.id
    message_id = message.id

    if message.text and len(message.text) <= 2800:
        if message.forward_from is None:
            if contains_letter(str(message.text)):
                try:
                    app.send_message(bot_id, f"""Пост из канала {chat_id} {message_id}|:
                    
{message.text.replace('"', '')}

Напиши комментарий от мужского пола на этот пост в 70 символов без хештегов на русском языке:""")
                except:
                    pass
            else:
                print('Получил текст из эмоджи - не комментирую')
        else:
            print('Получил пересланный пост - не комментирую')

    elif message.caption and len(message.caption) <= 2800:
        if contains_letter(str(message.caption)):
            if message.forward_from is None:
                try:
                    app.send_message(bot_id, f"""Пост из канала {chat_id} {message_id}|:
                    
{message.caption.replace('"', '')}

Напиши комментарий от мужского пола на этот пост в 70 символов без хештегов на русском языке:""")
                except:
                    pass
            else:
                print('Получил текст из эмоджи - не комментирую')
        else:
            print('Получил пересланный пост - не комментирую')



@app.on_message(filters.bot)
def handle_bot_message(client, message: types.Message):
    if str(message.from_user.username) in bot_id:
        comment_text = message.text.replace('"', '')
        if not message.reply_to_message:
            return

        try:
            replied_message_text = message.reply_to_message.text
        except:
            replied_message_text = message.reply_to_message.caption

        replied_message_text = replied_message_text.replace('"', '')

        msg_object = replied_message_text.replace("Напиши комментарий от мужского пола на этот пост в 70 символов без хештегов на русском языке: ","").split('|:\n', 2)[0].replace('Пост из канала ', '').replace('\n', '')
        print(msg_object)
        chat_id, message_id = msg_object.split(' ', 2)[0], int(msg_object.split(' ', 2)[1])
        print(chat_id, message_id)
        try:
            msg = app.get_discussion_message(chat_id, message_id)
            msg.reply(text=comment_text, quote=True)

        except ChannelPrivate:
            try:
                app.leave_chat(chat_id)
            except:
                pass
            app.send_message('@spambot', '/start')
            time.sleep(3)
            app.send_message('@spambot', 'OK')
            time.sleep(3)
            app.send_message('@spambot', '/start')

        except UserBannedInChannel:
            try:
                app.leave_chat(chat_id)
            except:
                pass

            app.send_message('@spambot', '/start')
            time.sleep(3)
            app.send_message('@spambot', 'OK')
            time.sleep(3)
            app.send_message('@spambot', '/start')

        except Forbidden:
            chat: Chat
            try:
                chat = app.get_chat(chat_id)
                chat.linked_chat.join()
            except Exception as e:
                print('Не удалось вступить в чат', e)
        except Exception as e:
            print('Ошибка', e)

        time.sleep(60)


app.run()

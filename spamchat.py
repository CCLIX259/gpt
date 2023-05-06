import asyncio
import os
import pyrogram
from pyrogram import Client, filters
from pyrogram.errors import RPCError

API_ID = 19309010
API_HASH = 'dfdf154157cca400bd53b00100468fa5'
BOT_TOKEN = ""
session_name = "my_account"
app = Client(session_name, API_ID, API_HASH)


# отвечаем на любое сообщение в личку
#@app.on_message(filters.private)
#async def hello(client, message):
#    await message.reply(f"")


async def spamer():
    count = 0
    error = 0
    nice = 0
    async with app:
        while True:
            # получаем последнее сообщение из своих сохраненок
            cnt = 0
            async for message in app.get_chat_history('me'):
                save_mess_text = str(message.text)
                cnt += 1
                if cnt == 1:
                    break
            # print(save_mess_text)

            async for dialog in app.get_dialogs():
                if str(dialog.chat.type) == "ChatType.SUPERGROUP" or str(dialog.chat.type) == "ChatType.GROUP":
                    # если не прочитанных сообщений == n отправляем message
                    # print(dialog.unread_messages_count)
                    if int(dialog.unread_messages_count) >= 5:
                        # print("nice")
                        try:
                            await app.send_message(dialog.chat.id, save_mess_text)
                            nice = nice + 1
                            print(f"\n\nОтправили сообщение в группу {dialog.chat.title}\nКоличество отправленных сообщений: {nice}")
                        except pyrogram.errors.exceptions.bad_request_400.BadRequest:
                            error = error + 1
                            print(f"\n\nНевозможно отправить сообщение в группу {dialog.chat.title}\nКоличество ошибок: {error}")
                            pass
                        except pyrogram.errors.exceptions.forbidden_403.ChatWriteForbidden:
                            error = error + 1
                            print(f"\n\nНевозможно отправить сообщение в группу {dialog.chat.title}\nКоличество ошибок: {error}")
                            pass
                        except pyrogram.errors.exceptions.flood_420.SlowmodeWait:
                            error = error + 1
                            print(f"\n\nНевозможно отправить сообщение в группу {dialog.chat.title}\nКоличество ошибок: {error}")
                            pass
                        except pyrogram.errors.exceptions.bad_request_400.MessageEmpty:
                            error = error + 1
                            print(f"\n\nНевозможно отправить пустое сообщение\nКоличество ошибок: {error}")
                        except pyrogram.errors.exceptions.flood_420.FloodWait as e:
                            error = error + 1
                            print(f"\n\nАккаунт поймал флуд на {e.value} секунд\nКоличество ошибок: {error}\nЗасыпаем на {e.value} секунд")
                            await asyncio.sleep(e.value)
                        except pyrogram.errors.exceptions.forbidden_403.Forbidden:
                            error = error + 1
                            print(f"\n\nНевозможно отправить сообщение в группу {dialog.chat.title}\nКоличество ошибок: {error}")
                            pass
                        except pyrogram.errors.exceptions.not_acceptable_406.NotAcceptable:
                            error = error + 1
                            print(f"\n\nНевозможно отправить сообщение в группу {dialog.chat.title}\nКоличество ошибок: {error}")
                            pass
                        await asyncio.sleep(1)
                    await asyncio.sleep(1)
            await asyncio.sleep(3600)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(spamer())

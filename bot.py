import time

from pyrogram import Client

api_id = 25205845
api_hash = "87d05772389e7fe982ef50738596b0c1"


def main():
    with Client("my_acc", api_id, api_hash) as app:
        with open('group.txt', 'r') as groupfile:
            for group in groupfile:
                try:
                    app.join_chat(group)
                    print(f"Вступил в группу {group}")
                    time.sleep(5)
                except Exception as e:
                    print(f"Ошибка: {e}")


if __name__ == '__main__':
    main()

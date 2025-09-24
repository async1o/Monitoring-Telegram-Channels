import asyncio
import json
import os
import random
from datetime import datetime, timedelta

from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

from dotenv import load_dotenv

from search import searching

load_dotenv()

with open('data.json', 'r') as file:
    data = json.load(file)

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')

client = TelegramClient(session='session.session', api_id=api_id, api_hash=api_hash, app_version='1.0', system_version='Ubuntu 22', device_model='PC')

choice_search = int(input('Желаете подобрать каналы по ключевому слову?\n1 - Да\n2- Нет\n> '))

if choice_search == 1:
    searching()

channels = data['channels']
comments = data['comments']


async def check_new_posts():
    last_processed_messages = {}
    while True:
        for channel in channels:
            try:
                posts = await client(GetHistoryRequest(
                    peer=channel,
                    limit=1,
                    offset_date=None,
                    offset_id=0,
                    max_id=0,
                    min_id=0,
                    add_offset=0,
                    hash=0
                ))

                for message in posts.messages:
                    if not message.message:
                        continue

                    if channel in last_processed_messages and message.id <= last_processed_messages[channel]:
                        continue

                    message_time = message.date
                    current_time = datetime.now(message_time.tzinfo)

                    if current_time - message_time < timedelta(minutes=5):
                        last_processed_messages[channel] = message.id

                        print(f"Найден новый пост в канале {channel}. Ожидание 1 минуты перед комментированием...")

                        await asyncio.sleep(60)

                        comment = random.choice(comments)
                        post = posts.messages[0]

                        await client.send_message(entity=channel, message=comment, comment_to=post)

                        print(f"Прокомментирован пост в канале {channel}: {comment}")

                        await asyncio.sleep(random.randint(5, 15))

            except Exception as e:
                print(f"Ошибка при обработке канала {channel}: {e}")

        await asyncio.sleep(60)

async def main():
    async with client:
        await check_new_posts()


if __name__ == '__main__':
    asyncio.run(main())

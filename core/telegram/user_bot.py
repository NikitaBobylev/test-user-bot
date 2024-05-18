import asyncio
import datetime
from dataclasses import dataclass, field
from pyrogram import Client, filters, handlers
from pyrogram.handlers import MessageHandler

from core.project.settings.main import api_hash, api_id

db = set()



@dataclass(eq=True)
class User:
    id: int
    next_message: datetime
    stage: int = field(default=1)
    status: str = field(default='alive')

    def __hash__(self):
        return self.id


async def message(client, message):
    if not any(message.from_user.id == user.id for user in db):
        user = User(
            id=message.from_user.id,
            next_message=datetime.datetime.now() + datetime.timedelta(minutes=5)
        )
        db.add(user)
    print(message.from_user.id)


async def main():

    async with Client("my_account", api_id, api_hash) as app:
        message_handler = MessageHandler(message)
        app.add_handler(message_handler)

        while True:

            now = datetime.datetime.now()
            for user in db:

                if user.status == 'alive' and \
                        (user.next_message.day, user.next_message.hour, user.next_message.minute) == (
                        now.day, now.hour, now.minute):
                    await app.send_message(user.id, 'hello world')
                    user.status = 'final'

            await asyncio.sleep(10)

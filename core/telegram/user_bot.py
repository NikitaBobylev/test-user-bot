import asyncio
import datetime

from pyrogram import Client, filters
from pyrogram.errors import BadRequest
from pyrogram.handlers import MessageHandler

from core.project.settings.main import api_hash, api_id, DALTA_SECOND_STAGE, DALTA_LAST_STAGE, TRIGGERS, \
    USER_CHECK_TICK_RATE, SKIP_TRIGGERS
from core.apps.users.services import UserOrmService
from core.apps.users.models import Stage, Status
from core.telegram.messages import msg_1, msg_2, msg_3

user_service = UserOrmService()


async def _send_message_to_user(app, telegram_id: str, message: str):
    try:
        await app.send_message(telegram_id, message)
    except BadRequest as ex:
        await user_service.change_user_status(
            telegram_id=telegram_id,
            new_user_status=Status.dead
        )


async def receive_message(client, message):
    print(f'message from {message.from_user.id}')

    await user_service.create_user(str(message.from_user.id))

    if any(trigger.lower() in message.text.lower() for trigger in TRIGGERS):
        print(f'trigger in message, finish user {message.from_user.id}')
        await user_service.change_user_status(
            telegram_id=str(message.from_user.id),
            new_user_status=Status.finished
        )

    if any(skip_trigger.lower() in message.text.lower() for skip_trigger in SKIP_TRIGGERS) \
            and await user_service.check_user_stage(
        telegram_id=str(message.from_user.id),
        stage=Stage.second
    ):
        await user_service.update_user_stage(
            telegram_id=str(message.from_user.id),
            stage=Stage.last,
            delta_stage=DALTA_LAST_STAGE
        )
        print(f'trigger in message, skip stage user {message.from_user.id}')


async def _change_user_stage(
        app,
        message: str,
        telegram_id: str,
        stage: str,
        delta_stage: datetime.timedelta
):
    await _send_message_to_user(
        app=app,
        telegram_id=telegram_id,
        message=message
    )
    await user_service.update_user_stage(
        telegram_id=telegram_id,
        stage=stage,
        delta_stage=delta_stage
    )


async def _change_user_to_finish(
        app,
        telegram_id: str,
        message: str,

):
    await _send_message_to_user(
        app=app,
        telegram_id=telegram_id,
        message=message
    )
    await user_service.change_user_status(
        telegram_id=telegram_id,
        new_user_status=Status.finished
    )


async def main():
    async with Client("my_account", api_id, api_hash) as app:
        message_handler = MessageHandler(receive_message, filters=filters.text & filters.private)
        app.add_handler(message_handler)

        while True:

            users = await user_service.get_users_to_send_message()
            print(users)
            for user in users:
                if user.stage is Stage.first:
                    await _change_user_stage(
                        app=app,
                        message=msg_1,
                        telegram_id=user.telegram_id,
                        stage=Stage.second,
                        delta_stage=DALTA_SECOND_STAGE
                    )
                    print(f'SEND message {msg_1} to {user.telegram_id}')

                elif user.stage is Stage.second:
                    await _change_user_stage(
                        app=app,
                        message=msg_2,
                        telegram_id=user.telegram_id,
                        stage=Stage.last,
                        delta_stage=DALTA_LAST_STAGE
                    )
                    print(f'SEND message {msg_2} to {user.telegram_id}')

                elif user.stage is Stage.last:
                    await _change_user_to_finish(
                        app=app,
                        telegram_id=user.telegram_id,
                        message=msg_3
                    )
                    
                    print(f'SEND message {msg_3} to {user.telegram_id} and finish user')

            await asyncio.sleep(USER_CHECK_TICK_RATE)

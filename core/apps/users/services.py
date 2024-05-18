import asyncio
import datetime

from sqlalchemy import select, update

from core.apps.users.entities import User as UserEntity
from core.project.settings.database import async_session
from core.project.settings.main import DALTA_SECOND_STAGE, DALTA_LAST_STAGE
from core.apps.users.models import UsersOrm, Stage, Status


class UserOrmService:
    def __init__(self):
        self.model = UsersOrm

    async def get_users_to_send_message(self) -> list[UserEntity]:
        async with async_session() as session:
            start, end = datetime.datetime.utcnow() - datetime.timedelta(
                minutes=1), datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
            stmt = (
                select(UsersOrm)
                .filter(UsersOrm.status == Status.alive)
                .filter(UsersOrm.to_send_message.between(start, end))
            )
            users = await session.execute(stmt, )
            users = users.scalars().all()
            return [user.to_entity() for user in users]

    async def change_user_status(self, telegram_id: str, new_user_status: str) -> None:
        async with async_session() as session:
            stmt = (
                update(UsersOrm)
                .values(
                    status=new_user_status,
                    status_updated_at=datetime.datetime.utcnow()
                )
                .filter_by(telegram_id=telegram_id)
            )
            await session.execute(stmt, )
            await session.commit()

    async def update_user_stage(
            self,
            telegram_id: str,
            stage: str,
            delta_stage: datetime.timedelta
    ) -> None:
        async with async_session() as session:
            stmt = (
                update(UsersOrm)
                .values(
                    stage=stage,
                    to_send_message=datetime.datetime.utcnow() + delta_stage
                )
                .filter_by(telegram_id=telegram_id)
            )
            await session.execute(stmt, )
            await session.commit()


service = UserOrmService()

import datetime

from sqlalchemy import select, update, or_

from core.apps.users.entities import User as UserEntity
from core.project.settings.database import async_session
from core.apps.users.models import UsersOrm, Stage, Status
from core.project.settings.main import DELTA_FIRST_STAGE


class UserOrmService:
    def __init__(self):
        self.model = UsersOrm

    async def create_user(
            self,
            telegram_id: str,
    ) -> None:
        async with async_session() as session:
            stmt = (
                select(UsersOrm)
                .filter_by(
                    telegram_id=telegram_id
                )
            )
            res = await session.execute(stmt)
            user = res.scalars().first()

            if user:
                return

            new_user = UsersOrm(
                telegram_id=telegram_id,
                to_send_message=datetime.datetime.utcnow() + DELTA_FIRST_STAGE,
            )
            session.add_all([new_user])
            await session.commit()

    async def get_users_to_send_message(self) -> list[UserEntity]:
        async with async_session() as session:
            start, end = datetime.datetime.utcnow() - datetime.timedelta(
                seconds=7), datetime.datetime.utcnow() + datetime.timedelta(seconds=7)
            stmt = (
                select(UsersOrm)
                .filter(UsersOrm.status == Status.alive)
                .filter(or_(UsersOrm.to_send_message.between(start, end),
                            UsersOrm.to_send_message < start))
            )
            users = await session.execute(stmt, )
            users = users.scalars().all()
            return [user.to_entity() for user in users]

    async def check_user_stage(self, telegram_id: str, stage: str) -> bool:
        async with async_session() as session:
            stmt = (
                select(UsersOrm)
                .filter_by(telegram_id=telegram_id)
            )
            res = await session.execute(stmt, )
            user = res.first()
            if not user:
                return False
            user = user[0]
            return bool(user and user.status is Status.alive and user.stage is stage)

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
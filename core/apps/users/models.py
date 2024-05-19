import datetime
from enum import Enum

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.project.settings.database import Base
from core.apps.users.entities import User as UserEntity


class Status(Enum):
    alive: str = 'alive'
    dead: str = 'dead'
    finished: str = 'finished'


class Stage(Enum):
    first: str = 'first'
    second: str = 'second'
    last: str = 'last'


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[str] = mapped_column(unique=True)
    status: Mapped[Status] = mapped_column(default=Status.alive)
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
    )
    status_updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    to_send_message: Mapped[datetime.datetime]
    stage: Mapped[Stage] = mapped_column(
        default=Stage.first
    )

    def __str__(self):
        return f'UsersOrm telegram_id-{self.id} status-{self.status} stage-{self.stage}'

    def to_entity(self) -> UserEntity:
        return UserEntity(
            telegram_id=self.telegram_id,
            stage=self.stage
        )



from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from core.project.settings.main import db_host, db_name, db_password, db_username, db_port

database_url = f'postgresql+asyncpg://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'

async_engine = create_async_engine(
    database_url,
    echo=True,
    future=True,
)

async_session = async_sessionmaker(async_engine)


class Base(DeclarativeBase):
    ...

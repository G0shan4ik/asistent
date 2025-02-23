from sqlalchemy.orm import DeclarativeBase, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from loguru import logger

from os import getenv
from dotenv import load_dotenv

load_dotenv()


USER = getenv("POSTGRES_USER") or None
PASSWORD = getenv("POSTGRES_PASSWORD") or None
HOST = getenv("POSTGRES_HOST")
PORT = getenv("POSTGRES_PORT")
DB = getenv("POSTGRES_DB")

uri = f"{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"

if bool(getenv("DEBUG", False)):
    logger.info(f'DB URI postgresql+psycopg_async://{uri}')

engine = create_async_engine(
    url=f"postgresql+psycopg_async://{uri}",
    echo=bool(getenv("DEBUG", False))
)

Base: DeclarativeBase = declarative_base()
session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=engine)


async def init_database():
    async with engine.connect() as connection:

        # await connection.run_sync(Base.metadata.drop_all)

        await connection.run_sync(Base.metadata.create_all)
        if bool(getenv("DEBUG", False)):
            logger.debug(
                "Created tables: " + (", ".join(i for i in Base.metadata.tables))
            )
        await connection.commit()


async def init():
    await init_database()

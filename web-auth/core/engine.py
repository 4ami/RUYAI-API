from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine,create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from dotenv import load_dotenv
import os
load_dotenv()

url:str=os.getenv('DB_ENGINE').format(
    DB_USER = os.getenv('DB_USER'),
    DB_PASSWORD = os.getenv('DB_PASS'),
    DB_HOST = os.getenv('DB_HOST'),
    DB_NAME = os.getenv('DB_NAME')
)

_engine:AsyncEngine=create_async_engine(
    url=url,
    pool_size=10,
    max_overflow=5,
    pool_timeout=30,
    pool_recycle=1800,
    echo=True        # Logging excuted queries // Disable in production
)

_AsyncSession=sessionmaker(
    bind=_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def GET_ENGINE()->AsyncGenerator[AsyncSession, None]:
    async with _AsyncSession() as session:
        yield session

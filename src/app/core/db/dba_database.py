from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.app.core.config import settings

DBA_URI = settings.DBAPOSTGRES_URI
DBA_PREFIX = settings.DBAPOSTGRES_ASYNC_PREFIX
DBA_URL = f"{DBA_PREFIX}{DBA_URI}"



async_dba_engine = create_async_engine(DBA_URL, echo=False, future=True)

local_session_dba = async_sessionmaker(bind=async_dba_engine, class_=AsyncSession, expire_on_commit=False)

async def async_get_dba() -> AsyncGenerator[AsyncSession, None]:
    async with local_session_dba() as db:
        yield db

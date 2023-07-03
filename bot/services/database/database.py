from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import registry, sessionmaker, Session
from sqlalchemy.engine import make_url

from sqlalchemy.ext.declarative import declarative_base




mapper_registry = registry()
Base = declarative_base()


async def create_engine(db_url, echo=True):
    engine = create_async_engine(make_url(db_url), echo=echo, pool_recycle=60 * 5, pool_pre_ping=True)
    return engine


async def create_pool(engine):

    _sessionmaker = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=True)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    return _sessionmaker
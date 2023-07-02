from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import registry, sessionmaker, Session
from sqlalchemy.engine import make_url



mapper_registry = registry()
Base = mapper_registry.generate_base()


async def create_pool(db_url, echo=True):
    engine = create_async_engine(make_url(db_url), echo=echo, future=True)

    _sessionmaker = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=True)
    
    async with engine.begin() as conn:
        print("Creating tables")
        await conn.run_sync(Base.metadata.create_all)

    return _sessionmaker

class Database:
    def __init__(self, db_url, echo=True):
        _sessionmaker = Database._configure_sqla(db_url, echo=echo)
        self._sessionmaker = _sessionmaker

    def new_session(self) -> Session:
        return self._sessionmaker()

    @staticmethod
    async def _configure_sqla(db_url, echo) -> sessionmaker:
        engine = create_async_engine(make_url(db_url), echo=echo, future=True)

        _sessionmaker = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=True)
        
        async with engine.begin() as conn:
            print("Creating tables")
            await conn.run_sync(Base.metadata.create_all)

        return _sessionmaker

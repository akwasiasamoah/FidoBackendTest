from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./fidobackendtest.db"


async_engine = create_async_engine(DATABASE_URL, echo=True)


AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession
)


Base = declarative_base()

sync_engine = create_engine(DATABASE_URL.replace("aiosqlite", "pysqlite"))


def create_tables():
    Base.metadata.create_all(bind=sync_engine)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

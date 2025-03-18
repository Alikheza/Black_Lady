from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from .models import Base

# will be removed from here and added to the config file
DATABASE_URL = "sqlite+aiosqlite:///BLACKLADY.db"

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = async_sessionmaker(bind=engine)

async def create_all_table():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
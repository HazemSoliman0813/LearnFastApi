from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine

from app.config import Config
from app.books.models import Book

engine = AsyncEngine(
    create_engine(
        url=Config.DATABASE_URL,
        echo=True
    )
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

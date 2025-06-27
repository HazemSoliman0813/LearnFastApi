from sqlmodel import create_engine, text
from sqlalchemy.ext.asyncio import AsyncEngine

from app.config import Config

engine = AsyncEngine(
    create_engine(
        url=Config.DATABASE_URL,
        echo=True
    )
)


async def init_db():
    async with engine.begin() as conn:
        statement = text("SELECT 'Hello'")

        result = await conn.execute(statement)
        print(result.all())

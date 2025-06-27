from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.books.routes import book_router
from app.db.main import init_db


@asynccontextmanager
async def life_span(app: FastAPI):
    print('server is started')
    await init_db()
    yield
    print('server stopped')


version = 'V1'

app = FastAPI(
    title='Bookly api',
    description='A rest api for book service',
    version=version,
    lifespan=life_span)

app.include_router(book_router, prefix=f'/api/{version}/books', tags=['Books'])

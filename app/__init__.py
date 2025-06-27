from fastapi import FastAPI

from app.books.routes import book_router


version = 'V1'

app = FastAPI(
    title='Bookly api',
    description='A rest api for book service',
    version=version)

app.include_router(book_router, prefix=f'/api/{version}/books', tags=['Books'])

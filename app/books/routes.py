from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from typing import List

from app.books.schemas import Book, BookUpdate
from app.books.book_data import books

book_router = APIRouter()


@book_router.get('/', response_model=List[Book])
async def get_all_books():
    return books


@book_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_a_book(book_date: Book) -> dict:
    new_book = book_date.model_dump()
    books.append(new_book)
    return new_book


@book_router.get('/{id}')
async def get_book(id: int) -> dict:
    for book in books:
        if book['id'] == id:
            return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Book not found')


@book_router.patch('/{id}')
async def update_book(id: int, book_update: BookUpdate) -> dict:
    for book in books:
        if book['id'] == id:
            book['title'] = book_update.title
            book['author'] = book_update.author
            book['publisher'] = book_update.publisher
            book['page_count'] = book_update.page_count
            book['language'] = book_update.language

            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Book not found')


@book_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(id: int):
    for book in books:
        if book['id'] == id:
            books.remove(book)

            return {}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Book not found')

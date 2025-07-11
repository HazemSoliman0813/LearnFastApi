from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from datetime import datetime

from .schemas import BookCreate, BookUpdate
from .models import Book


class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_book_byId(self, book_uid: str, session: AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.exec(statement)
        book = result.first()

        return book if book is not None else None

    async def create_book(self, book_data: BookCreate, session: AsyncSession):
        async with session.begin():
            try:
                book_data_dict = book_data.model_dump()
                new_book = Book(**book_data_dict)
                new_book.published_date = datetime.strptime(
                    book_data_dict['published_date'], '%Y-%m-%d')
                session.add(new_book)
                await session.commit()

                return new_book
            except Exception as e:
                await session.rollback()
                raise Exception(f'failed to create book: {str(e)}')

    async def update_book(self, book_uid: str, update_data: BookUpdate, session: AsyncSession):
        async with session.begin():
            book_to_update = await self.get_book_byId(book_uid, session)

            if book_to_update is not None:
                update_data_dict = update_data.model_dump()

                for k, v in update_data_dict.items():
                    setattr(book_to_update, k, v)

                await session.commit()
                return book_to_update
            else:
                return None

    async def delete_book_byId(self, book_uid: str, session: AsyncSession):
        async with session.begin():
            book_to_delete = await self.get_book_byId(book_uid, session)

            if book_to_delete is not None:
                await session.delete(book_to_delete)
                await session.commit()
                return {}
            else:
                return None

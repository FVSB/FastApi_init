from datetime import datetime
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Sequence
from src.db.models import Book
from src.books.schemas import BookModel, BookCreateModel, BookUpdateModel
import uuid

class BookService:
    async def get_all_books(self, session: AsyncSession) -> Sequence[Book]:
        statement = select(Book).order_by(desc(Book.created_at))

        result = await session.exec(statement)
        
        return result.all()

    async def get_book(self, book_uid: uuid.UUID , session: AsyncSession) -> Book | None:
        statement = select(Book).where(Book.uid == book_uid)

        result = await session.exec(statement)

        book = result.first()
        
        
        return book
        
    
    async def create_book(
        self, book_data: BookCreateModel, session: AsyncSession
    ):
        book_data_dict = book_data.model_dump()

        new_book = Book(**book_data_dict)
        
        new_book.published_date = datetime.strptime(
            book_data_dict["published_date"], "%Y-%m-%d")

        session.add(new_book)

        await session.commit()

        return new_book

    async def update_book(
        self, book_uid: uuid.UUID, update_data: BookUpdateModel, session: AsyncSession
    ):
        book_to_update = await self.get_book(book_uid, session)

        if book_to_update is None:
            return None
        
        update_data_dict = update_data.model_dump()

        for k, v in update_data_dict.items():
            print(f"3355 {k}")
            setattr(book_to_update, k, v)
            
        await session.commit()
        
        await session.refresh(book_to_update)
        
      
        
        return book_to_update
    
    
    async def delete_book(self, book_uid: uuid.UUID, session: AsyncSession):
        book_to_delete = await self.get_book(book_uid, session)

        if book_to_delete is None:
            return None
        
        
        await session.delete(book_to_delete)

        await session.commit()

        return {}

        

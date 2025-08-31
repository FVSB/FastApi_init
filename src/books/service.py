from datetime import datetime
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
from typing import Sequence
from src.db.models import Book
from src.books.schemas import BookModel, BookCreateModel, BookUpdateModel, BookTagModel
from src.utils.errors import BookNotFound
import uuid

class BookService:
    async def get_all_books(self, session: AsyncSession, with_tags:bool=True) -> Sequence[Book]:
        statement = select(Book).order_by(desc(Book.created_at)) if not with_tags else select(Book).options(selectinload(Book.tags)).order_by(desc(Book.created_at))

        result = await session.exec(statement)
        
        return result.all()

    async def get_book_or_404(self, book_uid: uuid.UUID , session: AsyncSession, with_tags:bool=True) -> Book | None:
        statement = select(Book).where(Book.uid == book_uid) if not with_tags else select(Book).options(selectinload(Book.tags)).where(Book.uid == book_uid)
       
        result = await session.exec(statement)
        
        book = result.first()
        if  book is None:
            raise BookNotFound()
        
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
        book_to_update = await self.get_book_or_404(book_uid=book_uid,with_tags=False,session= session)

        if book_to_update is None:
            return None
        
        update_data_dict = update_data.model_dump()

        for k, v in update_data_dict.items():

            setattr(book_to_update, k, v)
            
        await session.commit()
        
        await session.refresh(book_to_update)
        
      
        
        return book_to_update
    
    
    async def delete_book(self, book_uid: uuid.UUID, session: AsyncSession):
        book_to_delete = await self.get_book_or_404(book_uid=book_uid,with_tags=True, session=session)

        if book_to_delete is None:
            return None
        
        
        await session.delete(book_to_delete)

        await session.commit()

        return {}

        

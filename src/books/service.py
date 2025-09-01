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
        """
        Retrieve a specific book by ID or raise 404 if not found.

        Args:
            book_id (int): The unique identifier of the book.
            session (AsyncSession): Database session for executing queries.
            with_tags (bool): Whether to include associated tags. Defaults to True.

        Returns:
            Book: The requested book with or without tags.

        Raises:
            BookNotFound: If no book exists with the given ID.

        Note:
            Uses selectinload for efficient tag loading when with_tags=True.
        """
        
        statement = select(Book).order_by(desc(Book.created_at)) if not with_tags else select(Book).options(selectinload(Book.tags)).order_by(desc(Book.created_at))

        result = await session.exec(statement)
        
        return result.all()

    async def get_book_or_404(self, book_id: int, session: AsyncSession, with_tags:bool=True) -> Book | None:
        
        """
        Retrieve a specific book by ID or raise 404 if not found.

        Args:
            book_id (int): The unique identifier of the book.
            session (AsyncSession): Database session for executing queries.
            with_tags (bool): Whether to include associated tags. Defaults to True.
            session (AsyncSession): Database session for executing the transaction.
        
        Note:
            Uses selectinload for efficient tag loading when with_tags=True.

        """


        statement = select(Book).where(Book.id == book_id) if not with_tags else select(Book).options(selectinload(Book.tags)).where(Book.id == book_id)
       
        result = await session.exec(statement)
        
        book = result.first()
        if  book is None:
            raise BookNotFound()
        
        return book
        
    
    async def create_book(
        self, book_data: BookCreateModel, session: AsyncSession
    ):
        """
        Create a new book in the database.

        Args:
            book_data (BookCreateModel): Book information with title, author, 
                                       publisher, published_date (as string), 
                                       language_code, and page_count.
            session (AsyncSession): Database session for executing the transaction.

        """
        book_data_dict = book_data.model_dump()

        new_book = Book(**book_data_dict)
        

        session.add(new_book)

        await session.commit()

        return new_book

    async def update_book(
        self, book_id:int , update_data: BookUpdateModel, session: AsyncSession
    ):
        """
        Update an existing book with new data.

        Args:
            book_id (int): The unique identifier of the book to update.
            update_data (BookUpdateModel): New book data to apply.
            session (AsyncSession): Database session for executing the transaction.

        Returns:
            Book | None: The updated book instance, or None if book not found.

        Raises:
            BookNotFound: If no book exists with the given ID.

        Note:
            Updates all provided fields dynamically using setattr.
            Refreshes the instance after commit to get updated values.
        """
        book_to_update = await self.get_book_or_404(book_id=book_id, with_tags=False, session= session)

        if book_to_update is None:
            return None
        
        update_data_dict = update_data.model_dump()

        for k, v in update_data_dict.items():

            setattr(book_to_update, k, v)
            
        await session.commit()
        
        await session.refresh(book_to_update)
        
      
        
        return book_to_update
    
    
    async def delete_book(self, book_id:int , session: AsyncSession):
        """
        Delete a book from the database by its ID.

        Args:
            book_id (int): The unique identifier of the book to delete.
            session (AsyncSession): Database session for executing the transaction.

        Returns:
            dict | None: Empty dict if deletion successful, None if book not found.

        Raises:
            BookNotFound: If no book exists with the given ID.

        Note:
            Loads the book with tags before deletion to handle any cascade operations.
            Returns empty dict to indicate successful deletion.
        """

        
        book_to_delete = await self.get_book_or_404(book_id=book_id, with_tags=True, session=session)

        if book_to_delete is None:
            return None
        
        
        await session.delete(book_to_delete)

        await session.commit()

        return {}

        

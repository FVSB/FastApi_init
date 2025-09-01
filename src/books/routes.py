from fastapi import APIRouter, HTTPException, status, Depends
from src.db.main import get_session
from typing import List
from datetime import datetime, date
from pydantic import BaseModel
from src.books.schemas import BookModel, BookCreateModel, BookUpdateModel, BookTagModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService
from src.utils.errors import BookDemoException, BookNotFound
import uuid

book_router = APIRouter()
book_service = BookService()


# Get all books
@book_router.get("/")
async def get_all_books(with_tags: bool = True, session: AsyncSession = Depends(get_session)):
    """
    Retrieve all books from the database.
    
    Args:
        with_tags (bool): Include associated tags in response. Defaults to True.
        session (AsyncSession): Database session dependency.
    
    Returns:
        List[BookTagModel] | List[BookModel]: List of books with or without tags.
    
    Example:
        GET /books?with_tags=true  -> Returns books with tags
        GET /books?with_tags=false -> Returns books without tags
    """
    
    books = await book_service.get_all_books(session, with_tags=with_tags)
    
    if with_tags:
        return [BookTagModel.model_validate(book) for book in books]
    else:
        return [BookModel.model_validate(book) for book in books]


# Get a book by id  
@book_router.get("/books/{book_id}")
async def get_book(book_id: int, with_tags: bool = True, session: AsyncSession = Depends(get_session)):
    """
    Retrieve a specific book by its ID.
    
    Args:
        book_id (int): The unique identifier of the book.
        with_tags (bool): Include associated tags in response. Defaults to True.
        session (AsyncSession): Database session dependency.
    
    Returns:
        BookTagModel | BookModel: Book data with or without tags.
    
    Raises:
        404: Book not found.
    
    Example:
        GET /books/1?with_tags=true  -> Returns book with tags
        GET /books/1?with_tags=false -> Returns book without tags
    """
    
    book = await book_service.get_book_or_404(book_id=book_id, with_tags=with_tags, session=session)
    

    if with_tags:
        return BookTagModel.model_validate(book,from_attributes=True)
    else:
        return BookModel.model_validate(book)


# Create a new book
@book_router.post(
    "/books", response_model=BookModel, status_code=status.HTTP_201_CREATED
)
async def create_book(
    book_data: BookCreateModel, session: AsyncSession = Depends(get_session)
):
    """
    Create a new book in the database.
    
    Args:
        book_data (BookCreateModel): Book information including title, author, 
                                   publisher, published_date, language_code, and page_count.
        session (AsyncSession): Database session dependency.
    
    Returns:
        BookModel: The newly created book data.
    
    Raises:
        422: Validation error for invalid input data.
        500: Internal server error if creation fails.
    
    Example:
        POST /books
        {
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "publisher": "Scribner",
            "published_date": "1925-04-10",
            "language_code": "En",
            "page_count": 180
        }
    """
    
    new_book = await book_service.create_book(book_data, session)
    return new_book


# Update a book
@book_router.put("/books/{book_id}", response_model=BookModel)
async def update_book(
    book_id: int,
    updated_book_data: BookUpdateModel,
    session: AsyncSession = Depends(get_session),
):
    """
    Update an existing book by its ID.
    
    Args:
        book_id (int): The unique identifier of the book to update.
        updated_book_data (BookUpdateModel): Updated book information.
        session (AsyncSession): Database session dependency.
    
    Returns:
        BookModel: The updated book data.
    
    Raises:
        404: Book not found.
        422: Validation error for invalid input data.
    
    Example:
        PUT /books/1
        {
            "title": "Updated Title",
            "author": "Updated Author",
            "publisher": "Updated Publisher",
            "published_date": "2024-01-15",
            "language_code": "Es",
            "page_count": 250
        }
    """
    
    
    updated_book = await book_service.update_book(book_id, updated_book_data, session)
    if updated_book is None:
        raise BookNotFound()

    return updated_book


# Delete a book
@book_router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id:int, session: AsyncSession = Depends(get_session)
):
    """
    Delete a book by its ID.
    
    Args:
        book_id (int): The unique identifier of the book to delete.
        session (AsyncSession): Database session dependency.
    
    Returns:
        dict: Empty response body (204 No Content).
    
    Raises:
        404: Book not found.
    
    Example:
        DELETE /books/1
        Response: 204 No Content (empty body)
    """

    book_to_delete = await book_service.delete_book(book_id, session)
    if book_to_delete is None:
        raise BookNotFound()
    return {}

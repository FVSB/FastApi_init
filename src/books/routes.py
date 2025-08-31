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
    books = await book_service.get_all_books(session, with_tags=with_tags)
    
    if with_tags:
        return [BookTagModel.model_validate(book) for book in books]
    else:
        return [BookModel.model_validate(book) for book in books]


# Get book by id  
@book_router.get("/books/{book_uid}")
async def get_book(book_uid: uuid.UUID, with_tags: bool = True, session: AsyncSession = Depends(get_session)):
    book = await book_service.get_book_or_404(book_uid=book_uid, with_tags=with_tags, session=session)
    
    # Convertir SQLModel a diccionario y luego a schema Pydantic
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
    new_book = await book_service.create_book(book_data, session)
    return new_book


# Update a book
@book_router.put("/books/{book_uid}", response_model=BookModel)
async def update_book(
    book_uid: uuid.UUID,
    updated_book_data: BookUpdateModel,
    session: AsyncSession = Depends(get_session),
):
    updated_book = await book_service.update_book(book_uid, updated_book_data, session)
    if updated_book is None:
        raise BookNotFound()

    return updated_book


# Delete a book
@book_router.delete("/books/{book_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_uid: uuid.UUID, session: AsyncSession = Depends(get_session)
):
    book_to_delete = await book_service.delete_book(book_uid, session)
    if book_to_delete is None:
        raise BookNotFound()
    return {}

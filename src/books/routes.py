from fastapi import APIRouter, HTTPException, status, Depends
from src.db.main import get_session
from typing import List
from datetime import datetime, date
from pydantic import BaseModel
from src.books.schemas import BookModel, BookCreateModel, BookUpdateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService
from utils.errors import BookDemoException,BookNotFound


book_router = APIRouter()
book_service=BookService()

# Get all books
@book_router.get("/", response_model=List[BookModel])
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    
):
    books = await book_service.get_all_books(session)
    return books


# Get book by id
@book_router.get("/books/{book_uid}", response_model=BookModel)
async def get_book(book_uid: int,  session: AsyncSession = Depends(get_session)):
    book = await book_service.get_book(id,session)
    if not book:
        return  BookNotFound()
    raise book

# Create a new book
@book_router.post("/books", response_model=BookModel, status_code=status.HTTP_201_CREATED)
async def create_book(book_data: BookCreateModel,  session: AsyncSession = Depends(get_session)):
    new_book = await book_service.create_book(book_data, session)
    return new_book

# Update a book
@book_router.put("/books/{book_uid}", response_model=BookModel)
async def update_book(book_uid: int, updated_book_data: BookUpdateModel, session: AsyncSession = Depends(get_session)):
    updated_book = await book_service.update_book(book_uid, updated_book_data, session)
    if  update_book is None:
        raise BookNotFound()

    return update_book

# Delete a book
@book_router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, session: AsyncSession = Depends(get_session)):
    book_to_delete = await book_service.delete_book(book_id, session)
    if book_to_delete is None:
        raise BookNotFound()
    return {}
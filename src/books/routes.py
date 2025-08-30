from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime, date
from pydantic import BaseModel


class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime
    update_at: datetime


router = APIRouter()


# Simulated list with one initial book
books_db: List[Book] = [
    Book(
        id=1,
        title="Cien años de soledad",
        author="Gabriel García Márquez",
        publisher="Editorial Sudamericana",
        published_date=date(1967, 5, 30),
        page_count=417,
        language="español",
        created_at=datetime.now(),
        update_at=datetime.now()
    )
]


# Create a new book
@router.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(book: Book):
    books_db.append(book)
    return book


# Get all books
@router.get("/books", response_model=List[Book])
def get_books():
    return books_db


# Get book by id
@router.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    for book in books_db:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


# Update a book
@router.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, updated_book: Book):
    for index, book in enumerate(books_db):
        if book.id == book_id:
            books_db[index] = updated_book
            return updated_book
    raise HTTPException(status_code=404, detail="Book not found")


# Delete a book
@router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int):
    for index, book in enumerate(books_db):
        if book.id == book_id:
            books_db.pop(index)
            return
    raise HTTPException(status_code=404, detail="Book not found")

from datetime import date, datetime, timezone
from typing import List, Optional
from sqlmodel import SQLModel,Column,Field,Integer
import sqlalchemy.dialects.postgresql as pg

class Book(SQLModel, table=True):
    __tablename__ = "books"
    uid: int = Field(
        sa_column=Column(Integer, autoincrement=True, primary_key=True)
    )
    title: str
    author: str
    publisher: str 
    published_date: date
    page_count: int
    language_code: str= Field(max_length=5)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP,  default=lambda: datetime.now(timezone.utc)))
    update_at: datetime = Field(sa_column=Column(pg.TIMESTAMP,  default=lambda: datetime.now(timezone.utc)))

    def __repr__(self):
        return f"__Book {self.title}__"
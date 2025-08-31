from datetime import date, datetime, timezone
from typing import List, Optional
from sqlmodel import SQLModel,Column,Field,Integer
from sqlalchemy  import func
import sqlalchemy.dialects.postgresql as pg
import uuid

class Book(SQLModel, table=True):
    __tablename__ = "books"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    title: str
    author: str
    publisher: str 
    published_date: date
    page_count: int
    language_code: str= Field(max_length=5)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True), default=func.now() ))
    update_at: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True),  default= func.now() ))

    def __repr__(self):
        return f"__Book {self.title}__"
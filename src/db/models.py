from datetime import date, datetime, timezone
from typing import List, Optional
from sqlmodel import SQLModel,Column,Field,Integer, Relationship
from sqlalchemy  import func
import sqlalchemy.dialects.postgresql as pg
import uuid

    
class BookTag(SQLModel, table=True):
    book_id: uuid.UUID = Field(default=None, foreign_key="books.uid", primary_key=True)
    tag_id: uuid.UUID = Field(default=None, foreign_key="tags.uid", primary_key=True)

class Tag(SQLModel, table=True):
    __tablename__ = "tags"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    name: str = Field(sa_column=Column(pg.VARCHAR(length=100), nullable=False, unique=True))
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    books: List["Book"] = Relationship(
        link_model=BookTag,
        back_populates="tags",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    def __repr__(self) -> str:
        return f"__Tag_{self.name}__"
    


class Book(SQLModel, table=True):
    __tablename__ = "books"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    title: str = Field(sa_column=Column(pg.VARCHAR(100), nullable=False,  unique=True))
    author: str =  Field(sa_column=Column(pg.VARCHAR(100), nullable=True))
    publisher: str 
    published_date: date
    page_count: int
    language_code: str= Field(max_length=5, sa_column=Column(pg.VARCHAR, nullable=False))
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True), default=func.now() ))
    update_at: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True),  default= func.now() ))
    tags: List[Tag] = Relationship(
        link_model=BookTag,
        back_populates="books",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    def __repr__(self):
        return f"__Book {self.title}__"
    


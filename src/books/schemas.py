from pydantic import BaseModel, Field
from datetime import date,datetime
import uuid
class BookModel(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language_code: str =Field(max_length=5)
    created_at: datetime
    update_at: datetime
    
    def __repr__(self):
        return f"__Book {self.title}__"

class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language_code: str
    
    
class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language_code: str

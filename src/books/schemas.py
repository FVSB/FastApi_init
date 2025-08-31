from pydantic import BaseModel, Field,ConfigDict
from datetime import date,datetime
from src.tags.schemas import TagModel
from typing import List, Union
import uuid

from abc import ABC

class BookAbstract(ABC,BaseModel):
    title: str =Field(max_length=100)
    author: str =Field(max_length=100)
    publisher: str
    page_count: int
    language_code: str = Field(max_length=5)
    def __repr__(self):
        return f"__Book_{self.title}__"
    
class BookCreateModel(BookAbstract):
    published_date: str  # Se enviará como string y se convertirá en el servicio
    
class BookUpdateModel(BookAbstract):
    published_date: str
    
class BookModel(BookAbstract):
    uid: uuid.UUID
    published_date: date
    created_at: datetime
    update_at: datetime
    
class BookTagModel(BookModel):
    model_config = ConfigDict(from_attributes=True)
    tags: List[TagModel]
    
    
    


    
    

    

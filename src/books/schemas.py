from pydantic import BaseModel, Field
from datetime import date,datetime
from src.tags.schemas import TagModel
from typing import List
import uuid

from abc import ABC

class BookAbstract(ABC,BaseModel):
    title: str =Field(max_length=100)
    author: str =Field(max_length=100,unique=True)
    publisher: str
    page_count: int
    language_code: str = Field(max_length=5)
    def __repr__(self):
        return f"__Book_{self.title}__"
    
class BookCreateModel(BookAbstract):
    pass
    
class BookUpdateModel(BookAbstract):
    pass
class BookModel(BookAbstract):
    uid: uuid.UUID
    
    
class BookTagModel(BookModel):
    tags:List[TagModel]
    
    
    


    
    

    

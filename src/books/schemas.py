from pydantic import BaseModel, Field,ConfigDict
from datetime import date,datetime
from src.tags.schemas import TagModel
from typing import List, Union

from abc import ABC

class BookAbstract(ABC,BaseModel):
    title: str =Field(max_length=100)
    author: str =Field(max_length=100)
    publisher: str
    published_date: date 
    page_count: int
    language_code: str = Field(max_length=5)
    created_at: datetime
    update_at: datetime
    def __repr__(self):
        return f"__Book_{self.title}__"
    
class BookCreateModel(BookAbstract):
     pass
    
class BookUpdateModel(BookAbstract):
    pass
    
class BookModel(BookAbstract):
    id: int
    
    
class BookTagModel(BookModel):
    model_config = ConfigDict(from_attributes=True)
    tags: List[TagModel]
    
    
    


    
    

    

import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel,ConfigDict


class TagModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    uid: uuid.UUID
    name: str
    created_at: datetime


class TagCreateModel(BaseModel):
    name: str


class TagAddModel(BaseModel):
    tags: List[TagCreateModel]

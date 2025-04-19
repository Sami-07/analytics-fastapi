from pydantic import BaseModel, Field
from typing import List, Optional 
class EventSchema(BaseModel):
    id: int
    page: Optional[int] = Field(default=None)

class EventCreateSchema(BaseModel):
    id: int
    page: Optional[int] = Field(default=None)

class EventListSchema(BaseModel):
    results: List[EventSchema]


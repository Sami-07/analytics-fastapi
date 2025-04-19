from sqlmodel import SQLModel, Field, DateTime
from datetime import datetime, timezone
from typing import List, Optional

def get_utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=timezone.utc)

class EventModel(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    description: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=get_utc_now, nullable=False)
    updated_at: datetime = Field(default_factory=get_utc_now, nullable=False)

class EventCreateSchema(SQLModel):
    description: Optional[str] = Field(default=None)

class EventUpdateSchema(SQLModel):
    description: Optional[str] = Field(default=None)

class EventListSchema(SQLModel):
    results: List[EventModel]

from sqlmodel import SQLModel, Field, DateTime
from datetime import datetime, timezone
from typing import List, Optional
from timescaledb import TimescaleModel

def get_utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=timezone.utc)

class EventModel(TimescaleModel, table=True):
    page: str = Field(index=True) # /about, /contact, /pricing
    user_agent: Optional[str] = Field(default="", index=True) # browser
    ip_address: Optional[str] = Field(default="", index=True)
    referrer: Optional[str] = Field(default="", index=True) 
    session_id: Optional[str] = Field(index=True)
    duration: Optional[int] = Field(default=0) 

    __chunk_time_interval__ = "INTERVAL 1 day"
    __drop_after__ = "INTERVAL 3 months"

class EventCreateSchema(SQLModel):
    page: str
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None
    referrer: Optional[str] = None
    session_id: Optional[str] = None
    duration: Optional[int] = None



class EventResponseSchema(SQLModel):
    bucket: datetime
    page: str
    count: int


class EventListSchema(SQLModel):
    results: List[EventResponseSchema]

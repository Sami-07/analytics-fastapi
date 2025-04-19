from fastapi import APIRouter
from .schema import EventSchema, EventListSchema, EventCreateSchema
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

DATABASE_URL = os.getenv("DATABASE_URL")

@router.get("/")
def read_events() -> EventListSchema:
    print("DATABASE_URL", DATABASE_URL)
    return EventListSchema(results=[EventSchema(id=1), EventSchema(id=2)])

@router.post("/")
def create_event(payload: EventCreateSchema) -> EventSchema:
    return EventSchema(id=payload.id)

@router.get("/{event_id}")
def read_event_by_id(event_id: int) -> EventSchema:
    return EventSchema(id=event_id)

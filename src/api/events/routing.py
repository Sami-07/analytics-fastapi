from fastapi import APIRouter
from .schema import EventSchema
router = APIRouter()

@router.get("/")
def read_events():
    return {"items": [1, 2, 3]}

@router.get("/{event_id}")
def read_event_by_id(event_id: int) -> EventSchema:
    return EventSchema(id=event_id)
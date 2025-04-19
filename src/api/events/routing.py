from fastapi import APIRouter, Depends, HTTPException
from .models import (EventModel, EventListSchema,
                     EventCreateSchema, EventUpdateSchema)
import os
from sqlmodel import Session, select
from dotenv import load_dotenv
from api.db.session import get_session
load_dotenv()

router = APIRouter()

DATABASE_URL = os.getenv("DATABASE_URL")


@router.get("/", response_model=EventListSchema)
def read_events(page: int, session: Session = Depends(get_session)):
    statement = select(EventModel).offset((page - 1) * 10).limit(10)
    results = session.exec(statement).all()
    return EventListSchema(results=list(results))


@router.post("/", response_model=EventModel)
def create_event(payload: EventCreateSchema,
                 session: Session = Depends(get_session)):
    data = payload.model_dump()
    obj = EventModel.model_validate(data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


@router.get("/{event_id}", response_model=EventModel)
def read_event_by_id(event_id: int, session: Session = Depends(get_session)):
    query = select(EventModel).where(EventModel.id == event_id)
    result = session.exec(query).first()
    if result is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return result


@router.put("/{event_id}", response_model=EventModel)
def update_event(event_id: int, payload: EventUpdateSchema, session: Session = Depends(get_session)):
    query = select(EventModel).where(EventModel.id == event_id)
    result = session.exec(query).first()
    if result is None:
        raise HTTPException(status_code=404, detail="Event not found")
    data = payload.model_dump()
    for key, value in data.items():
        setattr(result, key, value)
    session.add(result)
    session.commit()
    session.refresh(result)
    return result


@router.delete("/{event_id}", status_code=204)
def delete_event(event_id: int, session: Session = Depends(get_session)):
    query = select(EventModel).where(EventModel.id == event_id)
    result = session.exec(query).first()
    if result is None:
        raise HTTPException(status_code=404, detail="Event not found")
    session.delete(result)
    session.commit()
    return {"message": "Event deleted successfully"}


from fastapi import APIRouter, Depends, HTTPException, Query
from .models import (EventModel, EventListSchema,
                     EventCreateSchema, EventResponseSchema)
import os
from sqlmodel import Session, select, func
from dotenv import load_dotenv
from api.db.session import get_session
from timescaledb.hyperfunctions import time_bucket
from typing import List
load_dotenv()

router = APIRouter()

DATABASE_URL = os.getenv("DATABASE_URL")


@router.get("/", response_model=List[EventResponseSchema])
def read_events(session: Session = Depends(get_session)):
    bucket = time_bucket("1 minute", EventModel.time)
    query = (select(bucket, EventModel.page, func.count()).group_by(bucket, EventModel.page)).order_by(bucket,
                                                                                                       EventModel.page)
    results = session.exec(query).all()
    return [EventResponseSchema(bucket=r[0], page=r[1], count=r[2]) for r in results]


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


@router.delete("/{event_id}", status_code=204)
def delete_event(event_id: int, session: Session = Depends(get_session)):
    query = select(EventModel).where(EventModel.id == event_id)
    result = session.exec(query).first()
    if result is None:
        raise HTTPException(status_code=404, detail="Event not found")
    session.delete(result)
    session.commit()
    return {"message": "Event deleted successfully"}

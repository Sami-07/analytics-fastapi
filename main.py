from fastapi import FastAPI
from src.api.events import router as events_router

app = FastAPI()
app.include_router(events_router, prefix="/events", tags=["events"]) 
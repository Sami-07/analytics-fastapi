from fastapi import FastAPI
from api.events import router as events_router

app = FastAPI()

app.include_router(events_router, prefix="/api/events")


@app.get("/health")
async def health():
    return {"status": "ok"}
from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.events import router as events_router
from api.db.session import init_db
from fastapi.middleware.cors import CORSMiddleware
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(events_router, prefix="/api/events")


@app.get("/health")
async def health():
    return {"status": "ok"}
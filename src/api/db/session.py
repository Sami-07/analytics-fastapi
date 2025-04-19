from sqlmodel import create_engine, SQLModel, Session
from dotenv import load_dotenv
import os
import timescaledb
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "")
print(f"DEBUG: Using DATABASE_URL: {DATABASE_URL}")  # Debug line

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")

engine = create_engine(DATABASE_URL)


def init_db():
    print("Creating tables")
    SQLModel.metadata.create_all(engine)
    print("Creating hypertables for timescaledb")
    timescaledb.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

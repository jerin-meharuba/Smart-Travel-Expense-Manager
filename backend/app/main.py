from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_frontend_origin
from app.database import create_tables
from app.trips.router import router as trips_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Create the local development tables before requests are handled."""
    create_tables()
    yield


app = FastAPI(title="Smart Travel Expense Manager", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[get_frontend_origin()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(trips_router, prefix="/api/v1")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Smart Travel Expense Manager API"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

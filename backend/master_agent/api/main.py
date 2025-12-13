from fastapi import FastAPI
from contextlib import asynccontextmanager

from .research import router as research_router
from .internal import router as internal_router
from backend.common.storage.minio_client import initialize_buckets


@asynccontextmanager
async def lifespan(app:FastAPI):
    initialize_buckets()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(research_router)
app.include_router(internal_router)

@app.get("/health")
def health():
    return {"status": "ok"}
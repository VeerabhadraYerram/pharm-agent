from fastapi import FastAPI
from contextlib import asynccontextmanager

from .research import router as research_router
from .internal import router as internal_router
from backend.common.storage.minio_client import initialize_buckets
from backend.celery_app import celery_app # Force load Celery config


from backend.database import engine
from backend.master_agent.models.base import Base
# Import all models to ensure they are registered
from backend.master_agent.models import job
from backend.master_agent.models import task
from backend.master_agent.models import worker_response

@asynccontextmanager
async def lifespan(app:FastAPI):
    initialize_buckets()
    Base.metadata.create_all(bind=engine)
    yield

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(lifespan=lifespan)
print("DEBUG: SERVER STARTED WITH MIDDLEWARE", flush=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.requests import Request
from fastapi.responses import JSONResponse
import traceback

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"GLOBAL ERROR: {exc}", flush=True)
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "traceback": traceback.format_exc()}
    )

@app.middleware("http")
async def debug_middleware(request: Request, call_next):
    print(f"DEBUG: Request {request.method} {request.url}", flush=True)
    try:
        response = await call_next(request)
        return response
    except Exception as exc:
        print(f"DEBUG: Middleware caught exception: {exc}", flush=True)
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"error": str(exc), "traceback": traceback.format_exc()}
        )

app.include_router(research_router)
app.include_router(internal_router)

@app.get("/health")
def health():
    return {"status": "ok"}
from fastapi import FastAPI
from .research import router as research_router
from .internal import router as internal_router

app = FastAPI()
app.include_router(research_router)
app.include_router(internal_router)

@app.get("/health")
def health():
    return {"status": "ok"}
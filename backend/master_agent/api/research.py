from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
import uuid6
from sqlalchemy.orm import Session

from .auth import verify_api_key
from backend.database import SessionLocal
from backend.master_agent.models.job import Job
from backend.common.schemas.api_requests import ResearchRequest


from backend.master_agent.orchestration.conductor import run_research_workflow


router = APIRouter()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@router.post("/api/research", dependencies=[Depends(verify_api_key)])
async def create_research_job(
    request: ResearchRequest,
    db: Session = Depends(get_db)
):
    import traceback
    try:
        print(f"Creating job for {request.molecule}...")
        job = Job(
            id=uuid6.uuid7(),
            prompt_original=request.prompt,
            prompt_normalized=request.prompt,
            molecule=request.molecule,
            status="queued"
        )

        db.add(job)
        db.commit()
        db.refresh(job)

        # Trigger workflow
        print(f"Triggering workflow for {job.id}...")
        print(f"DEBUG: Celery Broker URL: {run_research_workflow.app.conf.broker_url}")
        run_research_workflow.delay(str(job.id), request.molecule)
        print("Workflow triggered.")

        return {"job_id": str(job.id)}
    except Exception as e:
        print(f"ERROR: {e}")
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "traceback": traceback.format_exc()}
        )

@router.get("/api/research/{job_id}/status", dependencies=[Depends(verify_api_key)])
async def get_research_status(job_id: str, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(404, "Job not found")
    return {
        "job_id": str(job.id),
        "status": job.status,
        "canonical_result": job.canonical_result,
        "created_at": job.created_at
    }

from fastapi.responses import StreamingResponse
from backend.common.storage.minio_client import minio_client

@router.get("/api/research/{job_id}/download/{file_type}")
async def download_artifact(job_id: str, file_type: str):
    if file_type not in ["pdf", "ppt"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Use 'pdf' or 'ppt'.")

    # mapped filename convention from report/worker.py
    object_name = f"{job_id}_report.pdf" if file_type == "pdf" else f"{job_id}_slides.pptx"
    content_type = "application/pdf" if file_type == "pdf" else "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    
    try:
        # Proxy stream from MinIO
        data_stream = minio_client.get_object("artifacts", object_name)
        return StreamingResponse(
            data_stream,
            media_type=content_type,
            headers={"Content-Disposition": f'attachment; filename="{object_name}"'}
        )
    except Exception as e:
        print(f"Download error: {e}")
        raise HTTPException(status_code=404, detail="Artifact not found. Research might still be processing.")
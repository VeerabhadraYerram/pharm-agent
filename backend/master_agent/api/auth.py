from fastapi import Request, HTTPException, status


API_KEY = "supersecret"
WORKER_TOKEN = "workersecret"

async def verify_api_key(request: Request):
    """
    For user-facing endpoints:
        - /api/research
        - /api/research/{job_id}/status

    Requires header: X-API-Key: <API_KEY>
    """

    key = request.headers.get("X-API-Key")
    if key != API_KEY:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
async def verify_worker_token(request: Request):
    """
    For internal worker callbacks:
        - /internal/task/{task_id}/complete
    
    Requires header: X-Worker-Token: <WORKER_TOKEN>
    """

    token = request.headers.get("X-Worker-Token")
    if token != WORKER_TOKEN:
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail="Invalid worker token"
        )
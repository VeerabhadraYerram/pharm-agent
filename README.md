## Executive Summary

This repository hosts **pharm-agent**, a backend-first prototype for orchestrating pharmaceutical research workflows. The backend is built with FastAPI and Celery, and separates concerns into distinct layers:

- **APIs and orchestration:** user-facing research endpoints (`/api/research`, `/api/research/{job_id}/status`) are protected by API keys, and worker callbacks on `/internal/task/{task_id}/complete` require a worker token.
- **Persistence and migrations:** SQLAlchemy models and Alembic scripts target Postgres to store jobs, tasks, worker responses, LLM call history, and artifacts. Migrations in `backend/migrations` include GIN indexes to speed JSONB search.
- **Storage readiness:** the service initializes MinIO buckets at startup to keep generated artifacts and audit data aligned with job metadata.

Common utilities:

- Shared schemas cover API requests, worker envelopes, canonical results, and task parameters.
- MinIO helpers initialize required buckets, upload artifacts, and generate presigned URLs for downloads.
- A Groq-powered LLM client enforces structured JSON responses against Pydantic schemas, logs prompts/responses to the database, and captures token usage for observability.

Workers and orchestration:

- `clinical_trials` filters a mocked dataset, normalizes entries into `TrialRecord` objects, and returns a typed envelope with provenance metadata.
- `report` generates PDF and PPT summaries from a `CanonicalResult`, uploads them to MinIO, and returns download-ready URIs.
- `market`, `patent`, `web`, and `internal_summarizer` workers are scaffolded for future data sources.
- The orchestration layer includes placeholders for a scheduler and task graph builder to coordinate dependencies across tasks.

Supporting assets include:

- `frontend/react-app`: placeholder for the planned user interface.
- `infra/terraform`: placeholder for future infrastructure-as-code definitions.
- `docker-compose.yml`: provisions Redis, Postgres, and MinIO so the stack can run locally without additional setup.
- `backend/requirements.txt`: pins the FastAPI/Celery/SQLAlchemy stack alongside LLM, storage, and reporting libraries.

Overall, the project establishes a modular foundation for evidence synthesis: ingesting research prompts, dispatching specialized workers, synthesizing clinical findings with LLM assistance, and packaging results as shareable artifacts with lineage and confidence metadata.

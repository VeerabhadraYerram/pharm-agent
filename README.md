# Pharm-Agent: AI-Driven Pharmaceutical Research Assistant

## Overview

Pharm-Agent is an advanced AI-powered platform designed to accelerate pharmaceutical research and clinical trial analysis. Leveraging the power of Large Language Models (LLMs) and autonomous agents, it automates the extraction, synthesis, and reporting of complex medical data. This tool aims to streamline the workflow for researchers by providing high-quality, data-driven insights from clinical trial repositories and scientific literature.

This prototype demonstrates an end-to-end workflow: from analyzing clinical trial data to synthesizing findings and generating comprehensive reports.

## Key Features

*   **Clinical Trials Analysis**: Automated ingestion and analysis of clinical trial data (e.g., from ClinicalTrials.gov) to identify study designs, patient cohorts, and outcomes.
*   **Intelligent Synthesis**: Uses multi-agent orchestration to synthesize disparate information into coherent medical insights.
*   **Automated Reporting**: Generates structured reports in PDF format, summarizing key findings, methodology, and conclusions.
*   **Interactive Dashboard**: A modern React-based user interface for initiating research jobs and viewing real-time status and results.
*   **Scalable Architecture**: Built on a robust microservices architecture using Docker, Celery, and Redis for reliable asynchronous task processing.

## Architecture

The system follows a modern microservices pattern:

1.  **Frontend**: A responsive Single Page Application (SPA) built with React and Vite, utilizing TailwindCSS for styling and Framer Motion for interactions.
2.  **API Layer**: A high-performance FastAPI backend that serves as the entry point for research requests and status updates.
3.  **Task Orchestration**: A distributed task queue system using Celery and Redis to manage long-running research jobs (Clinical Trials -> Synthesis -> Reporting).
4.  **Database**: PostgreSQL for persistent storage of research results and job metadata.
5.  **Object Storage**: MinIO for secure storage of generated reports and documents.

## Technology Stack

### Frontend
*   **Framework**: React 19 (Vite)
*   **Styling**: TailwindCSS 4, Vanilla CSS
*   **State Management/API**: Axios, React Hooks
*   **Animation**: Framer Motion

### Backend & Infrastructure
*   **API Framework**: FastAPI (Python 3.10+)
*   **Asynchronous Processing**: Celery, Redis
*   **Database**: PostgreSQL 14
*   **Storage**: MinIO (S3 compatible)
*   **AI/ML**: LangChain, OpenAI API integration
*   **Containerization**: Docker, Docker Compose

## Getting Started

### Prerequisites
*   Docker & Docker Compose
*   Node.js 18+ (for local frontend development)
*   Python 3.10+ (for local backend development)

### Environment Setup
1.  Clone the repository.
2.  Create a `.env` file in the root directory with the necessary API keys and configuration (see `.env.example` if available, otherwise ensure `OPENAI_API_KEY`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, etc., are set).

### Running with Docker (Recommended)
The easiest way to run the full stack is via Docker Compose:

```bash
docker-compose up --build
```

This command will start:
*   Postgres database (Port 5433)
*   Redis message broker (Port 6380)
*   MinIO object storage (Ports 9002/9003)
*   Backend API (Port 8000)
*   Celery Worker
*   Frontend Application (Port 5173 or as configured)

### Accessing the Application
*   **Frontend Dashboard**: http://localhost:5173
*   **API Documentation (Swagger)**: http://localhost:8000/docs
*   **MinIO Console**: http://localhost:9003

## Usage

1.  Navigate to the Frontend Dashboard.
2.  Click on **New Research** to start a new analysis task.
3.  Monitor the progress in the **Research Status** panel. The system will move through Clinical Analysis, Synthesis, and Report Generation stages.
4.  Once complete, view the summary or download the generated PDF report from the **History** section.

## License

[License information here]

---
**Note**: This project is a prototype developed for Hackathon purposes.

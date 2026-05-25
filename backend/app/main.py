from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import ExplainRequest, ExplainResponse
from app.services.explain_service import ExplainService, provider_status


app = FastAPI(title="MedEase Backend", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

service = ExplainService()


@app.get("/api/health")
def health() -> dict[str, str | bool]:
    return provider_status(service.complexity.ready)


@app.post("/api/explain", response_model=ExplainResponse)
def explain(request: ExplainRequest) -> ExplainResponse:
    return service.explain(request)

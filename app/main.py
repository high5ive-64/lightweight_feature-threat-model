from fastapi import FastAPI, HTTPException, Response
from app.config import settings
from app.llm.factory import list_supported_providers
from app.markdown import render_markdown
from app.schemas import FeatureInput, ThreatModelResponse
from app.service import ThreatModelService

app = FastAPI(title=settings.app_name, version="0.1.0")
service = ThreatModelService()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "provider": settings.provider}


@app.get("/providers")
def providers() -> dict:
    return {
        "configured": settings.provider,
        "supported": list_supported_providers(),
    }


@app.post("/threat-model", response_model=ThreatModelResponse)
def create_threat_model(feature: FeatureInput) -> ThreatModelResponse:
    try:
        return service.generate(feature)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/threat-model.md")
def create_threat_model_markdown(feature: FeatureInput) -> Response:
    try:
        model = service.generate(feature)
        markdown = render_markdown(feature, model)
        return Response(content=markdown, media_type="text/markdown")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
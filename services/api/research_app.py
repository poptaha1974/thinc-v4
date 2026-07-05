from __future__ import annotations

from fastapi import FastAPI
from services.api.external_research_routes import router

app = FastAPI(title="THINC External Research API")
app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "thinc-external-research-api"}

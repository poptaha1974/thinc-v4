from __future__ import annotations

from fastapi import FastAPI

from services.api.errors import install_error_handlers
from services.api.external_research_routes import router

app = FastAPI(title="THINC External Research API")
install_error_handlers(app)
app.include_router(router)

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "thinc-external-research-api"}

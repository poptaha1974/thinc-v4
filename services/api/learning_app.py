from __future__ import annotations

from fastapi import FastAPI
from services.api.adaptive_learning_routes import router

app = FastAPI(title="THINC Learning API")
app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "thinc-learning-api"}

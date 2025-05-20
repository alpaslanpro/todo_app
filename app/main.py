from fastapi import FastAPI
from app.api.v1.routes import router as v1_router

app = FastAPI(
    title="Todo API",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs"
)

app.include_router(v1_router, prefix="/api/v1")


@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}

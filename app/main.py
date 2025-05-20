from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.db.database import create_tables

def create_app():
    from fastapi import FastAPI
    from app.api.v1.routes import router as v1_router
    
    app = FastAPI(
        title="Todo API",
        version="1.0.0",
        openapi_url="/api/v1/openapi.json",
        docs_url="/api/v1/docs"
    )
    
    # Setup CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routes
    app.include_router(v1_router, prefix="/api/v1")
    
    @app.get("/health")
    def health_check():
        return {"status": "ok"}
    
    # Create database tables
    create_tables()
    
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
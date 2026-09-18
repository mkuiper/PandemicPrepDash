"""
Incident Response Dashboard - FastAPI Application Entrypoint.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import uvicorn
import os

from .api import api_router
from .core.state_manager import StateManager

app = FastAPI(
    title="Incident Response Dashboard",
    description="Second Eyes: all-hazards workshop demonstrator for incident coordination and decision tracking",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Incident Response Dashboard",
        "version": "0.1.0",
        "framework": "Second Eyes all-hazards workshop demonstration",
    }


# Static files mount
static_dir = Path(__file__).resolve().parent.parent.parent / "static"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")


def main():
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    print(f"Starting Second Eyes (Incident Response Dashboard) on http://{host}:{port}")
    uvicorn.run("pandemic_prep_dash.main:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    main()

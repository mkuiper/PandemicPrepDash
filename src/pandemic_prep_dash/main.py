"""
CBRN Rapid Response - FastAPI Application Entrypoint.
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
    title="CBRN Rapid Response",
    description="Workshop demonstrator for CBRN incident coordination, response pathways and decision tracking",
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
        "service": "CBRN Rapid Response",
        "version": "0.1.0",
        "framework": "CBRN rapid response workshop demonstration",
    }


# Static files mount
static_dir = Path(__file__).resolve().parent.parent.parent / "static"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")


def main():
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    print(f"Starting CBRN Rapid Response on http://{host}:{port}")
    uvicorn.run("pandemic_prep_dash.main:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    main()

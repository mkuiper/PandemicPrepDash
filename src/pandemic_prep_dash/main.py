"""
CBRN Rapid Response - FastAPI Application Entrypoint.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from pathlib import Path
import uvicorn
import os

from .api import api_router
from .core.state_manager import StateManager


def _cors_origins() -> list[str]:
    port = os.getenv("PORT", "8000")
    origins = [
        f"http://127.0.0.1:{port}",
        f"http://localhost:{port}",
        "http://testserver",
    ]
    extra = os.getenv("CORS_ORIGINS", "")
    origins.extend(item.strip() for item in extra.split(",") if item.strip())
    return origins


class DemoSecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Small real headers for the demo. Not a substitute for ISM or IRAP."""

    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        return response

app = FastAPI(
    title="CBRN Rapid Response",
    description="Workshop demonstrator for CBRN incident coordination, response pathways and decision tracking",
    version="0.1.0",
)

app.add_middleware(DemoSecurityHeadersMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
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
        "demo": True,
        "accreditation": "none",
        "security_note": "Not ISM, PSPF, or IRAP assessed. See Help: Security considerations.",
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

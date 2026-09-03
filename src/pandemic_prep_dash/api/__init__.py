from fastapi import APIRouter
from .routes_scenarios import router as scenarios_router
from .routes_pathways import router as pathways_router
from .routes_execution import router as execution_router
from .routes_agencies import router as agencies_router
from .routes_agents import router as agents_router
from .routes_hub import router as hub_router
from .routes_docs import router as docs_router
from .routes_governance import router as governance_router

api_router = APIRouter()
api_router.include_router(scenarios_router)
api_router.include_router(pathways_router)
api_router.include_router(execution_router)
api_router.include_router(agencies_router)
api_router.include_router(agents_router)
api_router.include_router(hub_router)
api_router.include_router(docs_router)
api_router.include_router(governance_router)

__all__ = ["api_router"]

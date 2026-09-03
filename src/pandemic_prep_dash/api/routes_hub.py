"""
Central Information Hub (Blackboard) & Blocker Alert API routes.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from ..core.state_manager import StateManager

router = APIRouter(prefix="/api/hub", tags=["Central Data Hub"])


class ResolveBlockerRequest(BaseModel):
    resolution_notes: str = "Authorized / mitigated by Incident Controller"


@router.get("/data")
def get_central_data_hub():
    engine = StateManager.get_engine()
    return {"data_hub": engine.data_hub.model_dump()}


@router.get("/blockers")
def get_blocker_alerts():
    engine = StateManager.get_engine()
    return {"blockers": [b.model_dump() for b in engine.data_hub.blockers]}


@router.post("/blockers/{alert_id}/resolve")
def resolve_blocker(alert_id: str, req: ResolveBlockerRequest):
    engine = StateManager.get_engine()
    success = engine.data_hub.resolve_blocker(alert_id, req.resolution_notes)
    if not success:
        raise HTTPException(status_code=404, detail=f"Blocker alert '{alert_id}' not found")
    return {"status": "resolved", "alert_id": alert_id, "notes": req.resolution_notes}

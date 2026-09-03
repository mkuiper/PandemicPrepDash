"""
Central Information Hub (Blackboard), Blocker Alert & Collaborative Message Board API routes.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

from ..core.state_manager import StateManager
from ..core.data_hub import HubMessage, MessageSenderType

router = APIRouter(prefix="/api/hub", tags=["Central Data Hub"])


class ResolveBlockerRequest(BaseModel):
    resolution_notes: str = "Authorized / mitigated by Incident Controller"


class PostHubMessageRequest(BaseModel):
    sender_name: str = "Human Duty Officer"
    sender_role: str = "Incident Specialist"
    target_node_id: Optional[str] = "@all"
    content: str
    tags: List[str] = Field(default_factory=list)
    is_urgent: bool = False


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


@router.get("/messages")
def list_hub_messages():
    """Lists human-agent collaborative messages posted to the Central Control Board."""
    engine = StateManager.get_engine()
    return {"messages": [m.model_dump() for m in engine.data_hub.messages]}


@router.post("/messages")
def post_hub_message(req: PostHubMessageRequest):
    """Allows human experts or controllers to post questions, clarifications, or directives."""
    engine = StateManager.get_engine()
    new_msg = HubMessage(
        message_id=f"msg_usr_{uuid.uuid4().hex[:6]}",
        sender_type=MessageSenderType.HUMAN_EXPERT,
        sender_name=req.sender_name,
        sender_role=req.sender_role,
        target_node_id=req.target_node_id,
        content=req.content,
        tags=req.tags or ["HUMAN_INPUT"],
        is_urgent=req.is_urgent,
        timestamp=datetime.utcnow().isoformat() + "Z",
    )
    engine.data_hub.post_message(new_msg)
    return {"status": "posted", "message": new_msg.model_dump()}

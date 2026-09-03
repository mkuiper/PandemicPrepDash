"""
Situation Version Control & Incident Snapshot API Routes.
Provides timeline auditing and checkpoint creation for human controllers.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

from ..core.version_control import VersionControlManager
from ..core.state_manager import StateManager
from ..core.lab_bridge import LabBridgeManager

router = APIRouter(prefix="/api/version-control", tags=["Situation Version Control"])


class CreateSnapshotRequest(BaseModel):
    checkpoint_name: str
    change_summary: str
    created_by: str = "Commonwealth Duty Officer"
    trigger_event: str = "MANUAL_DUTY_OFFICER_CHECKPOINT"


@router.get("/snapshots")
def list_situation_snapshots():
    """Lists the full chronological timeline of immutable situation snapshots."""
    # Ensure initialized
    if not VersionControlManager.list_snapshots():
        engine = StateManager.get_engine()
        scen_name = engine.scenario_data.get("name", "Active Scenario")
        total_nodes = len(engine.pathway.nodes)
        VersionControlManager.initialize_scenario_timeline(scen_name, total_nodes)

    return {"snapshots": [s.model_dump() for s in VersionControlManager.list_snapshots()]}


@router.post("/snapshots")
def create_situation_snapshot(body: CreateSnapshotRequest):
    """Manually creates a new immutable situation checkpoint in the incident progression."""
    engine = StateManager.get_engine()
    completed_nodes = len(engine.run.completed_node_ids)
    total_nodes = len(engine.pathway.nodes)
    open_blockers = len([b for b in engine.data_hub.blockers if b.status == "OPEN"])
    lab_requests = len(LabBridgeManager.list_requests())

    snapshot = VersionControlManager.capture_snapshot(
        checkpoint_name=body.checkpoint_name,
        trigger_event=body.trigger_event,
        created_by=body.created_by,
        completed_nodes_count=completed_nodes,
        total_nodes_count=total_nodes,
        open_blockers_count=open_blockers,
        dispatched_assays_count=lab_requests,
        change_summary=body.change_summary,
        artifacts_preview={k: str(type(v).__name__) for k, v in engine.run.node_artifacts.items()},
    )
    return {"status": "created", "snapshot": snapshot.model_dump()}


@router.get("/snapshots/{version_id}")
def get_situation_snapshot(version_id: str):
    """Retrieves detailed state snapshot for a specific version ID."""
    snapshot = VersionControlManager.get_snapshot(version_id)
    if not snapshot:
        raise HTTPException(status_code=404, detail=f"Snapshot '{version_id}' not found")
    return {"snapshot": snapshot.model_dump()}

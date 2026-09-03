"""
Physical Laboratory & Reference Assay Coordination API routes.
Connects computational agent squads with accredited Australian reference facilities
(ACDP Geelong PC4, ANSTO Lucas Heights, TGA Laboratories, ARPANSA Health Physics).
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime

from ..models.lab_bridge import (
    PhysicalAssayRequest,
    AssayCategory,
    FacilityIdentifier,
    AssayRequestStatus,
)
from ..core.lab_bridge import LabBridgeManager
from ..core.state_manager import StateManager
from ..core.data_hub import HubMessage, MessageSenderType

router = APIRouter(prefix="/api/lab-bridge", tags=["Physical Lab & Assay Bridge"])


class DispatchAssayRequest(BaseModel):
    authorized_by: str = "Commonwealth Incident Controller"


class IngestAssayResultsRequest(BaseModel):
    results_payload: Dict[str, Any]
    impact_notes: str = "Empirical validation ingested into computational pipeline."
    tested_by_specialist: str = "ACDP Senior Microbiologist"


@router.get("/requests")
def list_assay_requests():
    """Lists all physical laboratory requests, current lifecycle statuses, and turnaround times."""
    engine = StateManager.get_engine()
    # Initialize if empty
    if not LabBridgeManager.list_requests():
        threat_type = str(engine.pathway.threat_type)
        scen_id = engine.scenario_data.get("scenario_id", "scen_h5n1_avian_flu")
        LabBridgeManager.initialize_scenario_requests(threat_type, scen_id)
    return {"requests": [r.model_dump() for r in LabBridgeManager.list_requests()]}


@router.post("/requests")
def propose_assay_request(req: PhysicalAssayRequest):
    """Allows an agent squad or human expert to propose an empirical laboratory assay."""
    created = LabBridgeManager.propose_request(req)
    
    # Broadcast to Central Hub Message Board
    engine = StateManager.get_engine()
    engine.data_hub.post_message(
        HubMessage(
            message_id=f"msg_lab_{req.request_id}",
            sender_type=MessageSenderType.AGENT,
            sender_name=req.requesting_agent_role,
            sender_role="Laboratory Liaison",
            target_node_id=req.originating_node_id,
            content=f"🧪 PROPOSED PHYSICAL ASSAY: '{req.title}' at {req.target_facility.value}. Critical Question: {req.critical_question}",
            tags=["LAB_ASSAY", "EMPIRICAL_REQUEST"],
            is_urgent=(req.priority == "CRITICAL"),
        )
    )
    return {"status": "proposed", "request": created.model_dump()}


@router.post("/requests/{request_id}/dispatch")
def dispatch_assay_request(request_id: str, body: DispatchAssayRequest):
    """Authorizes and dispatches an assay request to the accredited reference facility."""
    success = LabBridgeManager.dispatch_request(request_id, body.authorized_by)
    if not success:
        raise HTTPException(status_code=404, detail=f"Assay request '{request_id}' not found")

    req = LabBridgeManager.get_request(request_id)
    engine = StateManager.get_engine()
    engine.data_hub.post_message(
        HubMessage(
            message_id=f"msg_disp_{request_id}",
            sender_type=MessageSenderType.HUMAN_EXPERT,
            sender_name=body.authorized_by,
            sender_role="Incident Controller",
            target_node_id="@all",
            content=f"📦 DISPATCHED TO FACILITY: '{req.title}' dispatched to {req.target_facility.value}. Estimated turnaround: {req.estimated_turnaround_hours}h.",
            tags=["DISPATCHED", "CHAIN_OF_CUSTODY"],
        )
    )
    return {"status": "dispatched", "request": req.model_dump()}


@router.post("/requests/{request_id}/results")
def record_assay_results(request_id: str, body: IngestAssayResultsRequest):
    """Ingests empirical lab results into the dashboard, updating the blackboard and notifying squads."""
    success = LabBridgeManager.record_results(request_id, body.results_payload, body.impact_notes)
    if not success:
        raise HTTPException(status_code=404, detail=f"Assay request '{request_id}' not found")

    req = LabBridgeManager.get_request(request_id)
    engine = StateManager.get_engine()

    # Feed results into blackboard artifacts
    engine.run.node_artifacts[f"lab_results_{request_id}"] = {
        "title": req.title,
        "facility": req.target_facility.value,
        "results": body.results_payload,
        "impact": body.impact_notes,
        "received_at": req.results_received_at,
    }

    # Broadcast empirical confirmation on the message board
    engine.data_hub.post_message(
        HubMessage(
            message_id=f"msg_res_{request_id}",
            sender_type=MessageSenderType.AGENT,
            sender_name=f"Reference Lab Officer ({body.tested_by_specialist})",
            sender_role="Physical Verification",
            target_node_id=req.originating_node_id,
            content=f"🔬 EMPIRICAL LAB FINDINGS RECEIVED: '{req.title}'. Results: {body.results_payload}. Impact: {body.impact_notes}",
            tags=["LAB_FINDINGS", "VALIDATED"],
        )
    )

    return {"status": "results_recorded", "request": req.model_dump()}

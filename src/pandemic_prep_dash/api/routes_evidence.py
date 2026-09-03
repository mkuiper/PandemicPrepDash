"""
Evidence Synthesis & Knowledge Gap Analysis API Routes.
Exposes critical evidence audits, conflicting evidence identification, and physical assay requirements.
"""

from fastapi import APIRouter
from typing import Dict, Any, List
from ..core.state_manager import StateManager
from ..core.evidence_analyzer import EvidenceAnalyzer
from ..models.evidence import EvidenceAnalysisReport

router = APIRouter(prefix="/api/hub/evidence", tags=["Evidence & Knowledge Gap Analysis"])


@router.get("/analysis")
def get_evidence_analysis():
    """Performs a comprehensive evidentiary audit of current incident artifacts."""
    engine = StateManager.get_engine()
    scen_id = engine.scenario_data.get("scenario_id", "scen_h5n1_avian_flu")
    threat_type = str(engine.pathway.threat_type)
    artifacts = engine.run.node_artifacts
    completed_nodes = engine.run.completed_node_ids

    report = EvidenceAnalyzer.analyze_incident_evidence(
        scenario_id=scen_id,
        threat_type=threat_type,
        node_artifacts=artifacts,
        completed_node_ids=completed_nodes,
    )
    return {"report": report.model_dump()}


@router.post("/analysis/audit")
def run_evidence_audit():
    """Forces an immediate evidentiary audit and returns the updated report."""
    return get_evidence_analysis()

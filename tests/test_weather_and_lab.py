"""Flood scenario alignment and lab-bridge lifecycle regressions."""
import pytest
from fastapi.testclient import TestClient
from pandemic_prep_dash.main import app
from pandemic_prep_dash.core.engine import PathwayExecutionEngine
from pandemic_prep_dash.core.registry import create_default_biological_pathway
from pandemic_prep_dash.core.state_manager import StateManager
from pandemic_prep_dash.core.lab_bridge import LabBridgeManager
from pandemic_prep_dash.core.evidence_analyzer import EvidenceAnalyzer
from pandemic_prep_dash.models.bio_chem import ThreatType
from pandemic_prep_dash.models.agency import AgencyIdentifier
from pandemic_prep_dash.models.lab_bridge import (
    PhysicalAssayRequest,
    AssayCategory,
    FacilityIdentifier,
    AssayRequestStatus,
)
from pandemic_prep_dash.models.pathway import NodeStatus, RunStatus


def test_flood_scenario_aligns_weather_pathway_and_pauses_for_approval():
    engine = PathwayExecutionEngine(create_default_biological_pathway(), "scen_h5n1_avian_flu")
    engine.set_scenario("scen_east_coast_low_flood")
    assert engine.pathway.threat_type == ThreatType.SEVERE_WEATHER
    assert engine.pathway.id == "pathway_default_severe_weather"
    assert engine.scenario_id == "scen_east_coast_low_flood"

    result = engine.execute_all()
    assert result["status"] == "approval_required"
    gate = next(n for n in engine.pathway.nodes if n.requires_human_approval)
    assert gate.id == "node_wx_approval"
    assert gate.status == NodeStatus.PAUSED
    assert "SSBA" not in (gate.label + gate.description)
    assert "drug_candidates" not in engine.run.node_artifacts
    assert "vaccine_candidates" not in engine.run.node_artifacts

    assert engine.approve_node(gate.id)
    assert engine.execute_all()["status"] == "completed"
    assert engine.run.status == RunStatus.COMPLETED
    assert "recovery" in engine.run.node_artifacts
    reports = engine.run.node_artifacts["agency_reports"]
    assert reports[AgencyIdentifier.BOM.value]["is_relevant"] is True
    assert reports[AgencyIdentifier.NSW_SES.value]["is_relevant"] is True
    assert reports[AgencyIdentifier.NEMA.value]["is_relevant"] is True
    assert reports[AgencyIdentifier.ACDP.value]["is_relevant"] is False
    assert reports[AgencyIdentifier.TGA.value]["is_relevant"] is False
    assert "Section 19A" not in reports[AgencyIdentifier.NEMA.value]["executive_summary"]
    assert "Oseltamivir" not in str(engine.run.node_artifacts).lower()


def test_weather_playbook_selects_matching_data():
    with TestClient(app) as client:
        response = client.post("/api/pathways/templates/load/pathway_default_severe_weather")
        assert response.status_code == 200
        state = client.get("/api/pathways/state").json()
    assert state["run"]["scenario_id"] == "scen_east_coast_low_flood"
    assert state["scenario"]["threat_type"] == "severe_weather"
    assert state["pathway"]["id"] == "pathway_default_severe_weather"


def test_flood_evidence_is_not_nerve_agent():
    report = EvidenceAnalyzer.analyze_incident_evidence(
        scenario_id="scen_east_coast_low_flood",
        threat_type="severe_weather",
        node_artifacts={},
        completed_node_ids=["node_wx_intake", "node_wx_triage", "node_wx_evidence"],
    )
    blob = report.model_dump()
    assert "Novichok" not in str(blob)
    assert "oxime" not in str(blob).lower()
    assert any("overtopping" in c.title.lower() or "forecast" in c.title.lower() for c in report.conflicting_evidence)


def test_lab_requests_reset_on_scenario_switch_and_start_as_proposals():
    engine = StateManager.get_engine()
    LabBridgeManager.initialize_scenario_requests("biological_virus", "scen_h5n1_avian_flu")
    bio_ids = {r.request_id for r in LabBridgeManager.list_requests()}
    assert bio_ids
    assert all(r.status == AssayRequestStatus.PROPOSED_BY_AGENT for r in LabBridgeManager.list_requests())
    assert all(r.dispatched_at is None for r in LabBridgeManager.list_requests())

    engine.set_scenario("scen_east_coast_low_flood")
    flood_ids = {r.request_id for r in LabBridgeManager.list_requests()}
    assert flood_ids
    assert flood_ids.isdisjoint(bio_ids)
    assert all("ACDP" not in r.target_facility.value for r in LabBridgeManager.list_requests())
    assert all(r.status == AssayRequestStatus.PROPOSED_BY_AGENT for r in LabBridgeManager.list_requests())

    engine.set_scenario("scen_h5n1_avian_flu")
    restored = {r.request_id for r in LabBridgeManager.list_requests()}
    assert restored == bio_ids


def test_lab_bridge_rejects_illegal_transitions_duplicates_and_replay():
    LabBridgeManager.initialize_scenario_requests("biological_virus", "scen_h5n1_avian_flu")
    first = LabBridgeManager.list_requests()[0]

    with pytest.raises(ValueError, match="dispatch"):
        LabBridgeManager.record_results(first.request_id, {"ok": True}, "too early")

    assert LabBridgeManager.dispatch_request(first.request_id, "Incident Controller")
    assert LabBridgeManager.record_results(first.request_id, {"ok": True}, "operator entered")
    stored = LabBridgeManager.get_request(first.request_id)
    assert stored.status == AssayRequestStatus.RESULTS_RECEIVED
    assert stored.simulated is True

    with pytest.raises(ValueError, match="dispatch"):
        LabBridgeManager.dispatch_request(first.request_id, "Incident Controller")

    duplicate = PhysicalAssayRequest(
        request_id=first.request_id,
        title="Duplicate",
        assay_category=AssayCategory.FIELD_RECONNAISSANCE,
        target_facility=FacilityIdentifier.BOM_OBSERVING,
        originating_node_id="node_wx_evidence",
        requesting_agent_role="tester",
        hypothesis_to_test="dup",
        critical_question="dup",
        specimen_requirements="none",
    )
    with pytest.raises(ValueError, match="already exists"):
        LabBridgeManager.propose_request(duplicate)


def test_lab_bridge_api_returns_conflict_for_illegal_results():
    with TestClient(app) as client:
        requests = client.get("/api/lab-bridge/requests").json()["requests"]
        req_id = requests[0]["request_id"]
        assert requests[0]["status"] == "PROPOSED_BY_AGENT"
        response = client.post(
            f"/api/lab-bridge/requests/{req_id}/results",
            json={"results_payload": {"ok": True}, "impact_notes": "illegal"},
        )
        assert response.status_code == 409
        assert client.post(
            "/api/lab-bridge/requests",
            json={**{k: requests[0][k] for k in (
                "title", "assay_category", "target_facility", "originating_node_id",
                "requesting_agent_role", "hypothesis_to_test", "critical_question",
                "specimen_requirements",
            )}, "request_id": req_id},
        ).status_code == 409

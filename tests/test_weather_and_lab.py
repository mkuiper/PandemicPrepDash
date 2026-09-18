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


def test_factory_fire_starts_at_site_looks_up_neighbours_and_records_events():
    engine = PathwayExecutionEngine(create_default_biological_pathway(), "scen_h5n1_avian_flu")
    engine.set_scenario("scen_industrial_warehouse_fire")
    assert engine.pathway.threat_type == ThreatType.INDUSTRIAL_FIRE
    assert engine.pathway.id == "pathway_default_industrial_fire"
    kinds = [e.kind for e in engine.run.event_log]
    assert "run_started" in kinds
    assert "scenario_selected" in kinds

    result = engine.execute_all()
    assert result["status"] == "approval_required"
    gate = next(n for n in engine.pathway.nodes if n.requires_human_approval)
    assert gate.id == "node_ff_approval"
    neighbours = engine.run.node_artifacts["adjacent_sites"]
    assert any(n.get("inventory_status") == "unknown" for n in neighbours)
    assert engine.data_hub.plume_and_environmental.get("planning_distance_km") == 3.2
    assert "drug_candidates" not in engine.run.node_artifacts
    assert any(e.kind == "approval_required" for e in engine.run.event_log)

    assert engine.approve_node(gate.id)
    assert engine.execute_all()["status"] == "completed"
    reports = engine.run.node_artifacts["agency_reports"]
    assert reports[AgencyIdentifier.FRNSW.value]["is_relevant"] is True
    assert reports[AgencyIdentifier.EPA_NSW.value]["is_relevant"] is True
    assert reports[AgencyIdentifier.NSW_AMBULANCE.value]["is_relevant"] is True
    assert reports[AgencyIdentifier.ACDP.value]["is_relevant"] is False
    assert reports[AgencyIdentifier.TGA.value]["is_relevant"] is False
    assert "Section 19A" not in reports[AgencyIdentifier.FRNSW.value]["executive_summary"]
    assert any(e.kind == "approved" for e in engine.run.event_log)
    assert any(e.kind == "run_completed" for e in engine.run.event_log)
    assert "HYSPLIT" in str(engine.run.node_artifacts.get("plume_model", {})).upper() or "hysplit" in str(
        engine.run.node_artifacts.get("plume_model", {})
    ).lower()


def test_factory_fire_playbook_selects_matching_data():
    with TestClient(app) as client:
        response = client.post("/api/pathways/templates/load/pathway_default_industrial_fire")
        assert response.status_code == 200
        state = client.get("/api/pathways/state").json()
    assert state["run"]["scenario_id"] == "scen_industrial_warehouse_fire"
    assert state["scenario"]["threat_type"] == "industrial_fire"
    assert state["run"]["event_log"]


def test_lead_context_is_grounded_and_dialogues_stay_on_pathway():
    from pandemic_prep_dash.core.lead_context import build_lead_context, filter_dialogues
    from pandemic_prep_dash.models.pathway import PathwayNode, NodeCategory
    from pandemic_prep_dash.models.agent import InterNodeDialogue, DialogueMessageType

    node = PathwayNode(id="node_ff_adjacent", label="Adjacent", description="x", category=NodeCategory.TRIAGE)
    ctx = build_lead_context(node, {"adjacent_sites": [{"name": "Tank farm", "inventory_status": "unknown"}]}, ["node_ff_adjacent"], "industrial_fire")
    blob = str(ctx).lower()
    assert "unknown" in blob
    assert "m7" not in blob or "inventory" in blob
    assert "oseltamivir" not in blob

    bio = PathwayNode(id="node_genomic_characterization", label="G", description="x", category=NodeCategory.CHARACTERIZATION)
    bio_ctx = build_lead_context(bio, {"identification": {"agent_name": "H5N1"}}, ["node_genomic_characterization"], "biological_virus")
    assert "M7" not in str(bio_ctx)

    kept = filter_dialogues(
        [InterNodeDialogue(
            dialogue_id="d1", source_node_id="a", source_agent_id="x", source_agent_name="A",
            target_node_id="node_genomic_characterization", target_agent_id="y", target_agent_name="B",
            message_type=DialogueMessageType.REQUEST_INFO, subject="s", content="c",
        )],
        ["node_ff_intake"],
    )
    assert kept == []


def test_factory_fire_run_publishes_lead_context_without_genomic_dialogue():
    engine = PathwayExecutionEngine(create_default_biological_pathway(), "scen_h5n1_avian_flu")
    engine.set_scenario("scen_industrial_warehouse_fire")
    engine.execute_all()
    adj = next(n for n in engine.pathway.nodes if n.id == "node_ff_adjacent")
    assert adj.outputs.get("lead_context")
    assert any("unknown" in str(q).lower() for q in adj.outputs["lead_context"])
    assert all(d.target_node_id in {n.id for n in engine.pathway.nodes} for d in engine.run.inter_node_dialogues)
    assert any(e.kind == "lead_context" for e in engine.run.event_log)


def test_factory_fire_evidence_is_not_nerve_agent():
    report = EvidenceAnalyzer.analyze_incident_evidence(
        scenario_id="scen_industrial_warehouse_fire",
        threat_type="industrial_fire",
        node_artifacts={},
        completed_node_ids=["node_ff_intake", "node_ff_adjacent", "node_ff_dispersal"],
    )
    blob = str(report.model_dump())
    assert "Novichok" not in blob
    assert "oxime" not in blob.lower()
    assert "tank-farm" in blob.lower() or "contour" in blob.lower()


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

"""
API integration tests for PandemicPrepDash endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from pandemic_prep_dash.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "PandemicPrepDash"


def test_scenarios_endpoints():
    # List scenarios
    res = client.get("/api/scenarios")
    assert res.status_code == 200
    scenarios = res.json()["scenarios"]
    assert len(scenarios) >= 3
    
    # Get specific scenario
    res_scen = client.get("/api/scenarios/scen_h5n1_avian_flu")
    assert res_scen.status_code == 200
    assert "H5N1" in res_scen.json()["name"]
    
    # Select scenario
    res_sel = client.post("/api/scenarios/select/scen_novel_coronavirus")
    assert res_sel.status_code == 200


def test_pathway_state_and_step_execution():
    # Reset
    client.post("/api/execution/reset")
    
    # State inspection
    res_state = client.get("/api/pathways/state")
    assert res_state.status_code == 200
    state = res_state.json()
    assert "pathway" in state
    assert len(state["pathway"]["nodes"]) > 0
    
    # Step forward
    res_step = client.post("/api/execution/step")
    assert res_step.status_code == 200
    assert res_step.json()["run_status"] in ["running", "paused"]


def test_agencies_endpoints():
    # List agencies
    res = client.get("/api/agencies")
    assert res.status_code == 200
    agencies = res.json()["agencies"]
    assert any(a["id"] == "ACDC" for a in agencies)
    assert any(a["id"] == "TGA" for a in agencies)
    assert any(a["id"] == "DAFF" for a in agencies)
    assert any(a["id"] == "DSTG" for a in agencies)
    
    # Get specific agency report preview
    res_rep = client.get("/api/agencies/TGA/report")
    assert res_rep.status_code == 200
    rep = res_rep.json()
    assert "Countermeasure" in rep["title"]
    
    # Export Markdown
    res_md = client.get("/api/agencies/ACDC/export/markdown")
    assert res_md.status_code == 200
    assert "ACDC Epidemiological & Surveillance Sitrep" in res_md.text
    
    # Dispatch briefing
    res_disp = client.post("/api/agencies/ACDC/dispatch")
    assert res_disp.status_code == 200
    assert res_disp.json()["status"] == "dispatched"


def test_custom_scenario_creation():
    payload = {
        "name": "Synthetic Bunyavirus Candidate",
        "threat_type": "biological_virus",
        "sample_type": "RNA",
        "raw_payload": ">Bunyavirus_Segment_L\nACGTACGTACGTNNNACGT",
        "source_location": "Top End, Northern Territory",
        "description": "Unexplained hemorrhagic syndrome cluster",
    }
    res = client.post("/api/scenarios/custom", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert "scen_custom_" in data["scenario_id"]

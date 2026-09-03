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


def test_dummy_sequences_and_templates_api():
    # Test dummy sequences
    res_seq = client.get("/api/scenarios/dummy-sequences")
    assert res_seq.status_code == 200
    seqs = res_seq.json()["dummy_sequences"]
    assert len(seqs) >= 5
    assert any("H5N1" in s["name"] for s in seqs)
    
    # Test templates list
    res_tmpl = client.get("/api/pathways/templates")
    assert res_tmpl.status_code == 200
    templates = res_tmpl.json()["templates"]
    assert len(templates) >= 4
    
    # Save template
    res_save = client.post("/api/pathways/templates/save", json={
        "name": "EPI-Rapid Response Template",
        "description": "Rapid epidemic response template test"
    })
    assert res_save.status_code == 200
    tmpl_id = res_save.json()["template_id"]
    
    # Load template
    res_load = client.post(f"/api/pathways/templates/load/{tmpl_id}")
    assert res_load.status_code == 200
    
    # Export pathway JSON
    res_exp = client.get("/api/pathways/export/json")
    assert res_exp.status_code == 200
    assert "nodes" in res_exp.json()
    assert "edges" in res_exp.json()
    
    # Delete saved template
    res_del = client.delete(f"/api/pathways/templates/{tmpl_id}")
    assert res_del.status_code == 200


def test_skills_toolbox_and_mcp_api():
    # Australian Gov skills endpoint
    res_skills = client.get("/api/agents/skills")
    assert res_skills.status_code == 200
    skills = res_skills.json()["skills"]
    assert len(skills) >= 4
    assert any(s["skill_id"] == "AUS-SKILL-SSBA-REPORTING" for s in skills)
    assert any("ARPANSA" in s["skill_id"] for s in skills)

    # Computational software toolbox endpoint
    res_tools = client.get("/api/agents/toolbox")
    assert res_tools.status_code == 200
    tools = res_tools.json()["toolbox"]
    assert len(tools) >= 5
    assert any("BLAST+" in t["name"] for t in tools)
    assert any("AlphaFold" in t["name"] for t in tools)

    # MCP servers registry endpoint
    res_mcps = client.get("/api/agents/mcps")
    assert res_mcps.status_code == 200
    mcps = res_mcps.json()["mcps"]
    assert len(mcps) >= 5
    assert any("ncbi-blast" in m["server_id"] for m in mcps)
    assert any("arpansa-rad" in m["server_id"] for m in mcps)

    # Model providers endpoint
    res_prov = client.get("/api/agents/providers")
    assert res_prov.status_code == 200
    providers = res_prov.json()["providers"]
    assert len(providers) >= 3
    assert any(p["id"] == "local_open_weights" for p in providers)
    assert any(p["id"] == "sovereign_australian_cloud" for p in providers)



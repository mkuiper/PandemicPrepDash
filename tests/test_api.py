"""
API integration tests for PandemicPrepDash endpoints.
Includes tests for ACDP, statutory links, Central Data Hub, Blocker Alerts,
Docs Center, and targeted agency relevance filtering.
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
    assert "data_hub" in state
    
    # Step forward
    res_step = client.post("/api/execution/step")
    assert res_step.status_code == 200
    assert res_step.json()["run_status"] in ["running", "paused"]


def test_acdp_agencies_endpoints_and_links():
    # List agencies
    res = client.get("/api/agencies")
    assert res.status_code == 200
    agencies = res.json()["agencies"]
    
    # ACDP must be present (not ACDC)
    assert any(a["id"] == "ACDP" for a in agencies)
    assert not any(a["id"] == "ACDC" for a in agencies)
    assert any(a["id"] == "TGA" for a in agencies)
    assert any(a["id"] == "DAFF" for a in agencies)
    assert any(a["id"] == "ARPANSA" for a in agencies)

    # Check official links exist on every agency
    for a in agencies:
        assert "official_website" in a and a["official_website"].startswith("http")
        assert "legislation_url" in a and a["legislation_url"].startswith("http")
        assert "relevant_threat_types" in a and len(a["relevant_threat_types"]) > 0

    # Get ACDP report
    res_rep = client.get("/api/agencies/ACDP/report")
    assert res_rep.status_code == 200
    rep = res_rep.json()
    assert "ACDP" in rep["title"]
    assert "is_relevant" in rep
    
    # Export Markdown
    res_md = client.get("/api/agencies/ACDP/export/markdown")
    assert res_md.status_code == 200
    assert "ACDP High-Containment Diagnostic" in res_md.text
    
    # Dispatch briefing
    res_disp = client.post("/api/agencies/ACDP/dispatch")
    assert res_disp.status_code == 200
    assert res_disp.json()["status"] == "dispatched"


def test_agency_relevance_filtering():
    # Select biological scenario
    client.post("/api/scenarios/select/scen_h5n1_avian_flu")
    client.post("/api/execution/reset")

    # Run execution
    client.post("/api/execution/run", json={"auto_approve": True})

    # In a biological scenario, ACDP and TGA should be relevant; ARPANSA should be standby
    res_acdp = client.get("/api/agencies/ACDP/report").json()
    assert res_acdp["is_relevant"] is True

    res_arpansa = client.get("/api/agencies/ARPANSA/report").json()
    assert res_arpansa["is_relevant"] is False
    assert "Standby" in res_arpansa["relevance_reason"]


def test_central_data_hub_and_blockers():
    # Select scenario and run
    client.post("/api/scenarios/select/scen_h5n1_avian_flu")
    client.post("/api/execution/reset")
    client.post("/api/execution/run", json={"auto_approve": True})

    # Inspect Data Hub data
    res_hub = client.get("/api/hub/data")
    assert res_hub.status_code == 200
    hub_data = res_hub.json()["data_hub"]
    assert "specimen_intel" in hub_data
    assert "literature_research" in hub_data
    assert "blockers" in hub_data

    # Inspect Blockers
    res_blockers = client.get("/api/hub/blockers")
    assert res_blockers.status_code == 200
    blockers = res_blockers.json()["blockers"]
    assert len(blockers) > 0

    # Resolve first blocker
    first_id = blockers[0]["alert_id"]
    res_res = client.post(f"/api/hub/blockers/{first_id}/resolve", json={
        "resolution_notes": "Duty Officer confirmed laboratory mitigation protocols."
    })
    assert res_res.status_code == 200
    assert res_res.json()["status"] == "resolved"


def test_documentation_center_endpoints():
    res_docs = client.get("/api/docs")
    assert res_docs.status_code == 200
    chapters = res_docs.json()["chapters"]
    assert len(chapters) >= 5
    assert any(c["id"] == "conops-overview" for c in chapters)
    assert any(c["id"] == "central-data-hub" for c in chapters)
    assert any(c["id"] == "statutory-acts-matrix" for c in chapters)

    # Read specific chapter
    res_ch = client.get("/api/docs/conops-overview")
    assert res_ch.status_code == 200
    assert "Operational Overview" in res_ch.json()["chapter"]["content"]


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

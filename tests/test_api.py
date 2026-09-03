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


def test_human_agent_collaborative_message_board():
    # 1. Retrieve messages
    res = client.get("/api/hub/messages")
    assert res.status_code == 200
    msgs = res.json()["messages"]
    assert len(msgs) >= 1  # Contains initialized welcome
    assert any(m["sender_type"] == "SYSTEM" for m in msgs)

    # 2. Post human expert message
    post_res = client.post("/api/hub/messages", json={
        "sender_name": "Dr. Sarah Chen, Epidemiologist",
        "sender_role": "Incident Specialist",
        "target_node_id": "@node_biosecurity_assessment",
        "content": "Please verify if this sample has any markers of dual-use gain-of-function.",
        "tags": ["HUMAN_INPUT", "GOF_CHECK"],
    })
    assert post_res.status_code == 200
    new_msg = post_res.json()["message"]
    assert new_msg["sender_name"] == "Dr. Sarah Chen, Epidemiologist"
    assert new_msg["target_node_id"] == "@node_biosecurity_assessment"
    assert new_msg["sender_type"] == "HUMAN_EXPERT"

    # 3. Check message in list
    res_after = client.get("/api/hub/messages")
    msgs_after = res_after.json()["messages"]
    assert any(m["content"] == "Please verify if this sample has any markers of dual-use gain-of-function." for m in msgs_after)


def test_governance_and_cloud_compute_api():
    # 1. Get governance settings
    res = client.get("/api/governance/settings")
    assert res.status_code == 200
    settings = res.json()["settings"]
    assert "compute" in settings
    assert "compliance" in settings
    assert settings["compliance"]["pspf_aligned"] is True
    assert "Australia" in settings["compliance"]["data_residency"]

    # 2. Update compute settings
    res_update = client.post("/api/governance/settings", json={
        "compute": {
            "provider": "aws_healthomics",
            "gpu_type": "NVIDIA H100 (80GB SXM5)",
            "gpu_count": 8,
            "cluster_endpoint": "https://healthomics.ap-southeast-2.amazonaws.com",
            "cloud_storage_bucket": "s3://aus-healthomics-emergency-vault/",
            "auto_scale_on_surge": True,
        }
    })
    assert res_update.status_code == 200
    updated_settings = res_update.json()["settings"]
    assert updated_settings["compute"]["provider"] == "aws_healthomics"
    assert updated_settings["compute"]["gpu_count"] == 8

    # 3. Get Australian Government policies
    res_pol = client.get("/api/governance/policies")
    assert res_pol.status_code == 200
    policies = res_pol.json()["policies"]
    assert len(policies) >= 4
    assert any("PSPF" in p["name"] for p in policies)
    assert any("ISM" in p["name"] for p in policies)
    assert any("SSBA" in p["name"] for p in policies)


def test_physical_lab_bridge_lifecycle():
    # 1. List pre-seeded assay requests
    res = client.get("/api/lab-bridge/requests")
    assert res.status_code == 200
    requests = res.json()["requests"]
    assert len(requests) >= 2
    assert any("ACDP" in r["target_facility"] for r in requests)

    # 2. Propose a new physical assay request
    new_req = {
        "title": "Emergency Pseudovirus PRNT50 Cross-Neutralization Assay",
        "assay_category": "virology_neutralization",
        "target_facility": "ACDP (CSIRO Australian Centre for Disease Prevention - PC4)",
        "originating_node_id": "node_vaccine_design",
        "requesting_agent_role": "Vaccine Squad Lead",
        "hypothesis_to_test": "Monoclonal antibody cocktail mAb-AUS-01 demonstrates sub-nanomolar neutralization.",
        "critical_question": "Does mAb-AUS-01 neutralize emerging clade with IC50 < 0.5 ug/mL?",
        "specimen_requirements": "100 uL serum sample",
        "biosafety_level": "PC4 Containment",
        "estimated_turnaround_hours": 24,
        "priority": "CRITICAL",
    }
    res_prop = client.post("/api/lab-bridge/requests", json=new_req)
    assert res_prop.status_code == 200
    created = res_prop.json()["request"]
    req_id = created["request_id"]
    assert created["status"] == "PROPOSED_BY_AGENT"

    # 3. Authorize and dispatch to reference facility
    res_disp = client.post(f"/api/lab-bridge/requests/{req_id}/dispatch", json={
        "authorized_by": "National Incident Commander"
    })
    assert res_disp.status_code == 200
    dispatched = res_disp.json()["request"]
    assert dispatched["status"] == "DISPATCHED_TO_FACILITY"
    assert dispatched["authorized_by"] == "National Incident Commander"

    # 4. Ingest real-world empirical lab findings
    res_res = client.post(f"/api/lab-bridge/requests/{req_id}/results", json={
        "results_payload": {
            "neutralization_confirmed": True,
            "IC50_ug_per_ml": 0.18,
            "potency_index": "STRONG_PROTECTION"
        },
        "impact_notes": "Sub-nanomolar neutralization confirmed empirically at ACDP PC4.",
        "tested_by_specialist": "Dr. Ian Barr, ACDP"
    })
    assert res_res.status_code == 200
    completed = res_res.json()["request"]
    assert completed["status"] == "RESULTS_RECEIVED"
    assert completed["results_payload"]["IC50_ug_per_ml"] == 0.18

    # 5. Check announcement on Message Board
    res_msgs = client.get("/api/hub/messages")
    assert res_msgs.status_code == 200
    msgs = res_msgs.json()["messages"]
    assert any("EMPIRICAL LAB FINDINGS RECEIVED" in m["content"] for m in msgs)


def test_lab_bridge_docs_chapter():
    res = client.get("/api/docs/real-world-lab-bridge")
    assert res.status_code == 200
    chapter = res.json()["chapter"]
    assert chapter["id"] == "real-world-lab-bridge"
    assert "ACDP" in chapter["content"]
    assert "ANSTO" in chapter["content"]


def test_evidence_analyzer_audit_endpoint():
    res = client.get("/api/hub/evidence/analysis")
    assert res.status_code == 200
    rep = res.json()["report"]
    assert "overall_confidence_score" in rep
    assert "domain_scores" in rep
    assert len(rep["knowledge_gaps"]) >= 1
    assert len(rep["conflicting_evidence"]) >= 1
    assert len(rep["required_validations"]) >= 1

    # Check specific conflict structure
    conflict = rep["conflicting_evidence"][0]
    assert "claim_a" in conflict
    assert "claim_b" in conflict
    assert "recommended_arbitration" in conflict

    # Trigger audit endpoint
    res_audit = client.post("/api/hub/evidence/analysis/audit")
    assert res_audit.status_code == 200
    assert "report" in res_audit.json()


def test_situation_version_control_timeline():
    # 1. List pre-seeded snapshots
    res = client.get("/api/version-control/snapshots")
    assert res.status_code == 200
    snaps = res.json()["snapshots"]
    assert len(snaps) >= 1
    assert any("Baseline" in s["checkpoint_name"] or "Ingestion" in s["checkpoint_name"] for s in snaps)

    # 2. Create a manual checkpoint
    res_create = client.post("/api/version-control/snapshots", json={
        "checkpoint_name": "Antiviral IC50 Confirmed & NMS Activated",
        "created_by": "Chief Medical Officer",
        "change_summary": "Empirical lab assays validate therapeutic window; Section 19A emergency approval granted.",
        "trigger_event": "MANUAL_DUTY_OFFICER_CHECKPOINT"
    })
    assert res_create.status_code == 200
    new_snap = res_create.json()["snapshot"]
    assert new_snap["checkpoint_name"] == "Antiviral IC50 Confirmed & NMS Activated"
    assert new_snap["created_by"] == "Chief Medical Officer"
    ver_id = new_snap["version_id"]

    # 3. Fetch single snapshot by ID
    res_get = client.get(f"/api/version-control/snapshots/{ver_id}")
    assert res_get.status_code == 200
    assert res_get.json()["snapshot"]["version_id"] == ver_id


def test_operational_playbooks_metadata():
    res = client.get("/api/pathways/templates")
    assert res.status_code == 200
    tmpls = res.json()["templates"]
    assert len(tmpls) >= 4
    # Ensure playbooks metadata fields exist
    bio_pb = next((t for t in tmpls if t["id"] == "pathway_default_biological"), None)
    assert bio_pb is not None
    assert "playbook_title" in bio_pb
    assert "scenario_scope" in bio_pb
    assert "trigger_criteria" in bio_pb
    assert "lead_agency" in bio_pb


def test_architecture_documentation_chapter():
    res = client.get("/api/docs/platform-system-architecture")
    assert res.status_code == 200
    chapter = res.json()["chapter"]
    assert chapter["id"] == "platform-system-architecture"
    assert "DAG Pipeline Engine" in chapter["content"]
    assert "AGY" in chapter["content"]
    assert "Claude Code" in chapter["content"]
    assert "Codex" in chapter["content"]




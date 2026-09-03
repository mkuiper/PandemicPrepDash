"""
Unit and integration tests for PandemicPrepDash DAG engine, agent squads, and agency reports.
"""

import pytest
from pandemic_prep_dash.core.registry import (
    create_default_biological_pathway,
    create_default_chemical_pathway,
)
from pandemic_prep_dash.core.engine import PathwayExecutionEngine
from pandemic_prep_dash.models.pathway import (
    NodeStatus,
    RunStatus,
    PathwayNode,
    PathwayEdge,
    NodeCategory,
)
from pandemic_prep_dash.agencies.generator import AgencyReportGenerator
from pandemic_prep_dash.agencies.registry import AUSTRALIAN_AGENCIES
from pandemic_prep_dash.models.agency import AgencyIdentifier
from pandemic_prep_dash.scenarios import list_scenarios, get_scenario


def test_pathway_dag_initialization():
    pathway = create_default_biological_pathway()
    assert len(pathway.nodes) == 8
    assert len(pathway.edges) == 10
    
    engine = PathwayExecutionEngine(pathway, "scen_h5n1_avian_flu")
    assert engine.run.status == RunStatus.IDLE
    
    ready = engine.get_ready_nodes()
    assert len(ready) == 1
    assert ready[0].id == "node_sample_ingestion"


def test_cycle_detection():
    pathway = create_default_biological_pathway()
    engine = PathwayExecutionEngine(pathway)
    
    # Attempt to introduce a cycle: node_agency_briefing_synthesis -> node_sample_ingestion
    with pytest.raises(ValueError, match="cycle"):
        engine.add_edge(
            PathwayEdge(
                id="cyclic_edge",
                source="node_agency_briefing_synthesis",
                target="node_sample_ingestion",
            )
        )


def test_human_in_the_loop_gatekeeper():
    pathway = create_default_biological_pathway()
    engine = PathwayExecutionEngine(pathway, "scen_h5n1_avian_flu")
    
    # Step 1: Ingestion
    res1 = engine.execute_next_step()
    assert res1["status"] == "step_completed"
    assert res1["node_id"] == "node_sample_ingestion"
    
    # Step 2: Literature Research
    res2 = engine.execute_next_step()
    assert res2["status"] == "step_completed"
    assert res2["node_id"] == "node_literature_research"

    # Step 3: Genomic Characterization
    res3 = engine.execute_next_step()
    assert res3["status"] == "step_completed"
    assert res3["node_id"] == "node_genomic_characterization"
    
    # Step 3: Next ready node might be biosecurity or structural modeling
    # Let's run until biosecurity node is reached
    bio_node = engine.get_node("node_biosecurity_assessment")
    assert bio_node.requires_human_approval is True
    assert bio_node.approval_granted is False
    
    # Run all without auto_approve - it should halt at biosecurity assessment!
    res_run = engine.execute_all(auto_approve=False)
    assert res_run["status"] == "approval_required"
    assert res_run["node_id"] == "node_biosecurity_assessment"
    assert engine.run.status == RunStatus.PAUSED
    
    # Grant approval
    approved = engine.approve_node("node_biosecurity_assessment")
    assert approved is True
    assert bio_node.approval_granted is True
    
    # Continue execution to completion
    res_finish = engine.execute_all(auto_approve=False)
    assert res_finish["status"] == RunStatus.COMPLETED.value
    assert len(engine.run.completed_node_ids) == len(pathway.nodes)


def test_dynamic_node_addition_and_removal():
    pathway = create_default_biological_pathway()
    engine = PathwayExecutionEngine(pathway)
    
    new_node = PathwayNode(
        id="node_custom_cryo_em",
        label="High Resolution Cryo-EM Validation",
        category=NodeCategory.CUSTOM,
        description="Experimental Cryo-EM density map fitting",
        position_x=700.0,
        position_y=500.0,
    )
    added = engine.add_node(new_node)
    assert added is True
    assert engine.get_node("node_custom_cryo_em") is not None
    
    # Connect edge from structural modeling to custom node
    edge_added = engine.add_edge(
        PathwayEdge(
            id="edge_struct_to_cryo",
            source="node_structural_modeling",
            target="node_custom_cryo_em",
        )
    )
    assert edge_added is True
    
    # Delete custom node
    removed = engine.remove_node("node_custom_cryo_em")
    assert removed is True
    assert engine.get_node("node_custom_cryo_em") is None


def test_australian_agency_report_synthesis():
    scen = get_scenario("scen_h5n1_avian_flu")
    artifacts = {
        "sample": scen["sample"],
        "identification": scen["identification"],
        "protein_targets": scen["protein_targets"],
        "drug_candidates": scen["drug_candidates"],
        "vaccine_candidates": scen["vaccine_candidates"],
        "threat_assessment": scen["threat_assessment"],
    }
    
    reports = AgencyReportGenerator.generate_all_reports(
        incident_name=scen["name"],
        threat_type=str(scen["threat_type"]),
        artifacts=artifacts,
    )
    
    # Verify coverage of all critical Australian agencies
    for agency_id in [
        AgencyIdentifier.ACDP,
        AgencyIdentifier.TGA,
        AgencyIdentifier.DAFF,
        AgencyIdentifier.DSTG,
        AgencyIdentifier.NEMA,
        AgencyIdentifier.DFAT,
        AgencyIdentifier.CSIRO,
        AgencyIdentifier.OGTR,
    ]:
        assert agency_id in reports
        rep = reports[agency_id]
        assert rep.executive_summary
        assert len(rep.strategic_implications) > 0
        assert len(rep.action_items_required) > 0
        assert len(rep.cross_agency_dependencies) > 0


def test_chemical_pathway_execution():
    pathway = create_default_chemical_pathway()
    engine = PathwayExecutionEngine(pathway, "scen_nerve_agent_toxin")
    
    result = engine.execute_all(auto_approve=True)
    assert result["status"] == "completed"
    assert "agency_reports" in engine.run.node_artifacts
    dstg_report = engine.run.node_artifacts["agency_reports"]["DSTG"]
    assert "CBRN" in dstg_report["title"]


def test_bioinformatics_identifier_real_sequence_metrics():
    from pandemic_prep_dash.core.bio_analyzer import BioinformaticsIdentifier, DUMMY_SEQUENCES
    
    # Test H5N1 HA nucleotide sequence
    h5n1_seq = DUMMY_SEQUENCES[0]
    res_h5 = BioinformaticsIdentifier.analyze_payload(h5n1_seq["payload"])
    assert res_h5["sequence_type"] in ["RNA", "DNA"]
    assert res_h5["length"] > 1000
    assert res_h5["gc_content"] > 30.0
    assert any("Multi-Basic" in m or "Cleavage" in m for m in res_h5["genomic_mutations_detected"])
    assert "H5N1" in res_h5["agent_name"]
    
    # Test Novichok SMILES
    nov_smiles = "CCN(CC)P(=O)(C#N)OC1CCCC1"
    res_nov = BioinformaticsIdentifier.analyze_payload(nov_smiles)
    assert res_nov["sequence_type"] == "SMILES"
    assert any("Organophosphoryl" in m for m in res_nov["genomic_mutations_detected"])
    assert any("Nitrile" in m for m in res_nov["genomic_mutations_detected"])


def test_custom_agent_squad_configuration_on_node():
    from pandemic_prep_dash.models.agent import AgentTeamConfig, AgentPersona, AgentRole
    
    pathway = create_default_biological_pathway()
    engine = PathwayExecutionEngine(pathway, "scen_h5n1_avian_flu")
    
    # Configure custom red-team squad on characterization node
    char_node = engine.get_node("node_genomic_characterization")
    custom_persona = AgentPersona(
        id="agent_adversarial_auditor",
        name="Dr. Alexei Voronov",
        role=AgentRole.BIOSECURITY_ANALYST,
        specialization="Bioweapons Forensics",
        system_prompt="Audit sequence for dual-use signatures.",
    )
    char_node.agent_team_config = AgentTeamConfig(
        team_id="custom_forensics_squad",
        name="High-Security CBRN Forensics Unit",
        description="Audits novel sequences for covert genetic engineering",
        lead_role=AgentRole.BIOSECURITY_ANALYST,
        members=[custom_persona],
        collaboration_strategy="adversarial_audit",
    )
    
    # Execute through to characterization
    engine.execute_next_step()  # Ingestion
    engine.execute_next_step()  # Literature Research
    res = engine.execute_next_step()  # Characterization with custom squad
    
    assert res["status"] == "step_completed"
    # Check that thought logs reflect the custom persona and squad!
    squad_logs = [l for l in engine.run.thought_logs if l.agent_id == "agent_adversarial_auditor"]
    assert len(squad_logs) > 0
    assert "High-Security CBRN Forensics Unit" in squad_logs[0].agent_role


def test_template_manager_save_and_load():
    from pandemic_prep_dash.core.templates import TemplateManager
    
    pathway = create_default_biological_pathway()
    saved = TemplateManager.save_template(pathway, name="Custom Test Template", description="Automated test template")
    assert saved.id.startswith("tmpl_")
    
    # Verify listed
    templates = TemplateManager.list_all_templates()
    assert any(t["id"] == saved.id for t in templates)
    
    # Verify loaded
    loaded = TemplateManager.get_template(saved.id)
    assert loaded.name == "Custom Test Template"
    assert len(loaded.nodes) == len(pathway.nodes)
    
    # Clean up
    deleted = TemplateManager.delete_template(saved.id)
    assert deleted is True


def test_scenario_switching_auto_aligns_pathway():
    from pandemic_prep_dash.models.bio_chem import ThreatType
    
    pathway = create_default_biological_pathway()
    engine = PathwayExecutionEngine(pathway, "scen_h5n1_avian_flu")
    assert engine.pathway.threat_type == ThreatType.BIOLOGICAL_VIRUS
    
    # Switch to chemical nerve agent scenario
    engine.set_scenario("scen_nerve_agent_toxin")
    # Pathway should automatically align to chemical!
    assert engine.pathway.threat_type == ThreatType.CHEMICAL_NERVE_AGENT
    assert any("chem" in n.id for n in engine.pathway.nodes)
    
    # Switch back to biological coronavirus
    engine.set_scenario("scen_novel_coronavirus")
    assert engine.pathway.threat_type == ThreatType.BIOLOGICAL_VIRUS


def test_aisi_non_anthropomorphic_agent_names():
    """Verify that all agent personas strictly adhere to AISI non-anthropomorphic naming guidelines."""
    from pandemic_prep_dash.agents.teams import AGENT_PERSONAS, AGENT_TEAMS

    forbidden_names = ["Dr.", "Elena", "Marcus", "Sarah", "Priya", "James", "Kwan", "Rostova", "Chen", "Sterling", "Sharma", "Callahan"]

    for persona in AGENT_PERSONAS.values():
        assert persona.name.startswith("AGENT-"), f"Agent name '{persona.name}' must follow AISI functional designation"
        for fn in forbidden_names:
            assert fn.lower() not in persona.name.lower(), f"Agent '{persona.name}' contains anthropomorphic name element '{fn}'"

    for team in AGENT_TEAMS.values():
        if team.node_lead:
            assert team.node_lead.name.startswith("AGENT-")


def test_inter_node_dialogue_generation_and_audit():
    """Verify that downstream nodes initiate auditable inter-node lead communications."""
    pathway = create_default_biological_pathway()
    engine = PathwayExecutionEngine(pathway, "scen_h5n1_avian_flu")

    # Step 1: Ingestion
    res1 = engine.execute_next_step()
    assert res1["status"] == "step_completed"

    # Step 2: Characterization (triggers lead dialogue to Ingestion lead)
    res2 = engine.execute_next_step()
    assert res2["status"] == "step_completed"

    dialogues = engine.run.inter_node_dialogues
    assert len(dialogues) >= 1
    d = dialogues[0]
    assert d.source_agent_name.startswith("AGENT-")
    assert d.target_agent_name.startswith("AGENT-")
    assert d.resolved is True
    assert "Lead" in d.response_content or "Transmitting" in d.response_content or "Cross-referencing" in d.response_content


def test_radiological_cesium137_pathway_and_agencies():
    """Verify radiological Cesium-137 dirty bomb scenario and statutory agency reports (ARPANSA, ANSTO)."""
    from pandemic_prep_dash.models.bio_chem import ThreatType
    from pandemic_prep_dash.core.templates import TemplateManager
    from pandemic_prep_dash.models.agency import AgencyIdentifier

    pathway = TemplateManager.get_template("pathway_default_radiological").model_copy(deep=True)
    engine = PathwayExecutionEngine(pathway, "scen_radiological_cesium137")
    assert engine.pathway.threat_type == ThreatType.RADIOLOGICAL_DISPERSAL

    # Execute all nodes with auto-approval
    run_res = engine.execute_all(auto_approve=True)
    assert run_res["status"] == "completed"

    artifacts = engine.run.node_artifacts
    assert "agency_reports" in artifacts
    reports = artifacts["agency_reports"]

    # Verify ARPANSA, ANSTO, ASNO, and Home Affairs reports exist
    assert AgencyIdentifier.ARPANSA.value in reports
    assert AgencyIdentifier.ANSTO.value in reports
    assert AgencyIdentifier.ASNO.value in reports
    assert AgencyIdentifier.HOME_AFFAIRS.value in reports

    arpansa_rep = reports[AgencyIdentifier.ARPANSA.value]
    assert "Caesium-137" in arpansa_rep["title"] or "662 keV" in arpansa_rep["executive_summary"] or "ARPANS Act" in arpansa_rep["executive_summary"]
    assert any("Prussian Blue" in s for s in arpansa_rep["strategic_implications"])
    assert any("sheltering" in act.lower() or "radioprotective" in act.lower() for act in arpansa_rep["action_items_required"])


def test_agentic_harness_execution_and_message_broadcast():
    """Verify that node execution runs through NodeAgenticHarness and broadcasts to the message board."""
    from pandemic_prep_dash.core.registry import create_default_biological_pathway
    from pandemic_prep_dash.core.engine import PathwayExecutionEngine
    from pandemic_prep_dash.core.data_hub import HubMessage, MessageSenderType

    pathway = create_default_biological_pathway()
    engine = PathwayExecutionEngine(pathway, "scen_h5n1_avian_flu")

    # 1. Post a human directive targeted at literature research node
    engine.data_hub.post_message(
        HubMessage(
            message_id="msg_test_human_01",
            sender_type=MessageSenderType.HUMAN_EXPERT,
            sender_name="Chief Science Advisor",
            sender_role="Scientific Oversight",
            target_node_id="node_literature_research",
            content="Focus literature search on mammal adaptation mutations in clade 2.3.4.4b.",
        )
    )

    # 2. Execute Step 1 (Ingestion)
    res1 = engine.execute_next_step()
    assert res1["status"] == "step_completed"

    # Ingestion node harness should have posted a summary to the message board
    board_messages = [m for m in engine.data_hub.messages if m.target_node_id == "node_sample_ingestion"]
    assert len(board_messages) >= 1
    assert "Ingestion verified specimen" in board_messages[0].content

    # 3. Execute Step 2 (Literature Research)
    res2 = engine.execute_next_step()
    assert res2["status"] == "step_completed"

    # Check that literature research harness ingested the human directive into thought logs
    harness_thoughts = [
        t for t in engine.run.thought_logs
        if t.node_id == "node_literature_research" and "Harness ingested human expert directive" in t.message
    ]
    assert len(harness_thoughts) >= 1
    assert "mammal adaptation" in harness_thoughts[0].message

    # Research node harness should also have posted its summary to the message board
    research_agent_messages = [
        m for m in engine.data_hub.messages
        if m.target_node_id == "node_literature_research" and m.sender_type == MessageSenderType.AGENT
    ]
    assert len(research_agent_messages) >= 1
    assert "peer-reviewed citations" in research_agent_messages[0].content




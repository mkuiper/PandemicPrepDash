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
    assert len(pathway.nodes) == 7
    assert len(pathway.edges) == 8
    
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
    
    # Step 2: Genomic characterization
    res2 = engine.execute_next_step()
    assert res2["status"] == "step_completed"
    assert res2["node_id"] == "node_genomic_characterization"
    
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
        AgencyIdentifier.ACDC,
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

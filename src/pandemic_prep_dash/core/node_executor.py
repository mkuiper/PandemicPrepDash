"""
Node Executor - executes individual pathway nodes using agentic team reasoning
and produces structured biological, chemical, and agency reporting artifacts.
"""

from typing import Dict, Any, List, Tuple
from datetime import datetime
import uuid
import time
from ..models.pathway import PathwayNode, NodeStatus, NodeCategory
from ..models.agent import AgentThoughtLog, AgentThoughtPhase, AgentRole
from ..agents.teams import AGENT_TEAMS, AGENT_PERSONAS
from ..agencies.generator import AgencyReportGenerator
from ..agencies.registry import AUSTRALIAN_AGENCIES


class NodeExecutor:
    """Executes a single node in the DAG, producing thought logs and updating the blackboard."""

    @classmethod
    def execute_node(
        cls,
        node: PathwayNode,
        blackboard: Dict[str, Any],
        scenario_data: Dict[str, Any],
    ) -> Tuple[PathwayNode, List[AgentThoughtLog], Dict[str, Any]]:
        """
        Executes node logic using assigned agent squad.
        Returns updated node, new thought logs, and artifacts to merge into blackboard.
        """
        start_time = time.time()
        node.status = NodeStatus.RUNNING
        new_logs: List[AgentThoughtLog] = []
        new_artifacts: Dict[str, Any] = {}

        team_config = AGENT_TEAMS.get(node.agent_team_id)
        lead_persona = team_config.members[0] if team_config and team_config.members else AGENT_PERSONAS["dr_rostova"]

        if node.category == NodeCategory.INGESTION:
            sample_data = scenario_data.get("sample", {})
            new_logs.append(
                AgentThoughtLog(
                    id=f"th_{uuid.uuid4().hex[:8]}",
                    agent_id=lead_persona.id,
                    agent_name=lead_persona.name,
                    agent_role=lead_persona.role.value,
                    node_id=node.id,
                    phase=AgentThoughtPhase.OBSERVATION,
                    message=f"Received raw input sample '{sample_data.get('name', 'Sample')}'. Initiating format parsing and QC audit.",
                    confidence=0.98,
                )
            )
            new_logs.append(
                AgentThoughtLog(
                    id=f"th_{uuid.uuid4().hex[:8]}",
                    agent_id=lead_persona.id,
                    agent_name=lead_persona.name,
                    agent_role=lead_persona.role.value,
                    node_id=node.id,
                    phase=AgentThoughtPhase.TOOL_EXECUTION,
                    message="Parsed sequence payload and verified source coordinates.",
                    tool_name="fasta_smiles_parser",
                    tool_input={"format": sample_data.get("sample_type", "RNA"), "location": sample_data.get("source_location")},
                    tool_output_summary="Quality checks passed. Sequence length/structure conforms to diagnostic threshold.",
                    confidence=0.99,
                )
            )
            new_artifacts["sample"] = sample_data
            node.outputs = {"sample_id": sample_data.get("sample_id"), "status": "verified"}

        elif node.category == NodeCategory.CHARACTERIZATION:
            ident_data = scenario_data.get("identification", {})
            new_logs.append(
                AgentThoughtLog(
                    id=f"th_{uuid.uuid4().hex[:8]}",
                    agent_id=lead_persona.id,
                    agent_name=lead_persona.name,
                    agent_role=lead_persona.role.value,
                    node_id=node.id,
                    phase=AgentThoughtPhase.HYPOTHESIS,
                    message="Comparing sequence against reference databases to determine taxonomy and evolutionary lineage.",
                    confidence=0.94,
                )
            )
            new_logs.append(
                AgentThoughtLog(
                    id=f"th_{uuid.uuid4().hex[:8]}",
                    agent_id=lead_persona.id,
                    agent_name=lead_persona.name,
                    agent_role=lead_persona.role.value,
                    node_id=node.id,
                    phase=AgentThoughtPhase.TOOL_EXECUTION,
                    message="Completed high-sensitivity database alignment and variant calling.",
                    tool_name="blast_and_clade_classifier",
                    tool_input={"target_databases": ["NCBI_RefSeq", "GISAID", "PubChem"]},
                    tool_output_summary=f"Matched {ident_data.get('agent_name')} ({ident_data.get('clade_or_lineage')}) with {ident_data.get('alignment_confidence', 99)}% identity.",
                    confidence=0.97,
                )
            )
            new_logs.append(
                AgentThoughtLog(
                    id=f"th_{uuid.uuid4().hex[:8]}",
                    agent_id=lead_persona.id,
                    agent_name=lead_persona.name,
                    agent_role=lead_persona.role.value,
                    node_id=node.id,
                    phase=AgentThoughtPhase.SYNTHESIS,
                    message=f"Key molecular determinants identified: {', '.join(ident_data.get('genomic_mutations_detected', []))}",
                    confidence=0.96,
                )
            )
            new_artifacts["identification"] = ident_data
            node.outputs = ident_data

        elif node.category == NodeCategory.STRUCTURAL_BIOLOGY:
            protein_data = scenario_data.get("protein_targets", [])
            lead_vance = AGENT_PERSONAS["dr_vance"]
            new_logs.append(
                AgentThoughtLog(
                    id=f"th_{uuid.uuid4().hex[:8]}",
                    agent_id=lead_vance.id,
                    agent_name=lead_vance.name,
                    agent_role=lead_vance.role.value,
                    node_id=node.id,
                    phase=AgentThoughtPhase.OBSERVATION,
                    message=f"Extracted {len(protein_data)} functional targets from characterization outputs. Commencing AlphaFold inference.",
                    confidence=0.95,
                )
            )
            for p in protein_data:
                new_logs.append(
                    AgentThoughtLog(
                        id=f"th_{uuid.uuid4().hex[:8]}",
                        agent_id=lead_vance.id,
                        agent_name=lead_vance.name,
                        agent_role=lead_vance.role.value,
                        node_id=node.id,
                        phase=AgentThoughtPhase.TOOL_EXECUTION,
                        message=f"Resolved 3D conformation for target '{p.get('name')}'.",
                        tool_name="alphafold_structural_predictor",
                        tool_input={"target_id": p.get("id"), "sequence_length": p.get("sequence_length")},
                        tool_output_summary=f"pLDDT: {p.get('plddt_confidence')}, Active Pocket: {p.get('pocket_volume_angstrom3')} Å³, Druggability: {p.get('druggability_score')}",
                        confidence=0.96,
                    )
                )
            new_artifacts["protein_targets"] = protein_data
            node.outputs = {"targets_resolved": len(protein_data), "top_target": protein_data[0].get("name") if protein_data else None}

        elif node.category == NodeCategory.THERAPEUTICS:
            drug_data = scenario_data.get("drug_candidates", [])
            lead_sharma = AGENT_PERSONAS["dr_sharma"]
            new_logs.append(
                AgentThoughtLog(
                    id=f"th_{uuid.uuid4().hex[:8]}",
                    agent_id=lead_sharma.id,
                    agent_name=lead_sharma.name,
                    agent_role=lead_sharma.role.value,
                    node_id=node.id,
                    phase=AgentThoughtPhase.OBSERVATION,
                    message="Querying approved chemical libraries and ARTG register for high-affinity candidate molecules.",
                    confidence=0.92,
                )
            )
            for d in drug_data:
                new_logs.append(
                    AgentThoughtLog(
                        id=f"th_{uuid.uuid4().hex[:8]}",
                        agent_id=lead_sharma.id,
                        agent_name=lead_sharma.name,
                        agent_role=lead_sharma.role.value,
                        node_id=node.id,
                        phase=AgentThoughtPhase.TOOL_EXECUTION,
                        message=f"Virtual docking for '{d.get('name')}' against catalytic pocket.",
                        tool_name="autodock_vina_screener",
                        tool_input={"molecule": d.get("name"), "target": d.get("target_protein_id")},
                        tool_output_summary=f"Binding Affinity: {d.get('binding_affinity_kcal_mol')} kcal/mol, TGA: {d.get('tga_artg_status')}, NMS: {d.get('australian_stockpile_status')}",
                        confidence=0.95,
                    )
                )
            new_artifacts["drug_candidates"] = drug_data
            node.outputs = {"candidates_screened": len(drug_data), "lead_candidate": drug_data[0].get("name") if drug_data else None}

        elif node.category == NodeCategory.VACCINOLOGY:
            vac_data = scenario_data.get("vaccine_candidates", [])
            lead_oconnor = AGENT_PERSONAS["dr_oconnor"]
            new_logs.append(
                AgentThoughtLog(
                    id=f"th_{uuid.uuid4().hex[:8]}",
                    agent_id=lead_oconnor.id,
                    agent_name=lead_oconnor.name,
                    agent_role=lead_oconnor.role.value,
                    node_id=node.id,
                    phase=AgentThoughtPhase.OBSERVATION,
                    message="Scanning surface protein interfaces for conserved neutralizing epitopes.",
                    confidence=0.93,
                )
            )
            for v in vac_data:
                new_logs.append(
                    AgentThoughtLog(
                        id=f"th_{uuid.uuid4().hex[:8]}",
                        agent_id=lead_oconnor.id,
                        agent_name=lead_oconnor.name,
                        agent_role=lead_oconnor.role.value,
                        node_id=node.id,
                        phase=AgentThoughtPhase.TOOL_EXECUTION,
                        message=f"Formulated {v.get('platform')} candidate targeting '{v.get('target_antigen')}'.",
                        tool_name="mrna_construct_optimizer",
                        tool_input={"antigen": v.get("target_antigen"), "platform": v.get("platform")},
                        tool_output_summary=f"Titer: {v.get('predicted_neutralization_titer')}, Facility: {v.get('local_manufacturing_capability')}",
                        confidence=0.94,
                    )
                )
            new_artifacts["vaccine_candidates"] = vac_data
            node.outputs = {"vaccine_designs": len(vac_data), "lead_platform": vac_data[0].get("platform") if vac_data else None}

        elif node.category == NodeCategory.BIOSECURITY:
            threat_data = scenario_data.get("threat_assessment", {})
            lead_sterling = AGENT_PERSONAS["cdr_sterling"]
            new_logs.append(
                AgentThoughtLog(
                    id=f"th_{uuid.uuid4().hex[:8]}",
                    agent_id=lead_sterling.id,
                    agent_name=lead_sterling.name,
                    agent_role=lead_sterling.role.value,
                    node_id=node.id,
                    phase=AgentThoughtPhase.HYPOTHESIS,
                    message="Evaluating biological/chemical security classification under National Health Security Act 2007.",
                    confidence=0.96,
                )
            )
            new_logs.append(
                AgentThoughtLog(
                    id=f"th_{uuid.uuid4().hex[:8]}",
                    agent_id=lead_sterling.id,
                    agent_name=lead_sterling.name,
                    agent_role=lead_sterling.role.value,
                    node_id=node.id,
                    phase=AgentThoughtPhase.TOOL_EXECUTION,
                    message="Conducted dual-use and aerosol hazard audit.",
                    tool_name="ssba_regulatory_classifier",
                    tool_input={"signatures": threat_data.get("gain_of_function_signatures", [])},
                    tool_output_summary=f"Classification: {threat_data.get('ssba_tier')}, Containment: {threat_data.get('containment_level_required')}, Dual-Use Concern: {threat_data.get('dual_use_concern_rating')}",
                    confidence=0.98,
                )
            )
            new_artifacts["threat_assessment"] = threat_data
            node.outputs = threat_data

        elif node.category == NodeCategory.AGENCY_REPORTING:
            lead_bradley = AGENT_PERSONAS["alison_bradley"]
            new_logs.append(
                AgentThoughtLog(
                    id=f"th_{uuid.uuid4().hex[:8]}",
                    agent_id=lead_bradley.id,
                    agent_name=lead_bradley.name,
                    agent_role=lead_bradley.role.value,
                    node_id=node.id,
                    phase=AgentThoughtPhase.OBSERVATION,
                    message="Compiling cross-disciplinary findings into Whole-of-Australian-Government situational briefings.",
                    confidence=0.97,
                )
            )
            # Synthesize reports using blackboard + new_artifacts
            merged_context = {**blackboard, **new_artifacts}
            reports = AgencyReportGenerator.generate_all_reports(
                incident_name=scenario_data.get("name", "Active Incident"),
                threat_type=str(scenario_data.get("threat_type", "Biological")),
                artifacts=merged_context,
            )
            new_logs.append(
                AgentThoughtLog(
                    id=f"th_{uuid.uuid4().hex[:8]}",
                    agent_id=lead_bradley.id,
                    agent_name=lead_bradley.name,
                    agent_role=lead_bradley.role.value,
                    node_id=node.id,
                    phase=AgentThoughtPhase.TOOL_EXECUTION,
                    message=f"Generated {len(reports)} agency-specific briefings for ACDC, TGA, DAFF, DSTG, NEMA, DFAT, CSIRO, and OGTR.",
                    tool_name="woag_brief_synthesizer",
                    tool_input={"agencies": [a.value for a in reports.keys()]},
                    tool_output_summary="All briefings generated with statutory citations and actionable recommendations.",
                    confidence=0.99,
                )
            )
            new_artifacts["agency_reports"] = {a.value: rep.model_dump() for a, rep in reports.items()}
            node.outputs = {"briefings_dispatched": len(reports), "agencies_notified": [a.value for a in reports.keys()]}

        else:
            # Custom or generic node
            new_logs.append(
                AgentThoughtLog(
                    id=f"th_{uuid.uuid4().hex[:8]}",
                    agent_id=lead_persona.id,
                    agent_name=lead_persona.name,
                    agent_role=lead_persona.role.value,
                    node_id=node.id,
                    phase=AgentThoughtPhase.TOOL_EXECUTION,
                    message=f"Executed custom processing step '{node.label}'.",
                    confidence=0.90,
                )
            )
            node.outputs = {"status": "success", "executed_at": datetime.utcnow().isoformat()}

        elapsed_ms = (time.time() - start_time) * 1000
        node.status = NodeStatus.COMPLETED
        node.latency_ms = round(elapsed_ms, 2)

        return node, new_logs, new_artifacts

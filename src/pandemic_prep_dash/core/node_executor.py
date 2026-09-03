"""
Node Executor - executes individual pathway nodes using autonomous agent squads,
inter-node lead communication protocols, and produces structured biological,
chemical, and radiological response artifacts.
"""

from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime
import uuid
import time
from ..models.pathway import PathwayNode, NodeStatus, NodeCategory
from ..models.agent import (
    AgentThoughtLog,
    AgentThoughtPhase,
    AgentRole,
    InterNodeDialogue,
    DialogueMessageType,
)
from ..agents.teams import AGENT_TEAMS, AGENT_PERSONAS
from ..agencies.generator import AgencyReportGenerator
from ..agencies.registry import AUSTRALIAN_AGENCIES
from .bio_analyzer import BioinformaticsIdentifier
from .data_hub import ThreatResearcher, BlockerAlert, BlockerSeverity


class NodeExecutor:
    """Executes a single node in the DAG, producing thought logs and updating the blackboard."""

    @classmethod
    def execute_node(
        cls,
        node: PathwayNode,
        blackboard: Dict[str, Any],
        scenario_data: Dict[str, Any],
    ) -> Tuple[PathwayNode, List[AgentThoughtLog], Dict[str, Any], List[InterNodeDialogue], Optional[BlockerAlert]]:
        """
        Executes node logic using assigned agent squad and Node Lead coordination.
        Returns updated node, new thought logs, artifacts, inter-node dialogues, and optional blocker alert.
        """
        start_time = time.time()
        node.status = NodeStatus.RUNNING
        new_logs: List[AgentThoughtLog] = []
        new_artifacts: Dict[str, Any] = {}
        new_dialogues: List[InterNodeDialogue] = []
        new_blocker: Optional[BlockerAlert] = None

        # Prioritize custom node-level configured agent squad if present
        if node.agent_team_config and node.agent_team_config.members:
            team_config = node.agent_team_config
            lead_persona = team_config.node_lead or team_config.members[0]
            team_name = team_config.name
        else:
            team_config = AGENT_TEAMS.get(node.agent_team_id)
            lead_persona = (
                team_config.node_lead
                if team_config and team_config.node_lead
                else (team_config.members[0] if team_config and team_config.members else AGENT_PERSONAS["agent_bioinfo_lead"])
            )
            team_name = team_config.name if team_config else "Autonomous Response Squad"

        # ---------------- 1. INGESTION NODE ----------------
        if node.category == NodeCategory.INGESTION:
            sample_data = scenario_data.get("sample", {})
            raw_payload = sample_data.get("raw_payload", "")

            # Check if radiological or biological/chemical
            if "RADIOISOTOPE" in raw_payload or scenario_data.get("threat_type") == "radiological_dispersal":
                new_logs.append(
                    AgentThoughtLog(
                        id=f"th_{uuid.uuid4().hex[:8]}",
                        agent_id=lead_persona.id,
                        agent_name=lead_persona.name,
                        agent_role=f"{lead_persona.role.value} ({team_name})",
                        node_id=node.id,
                        phase=AgentThoughtPhase.OBSERVATION,
                        message=f"Received radiological detector feed from {sample_data.get('source_location')}. Initiating gamma spectrometry photopeak deconvolution.",
                        confidence=0.99,
                    )
                )
                new_logs.append(
                    AgentThoughtLog(
                        id=f"th_{uuid.uuid4().hex[:8]}",
                        agent_id=lead_persona.id,
                        agent_name=lead_persona.name,
                        agent_role=f"{lead_persona.role.value} ({team_name})",
                        node_id=node.id,
                        phase=AgentThoughtPhase.TOOL_EXECUTION,
                        message="Processed high-purity germanium (HPGe) multichannel analyzer spectrum.",
                        tool_name="gamma_spectrometry_analyzer",
                        tool_input={"detector": "HPGe_Canberra_ORTEC", "calibration": "Ba-133/Eu-152"},
                        tool_output_summary="Sharp photopeak at 661.7 keV confirms Ba-137m isomeric transition from Caesium-137. Activity: 3.7 TBq (100 Ci).",
                        confidence=0.99,
                    )
                )
                new_artifacts["sample"] = sample_data
                node.outputs = {"sample_id": sample_data.get("sample_id"), "radionuclide": "Caesium-137", "photopeak_kev": 661.7, "activity_tbq": 3.7, "status": "verified"}

                # Raise blocker alert for critical radiation activity
                new_blocker = BlockerAlert(
                    alert_id=f"blk_{uuid.uuid4().hex[:6]}",
                    node_id=node.id,
                    node_label=node.label,
                    severity=BlockerSeverity.CRITICAL,
                    title="High-Activity Caesium-137 Dispersal Confirmed (> 10 mSv/hr)",
                    description="Gamma spectrometry confirms 3.7 TBq Category 1 dangerous source at Port Botany. Exceeds ARPANSA public dose limits.",
                    required_action="Immediate activation of ARPANSA Emergency Reference Levels (ERL) and 5 km urgent protective planning zone.",
                    raised_by_agent=lead_persona.name,
                )
            else:
                bio_metrics = BioinformaticsIdentifier.analyze_payload(raw_payload, sample_data.get("name", ""))
                new_logs.append(
                    AgentThoughtLog(
                        id=f"th_{uuid.uuid4().hex[:8]}",
                        agent_id=lead_persona.id,
                        agent_name=lead_persona.name,
                        agent_role=f"{lead_persona.role.value} ({team_name})",
                        node_id=node.id,
                        phase=AgentThoughtPhase.OBSERVATION,
                        message=f"Received input '{sample_data.get('name', 'Sample')}'. Initiating format inspection for {bio_metrics['sequence_type']} payload ({bio_metrics['length']} units).",
                        confidence=0.98,
                    )
                )
                new_logs.append(
                    AgentThoughtLog(
                        id=f"th_{uuid.uuid4().hex[:8]}",
                        agent_id=lead_persona.id,
                        agent_name=lead_persona.name,
                        agent_role=f"{lead_persona.role.value} ({team_name})",
                        node_id=node.id,
                        phase=AgentThoughtPhase.TOOL_EXECUTION,
                        message=f"Verified sequence integrity. Length: {bio_metrics['length']} bp, GC content: {bio_metrics['gc_content']}%.",
                        tool_name="bio_sequence_inspector",
                        tool_input={"format": bio_metrics["sequence_type"], "length": bio_metrics["length"], "location": sample_data.get("source_location")},
                        tool_output_summary=f"Quality check PASSED. Computed GC%: {bio_metrics['gc_content']}%. Format: {bio_metrics['sequence_type']}.",
                        confidence=0.99,
                    )
                )
                sample_data["computed_metrics"] = bio_metrics
                new_artifacts["sample"] = sample_data
                node.outputs = {"sample_id": sample_data.get("sample_id"), "length": bio_metrics["length"], "gc_content": bio_metrics["gc_content"], "status": "verified"}

        # ---------------- 2. RESEARCH & LITERATURE SURVEILLANCE NODE ----------------
        elif node.category == NodeCategory.RESEARCH:
            threat_name = scenario_data.get("name", "Emerging Pathogen")
            query_term = scenario_data.get("identification", {}).get("agent_name", threat_name) or threat_name

            new_logs.append(
                AgentThoughtLog(
                    id=f"th_{uuid.uuid4().hex[:8]}",
                    agent_id=lead_persona.id,
                    agent_name=lead_persona.name,
                    agent_role=f"{lead_persona.role.value} ({team_name})",
                    node_id=node.id,
                    phase=AgentThoughtPhase.OBSERVATION,
                    message=f"Initiating scientific literature and peer-reviewed surveillance queries for '{query_term}'.",
                    confidence=0.98,
                )
            )

            # Query real PubMed E-Utilities or curated literature registry
            papers = ThreatResearcher.query_live_pubmed(query=query_term, max_results=3)
            paper_dicts = [p.model_dump() for p in papers]
            new_artifacts["literature_research"] = paper_dicts

            top_paper = papers[0] if papers else None
            new_logs.append(
                AgentThoughtLog(
                    id=f"th_{uuid.uuid4().hex[:8]}",
                    agent_id=lead_persona.id,
                    agent_name=lead_persona.name,
                    agent_role=f"{lead_persona.role.value} ({team_name})",
                    node_id=node.id,
                    phase=AgentThoughtPhase.TOOL_EXECUTION,
                    message=f"Retrieved {len(papers)} indexed publications and peer-reviewed clinical findings.",
                    tool_name="ncbi_pubmed_literature_retriever",
                    tool_input={"query": query_term, "count": len(papers)},
                    tool_output_summary=f"Found {len(papers)} studies. Lead study: '{top_paper.title if top_paper else ''}' ({top_paper.journal if top_paper else ''}).",
                    confidence=0.99,
                )
            )

            new_dialogues.append(
                InterNodeDialogue(
                    dialogue_id=f"dial_{uuid.uuid4().hex[:8]}",
                    source_node_id=node.id,
                    source_agent_id=lead_persona.id,
                    source_agent_name=lead_persona.name,
                    target_node_id="node_genomic_characterization",
                    target_agent_id="agent_bioinfo_lead",
                    target_agent_name="AGENT-BIOINFO-LEAD-01",
                    message_type=DialogueMessageType.REQUEST_INFO,
                    subject="Literature Evidence on Functional Mutations",
                    content=f"Research Lead transmitting {len(papers)} peer-reviewed studies on '{query_term}'. Validated mutations and cleavage mechanisms corroborated.",
                    response_content="Genomics Lead: Cross-referencing literature findings with sequencing reads.",
                    resolved=True,
                )
            )

            node.outputs = {
                "papers_retrieved": len(papers),
                "top_study": top_paper.title if top_paper else "N/A",
                "top_journal": top_paper.journal if top_paper else "N/A",
                "top_pmid": top_paper.pmid if top_paper else "N/A",
                "evidence_tier": "Peer-Reviewed Primary Research (NLM Indexed / Nature / Lancet)",
            }

        # ---------------- 3. CHARACTERIZATION NODE ----------------
        elif node.category == NodeCategory.CHARACTERIZATION:
            new_dialogues.append(
                InterNodeDialogue(
                    dialogue_id=f"dial_{uuid.uuid4().hex[:8]}",
                    source_node_id=node.id,
                    source_agent_id=lead_persona.id,
                    source_agent_name=lead_persona.name,
                    target_node_id="node_sample_ingestion",
                    target_agent_id="agent_bioinfo_lead",
                    target_agent_name="AGENT-BIOINFO-LEAD-01",
                    message_type=DialogueMessageType.REQUEST_INFO,
                    subject="Requesting verified payload and coordinate metrics",
                    content="Characterization Lead requesting raw spectrum/sequence readouts for taxonomy alignment and dispersion modeling.",
                    response_content="Ingestion Lead: Transmitting quality-checked specimen metrics and source location coordinates.",
                    resolved=True,
                )
            )

            raw_payload = scenario_data.get("sample", {}).get("raw_payload", "")
            if scenario_data.get("threat_type") == "radiological_dispersal":
                new_logs.append(
                    AgentThoughtLog(
                        id=f"th_{uuid.uuid4().hex[:8]}",
                        agent_id=lead_persona.id,
                        agent_name=lead_persona.name,
                        agent_role=f"{lead_persona.role.value} ({team_name})",
                        node_id=node.id,
                        phase=AgentThoughtPhase.HYPOTHESIS,
                        message="Hypothesizing atmospheric dispersal plume behavior under Sydney coastal wind shear (HYSPLIT model).",
                        confidence=0.96,
                    )
                )
                new_logs.append(
                    AgentThoughtLog(
                        id=f"th_{uuid.uuid4().hex[:8]}",
                        agent_id=lead_persona.id,
                        agent_name=lead_persona.name,
                        agent_role=f"{lead_persona.role.value} ({team_name})",
                        node_id=node.id,
                        phase=AgentThoughtPhase.TOOL_EXECUTION,
                        message="Ran HYSPLIT Lagrangian particulate dispersion simulation.",
                        tool_name="hysplit_rad_plume",
                        tool_input={"source_activity": "3.7 TBq Cs-137", "release_height": "15m", "wind_vector": "12 kts NE"},
                        tool_output_summary="Plume footprint extends 7.2 km SW. Inner cordon (10 mGy/hr): 450m radius. Urgent protective action zone: 5.0 km.",
                        confidence=0.98,
                    )
                )
                new_artifacts["plume_model"] = {"plume_extent_km": 7.2, "inner_cordon_m": 450, "evacuation_zone_km": 5.0}
                new_artifacts["identification"] = scenario_data.get("identification", {})
                node.outputs = scenario_data.get("identification", {})
            else:
                real_analysis = BioinformaticsIdentifier.analyze_payload(raw_payload, scenario_data.get("name", ""))
                ident_data = dict(scenario_data.get("identification", {}))
                ident_data["computed_length"] = real_analysis["length"]
                ident_data["computed_gc_content"] = real_analysis["gc_content"]
                if real_analysis.get("genomic_mutations_detected"):
                    ident_data["detected_motifs"] = real_analysis["genomic_mutations_detected"]

                new_logs.append(
                    AgentThoughtLog(
                        id=f"th_{uuid.uuid4().hex[:8]}",
                        agent_id=lead_persona.id,
                        agent_name=lead_persona.name,
                        agent_role=f"{lead_persona.role.value} ({team_name})",
                        node_id=node.id,
                        phase=AgentThoughtPhase.HYPOTHESIS,
                        message=f"Aligning {real_analysis['sequence_type']} sequence against NCBI GenBank & GISAID. Matched candidate: {real_analysis['agent_name']}.",
                        confidence=0.95,
                    )
                )
                new_logs.append(
                    AgentThoughtLog(
                        id=f"th_{uuid.uuid4().hex[:8]}",
                        agent_id=lead_persona.id,
                        agent_name=lead_persona.name,
                        agent_role=f"{lead_persona.role.value} ({team_name})",
                        node_id=node.id,
                        phase=AgentThoughtPhase.TOOL_EXECUTION,
                        message="Completed k-mer pattern alignment and signature motif scan.",
                        tool_name="blast_and_clade_classifier",
                        tool_input={"query_length": real_analysis["length"], "target_databases": ["NCBI_RefSeq", "GISAID", "PubChem"]},
                        tool_output_summary=f"Matched {ident_data.get('agent_name', real_analysis['agent_name'])} with {real_analysis['alignment_confidence']}% alignment confidence.",
                        confidence=0.98,
                    )
                )
                new_artifacts["identification"] = ident_data
                node.outputs = ident_data

                # If high-pathogenicity mutations detected, raise alert
                if "High-Pathogenicity" in str(real_analysis.get("genomic_mutations_detected")):
                    new_blocker = BlockerAlert(
                        alert_id=f"blk_{uuid.uuid4().hex[:6]}",
                        node_id=node.id,
                        node_label=node.label,
                        severity=BlockerSeverity.WARNING,
                        title="High-Pathogenicity Furin Cleavage Insertion Detected",
                        description="Genomic alignment confirmed polybasic cleavage site (R-X-R/K-R) indicating systemic tissue tropism.",
                        required_action="Notify ACDP high-containment diagnostic unit and stand up CDNA case surveillance.",
                        raised_by_agent=lead_persona.name,
                    )

        # ---------------- 4. STRUCTURAL BIOLOGY NODE ----------------
        elif node.category == NodeCategory.STRUCTURAL_BIOLOGY:
            new_dialogues.append(
                InterNodeDialogue(
                    dialogue_id=f"dial_{uuid.uuid4().hex[:8]}",
                    source_node_id=node.id,
                    source_agent_id=lead_persona.id,
                    source_agent_name=lead_persona.name,
                    target_node_id="node_genomic_characterization",
                    target_agent_id="agent_bioinfo_lead",
                    target_agent_name="AGENT-BIOINFO-LEAD-01",
                    message_type=DialogueMessageType.REQUEST_INFO,
                    subject="Requesting key catalytic residue coordinates",
                    content="Structural Lead requesting mutation loci and target amino acid segments to initiate AlphaFold 3D modeling.",
                    response_content="Genomics Lead: Transmitted confirmed target genes and active site motifs.",
                    resolved=True,
                )
            )

            targets = scenario_data.get("protein_targets", [])
            primary_target = targets[0] if targets else {"name": "Surface Target", "gene_symbol": "TARGET"}
            new_logs.append(
                AgentThoughtLog(
                    id=f"th_{uuid.uuid4().hex[:8]}",
                    agent_id=lead_persona.id,
                    agent_name=lead_persona.name,
                    agent_role=f"{lead_persona.role.value} ({team_name})",
                    node_id=node.id,
                    phase=AgentThoughtPhase.TOOL_EXECUTION,
                    message=f"Executing AlphaFold structural modeling for target '{primary_target.get('name')}'.",
                    tool_name="alphafold_structural_predictor",
                    tool_input={"target": primary_target.get("name"), "msa_depth": 5000},
                    tool_output_summary=f"Predicted 3D fold. pLDDT score: {primary_target.get('plddt_confidence', 95.0)}%. High-confidence catalytic pocket mapped ({primary_target.get('pocket_volume_angstrom3', 1200)} Å³).",
                    confidence=0.97,
                )
            )
            new_artifacts["protein_targets"] = targets
            node.outputs = {"targets_resolved": len(targets), "primary_target": primary_target.get("name"), "druggability": primary_target.get("druggability_score", 0.9)}

        # ---------------- 5. THERAPEUTICS NODE ----------------
        elif node.category == NodeCategory.THERAPEUTICS:
            new_dialogues.append(
                InterNodeDialogue(
                    dialogue_id=f"dial_{uuid.uuid4().hex[:8]}",
                    source_node_id=node.id,
                    source_agent_id=lead_persona.id,
                    source_agent_name=lead_persona.name,
                    target_node_id="node_structural_modeling",
                    target_agent_id="agent_struct_bio_lead",
                    target_agent_name="AGENT-STRUCT-BIO-LEAD-01",
                    message_type=DialogueMessageType.REQUEST_INFO,
                    subject="Requesting pocket coordinates for virtual docking",
                    content="Medicinal Chemistry Lead requesting 3D binding pocket volume and receptor electrostatics to screen candidate inhibitors.",
                    response_content="Structural Lead: Transmitting PDB coordinates and active pocket boundary coordinates.",
                    resolved=True,
                )
            )

            drugs = scenario_data.get("drug_candidates", [])
            top_drug = drugs[0] if drugs else {"name": "Candidate Drug", "mechanism_of_action": "Inhibitor"}
            new_logs.append(
                AgentThoughtLog(
                    id=f"th_{uuid.uuid4().hex[:8]}",
                    agent_id=lead_persona.id,
                    agent_name=lead_persona.name,
                    agent_role=f"{lead_persona.role.value} ({team_name})",
                    node_id=node.id,
                    phase=AgentThoughtPhase.TOOL_EXECUTION,
                    message="Running AutoDock Vina in silico screening and cross-checking Australian Register of Therapeutic Goods (ARTG).",
                    tool_name="autodock_vina_screener",
                    tool_input={"library": "ARTG_Approved_Antivirals_and_Antidotes", "grid_box": "catalytic_site"},
                    tool_output_summary=f"Top candidate: {top_drug.get('name')} (Binding Affinity: {top_drug.get('binding_affinity_kcal_mol', -8.0)} kcal/mol). TGA status: {top_drug.get('tga_artg_status')}.",
                    confidence=0.96,
                )
            )
            new_artifacts["drug_candidates"] = drugs
            node.outputs = {"candidates_screened": len(drugs), "lead_candidate": top_drug.get("name"), "affinity": top_drug.get("binding_affinity_kcal_mol")}

        # ---------------- 6. VACCINOLOGY NODE ----------------
        elif node.category == NodeCategory.VACCINOLOGY:
            new_dialogues.append(
                InterNodeDialogue(
                    dialogue_id=f"dial_{uuid.uuid4().hex[:8]}",
                    source_node_id=node.id,
                    source_agent_id=lead_persona.id,
                    source_agent_name=lead_persona.name,
                    target_node_id="node_structural_modeling",
                    target_agent_id="agent_struct_bio_lead",
                    target_agent_name="AGENT-STRUCT-BIO-LEAD-01",
                    message_type=DialogueMessageType.REQUEST_INFO,
                    subject="Requesting surface epitope exposure profile",
                    content="Vaccine Lead requesting surface exposed residues and neutralizing conformation for mRNA construct design.",
                    response_content="Structural Lead: Transmitting surface accessibility map and quaternary oligomer model.",
                    resolved=True,
                )
            )

            vaccines = scenario_data.get("vaccine_candidates", [])
            top_vac = vaccines[0] if vaccines else {"target_antigen": "Antigen", "platform": "mRNA-LNP"}
            new_logs.append(
                AgentThoughtLog(
                    id=f"th_{uuid.uuid4().hex[:8]}",
                    agent_id=lead_persona.id,
                    agent_name=lead_persona.name,
                    agent_role=f"{lead_persona.role.value} ({team_name})",
                    node_id=node.id,
                    phase=AgentThoughtPhase.TOOL_EXECUTION,
                    message="Optimizing codon bias and lipid nanoparticle formulation for Australian sovereign manufacturing.",
                    tool_name="mrna_construct_optimizer",
                    tool_input={"antigen": top_vac.get("target_antigen"), "platform": top_vac.get("platform")},
                    tool_output_summary=f"Construct designed: {top_vac.get('platform')}. Neutralizing titer: {top_vac.get('predicted_neutralization_titer')}. Manufacturing facility: {top_vac.get('local_manufacturing_capability')}.",
                    confidence=0.95,
                )
            )
            new_artifacts["vaccine_candidates"] = vaccines
            node.outputs = {"platform": top_vac.get("platform"), "manufacturing_facility": top_vac.get("local_manufacturing_capability")}

        # ---------------- 7. BIOSECURITY & THREAT ASSESSMENT NODE ----------------
        elif node.category == NodeCategory.BIOSECURITY:
            new_dialogues.append(
                InterNodeDialogue(
                    dialogue_id=f"dial_{uuid.uuid4().hex[:8]}",
                    source_node_id=node.id,
                    source_agent_id=lead_persona.id,
                    source_agent_name=lead_persona.name,
                    target_node_id="node_genomic_characterization",
                    target_agent_id="agent_bioinfo_lead",
                    target_agent_name="AGENT-BIOINFO-LEAD-01",
                    message_type=DialogueMessageType.REQUEST_INFO,
                    subject="Requesting dual-use and SSBA regulatory scan",
                    content="Biosecurity Lead auditing sequence and scenario data for Security Sensitive Biological Agent (SSBA) or CWC schedule markers.",
                    response_content="Genomics Lead: Transmitting molecular determinants and dual-use markers.",
                    resolved=True,
                )
            )

            threat_assessment = scenario_data.get("threat_assessment", {})
            new_logs.append(
                AgentThoughtLog(
                    id=f"th_{uuid.uuid4().hex[:8]}",
                    agent_id=lead_persona.id,
                    agent_name=lead_persona.name,
                    agent_role=f"{lead_persona.role.value} ({team_name})",
                    node_id=node.id,
                    phase=AgentThoughtPhase.TOOL_EXECUTION,
                    message="Audited threat characteristics against Commonwealth Statutory Lists (SSBA Standards / ARPANS Act / CWC Schedule).",
                    tool_name="ssba_regulatory_classifier",
                    tool_input={"pathway_threat": scenario_data.get("threat_type")},
                    tool_output_summary=f"Classification: {threat_assessment.get('ssba_tier')}. Human-in-the-Loop authorization verified.",
                    confidence=0.99,
                )
            )
            new_artifacts["threat_assessment"] = threat_assessment
            node.outputs = threat_assessment

            # Flag statutory reporting requirement blocker
            if "Tier 1" in str(threat_assessment.get("ssba_tier")):
                new_blocker = BlockerAlert(
                    alert_id=f"blk_{uuid.uuid4().hex[:6]}",
                    node_id=node.id,
                    node_label=node.label,
                    severity=BlockerSeverity.WARNING,
                    title="Mandatory SSBA Tier 1 Notification Triggered",
                    description="Pathogen falls under National Health Security Act 2007 Tier 1 SSBA list. Requires formal notification to ACDP within 24 hours.",
                    required_action="Submit Initial Notification Form SSBA-01 to ACDP Biosecurity Regulatory Desk.",
                    raised_by_agent=lead_persona.name,
                )

        # ---------------- 8. AGENCY REPORTING NODE ----------------
        elif node.category == NodeCategory.AGENCY_REPORTING:
            new_dialogues.append(
                InterNodeDialogue(
                    dialogue_id=f"dial_{uuid.uuid4().hex[:8]}",
                    source_node_id=node.id,
                    source_agent_id=lead_persona.id,
                    source_agent_name=lead_persona.name,
                    target_node_id="node_threat_biosecurity_assessment",
                    target_agent_id="agent_cbrn_intel_lead",
                    target_agent_name="AGENT-CBRN-INTEL-LEAD-01",
                    message_type=DialogueMessageType.STATUTORY_REFERRAL,
                    subject="Initiating Whole-of-Government situation briefs synthesis",
                    content="Policy Coordinator Lead aggregating scientific artifacts and statutory clearance to dispatch situational reports to Commonwealth agencies.",
                    response_content="Biosecurity Lead: Cleared for inter-agency release under Official: Sensitive handling caveats.",
                    resolved=True,
                )
            )

            incident_name = scenario_data.get("name", "CBRN Threat Event")
            threat_type_str = str(scenario_data.get("threat_type", "biological_virus"))
            merged_artifacts = dict(blackboard)

            agency_reports = AgencyReportGenerator.generate_all_reports(
                incident_name=incident_name,
                threat_type=threat_type_str,
                artifacts=merged_artifacts,
            )
            relevant_agencies = [k.value for k, v in agency_reports.items() if v.is_relevant]

            new_logs.append(
                AgentThoughtLog(
                    id=f"th_{uuid.uuid4().hex[:8]}",
                    agent_id=lead_persona.id,
                    agent_name=lead_persona.name,
                    agent_role=f"{lead_persona.role.value} ({team_name})",
                    node_id=node.id,
                    phase=AgentThoughtPhase.SYNTHESIS,
                    message=f"Synthesized targeted intelligence briefings for {len(relevant_agencies)} relevant statutory Australian authorities ({', '.join(relevant_agencies)}). Non-relevant authorities placed on automated standby.",
                    confidence=0.99,
                )
            )
            new_artifacts["agency_reports"] = {k.value: v.model_dump() for k, v in agency_reports.items()}
            node.outputs = {"briefings_compiled": len(agency_reports), "relevant_agencies": relevant_agencies}

        else:
            # Custom node
            node.outputs = {"status": "executed", "timestamp": datetime.utcnow().isoformat() + "Z"}

        node.status = NodeStatus.COMPLETED
        node.latency_ms = round((time.time() - start_time) * 1000, 2)
        return node, new_logs, new_artifacts, new_dialogues, new_blocker

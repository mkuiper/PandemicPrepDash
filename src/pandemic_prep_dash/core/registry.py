"""
Pathway registry and default templates for Biological and Chemical response pathways.
Includes real scientific literature research nodes and targeted agency briefings.
"""

from typing import Dict
from ..models.pathway import Pathway, PathwayNode, PathwayEdge, NodeCategory, NodeStatus
from ..models.bio_chem import ThreatType


def create_default_biological_pathway() -> Pathway:
    """Creates the default multi-branch agentic pathway for biological threats."""
    nodes = [
        PathwayNode(
            id="node_sample_ingestion",
            label="Sample & Sequence Ingestion",
            category=NodeCategory.INGESTION,
            description="Ingests FASTA/FASTQ nucleotide sequences, verifies read quality, parses origin metadata.",
            status=NodeStatus.PENDING,
            agent_team_id="bioinformatics_squad",
            human_oversight_role="ACDP Specimen Reception Officer",
            position_x=80.0,
            position_y=250.0,
        ),
        PathwayNode(
            id="node_literature_research",
            label="Threat Research & Scientific Surveillance",
            category=NodeCategory.RESEARCH,
            description="Queries PubMed, BioRxiv, and WHO databases for peer-reviewed studies and clinical evidence.",
            status=NodeStatus.PENDING,
            agent_team_id="research_squad",
            human_oversight_role="Public Health Intelligence Analyst",
            position_x=320.0,
            position_y=140.0,
        ),
        PathwayNode(
            id="node_genomic_characterization",
            label="Genomic Identification & Phylogenetics",
            category=NodeCategory.CHARACTERIZATION,
            description="Runs NCBI/GISAID BLAST, places pathogen in phylogenetic tree, calls signature mutations.",
            status=NodeStatus.PENDING,
            agent_team_id="bioinformatics_squad",
            human_oversight_role="ACDP Senior Genomicist",
            position_x=320.0,
            position_y=360.0,
        ),
        PathwayNode(
            id="node_structural_modeling",
            label="Protein Target & Structural Modeling",
            category=NodeCategory.STRUCTURAL_BIOLOGY,
            description="Runs AlphaFold structural inference, annotates active catalytic pockets, computes druggability index.",
            status=NodeStatus.PENDING,
            agent_team_id="structural_biology_squad",
            human_oversight_role="CSIRO Structural Biologist",
            position_x=580.0,
            position_y=160.0,
        ),
        PathwayNode(
            id="node_biosecurity_assessment",
            label="CBRN Threat & SSBA Assessment",
            category=NodeCategory.BIOSECURITY,
            description="Evaluates SSBA Tier 1/2 classification, screens for dual-use gain-of-function markers, assesses aerosolization.",
            status=NodeStatus.PENDING,
            agent_team_id="biosecurity_squad",
            requires_human_approval=True,  # Critical security gatekeeper!
            approval_granted=False,
            human_oversight_role="Commonwealth Biosecurity Gatekeeper Delegate",
            position_x=580.0,
            position_y=360.0,
        ),
        PathwayNode(
            id="node_therapeutic_screening",
            label="Therapeutic Repurposing & Docking",
            category=NodeCategory.THERAPEUTICS,
            description="Performs in silico docking against target pockets, cross-references TGA ARTG register & National Medical Stockpile.",
            status=NodeStatus.PENDING,
            agent_team_id="medicinal_chemistry_squad",
            human_oversight_role="TGA Clinical Evaluator",
            position_x=820.0,
            position_y=100.0,
        ),
        PathwayNode(
            id="node_vaccine_design",
            label="Epitope Mapping & Vaccine Design",
            category=NodeCategory.VACCINOLOGY,
            description="Predicts neutralizing B/T-cell epitopes, designs mRNA-LNP constructs, assesses domestic manufacturing (CSIRO/Moderna).",
            status=NodeStatus.PENDING,
            agent_team_id="vaccine_squad",
            human_oversight_role="National Vaccine Formulation Specialist",
            position_x=820.0,
            position_y=230.0,
        ),
        PathwayNode(
            id="node_agency_briefing_synthesis",
            label="Whole-of-Government Agency Briefings",
            category=NodeCategory.AGENCY_REPORTING,
            description="Synthesizes and dispatches tailored situational reports to relevant statutory agencies (ACDP, TGA, DAFF, NEMA, DFAT).",
            status=NodeStatus.PENDING,
            agent_team_id="policy_squad",
            human_oversight_role="Crisis Policy Liaison Director",
            position_x=1080.0,
            position_y=250.0,
        ),
    ]

    edges = [
        PathwayEdge(id="edge_1", source="node_sample_ingestion", target="node_literature_research", label="Threat Name Extracted"),
        PathwayEdge(id="edge_2", source="node_sample_ingestion", target="node_genomic_characterization", label="Quality Passed"),
        PathwayEdge(id="edge_3", source="node_genomic_characterization", target="node_structural_modeling", label="Key Targets Identified"),
        PathwayEdge(id="edge_4", source="node_genomic_characterization", target="node_biosecurity_assessment", label="Pathogenicity Markers Flagged"),
        PathwayEdge(id="edge_5", source="node_structural_modeling", target="node_therapeutic_screening", label="Druggable Pockets Ready"),
        PathwayEdge(id="edge_6", source="node_structural_modeling", target="node_vaccine_design", label="Surface Antigen Trimer Resolved"),
        PathwayEdge(id="edge_7", source="node_therapeutic_screening", target="node_agency_briefing_synthesis", label="Candidates Ranked"),
        PathwayEdge(id="edge_8", source="node_vaccine_design", target="node_agency_briefing_synthesis", label="Formulation Ready"),
        PathwayEdge(id="edge_9", source="node_biosecurity_assessment", target="node_agency_briefing_synthesis", label="Threat Audited"),
        PathwayEdge(id="edge_10", source="node_literature_research", target="node_agency_briefing_synthesis", label="Evidence Corroborated"),
    ]

    return Pathway(
        id="pathway_default_biological",
        name="Whole-of-Government Biological Response Pathway",
        description="Standard adaptive DAG response pipeline for emerging viral, bacterial, and zoonotic pathogens.",
        threat_type=ThreatType.BIOLOGICAL_VIRUS,
        nodes=nodes,
        edges=edges,
    )


def create_default_chemical_pathway() -> Pathway:
    """Creates default response pathway for chemical toxins & nerve agents."""
    nodes = [
        PathwayNode(
            id="node_chem_sample_ingestion",
            label="Chemical Hazard & SMILES Ingestion",
            category=NodeCategory.INGESTION,
            description="Ingests GC-MS spectra, SMILES strings, and incident Hazmat sensor readings.",
            status=NodeStatus.PENDING,
            agent_team_id="bioinformatics_squad",
            human_oversight_role="Border HAZMAT Duty Officer",
            position_x=100.0,
            position_y=250.0,
        ),
        PathwayNode(
            id="node_chem_literature_research",
            label="Toxicology Research & Case Surveillance",
            category=NodeCategory.RESEARCH,
            description="Searches medical toxicology databases for aging kinetics, atropinization regimens, and oxime trials.",
            status=NodeStatus.PENDING,
            agent_team_id="research_squad",
            human_oversight_role="Poisons Information Consultant",
            position_x=340.0,
            position_y=140.0,
        ),
        PathwayNode(
            id="node_chem_structure_id",
            label="Molecular Fingerprinting & CWC Schedule",
            category=NodeCategory.CHARACTERIZATION,
            description="Evaluates SMILES/InChI, verifies Chemical Weapons Convention Schedule 1/2 criteria, models organophosphate aging kinetics.",
            status=NodeStatus.PENDING,
            agent_team_id="biosecurity_squad",
            human_oversight_role="ASNO CWC Verification Officer",
            position_x=340.0,
            position_y=360.0,
        ),
        PathwayNode(
            id="node_chem_target_docking",
            label="Enzyme Target (AChE) Docking & Reactivators",
            category=NodeCategory.THERAPEUTICS,
            description="Models human acetylcholinesterase phosphorylation cavity, screens oxime reactivators (Pralidoxime, Obidoxime, HI-6).",
            status=NodeStatus.PENDING,
            agent_team_id="medicinal_chemistry_squad",
            human_oversight_role="Clinical Toxicologist",
            position_x=640.0,
            position_y=180.0,
        ),
        PathwayNode(
            id="node_chem_containment_gate",
            label="CBRN Plume & Decontamination Signoff",
            category=NodeCategory.BIOSECURITY,
            description="Assesses volatile vapor pressure, downwind plume dispersion, hazmat PPE level, and municipal exclusion radius.",
            status=NodeStatus.PENDING,
            agent_team_id="biosecurity_squad",
            requires_human_approval=True,
            approval_granted=False,
            human_oversight_role="DSTG CBRN Commander & Police Hazmat Incident Controller",
            position_x=640.0,
            position_y=340.0,
        ),
        PathwayNode(
            id="node_chem_agency_reporting",
            label="Defence & HAZMAT SITREP Dispatch",
            category=NodeCategory.AGENCY_REPORTING,
            description="Issues immediate alerts to Defence/DSTG, NEMA Hazmat, TGA, and Home Affairs.",
            status=NodeStatus.PENDING,
            agent_team_id="policy_squad",
            human_oversight_role="Home Affairs Crisis Director",
            position_x=960.0,
            position_y=250.0,
        ),
    ]

    edges = [
        PathwayEdge(id="chem_edge_1", source="node_chem_sample_ingestion", target="node_chem_literature_research", label="Structure Parsed"),
        PathwayEdge(id="chem_edge_2", source="node_chem_sample_ingestion", target="node_chem_structure_id", label="Hazard Ingested"),
        PathwayEdge(id="chem_edge_3", source="node_chem_structure_id", target="node_chem_target_docking", label="Inhibitor Identified"),
        PathwayEdge(id="chem_edge_4", source="node_chem_structure_id", target="node_chem_containment_gate", label="Vapor Hazard Quantified"),
        PathwayEdge(id="chem_edge_5", source="node_chem_target_docking", target="node_chem_agency_reporting", label="Antidotes Stockpiled"),
        PathwayEdge(id="chem_edge_6", source="node_chem_containment_gate", target="node_chem_agency_reporting", label="Signoff Authorized"),
        PathwayEdge(id="chem_edge_7", source="node_chem_literature_research", target="node_chem_agency_reporting", label="Toxicology Corroborated"),
    ]

    return Pathway(
        id="pathway_default_chemical",
        name="Whole-of-Government Chemical / Nerve Agent Response Pathway",
        description="Rapid response DAG for organophosphate nerve agents, biological toxins (e.g. ricin, botulinum), and illicit synthetic agents.",
        threat_type=ThreatType.CHEMICAL_NERVE_AGENT,
        nodes=nodes,
        edges=edges,
    )


PATHWAY_TEMPLATES: Dict[str, Pathway] = {
    "pathway_default_biological": create_default_biological_pathway(),
    "pathway_default_chemical": create_default_chemical_pathway(),
}


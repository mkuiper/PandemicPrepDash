"""
Pathway registry and default templates for Biological and Chemical response pathways.
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
            position_x=100.0,
            position_y=250.0,
        ),
        PathwayNode(
            id="node_genomic_characterization",
            label="Genomic Identification & Phylogenetics",
            category=NodeCategory.CHARACTERIZATION,
            description="Runs NCBI/GISAID BLAST, places pathogen in phylogenetic tree, calls signature mutations.",
            status=NodeStatus.PENDING,
            agent_team_id="bioinformatics_squad",
            position_x=340.0,
            position_y=250.0,
        ),
        PathwayNode(
            id="node_structural_modeling",
            label="Protein Target & Structural Modeling",
            category=NodeCategory.STRUCTURAL_BIOLOGY,
            description="Runs AlphaFold structural inference, annotates active catalytic pockets, computes druggability index.",
            status=NodeStatus.PENDING,
            agent_team_id="structural_biology_squad",
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
            position_x=820.0,
            position_y=220.0,
        ),
        PathwayNode(
            id="node_agency_briefing_synthesis",
            label="Whole-of-Government Agency Briefings",
            category=NodeCategory.AGENCY_REPORTING,
            description="Synthesizes and dispatches tailored situational reports to ACDC, TGA, DAFF, DSTG, NEMA, DFAT.",
            status=NodeStatus.PENDING,
            agent_team_id="policy_squad",
            position_x=1060.0,
            position_y=250.0,
        ),
    ]

    edges = [
        PathwayEdge(id="edge_1", source="node_sample_ingestion", target="node_genomic_characterization", label="Quality Passed"),
        PathwayEdge(id="edge_2", source="node_genomic_characterization", target="node_structural_modeling", label="Key Targets Identified"),
        PathwayEdge(id="edge_3", source="node_genomic_characterization", target="node_biosecurity_assessment", label="Pathogenicity Markers Flagged"),
        PathwayEdge(id="edge_4", source="node_structural_modeling", target="node_therapeutic_screening", label="Druggable Pockets Ready"),
        PathwayEdge(id="edge_5", source="node_structural_modeling", target="node_vaccine_design", label="Surface Antigen Trimer Resolved"),
        PathwayEdge(id="edge_6", source="node_therapeutic_screening", target="node_agency_briefing_synthesis", label="Candidates Ranked"),
        PathwayEdge(id="edge_7", source="node_vaccine_design", target="node_agency_briefing_synthesis", label="Formulation Ready"),
        PathwayEdge(id="edge_8", source="node_biosecurity_assessment", target="node_agency_briefing_synthesis", label="Threat Audited"),
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
            position_x=100.0,
            position_y=250.0,
        ),
        PathwayNode(
            id="node_chem_characterization",
            label="Spectroscopic Identification & CWC Classification",
            category=NodeCategory.CHARACTERIZATION,
            description="Matches chemical fingerprint against CWC Schedule 1/2 registries, identifies chemical class.",
            status=NodeStatus.PENDING,
            agent_team_id="bioinformatics_squad",
            position_x=340.0,
            position_y=250.0,
        ),
        PathwayNode(
            id="node_chem_target_mechanism",
            label="Biochemical Target & Mechanism Analysis",
            category=NodeCategory.STRUCTURAL_BIOLOGY,
            description="Models human acetylcholinesterase/receptor covalent adducts and catalytic aging kinetics.",
            status=NodeStatus.PENDING,
            agent_team_id="structural_biology_squad",
            position_x=580.0,
            position_y=160.0,
        ),
        PathwayNode(
            id="node_chem_threat_intelligence",
            label="CBRN Threat & Counter-Terrorism Intelligence",
            category=NodeCategory.BIOSECURITY,
            description="Verifies OPCW schedule compliance, delivery vector hazard, and forensic attribution markers.",
            status=NodeStatus.PENDING,
            agent_team_id="biosecurity_squad",
            requires_human_approval=True,
            approval_granted=False,
            position_x=580.0,
            position_y=360.0,
        ),
        PathwayNode(
            id="node_chem_antidote_evaluation",
            label="Antidote & Oxime Reactivator Profiling",
            category=NodeCategory.THERAPEUTICS,
            description="Evaluates atropine / oxime reactivator efficacy, audits Defence & National Medical Stockpiles.",
            status=NodeStatus.PENDING,
            agent_team_id="medicinal_chemistry_squad",
            position_x=820.0,
            position_y=160.0,
        ),
        PathwayNode(
            id="node_chem_agency_reporting",
            label="Whole-of-Government CBRN Briefings",
            category=NodeCategory.AGENCY_REPORTING,
            description="Issues immediate alerts to Defence/DSTG, NEMA Hazmat, TGA, and ACDC.",
            status=NodeStatus.PENDING,
            agent_team_id="policy_squad",
            position_x=1060.0,
            position_y=250.0,
        ),
    ]

    edges = [
        PathwayEdge(id="chem_edge_1", source="node_chem_sample_ingestion", target="node_chem_characterization", label="Structure Validated"),
        PathwayEdge(id="chem_edge_2", source="node_chem_characterization", target="node_chem_target_mechanism", label="Toxin Class Confirmed"),
        PathwayEdge(id="chem_edge_3", source="node_chem_characterization", target="node_chem_threat_intelligence", label="CWC Schedule 1 Suspected"),
        PathwayEdge(id="chem_edge_4", source="node_chem_target_mechanism", target="node_chem_antidote_evaluation", label="Target Adduct Modeled"),
        PathwayEdge(id="chem_edge_5", source="node_chem_threat_intelligence", target="node_chem_agency_reporting", label="Security Verification"),
        PathwayEdge(id="chem_edge_6", source="node_chem_antidote_evaluation", target="node_chem_agency_reporting", label="Countermeasures Formulated"),
    ]

    return Pathway(
        id="pathway_default_chemical",
        name="Whole-of-Government Chemical/Toxin CBRN Response Pathway",
        description="Emergency DAG response pipeline for toxic chemicals, organophosphates, and novel nerve agents.",
        threat_type=ThreatType.CHEMICAL_NERVE_AGENT,
        nodes=nodes,
        edges=edges,
    )


PATHWAY_TEMPLATES: Dict[str, Pathway] = {
    "pathway_default_biological": create_default_biological_pathway(),
    "pathway_default_chemical": create_default_chemical_pathway(),
}

"""
Pre-configured Autonomous Synthetic Agent Personas and Teams for CBRN and Pandemic Response.
Complies with Australian AI Safety Institute (AISI) guidelines:
Strictly non-anthropomorphic, transparent functional designations.
"""

from typing import Dict, List
from ..models.agent import (
    AgentPersona,
    AgentRole,
    AgentTeamConfig,
    ModelProviderConfig,
    ModelProviderType,
)

AGENT_PERSONAS: Dict[str, AgentPersona] = {
    "agent_bioinfo_lead": AgentPersona(
        id="agent_bioinfo_lead",
        name="AGENT-BIOINFO-LEAD-01",
        role=AgentRole.BIOINFORMATICS_LEAD,
        avatar_icon="dna",
        is_node_lead=True,
        specialization="Viral Phylogenomics, Sequence Inspection & Variant Calling",
        system_prompt=(
            "You are AGENT-BIOINFO-LEAD-01, an autonomous bioinformatic agent assigned to lead genomics workflows. "
            "You inspect raw nucleotide/amino acid sequences, execute BLAST alignments, compute GC content, "
            "identify mutations, and detect pathogenicity determinants (e.g. furin cleavage sites, PB2 E627K)."
        ),
        tools=["blast_alignment", "phylogenetic_tree_builder", "mutation_scanner", "clade_classifier"],
        enabled_mcp_servers=["mcp-server-ncbi-blast", "mcp-server-gisaid"],
        enabled_aus_gov_skills=["AUS-SKILL-GENOMIC-SURVEILLANCE"],
    ),
    "agent_struct_bio_lead": AgentPersona(
        id="agent_struct_bio_lead",
        name="AGENT-STRUCT-BIO-LEAD-01",
        role=AgentRole.STRUCTURAL_BIOLOGIST,
        avatar_icon="atom",
        is_node_lead=True,
        specialization="Macromolecular 3D Modeling & Catalytic Pocket Profiling",
        system_prompt=(
            "You are AGENT-STRUCT-BIO-LEAD-01, an autonomous structural biology agent. You predict and evaluate "
            "3D protein structures using AlphaFold/ESMFold, calculate pLDDT confidence scores, detect catalytic "
            "binding pockets, and assess druggability."
        ),
        tools=["alphafold_structural_predictor", "fpocket_binding_detector", "surface_electrostatics_calculator"],
        enabled_mcp_servers=["mcp-server-alphafold-db", "mcp-server-rcsb-pdb"],
        enabled_aus_gov_skills=["AUS-SKILL-STRUCTURAL-TARGET-MODELING"],
    ),
    "agent_medchem_lead": AgentPersona(
        id="agent_medchem_lead",
        name="AGENT-MEDCHEM-LEAD-01",
        role=AgentRole.MEDICINAL_CHEMIST,
        avatar_icon="pill",
        is_node_lead=True,
        specialization="Therapeutic Repurposing, Virtual Docking & ARTG Verification",
        system_prompt=(
            "You are AGENT-MEDCHEM-LEAD-01, an autonomous medicinal chemistry agent. You screen ARTG-approved "
            "and investigational compounds against target pockets, compute binding affinities (kcal/mol), and "
            "cross-reference the Australian National Medical Stockpile."
        ),
        tools=["autodock_vina_screener", "tga_artg_lookup", "admet_toxicity_evaluator", "nms_stockpile_audit"],
        enabled_mcp_servers=["mcp-server-tga-artg", "mcp-server-chembl"],
        enabled_aus_gov_skills=["AUS-SKILL-TGA-SECTION19A"],
    ),
    "agent_vaccinology_lead": AgentPersona(
        id="agent_vaccinology_lead",
        name="AGENT-VACCINOLOGY-LEAD-01",
        role=AgentRole.VACCINE_IMMUNOLOGIST,
        avatar_icon="shield-virus",
        is_node_lead=True,
        specialization="Epitope Mapping, Neutralizing Titers & Sovereign mRNA Design",
        system_prompt=(
            "You are AGENT-VACCINOLOGY-LEAD-01, an autonomous vaccinology agent. You map conserved B/T-cell "
            "epitopes, formulate mRNA-LNP constructs, evaluate immunogenicity, and align specifications for "
            "domestic manufacturing at CSIRO ACDP and Moderna Victoria."
        ),
        tools=["iedb_epitope_predictor", "mrna_construct_optimizer", "immunogenicity_scorer", "thermostability_modeler"],
        enabled_mcp_servers=["mcp-server-iedb", "mcp-server-csiro-biomfg"],
        enabled_aus_gov_skills=["AUS-SKILL-VACCINE-SOVEREIGN-MAPPING"],
    ),
    "agent_cbrn_intel_lead": AgentPersona(
        id="agent_cbrn_intel_lead",
        name="AGENT-CBRN-INTEL-LEAD-01",
        role=AgentRole.BIOSECURITY_ANALYST,
        avatar_icon="biohazard",
        is_node_lead=True,
        specialization="CBRN Threat Intelligence, SSBA Classification & Dual-Use Audit",
        system_prompt=(
            "You are AGENT-CBRN-INTEL-LEAD-01, an autonomous biosecurity intelligence agent. You audit biological, "
            "chemical, and radiological threats against Commonwealth statutory registers (SSBA Tier 1/2, CWC Schedule 1), "
            "screening for engineered gain-of-function signatures and aerosol dispersal hazards."
        ),
        tools=["ssba_regulatory_classifier", "dual_use_signature_scanner", "aerosol_dispersion_estimator", "cwc_schedule_matcher"],
        enabled_mcp_servers=["mcp-server-ssba-registry", "mcp-server-cwc-checker"],
        enabled_aus_gov_skills=["AUS-SKILL-SSBA-REPORTING", "AUS-SKILL-CBRN-FORENSICS"],
    ),
    "agent_woag_policy_lead": AgentPersona(
        id="agent_woag_policy_lead",
        name="AGENT-WOAG-POLICY-LEAD-01",
        role=AgentRole.WHOLE_OF_GOV_LIAISON,
        avatar_icon="landmark",
        is_node_lead=True,
        specialization="National Emergency Health Policy & Australian Inter-Agency Coordination",
        system_prompt=(
            "You are AGENT-WOAG-POLICY-LEAD-01, an autonomous whole-of-government synthesis agent. You transform "
            "scientific and threat analytics into tailored briefings for statutory Australian authorities: "
            "ACDC, TGA, DAFF, DSTG, NEMA, DFAT, CSIRO, OGTR, and ARPANSA."
        ),
        tools=["woag_brief_synthesizer", "who_ihr_reporter", "tga_fast_track_notifier", "nema_supply_alert"],
        enabled_mcp_servers=["mcp-server-aus-legislation", "mcp-server-crisis-coordination"],
        enabled_aus_gov_skills=["AUS-SKILL-CRISIS-REPORTING"],
    ),
    "agent_radiological_physicist": AgentPersona(
        id="agent_radiological_physicist",
        name="AGENT-HEALTH-PHYSICIST-01",
        role=AgentRole.RADIOLOGICAL_PHYSICIST,
        avatar_icon="radiation",
        is_node_lead=True,
        specialization="Gamma Spectrometry, Radiation Dosimetry & Atmospheric Plume Modeling",
        system_prompt=(
            "You are AGENT-HEALTH-PHYSICIST-01, an autonomous radiological physics agent. You analyze gamma "
            "energy spectra (photopeaks), compute cumulative absorbed dose (mSv), run atmospheric plume dispersion "
            "models (HYSPLIT/HOTSPOT), and recommend evacuation radiuses and decorporation countermeasures."
        ),
        tools=["gamma_spectrometry_analyzer", "hysplit_plume_modeler", "absorbed_dose_calculator", "decorporation_screener"],
        enabled_mcp_servers=["mcp-server-arpansa-rad", "mcp-server-nucleonics"],
        enabled_aus_gov_skills=["AUS-SKILL-ARPANSA-DOSE-ASSESSMENT"],
    ),
    "agent_nuclear_safeguards": AgentPersona(
        id="agent_nuclear_safeguards",
        name="AGENT-NUCLEAR-SAFEGUARDS-01",
        role=AgentRole.NUCLEAR_FORENSICS_ANALYST,
        avatar_icon="shield-halved",
        is_node_lead=False,
        specialization="Radioisotope Attribution & Australian Nuclear Safeguards",
        system_prompt=(
            "You are AGENT-NUCLEAR-SAFEGUARDS-01, an autonomous nuclear forensics agent. You perform isotopic "
            "fingerprinting, source reactor attribution, and compliance audits under the Nuclear Non-Proliferation Act."
        ),
        tools=["isotope_fingerprinter", "asno_safeguards_audit", "source_attribution_engine"],
        enabled_mcp_servers=["mcp-server-ansto-forensics", "mcp-server-asno-safeguards"],
        enabled_aus_gov_skills=["AUS-SKILL-ANSTO-SOURCE-ATTRIBUTION"],
    ),
}

AGENT_TEAMS: Dict[str, AgentTeamConfig] = {
    "bioinformatics_squad": AgentTeamConfig(
        team_id="bioinformatics_squad",
        name="Genomics & Pathogen Identification Squad",
        description="Autonomous genomics squad parsing raw sequences, identifying clades, and calling mutations.",
        lead_role=AgentRole.BIOINFORMATICS_LEAD,
        node_lead=AGENT_PERSONAS["agent_bioinfo_lead"],
        members=[AGENT_PERSONAS["agent_bioinfo_lead"], AGENT_PERSONAS["agent_cbrn_intel_lead"]],
        collaboration_strategy="sequential_refinement",
        enabled_mcp_servers=["mcp-server-ncbi-blast"],
        enabled_aus_gov_skills=["AUS-SKILL-GENOMIC-SURVEILLANCE"],
    ),
    "structural_biology_squad": AgentTeamConfig(
        team_id="structural_biology_squad",
        name="Structural Biology & Proteomics Squad",
        description="Autonomous structural squad predicting 3D folds, pLDDT metrics, and binding pockets.",
        lead_role=AgentRole.STRUCTURAL_BIOLOGIST,
        node_lead=AGENT_PERSONAS["agent_struct_bio_lead"],
        members=[AGENT_PERSONAS["agent_struct_bio_lead"]],
        collaboration_strategy="single_expert",
        enabled_mcp_servers=["mcp-server-alphafold-db"],
        enabled_aus_gov_skills=["AUS-SKILL-STRUCTURAL-TARGET-MODELING"],
    ),
    "medicinal_chemistry_squad": AgentTeamConfig(
        team_id="medicinal_chemistry_squad",
        name="Medicinal Chemistry & Repurposing Squad",
        description="Autonomous pharmacophore squad docking candidate inhibitors and checking ARTG registry.",
        lead_role=AgentRole.MEDICINAL_CHEMIST,
        node_lead=AGENT_PERSONAS["agent_medchem_lead"],
        members=[AGENT_PERSONAS["agent_medchem_lead"]],
        collaboration_strategy="single_expert",
        enabled_mcp_servers=["mcp-server-tga-artg"],
        enabled_aus_gov_skills=["AUS-SKILL-TGA-SECTION19A"],
    ),
    "vaccine_squad": AgentTeamConfig(
        team_id="vaccine_squad",
        name="Vaccinology & Epitope Engineering Squad",
        description="Autonomous immunology squad selecting neutralizing epitopes and formulating mRNA constructs.",
        lead_role=AgentRole.VACCINE_IMMUNOLOGIST,
        node_lead=AGENT_PERSONAS["agent_vaccinology_lead"],
        members=[AGENT_PERSONAS["agent_vaccinology_lead"]],
        collaboration_strategy="single_expert",
        enabled_mcp_servers=["mcp-server-iedb"],
        enabled_aus_gov_skills=["AUS-SKILL-VACCINE-SOVEREIGN-MAPPING"],
    ),
    "biosecurity_squad": AgentTeamConfig(
        team_id="biosecurity_squad",
        name="CBRN & Biosecurity Intelligence Squad",
        description="Autonomous biosecurity squad auditing SSBA compliance, dual-use risks, and aerosol transmission.",
        lead_role=AgentRole.BIOSECURITY_ANALYST,
        node_lead=AGENT_PERSONAS["agent_cbrn_intel_lead"],
        members=[AGENT_PERSONAS["agent_cbrn_intel_lead"], AGENT_PERSONAS["agent_woag_policy_lead"]],
        collaboration_strategy="adversarial_audit",
        enabled_mcp_servers=["mcp-server-ssba-registry"],
        enabled_aus_gov_skills=["AUS-SKILL-SSBA-REPORTING", "AUS-SKILL-CBRN-FORENSICS"],
    ),
    "policy_squad": AgentTeamConfig(
        team_id="policy_squad",
        name="Whole-of-Government Policy Squad",
        description="Autonomous liaison squad compiling statutory situation reports for Australian emergency agencies.",
        lead_role=AgentRole.WHOLE_OF_GOV_LIAISON,
        node_lead=AGENT_PERSONAS["agent_woag_policy_lead"],
        members=[AGENT_PERSONAS["agent_woag_policy_lead"]],
        collaboration_strategy="single_expert",
        enabled_mcp_servers=["mcp-server-aus-legislation"],
        enabled_aus_gov_skills=["AUS-SKILL-CRISIS-REPORTING"],
    ),
    "radiological_defense_squad": AgentTeamConfig(
        team_id="radiological_defense_squad",
        name="Radiological Defense & Health Physics Squad",
        description="Autonomous radiological squad evaluating radioisotope spectra, atmospheric plumes, and ARPANSA compliance.",
        lead_role=AgentRole.RADIOLOGICAL_PHYSICIST,
        node_lead=AGENT_PERSONAS["agent_radiological_physicist"],
        members=[AGENT_PERSONAS["agent_radiological_physicist"], AGENT_PERSONAS["agent_nuclear_safeguards"]],
        collaboration_strategy="sequential_refinement",
        enabled_mcp_servers=["mcp-server-arpansa-rad", "mcp-server-asno-safeguards"],
        enabled_aus_gov_skills=["AUS-SKILL-ARPANSA-DOSE-ASSESSMENT", "AUS-SKILL-ANSTO-SOURCE-ATTRIBUTION"],
    ),
}

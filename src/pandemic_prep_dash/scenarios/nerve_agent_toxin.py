"""
Scenario: Synthetic Organophosphate Nerve Agent (CBRN Chemical Risk).
"""

from typing import Dict, Any
from ..models.bio_chem import (
    ThreatType,
    SampleType,
    BiologicalSample,
    ProteinTarget,
    DrugCandidate,
    VaccineCandidate,
    VaccineEpitope,
    ThreatAssessment,
)

NERVE_AGENT_SAMPLE = BiologicalSample(
    sample_id="SMP-2026-CBRN-CBR02",
    sample_type=SampleType.SMILES,
    name="Unidentified Organophosphoramidocyanidate Neurotoxin Residue",
    raw_payload="CCN(CC)P(=O)(C#N)OC1CCCC1",
    source_location="Port of Brisbane Container Inspection Bay, Queensland, Australia",
    collection_date="2026-09-02",
    submitting_lab="DSTG CBRN Defence Laboratory, Fishermans Bend / Melbourne",
    metadata={
        "detection_method": "GC-MS & Tandem High-Resolution Mass Spectrometry",
        "sample_matrix": "Swab of sealed industrial transit cylinder valve",
        "purity_estimate": "94.2% pharmaceutical-grade weaponized liquid",
        "physical_state": "Colorless, odorless low-volatility persistent liquid",
    },
)

NERVE_AGENT_SCENARIO_DATA: Dict[str, Any] = {
    "scenario_id": "scen_nerve_agent_toxin",
    "name": "Synthetic Organophosphate Toxin Residue (A-Series Analogue)",
    "threat_type": ThreatType.CHEMICAL_NERVE_AGENT,
    "description": (
        "Detection of an illicit fourth-generation organophosphate nerve agent precursor/residue at an Australian maritime "
        "port. High lethality via irreversible acetylcholinesterase phosphorylation."
    ),
    "sample": NERVE_AGENT_SAMPLE.model_dump(),
    "identification": {
        "agent_name": "Fourth-Generation Organophosphate Neurotoxin (A-234 Related Analogue)",
        "clade_or_lineage": "CWC Schedule 1.A.13 Chemical Agent",
        "taxonomy": "Organophosphoramidate Cholinesterase Inhibitor",
        "host_tropism": "All mammalian cholinergic neuromuscular junctions and CNS synapses",
        "genomic_mutations_detected": [
            "N/A (Chemical Hazard - Synthetic Chemical Weapon)",
            "High persistence profile (half-life > 3 weeks on porous surfaces)",
            "Cholinesterase aging half-life: < 3.5 hours (requires rapid oxime administration)",
        ],
        "alignment_confidence": 99.9,
    },
    "protein_targets": [
        ProteinTarget(
            id="prot_human_ache",
            name="Human Acetylcholinesterase (AChE)",
            organism="Homo sapiens",
            gene_symbol="ACHE",
            accession_id="P22303",
            function_summary="Terminates neurotransmission at cholinergic synapses by hydrolyzing acetylcholine. Irreversibly phosphylated by organophosphates causing cholinergic crisis.",
            sequence_length=614,
            plddt_confidence=98.9,
            active_site_residues=["Ser203 (Catalytic Serine)", "His447", "Glu334", "Trp86 (Choline site)"],
            pocket_volume_angstrom3=620.0,
            druggability_score=0.99,
        ).model_dump(),
        ProteinTarget(
            id="prot_human_bche",
            name="Human Butyrylcholinesterase (BChE)",
            organism="Homo sapiens",
            gene_symbol="BCHE",
            accession_id="P06276",
            function_summary="Endogenous pseudocholinesterase enzyme capable of stoichiometric scavenging of circulating organophosphate molecules.",
            sequence_length=602,
            plddt_confidence=98.2,
            active_site_residues=["Ser198", "His438", "Glu325"],
            pocket_volume_angstrom3=730.0,
            druggability_score=0.91,
        ).model_dump(),
    ],
    "drug_candidates": [
        DrugCandidate(
            id="drug_atropine",
            name="Atropine Sulfate (Emergency Autoinjector)",
            smiles="CN1C2CCC1CC(C2)OC(=O)C(CO)C3=CC=CC=C3",
            mechanism_of_action="Competitive muscarinic acetylcholine receptor antagonist blocking hyperstimulation symptoms (bronchorrhea, bradycardia)",
            target_protein_id="prot_human_ache",
            repurposing_indication="Front-line Antidote for Organophosphate and Nerve Agent Poisoning",
            binding_affinity_kcal_mol=-10.1,
            predicted_ic50_nm=0.5,
            tga_artg_status="ARTG Registered (AUST R 162985)",
            australian_stockpile_status="Substantial National & Defence Force Stockpiles (ComboPen/Autoinjectors)",
            clinical_evidence_tier="Approved Standard of Care",
        ).model_dump(),
        DrugCandidate(
            id="drug_pralidoxime",
            name="Pralidoxime Chloride (2-PAM)",
            smiles="CC1=CC=CC(=[N+]1)C=NO.[Cl-]",
            mechanism_of_action="Nucleophilic oxime reactivator that hydrolyzes phosphorylated serine-203 before catalytic aging occurs",
            target_protein_id="prot_human_ache",
            repurposing_indication="Cholinesterase Reactivator Antidote",
            binding_affinity_kcal_mol=-8.4,
            predicted_ic50_nm=15.0,
            tga_artg_status="ARTG Registered (AUST R 19482)",
            australian_stockpile_status="Held in National Medical Stockpile & Major Trauma Centres",
            clinical_evidence_tier="Approved Clinical Antidote",
        ).model_dump(),
        DrugCandidate(
            id="drug_hi6",
            name="HI-6 Oxime Reactivator",
            smiles="C1=CC(=[N+](C=C1)CC(=O)C2=CC(=[N+](C=C2)C=NO)C(=O)N)C(=O)N.[Cl-].[Cl-]",
            mechanism_of_action="Bispyridinium oxime with enhanced blood-brain barrier permeability and efficacy against fourth-gen A-series agents",
            target_protein_id="prot_human_ache",
            repurposing_indication="Advanced CBRN Military Countermeasure",
            binding_affinity_kcal_mol=-9.3,
            predicted_ic50_nm=4.2,
            tga_artg_status="Military Investigational Countermeasure (SAS Special Access)",
            australian_stockpile_status="Specialized Defence CBRN Reserve Only",
            clinical_evidence_tier="Late Stage Preclinical / Military Stockpile",
        ).model_dump(),
    ],
    "vaccine_candidates": [
        VaccineCandidate(
            id="vac_cbrn_bioscavenger",
            platform="Recombinant Enzyme Bioscavenger (Prophylactic Protein)",
            target_antigen="Stoichiometric Clearance of Organophosphate Molecules in Plasma",
            formulation_details="Pegylated recombinant human butyrylcholinesterase (PEG-rBChE) 200 mg IV / IM formulation",
            stability_profile="Lyophilized room temperature stable for 24 months",
            predicted_neutralization_titer="Complete prophylaxis against up to 5x LD50 challenge in primate models",
            epitopes=[
                VaccineEpitope(
                    sequence="Active Serine Stoichiometric Binding Pocket (BChE)",
                    epitope_type="Enzymatic Trap",
                    antigenicity_score=1.0,
                    conserved_across_strains_pct=100.0,
                )
            ],
            local_manufacturing_capability="CSL Behring (Broadmeadows, Victoria) Recombinant Protein Line",
        ).model_dump()
    ],
    "threat_assessment": ThreatAssessment(
        hazard_class="Chemical Weapons Convention (CWC) Schedule 1 Toxic Chemical",
        ssba_tier="Chemical Security Priority - CWC Schedule 1.A",
        aerosol_transmission_feasibility="Moderate (Persistent contact liquid, low volatility unless disseminated via thermal fog or explosive)",
        evidence_of_genetic_manipulation=False,
        gain_of_function_signatures=[
            "N/A - Chemically synthesized military-grade nerve agent",
            "Fluorophosphonate backbone with dialkylaminoethyl sidechain",
        ],
        dual_use_concern_rating="Critical (Zero legitimate commercial or industrial application)",
        containment_level_required="Level A HAZMAT / Chemical Defence Containment Facility (DSTG Fishermans Bend)",
        who_pandemic_potential="CBRN Mass Casualty Terrorism Threat (Immediate OPCW Declaration Required)",
    ).model_dump(),
}

"""
Scenario: H5N1 High-Pathogenicity Avian Influenza (Clade 2.3.4.4b) Spillover.
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

H5N1_SAMPLE = BiologicalSample(
    sample_id="SMP-2026-H5N1-VIC01",
    sample_type=SampleType.RNA,
    name="Avian Influenza A(H5N1) Clade 2.3.4.4b Isolate",
    raw_payload=(
        ">A/dairy_cattle/Victoria/01/2026(H5N1)_segment_4_HA\n"
        "ATGGAGAAAATAGTGCTTCTTCTTGCAATAGTCAGTCTTGTTAAAAGTGATCAGATTTGCATTGGTTAC\n"
        "CATGCAAACAACTCGACAGAGCAGGTTGACACAATAATGGAAAAGAACGTTACTGTTACACATGCCCAA\n"
        "GACATACTGGAAAAGACACACAACGGGAAGCTCTGCGATCTAGATGGAGTGAAGCCTCTAATTTTGAGA\n"
        "GATTGTAGTGTAGCTGGATGGCTCCTCGGGAACCCAATGTGTGACGAATTCCTCAATGTGCCGGAATGG\n"
        "TCTTACATAGTGGAGAAGGCCAGTCCAGCCAATGACCTCTGTTACCCAGGGGATTTCAACGACTATGAA\n"
        "GAATTGAAACACCTATTGAGCAGAATAAACCATTTTGAGAAAATTCAGATCATCCCCAAAAGTTCTTGG\n"
        "TCCAGTCATGAAGCCTCATTAGGGGTGAGCTCAGCATGTCCATACCAGGGAAAGTCCTCCTTTTTCAGA\n"
        "AATGTGGTATGGCTTATCAAAAAGAACAGTACATACCCAACAATAAAGAAAAGCTACAATAATACCAAC\n"
        "CAAGAAGATCTTTTGGTACTGTGGGGGATTCACCATCCTAATGATGCGGCAGAGCAGACAAAGCTCTAT\n"
        "CAAAACCCAACCACCTATATTTCCGTTGGGACATCAACACTAAACCAGAGATTGGTACCAAGAATAGCT\n"
        "ACTAGATCCAAAGTAAACGGGCAAAGTGGAAGGATGGAGTTCTTCTGGACAATTTTAAAACCGAATGAT\n"
        "GCAATCAACTTCGAGAGTAATGGAAATTTCATTGCTCCAGAATATGCATACAAAATTGTCAAGAAAGGG\n"
        "GACTCAGCAATTATGAAAAGTGAATTGGAATATGGTAACTGCAACACCAAGTGTCAAACTCCAATGGGG\n"
        "GCGATAAACTCTAGTATGCCATTCCACAACATACACCCTCTCACCATCGGGGAATGCCCCAAATATGTG\n"
        "AAATCAAACAGATTAGTCCTTGCGACTGGGCTCAGAAATAGCCCTCAAGGAGAGAGAAGAAGAAAAAAG\n"
        "AGAGGACTATTTGGAGCTATAGCAGGTTTTATAGAGGGAGGATGGCAGGGAATGGTAGATGGTTGGTAT\n"
        "GGGTACCACCATAGCAATGAGCAGGGGAGTGGGTACGCTGCAGACAAAGAATCCACTCAAAAGGCAATA\n"
        "GATGGAGTCACCAATAAGGTCAACTCAATCATTGACAAAATGAACACTCAGTTTGAGGCCGTTGGAAGG\n"
        "GAATTTAATAACTTAGAAAGGAGAATAGAAAATTTAAACAAGAAGATGGAAGACGGGTTTCTAGATGTC\n"
        "TGGACATATAATGCTGAACTTCTGGTTCTCATGGAAAATGAGAGAACTCTAGACTTTCATGACTCAAAT\n"
        "GTTAAGAACCTCTACGACAAGGTCCGACTACAGCTTAGGGATAATGCAAAGGAGCTGGGTAACGGTTGT\n"
        "TTCGAGTTCTATCATAAATGTGATAATGAATGTATGGAAAGTATAAGAAACGGAACGTACAACTATCCA\n"
        "CAGTATTCAGAAGAAGCAAGATTAAAAAGAGAGGAAATAAGTGGGGTAAAATTGGAATCAATAGGAACT\n"
        "TACCAAATACTGTCAATTTATTCAACAGTGGCGAGTTCCCTAGCACTGGCAATCATGATGGCTGGTCTC\n"
        "TCTTTATGGATGTGCTCCAATGGGTCGTTACAATGCAGAATTTGCATTTAA"
    ),
    source_location="Goulburn Valley Agricultural District, Victoria, Australia",
    collection_date="2026-08-28",
    submitting_lab="Victorian Infectious Diseases Reference Laboratory (VIDRL) / ACDP",
    metadata={
        "host_species": "Bovine / Dairy Cattle & Avian Contact",
        "sample_matrix": "Bulk raw milk and nasal swab",
        "ct_value": 16.4,
        "preliminary_clade": "2.3.4.4b",
    },
)

H5N1_SCENARIO_DATA: Dict[str, Any] = {
    "scenario_id": "scen_h5n1_avian_flu",
    "name": "Avian Influenza A(H5N1) Clade 2.3.4.4b Zoonotic Spillover",
    "threat_type": ThreatType.BIOLOGICAL_VIRUS,
    "description": (
        "High-pathogenicity avian influenza A(H5N1) clade 2.3.4.4b spillover detected in Victorian dairy "
        "and poultry operations. Genomic screening reveals critical mammalian adaptation signatures."
    ),
    "sample": H5N1_SAMPLE.model_dump(),
    "identification": {
        "agent_name": "Influenza A virus (A/H5N1)",
        "clade_or_lineage": "Clade 2.3.4.4b (Genotype B3.13)",
        "taxonomy": "Orthomyxoviridae, Alphainfluenzavirus",
        "host_tropism": "Avian, Bovine, Swine, Human (Mammalian Receptor Alpha-2,6 linkage shift detected)",
        "genomic_mutations_detected": [
            "PB2: E627K (Critical mammalian adaptation marker conferring enhanced replication at 33°C in human upper respiratory tract)",
            "HA: Q226L substitution (Enhanced binding affinity to human-type alpha-2,6 sialic acid receptors)",
            "NA: H275Y (Absence confirmed - wild-type sensitive to neuraminidase inhibitors)",
        ],
        "alignment_confidence": 99.8,
    },
    "protein_targets": [
        ProteinTarget(
            id="prot_h5n1_ha",
            name="Hemagglutinin (HA) Glycoprotein",
            organism="Influenza A virus H5N1",
            gene_symbol="HA",
            accession_id="EPI_ISL_19024811",
            function_summary="Viral envelope surface glycoprotein mediating host cell sialic acid receptor attachment and membrane fusion.",
            sequence_length=568,
            plddt_confidence=94.6,
            active_site_residues=["Tyr98", "His183", "Glu190", "Leu226", "Gly228"],
            pocket_volume_angstrom3=842.0,
            druggability_score=0.82,
            pdb_snippet="ATOM      1  N   ASP A  11      12.450  24.120  15.890  1.00 94.60           N",
        ).model_dump(),
        ProteinTarget(
            id="prot_h5n1_na",
            name="Neuraminidase (NA) Tetrameric Sialidase",
            organism="Influenza A virus H5N1",
            gene_symbol="NA",
            accession_id="EPI_ISL_19024812",
            function_summary="Cleaves terminal sialic acids from host receptors to release budding virions; principal enzymatic antiviral target.",
            sequence_length=469,
            plddt_confidence=96.1,
            active_site_residues=["Arg118", "Asp151", "Arg152", "Arg224", "Glu276", "Arg292", "Arg371"],
            pocket_volume_angstrom3=980.5,
            druggability_score=0.95,
            pdb_snippet="ATOM      1  N   MET A   1      -4.120  18.420  32.110  1.00 96.10           N",
        ).model_dump(),
        ProteinTarget(
            id="prot_h5n1_pb2",
            name="RNA Polymerase Subunit PB2",
            organism="Influenza A virus H5N1",
            gene_symbol="PB2",
            accession_id="EPI_ISL_19024813",
            function_summary="Host cap-snatching and viral transcription initiator; key driver of species barrier crossing.",
            sequence_length=759,
            plddt_confidence=91.3,
            active_site_residues=["Phe323", "Phe404", "His357", "Lys627"],
            pocket_volume_angstrom3=710.0,
            druggability_score=0.78,
        ).model_dump(),
    ],
    "drug_candidates": [
        DrugCandidate(
            id="drug_oseltamivir",
            name="Oseltamivir Phosphate (Tamiflu)",
            smiles="CCOC(=O)C1=C[C@@H]([C@H]([C@@H](C1)NC(=O)C)N)OC(CC)CC",
            mechanism_of_action="Competitive inhibitor of viral neuraminidase enzymatic pocket preventing viral progeny release",
            target_protein_id="prot_h5n1_na",
            repurposing_indication="Approved for Seasonal & Pandemic Influenza A/B",
            binding_affinity_kcal_mol=-8.9,
            predicted_ic50_nm=1.8,
            tga_artg_status="ARTG Registered (AUST R 75176)",
            australian_stockpile_status="High Domestic Stockpile in National Medical Stockpile (NMS)",
            clinical_evidence_tier="Approved & Stockpiled",
        ).model_dump(),
        DrugCandidate(
            id="drug_baloxavir",
            name="Baloxavir Marboxil (Xofluza)",
            smiles="CC(=O)OCOP(=O)(O)O...",
            mechanism_of_action="Cap-dependent endonuclease inhibitor blocking viral RNA transcription in polymerase complex",
            target_protein_id="prot_h5n1_pb2",
            repurposing_indication="Approved for Acute Uncomplicated Influenza",
            binding_affinity_kcal_mol=-9.7,
            predicted_ic50_nm=0.7,
            tga_artg_status="ARTG Registered (AUST R 305101)",
            australian_stockpile_status="Moderate Holdings in NMS",
            clinical_evidence_tier="Approved Clinical Therapeutic",
        ).model_dump(),
        DrugCandidate(
            id="drug_zanamivir",
            name="Zanamivir Inhalation (Relenza)",
            smiles="CC(=O)N[C@@H]1[C@H](C=C(O[C@H]1[C@@H]([C@@H](CO)O)O)C(=O)O)NC(=N)N",
            mechanism_of_action="Inhaled neuraminidase inhibitor effective against oseltamivir-resistant H275Y mutants",
            target_protein_id="prot_h5n1_na",
            repurposing_indication="Second-line Neuraminidase Inhibitor",
            binding_affinity_kcal_mol=-9.1,
            predicted_ic50_nm=1.2,
            tga_artg_status="ARTG Registered (AUST R 66839)",
            australian_stockpile_status="Substantial National Holdings (Originally developed in Australia / CSIRO)",
            clinical_evidence_tier="Approved Therapeutic",
        ).model_dump(),
    ],
    "vaccine_candidates": [
        VaccineCandidate(
            id="vac_h5_mrna_01",
            platform="mRNA-LNP (Nucleoside-Modified)",
            target_antigen="Hemagglutinin HA (Clade 2.3.4.4b Pre-Fusion Trimer)",
            formulation_details="Lipid Nanoparticle encapsulation with SM-102 ionizable lipid, 50 mcg human adult dose",
            stability_profile="Standard -20°C (stable 6 months); 2-8°C for 30 days",
            predicted_neutralization_titer="High (>1:2560 in murine and ferret challenge models)",
            epitopes=[
                VaccineEpitope(
                    sequence="SSGYATAKESTQKAIDGVTNKVNSIID",
                    epitope_type="Conformational Neutralizing HA Stem Epitope",
                    antigenicity_score=0.94,
                    conserved_across_strains_pct=98.5,
                ),
                VaccineEpitope(
                    sequence="YATAKESTQKAIDGV",
                    epitope_type="CD4+ T-cell helper epitope",
                    mhc_allele_restriction="HLA-DRB1*04:01",
                    antigenicity_score=0.88,
                    conserved_across_strains_pct=96.0,
                ),
            ],
            local_manufacturing_capability="Moderna Victoria Manufacturing Facility (Monash Clayton) / CSIRO Pilot Suite",
        ).model_dump()
    ],
    "threat_assessment": ThreatAssessment(
        hazard_class="High-Consequence Zoonotic Pathogen with Pandemic Potential",
        ssba_tier="Tier 1 SSBA",
        aerosol_transmission_feasibility="High",
        evidence_of_genetic_manipulation=False,
        gain_of_function_signatures=[
            "Natural adaptive substitution: PB2 E627K",
            "Sialic acid receptor binding switch: HA Q226L",
        ],
        dual_use_concern_rating="High (Due to gain of mammalian transmission)",
        containment_level_required="PC3 (Animal PC3 / ACDP PC4 for live ferret aerosol challenge)",
        who_pandemic_potential="Critical Priority Alert (WHO Pandemic Influenza Preparedness Framework)",
    ).model_dump(),
}

"""
Scenario: Novel Engineered Coronaviral Agent (Variant Tartarus).
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

CORONA_SAMPLE = BiologicalSample(
    sample_id="SMP-2026-COV-SYD04",
    sample_type=SampleType.RNA,
    name="Betacoronavirus Isolate (Lineage B.1.x-Tartarus)",
    raw_payload=(
        ">SARS-CoV-X_Isolate_Sydney_Spike_Polyprotein\n"
        "MFVFLVLLPLVSSQCVNLTTRTQLPPAYTNSFTRGVYYPDKVFRSSVLHSTQDLFLPFFSNVTWFHAIH\n"
        "VSGTNGTKRFDNPVLPFNDGVYFASTEKSNIIRGWIFGTTLDSKTQSLLIVNNATNVVIKVCEFQFCND\n"
        "PFLGVYYHKNNKSWMESEFRVYSSANNCTFEYVSQPFLMDLEGKQGNFKNLREFVFKNIDGYFKIYSKH\n"
        "TPINLVRDLPQGFSALEPLVDLPIGINITRFQTLLALHRSYLTPGDSSSGWTAGAAAYYVGYLQPRTFL\n"
        "LKYNENGTITDAVDCALDPLSETKCTLKSFTVEKGIYQTSNFRVQPTESIVRFPNITNLCPFGEVFNAT\n"
        "RFASVYAWNRKRISNCVADYSVLYNSASFSTFKCYGVSPTKLNDLCFTNVYADSFVIRGDEVRQIAPGQ\n"
        "TGKIADYNYKLPDDFTGCVIAWNSNNLDSKVGGNYNYLYRLFRKSNLKPFERDISTEIYQAGSTPCNGV\n"
        "EGFNCYFPLQSYGFQPTNGVGYQPYRVVVLSFELLHAPATVCGPKKSTNLVKNKCVNFNFNGLTGTGVL\n"
        "TESNKKFLPFQQFGRDIADTTDAVRDPQTLEILDITPCSFGGVSVITPGTNTSNQVAVLYQDVNCTDVSP\n"
        "AIHADQLTPTWRVYSTGSNVFQTRAGCLIGAEHVNNSYECDIPIGAGICASYQTQTNSPRRAR*SVASQS\n"
        "IIAYTMSLGAENSVAYSNNSIAIPTNFTISVTTEILPVSMTKTSVDCTMYICGDSTECSNLLLQYGSFCT\n"
        "QLNRALTGIAVEQDKNTQEVFAQVKQIYKTPPIKDFGGFNFSQILPDPSKPSKRSFIEDLLFNKVTLAD\n"
        "AGFIKQYGDCLGDIAARDLICAQKFNGLTVLPPLLTDEMIAQYTSALLAGTITSGWTFGAGAALQIPFA\n"
        "MQMAYRFNGIGVTQNVLYENQKLIANQFNSAIGKIQDSLSSTASALGKLQDVVNQNAQALNTLVKQLSS\n"
        "NFGAISSVLNDILSRLDKVEAEVQIDRLITGRLQSLQTYVTQQLIRAAEIRASANLAATKMSECVLGQS\n"
        "KRVDFCGKGYHLMSFPQSAPHGVVFLHVTYVPAQEKNFTTAPAICHDGKAHFPREGVFVSNGTHWFVTQ\n"
        "RNFYEPQIITTDNTFVSGNCDVVIGIVNNTVYDPLQPELDSFKEELDKYFKNHTSPDVDLGDISGINAS\n"
        "VVNIQKEIDRLNEVAKNLNESLIDLQELGKYEQYIKWPWYIWLGFIAGLIAIVMVTIMLCCMTSCCSCL\n"
        "KGCCSCGSCCKFDEDDSEPVLKGVKLHYT"
    ),
    source_location="Sydney Metropolitan Hospital ICU, NSW, Australia",
    collection_date="2026-09-01",
    submitting_lab="ICPMR Westmead / Centre for Infectious Diseases and Microbiology",
    metadata={
        "clinical_presentation": "Severe acute respiratory distress with rapid oxygen desaturation",
        "icu_status": "Mechanical ventilation required within 36 hours",
        "ct_value": 14.1,
    },
)

CORONA_SCENARIO_DATA: Dict[str, Any] = {
    "scenario_id": "scen_novel_coronavirus",
    "name": "Novel Engineered Coronaviral Agent (Variant Tartarus)",
    "threat_type": ThreatType.SYNTHETIC_ENGINEERED,
    "description": (
        "Emergence of an uncharacterized betacoronavirus exhibiting unusual polybasic furin cleavage insertions "
        "and heightened human ACE2 binding affinity. High transmissibility and severe morbidity flagged."
    ),
    "sample": CORONA_SAMPLE.model_dump(),
    "identification": {
        "agent_name": "Novel Betacoronavirus (SARS-CoV-X)",
        "clade_or_lineage": "Lineage B.1.x-Tartarus (Synthetic Clade)",
        "taxonomy": "Coronaviridae, Betacoronavirus, Sarbecovirus",
        "host_tropism": "Human (High affinity for hACE2), Non-human primates",
        "genomic_mutations_detected": [
            "Spike: Insertion of PRRAR*S polybasic furin cleavage motif with non-canonical codon usage (CGG-CGG tandem)",
            "Spike RBD: T478K, N501Y, E484K, Q498R convergent hyper-affinity mutations for ACE2",
            "Mpro (3CLpro): Conserved catalytic dyad (Cys145 - His41), retaining sensitivity to nirmatrelvir",
        ],
        "alignment_confidence": 98.9,
    },
    "protein_targets": [
        ProteinTarget(
            id="prot_cov_spike",
            name="Spike (S) Glycoprotein Trimer",
            organism="Novel Betacoronavirus SARS-CoV-X",
            gene_symbol="S",
            accession_id="UNIPROT_CVX_S",
            function_summary="Class I viral fusion protein mediating host receptor recognition (ACE2) and cell entry via furin pre-activation.",
            sequence_length=1273,
            plddt_confidence=93.4,
            active_site_residues=["Lys417", "Tyr449", "Asn487", "Tyr501", "His505"],
            pocket_volume_angstrom3=1120.0,
            druggability_score=0.86,
        ).model_dump(),
        ProteinTarget(
            id="prot_cov_mpro",
            name="Main Protease (Mpro / 3CLpro)",
            organism="Novel Betacoronavirus SARS-CoV-X",
            gene_symbol="nsp5",
            accession_id="UNIPROT_CVX_MPRO",
            function_summary="Chymotrypsin-like cysteine protease essential for processing viral polyproteins; premier druggable enzymatic target.",
            sequence_length=306,
            plddt_confidence=97.8,
            active_site_residues=["His41", "Met49", "Phe140", "Gly143", "Cys145", "His163", "Glu166"],
            pocket_volume_angstrom3=890.0,
            druggability_score=0.98,
        ).model_dump(),
    ],
    "drug_candidates": [
        DrugCandidate(
            id="drug_nirmatrelvir",
            name="Nirmatrelvir (Paxlovid Component)",
            smiles="CC1(C2C1C(N(C2)C(=O)C(C(C)(C)C)NC(=O)C(F)(F)F)C(=O)NC(CC3CCNC3=O)C#N)C",
            mechanism_of_action="Reversible covalent inhibitor of SARS main protease (Mpro) catalytic cysteine Cys145",
            target_protein_id="prot_cov_mpro",
            repurposing_indication="Approved for COVID-19 in High-Risk Patients",
            binding_affinity_kcal_mol=-10.4,
            predicted_ic50_nm=3.1,
            tga_artg_status="ARTG Registered (AUST R 377402)",
            australian_stockpile_status="High Stockpile in NMS",
            clinical_evidence_tier="Approved Oral Antiviral",
        ).model_dump(),
        DrugCandidate(
            id="drug_ensitrelvir",
            name="Ensitrelvir (Xocova)",
            smiles="Cc1cc(n(n1)c2ccc(cc2)F)...",
            mechanism_of_action="Non-covalent, non-peptidic Mpro inhibitor with broad variant coverage",
            target_protein_id="prot_cov_mpro",
            repurposing_indication="Emergency Authorized in Japan / Singapore",
            binding_affinity_kcal_mol=-9.9,
            predicted_ic50_nm=5.8,
            tga_artg_status="Section 19A Priority Review Candidate",
            australian_stockpile_status="Not Stockpiled",
            clinical_evidence_tier="Late Stage Clinical Evaluation",
        ).model_dump(),
        DrugCandidate(
            id="drug_remdesivir",
            name="Remdesivir (Veklury IV)",
            smiles="CCC(CC)COC(=O)C(C)NP(=O)(OCC1C(C(C(O1)C#N)C2=CC=C3N2N=CN=C3N)O)OC4=CC=CC=C4",
            mechanism_of_action="Nucleotide analog prodrug inhibiting viral RNA-dependent RNA polymerase (RdRp)",
            target_protein_id="prot_cov_mpro",
            repurposing_indication="Hospitalized Severe Coronavirus Infections",
            binding_affinity_kcal_mol=-8.8,
            predicted_ic50_nm=12.0,
            tga_artg_status="ARTG Registered (AUST R 338243)",
            australian_stockpile_status="Stockpiled in Hospital ICUs",
            clinical_evidence_tier="Approved IV Therapeutic",
        ).model_dump(),
    ],
    "vaccine_candidates": [
        VaccineCandidate(
            id="vac_cov_mrna_hexapro",
            platform="mRNA-LNP (HexaPro Stabilized)",
            target_antigen="Engineered SARS-CoV-X Pre-Fusion Spike (6 Proline Substitutions)",
            formulation_details="Standard 30 mcg nucleoside-modified mRNA encapsulated in ionizable LNP",
            stability_profile="-20°C (standard freezer) / 2-8°C 10 weeks",
            predicted_neutralization_titer="Very High (>1:3200)",
            epitopes=[
                VaccineEpitope(
                    sequence="SALLAGTITSGWTFGAG",
                    epitope_type="Broadly Neutralizing S2 Stem Helix",
                    antigenicity_score=0.96,
                    conserved_across_strains_pct=99.2,
                )
            ],
            local_manufacturing_capability="Moderna Victoria Monash Facility (Rapid 45-day cycle)",
        ).model_dump()
    ],
    "threat_assessment": ThreatAssessment(
        hazard_class="Engineered Synthetic Respiratory Pathogen",
        ssba_tier="Tier 1 SSBA",
        aerosol_transmission_feasibility="High",
        evidence_of_genetic_manipulation=True,
        gain_of_function_signatures=[
            "Non-natural polybasic furin cleavage site with tandem CGG arginine codons",
            "Synthetically optimized ACE2 receptor binding domain motif",
            "Lack of intermediate phylogenetic lineage ancestors in GISAID database",
        ],
        dual_use_concern_rating="Critical Dual-Use Concern (Suspected Gain-of-Function Engineering)",
        containment_level_required="PC4 (High Containment - ACDP Geelong Mandatory)",
        who_pandemic_potential="Public Health Emergency of International Concern (PHEIC) Trigger",
    ).model_dump(),
}

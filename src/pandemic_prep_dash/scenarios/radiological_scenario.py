"""
Scenario 4: Radiological Dispersal Incident (Orphaned Industrial Caesium-137 Source).
Models gamma spectrometry identification, HYSPLIT atmospheric plume dispersion,
decorporation countermeasures (Prussian Blue), and ARPANSA / ANSTO statutory briefings.
"""

from typing import Dict, Any
from ..models.bio_chem import ThreatType, SampleType

SCENARIO_RADIOLOGICAL_CESIUM137: Dict[str, Any] = {
    "scenario_id": "scen_radiological_cesium137",
    "name": "Radiological Dispersal Incident: Orphaned Industrial Caesium-137 Source",
    "threat_type": ThreatType.RADIOLOGICAL_DISPERSAL,
    "description": (
        "High-activity orphaned industrial radiography source (Caesium-137, ~3.7 TBq) dispersed via mechanical "
        "or explosive detonation near Port Botany intermodal freight terminal in Sydney. Gamma spectrometry "
        "reveals sharp 662 keV photopeak requiring immediate ARPANSA Emergency Reference Level intervention."
    ),
    "sample": {
        "sample_id": "SMP-RAD-CS137-01",
        "sample_type": SampleType.RADIOLOGICAL_SPECTRUM,
        "name": "Gamma Spectrometry & Environmental Particulate: Port Botany Terminal",
        "source_location": "Port Botany Intermodal Facility, Sydney, NSW, Australia",
        "collection_date": "2026-09-02",
        "submitting_lab": "ARPANSA Emergency Response & ANSTO Lucas Heights Nuclear Forensics",
        "raw_payload": (
            "RADIOISOTOPE_SPECTRUM: Primary photopeak 661.7 keV (Ba-137m isomeric transition). "
            "Measured activity: 3.7 TBq (100 Ci). Half-life: 30.17 y. Isotopic purity: 99.4% Cs-137, trace Cs-134 (0.04%). "
            "Chemical Form: Caesium Chloride (CsCl) fine aerosolized particulate. "
            "Ambient Dose Equivalent Rate at 10m: 12.5 mSv/hr. Surface contamination: 85,000 Bq/cm²."
        ),
    },
    "identification": {
        "agent_name": "Caesium-137 (Cs-137 / 137mBa decay chain)",
        "clade_or_lineage": "IAEA Category 1 Dangerous Radioactive Source (High-Activity Sealed Source)",
        "taxonomy": "Radionuclide / Beta-Gamma Emitter (Alkali Metal Radioisotope)",
        "alignment_confidence": 99.9,
        "genomic_mutations_detected": [
            "Dominant gamma photopeak confirmed at 661.66 keV (HPGe detector resolution 1.8 keV FWHM)",
            "Specific activity: 3.2 TBq/g consistent with compacted industrial CsCl powder",
            "High environmental mobility: Cs+ acts as potassium potassium-congener with rapid soil/foliar uptake",
            "Physical half-life: 30.17 years; Biological clearance half-life in human tissue: 70-110 days",
        ],
    },
    "protein_targets": [
        {
            "name": "Enterocyte Na+/K+-ATPase & Renal Distal Tubule Potassium Channels",
            "gene_symbol": "ATP1A1 / KCNJ1",
            "plddt_confidence": 97.5,
            "pocket_volume_angstrom3": 1540.0,
            "druggability_score": 0.94,
            "function_summary": (
                "Hydrated Cs+ ions mimic K+ across gastrointestinal enterocytes and renal tubular transport channels, "
                "driving systemic biodistribution into skeletal muscle (80%) and hepatic tissue (10%)."
            ),
        },
        {
            "name": "Hematopoietic Stem Cell DNA Double-Strand Repair Complex (ATM/BRCA1)",
            "gene_symbol": "ATM",
            "plddt_confidence": 94.2,
            "pocket_volume_angstrom3": 2100.0,
            "druggability_score": 0.88,
            "function_summary": (
                "Cellular molecular target for acute radiation syndrome (ARS); internal gamma/beta radiation induces "
                "clustered double-strand breaks causing acute bone marrow suppression."
            ),
        },
    ],
    "drug_candidates": [
        {
            "name": "Prussian Blue (Insoluble Ferric Hexacyanoferrate / Radiogardase)",
            "mechanism_of_action": "Insoluble crystal lattice binding Cs+ in GI tract by ion-exchange for Fe2+, arresting enterohepatic cycling and accelerating fecal excretion by 70%.",
            "binding_affinity_kcal_mol": -14.8,
            "tga_artg_status": "Approved (TGA Emergency Orphan Register / ARTG AUST R 154321)",
            "australian_stockpile_status": "National Medical Stockpile (NMS) Tier 1 Deployment",
            "clinical_evidence_tier": "WHO & IAEA Recommended First-Line Decorporation Antidote",
        },
        {
            "name": "Ca-DTPA / Zn-DTPA (Calcium/Zinc Trisodium Pentetate)",
            "mechanism_of_action": "Synthetic aminopolycarboxylic chelating agent for transuranics and co-dispersed actinide contaminants.",
            "binding_affinity_kcal_mol": -12.4,
            "tga_artg_status": "Section 19A Emergency Exemption Authorized",
            "australian_stockpile_status": "Specialist Toxicological Depot (Lucas Heights / NMS)",
            "clinical_evidence_tier": "TGA Clinical Guidance for Internal Radionuclide Contamination",
        },
    ],
    "vaccine_candidates": [
        {
            "target_antigen": "Amifostine (WR-2721) / Sovereign Radioprotective Countermeasure",
            "platform": "Free-Radical Scavenger & Endothelial DNA Radioprotectant",
            "predicted_neutralization_titer": "Reduces acute radiation lethality by 45% (DRF 1.4)",
            "formulation_details": "Intravenous infusion or auto-injector formulation; dephosphorylated by alkaline phosphatase to active WR-1065 thiol.",
            "local_manufacturing_capability": "CSL Seqirus / Australian Sovereign Sterile Injectables Facility (Parkville, Vic)",
        }
    ],
    "threat_assessment": {
        "ssba_tier": "IAEA Category 1 / ARPANSA Dangerous Radiation Source",
        "dual_use_concerns": [
            "Source activity sufficient to cause acute radiation syndrome (ARS) within 50 meters of detonation epicenter.",
            "Aerosolized CsCl is highly water-soluble, posing severe downwind contamination to municipal water catchments and Sydney rail networks.",
            "Requires immediate activation of the National Counter-Terrorism Plan (NCTP) Radiological Response Annex.",
        ],
    },
}

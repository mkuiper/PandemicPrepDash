from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ThreatType(str, Enum):
    BIOLOGICAL_VIRUS = "biological_virus"
    BIOLOGICAL_BACTERIA = "biological_bacteria"
    CHEMICAL_TOXIN = "chemical_toxin"
    CHEMICAL_NERVE_AGENT = "chemical_nerve_agent"
    RADIOLOGICAL_DISPERSAL = "radiological_dispersal"
    NUCLEAR_MATERIAL = "nuclear_material"
    SYNTHETIC_ENGINEERED = "synthetic_engineered"
    UNKNOWN = "unknown"


class SampleType(str, Enum):
    DNA = "DNA"
    RNA = "RNA"
    PROTEIN = "PROTEIN"
    SMILES = "SMILES"
    RADIOLOGICAL_SPECTRUM = "RADIOLOGICAL_SPECTRUM"
    SYNDROMIC_TEXT = "SYNDROMIC_TEXT"


class BiologicalSample(BaseModel):
    sample_id: str
    sample_type: SampleType
    name: str
    raw_payload: str = Field(..., description="FASTA sequence, SMILES string, or clinical symptom narrative")
    source_location: str = Field("Unknown Location, Australia", description="Geographic point of origin or collection")
    collection_date: str = "2026-09-01"
    submitting_lab: str = "Australian Public Health Reference Laboratory"
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ProteinTarget(BaseModel):
    id: str
    name: str
    organism: str
    gene_symbol: Optional[str] = None
    accession_id: Optional[str] = None
    function_summary: str
    sequence_length: int
    plddt_confidence: float = Field(..., description="Average AlphaFold / structural model pLDDT confidence (0-100)")
    active_site_residues: List[str] = Field(default_factory=list)
    pocket_volume_angstrom3: Optional[float] = None
    druggability_score: float = Field(0.0, description="Druggability index 0.0 - 1.0")
    pdb_snippet: Optional[str] = None


class DrugCandidate(BaseModel):
    id: str
    name: str
    smiles: Optional[str] = None
    mechanism_of_action: str
    target_protein_id: str
    repurposing_indication: str = Field(..., description="Current indication or status e.g. Approved for Influenza / Experimental")
    binding_affinity_kcal_mol: float = Field(..., description="Estimated binding energy in kcal/mol (more negative = stronger)")
    predicted_ic50_nm: Optional[float] = None
    tga_artg_status: str = Field("Not Registered", description="Australian Register of Therapeutic Goods (ARTG) status")
    australian_stockpile_status: str = Field("None", description="National Medical Stockpile (NMS) availability")
    clinical_evidence_tier: str = Field("Preclinical In Silico", description="Evidence tier: In Silico, In Vitro, Phase I-III, Approved")


class VaccineEpitope(BaseModel):
    sequence: str
    epitope_type: str = Field("B-cell conformational", description="B-cell or T-cell (MHC-I / MHC-II)")
    mhc_allele_restriction: Optional[str] = None
    antigenicity_score: float = Field(..., description="Score 0.0 - 1.0")
    conserved_across_strains_pct: float = Field(..., description="Percentage conservation across known variants")


class VaccineCandidate(BaseModel):
    id: str
    platform: str = Field("mRNA-LNP", description="e.g. mRNA-LNP, Recombinant Subunit, ChAdOx1 Viral Vector")
    target_antigen: str
    formulation_details: str
    stability_profile: str = Field("Standard -20C required", description="Storage and stability")
    predicted_neutralization_titer: str = Field("High (>1:1280)", description="Expected immunogenicity")
    epitopes: List[VaccineEpitope] = Field(default_factory=list)
    local_manufacturing_capability: str = Field("CSIRO Biomedical Manufacturing / Moderna Victoria", description="Australian production capacity")


class ThreatAssessment(BaseModel):
    hazard_class: str = Field("High Consequence Pathogen", description="Risk classification")
    ssba_tier: str = Field("Tier 1 SSBA", description="Security Sensitive Biological Agent category under National Health Security Act 2007")
    aerosol_transmission_feasibility: str = Field("High", description="High / Moderate / Low")
    evidence_of_genetic_manipulation: bool = False
    gain_of_function_signatures: List[str] = Field(default_factory=list)
    dual_use_concern_rating: str = Field("Elevated", description="Negligible / Moderate / High / Critical")
    containment_level_required: str = Field("PC3 / PC4", description="Physical Containment level (PC2, PC3, PC4)")
    who_pandemic_potential: str = Field("High", description="Pandemic potential metric")

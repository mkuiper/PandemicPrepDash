"""
Physical Laboratory & Assay Coordination Models.
Bridges computational/in silico agent predictions with accredited physical reference facilities
(ACDP Geelong PC4, ANSTO Lucas Heights, TGA Laboratories, ARPANSA Health Physics).
"""

from typing import Dict, Any, List, Optional
from enum import Enum
from datetime import datetime
import uuid
from pydantic import BaseModel, Field


class AssayCategory(str, Enum):
    VIROLOGY_NEUTRALIZATION = "virology_neutralization"
    ANIMAL_CHALLENGE_STUDY = "animal_challenge_study"
    DIAGNOSTIC_PCR_VALIDATION = "diagnostic_pcr_validation"
    THERAPEUTIC_POTENCY_IC50 = "therapeutic_potency_ic50"
    GAMMA_SPECTROMETRY_ISOTOPES = "gamma_spectrometry_isotopes"
    IN_VIVO_BIOASSAY = "in_vivo_bioassay"
    CHEMICAL_TOXICOLOGY_GCMS = "chemical_toxicology_gcms"


class FacilityIdentifier(str, Enum):
    ACDP_GEELONG = "ACDP (CSIRO Australian Centre for Disease Prevention - PC4)"
    TGA_LABS = "TGA Laboratories Division (ACT)"
    ANSTO_LUCAS_HEIGHTS = "ANSTO Nuclear Science & Radiochemistry (Lucas Heights)"
    ARPANSA_YALLAMBIE = "ARPANSA Radiation Health Services (Yallambie)"
    DSTG_FISHERMANS_BEND = "DSTG CBRN Defence Laboratories (Fishermans Bend)"
    DAFF_ANIMAL_HEALTH = "DAFF National Animal Health Diagnostic Laboratories"


class AssayRequestStatus(str, Enum):
    PROPOSED_BY_AGENT = "PROPOSED_BY_AGENT"
    AUTHORIZED_BY_DUTY_OFFICER = "AUTHORIZED_BY_DUTY_OFFICER"
    DISPATCHED_TO_FACILITY = "DISPATCHED_TO_FACILITY"
    IN_PROGRESS_AT_LAB = "IN_PROGRESS_AT_LAB"
    RESULTS_RECEIVED = "RESULTS_RECEIVED"
    VALIDATED_IN_PIPELINE = "VALIDATED_IN_PIPELINE"


class PhysicalAssayRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: f"REQ-LAB-{uuid.uuid4().hex[:6].upper()}")
    title: str
    assay_category: AssayCategory
    target_facility: FacilityIdentifier
    originating_node_id: str
    requesting_agent_role: str
    hypothesis_to_test: str
    critical_question: str
    specimen_requirements: str
    biosafety_level: str = "PC4 / High Containment"
    estimated_turnaround_hours: int = 48
    priority: str = "HIGH"  # CRITICAL, HIGH, ROUTINE
    status: AssayRequestStatus = AssayRequestStatus.PROPOSED_BY_AGENT
    authorized_by: Optional[str] = None
    dispatched_at: Optional[str] = None
    results_received_at: Optional[str] = None
    results_payload: Dict[str, Any] = Field(default_factory=dict)
    impact_on_pipeline: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

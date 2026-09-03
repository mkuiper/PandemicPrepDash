"""
Evidence & Knowledge Gap Analysis Models.
Synthesizes blackboard findings, identifies critical uncertainties, flags conflicting evidence,
and specifies mandatory physical reference validations required for whole-of-government decision making.
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid
from pydantic import BaseModel, Field


class EvidenceDomain(str, Enum):
    GENOMICS = "Genomics & Phylogenetics"
    STRUCTURAL_BIOLOGY = "Structural Biology & Targets"
    PHARMACOLOGY = "Pharmacology & Therapeutics"
    EPIDEMIOLOGY = "Transmission & Epidemiology"
    HEALTH_PHYSICS = "Health Physics & Plume Dynamics"
    STATUTORY_LEGAL = "Statutory & Biosecurity Law"


class GapSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MODERATE = "MODERATE"
    LOW = "LOW"


class KnowledgeGap(BaseModel):
    gap_id: str = Field(default_factory=lambda: f"GAP-{uuid.uuid4().hex[:6].upper()}")
    domain: EvidenceDomain
    title: str
    description: str
    severity: GapSeverity = GapSeverity.HIGH
    related_node_ids: List[str] = Field(default_factory=list)
    impact_if_unresolved: str
    suggested_investigation: str


class ConflictingEvidence(BaseModel):
    conflict_id: str = Field(default_factory=lambda: f"CONF-{uuid.uuid4().hex[:6].upper()}")
    title: str
    domain: EvidenceDomain
    source_a: str
    claim_a: str
    source_b: str
    claim_b: str
    discrepancy_explanation: str
    operational_risk: str
    recommended_arbitration: str


class ExperimentalValidationNeed(BaseModel):
    validation_id: str = Field(default_factory=lambda: f"VAL-{uuid.uuid4().hex[:6].upper()}")
    assay_title: str
    target_facility: str
    critical_question: str
    urgency: str = "HIGH"  # CRITICAL, HIGH, ROUTINE
    specimen_spec: str
    unblocks_decision: str


class EvidenceAnalysisReport(BaseModel):
    report_id: str = Field(default_factory=lambda: f"EVID-AUDIT-{uuid.uuid4().hex[:6].upper()}")
    incident_name: str
    overall_confidence_score: float = 0.82  # 0.0 - 1.0
    domain_scores: Dict[str, float] = Field(default_factory=dict)
    knowledge_gaps: List[KnowledgeGap] = Field(default_factory=list)
    conflicting_evidence: List[ConflictingEvidence] = Field(default_factory=list)
    required_validations: List[ExperimentalValidationNeed] = Field(default_factory=list)
    synthesis_summary: str
    generated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

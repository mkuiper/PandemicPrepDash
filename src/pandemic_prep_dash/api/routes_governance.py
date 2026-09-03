"""
Data Governance, Cloud Resources & Australian Policy API routes.
"""

from fastapi import APIRouter
from typing import Dict, Any, List
from datetime import datetime

from ..models.governance import (
    GovernanceSettings,
    CloudComputeConfig,
    ComplianceFramework,
    ApiKeysConfig,
    SecurityClassification,
    CloudProviderType,
)

router = APIRouter(prefix="/api/governance", tags=["Data Governance & Cloud Infrastructure"])

# Global singleton settings in memory
CURRENT_GOVERNANCE_SETTINGS = GovernanceSettings()

AUSTRALIAN_GOV_POLICIES = [
    {
        "id": "pspf-infosec",
        "name": "Protective Security Policy Framework (PSPF) - Information Security",
        "authority": "Attorney-General's Department (AGD)",
        "summary": "Mandates security classifications (OFFICIAL, OFFICIAL: SENSITIVE, PROTECTED), information lifecycle management, and need-to-know access controls for emergency response intelligence.",
        "link": "https://www.protectivesecurity.gov.au",
        "key_requirements": [
            "All pathogen genomic sequencing and threat assessments tagged OFFICIAL: SENSITIVE or higher.",
            "Multi-factor access control and cryptographic audit trails for all synthetic agent decisions.",
            "De-identification of human clinical metadata prior to cross-agency transmission.",
        ],
    },
    {
        "id": "asd-ism-ai",
        "name": "Australian Information Security Manual (ISM) - AI & Cloud Security Guidelines",
        "authority": "Australian Signals Directorate (ASD) / Australian Cyber Security Centre (ACSC)",
        "summary": "Technical security controls for cloud-hosted analytical pipelines, model weights safeguarding, and prompt injection mitigation in autonomous agent systems.",
        "link": "https://www.cyber.gov.au/resources-business-and-government/essential-cyber-security/ism",
        "key_requirements": [
            "Data residency restricted to Australian onshore cloud infrastructure (ap-southeast-2).",
            "IRAP (Information Security Registered Assessors Program) assessment up to PROTECTED level.",
            "Container isolation and zero egress for sensitive CBRN analytical models.",
        ],
    },
    {
        "id": "ssba-regulatory-framework",
        "name": "Security Sensitive Biological Agents (SSBA) Standards v7.1",
        "authority": "Australian Centre for Disease Prevention (ACDP) / Department of Health and Aged Care",
        "summary": "Statutory reporting and chain-of-custody requirements under Part 3 of the National Health Security Act 2007 for Tier 1 and Tier 2 high-consequence pathogens.",
        "link": "https://www.health.gov.au/our-work/ssba",
        "key_requirements": [
            "Mandatory 24-hour initial notification upon presumptive identification of a Tier 1 SSBA.",
            "Complete electronic audit logs of sample handling, transfer, and genetic sequence dissemination.",
            "Certified Physical Containment (PC3/PC4) laboratory registration.",
        ],
    },
    {
        "id": "privacy-act-1988",
        "name": "Australian Privacy Principles (Privacy Act 1988)",
        "authority": "Office of the Australian Information Commissioner (OAIC)",
        "summary": "Regulates the handling of personal and health information collected during outbreak investigations and epidemiological contact tracing.",
        "link": "https://www.oaic.gov.au/privacy/australian-privacy-principles",
        "key_requirements": [
            "Health data minimization and secure segregation from public-facing interfaces.",
            "Permitted general situations under section 16B for public health emergencies.",
        ],
    },
]


@router.get("/settings")
def get_governance_settings():
    return {"settings": CURRENT_GOVERNANCE_SETTINGS.model_dump()}


@router.post("/settings")
def update_governance_settings(settings_data: Dict[str, Any]):
    global CURRENT_GOVERNANCE_SETTINGS
    try:
        data_copy = dict(settings_data)
        if "compute" in data_copy and isinstance(data_copy["compute"], dict):
            data_copy["compute"] = CloudComputeConfig(**data_copy["compute"])
        if "compliance" in data_copy and isinstance(data_copy["compliance"], dict):
            data_copy["compliance"] = ComplianceFramework(**data_copy["compliance"])
        if "api_keys" in data_copy and isinstance(data_copy["api_keys"], dict):
            data_copy["api_keys"] = ApiKeysConfig(**data_copy["api_keys"])

        updated = CURRENT_GOVERNANCE_SETTINGS.model_copy(update=data_copy)
        updated.updated_at = datetime.utcnow().isoformat() + "Z"
        CURRENT_GOVERNANCE_SETTINGS = updated
        return {"status": "success", "settings": CURRENT_GOVERNANCE_SETTINGS.model_dump()}
    except Exception as err:
        return {"status": "error", "message": str(err)}


@router.get("/policies")
def list_australian_policies():
    return {"policies": AUSTRALIAN_GOV_POLICIES}

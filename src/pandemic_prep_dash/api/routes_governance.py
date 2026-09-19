"""
Data Governance, Cloud Resources & Australian Policy API routes.
"""

from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
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
        "name": "Protective Security Policy Framework (PSPF)",
        "authority": "Attorney-General's Department",
        "summary": "Classification, need-to-know, personnel and physical security for government information. Not implemented in this demonstrator.",
        "link": "https://www.protectivesecurity.gov.au/",
        "implemented_in_demo": False,
        "key_requirements": [
            "Tag incident intelligence at OFFICIAL, OFFICIAL: Sensitive, PROTECTED or higher as required.",
            "Need-to-know before an agency brief is serialised.",
            "This demo has no login and does not enforce classification.",
        ],
    },
    {
        "id": "asd-ism",
        "name": "Information Security Manual (ISM)",
        "authority": "Australian Signals Directorate / ACSC",
        "summary": "Technical cyber controls for systems and data. This demonstrator is not ISM-assessed.",
        "link": "https://www.cyber.gov.au/resources-business-and-government/essential-cyber-security/ism",
        "implemented_in_demo": False,
        "key_requirements": [
            "Identity, encryption, logging, and secure development for an operational system.",
            "Australian data residency and hosting decisions belong in an IRAP story, not a UI badge.",
        ],
    },
    {
        "id": "essential-eight",
        "name": "Essential Eight",
        "authority": "Australian Signals Directorate / ACSC",
        "summary": "Baseline mitigations for internet-connected networks. Apply to the later estate, not as an in-app score.",
        "link": "https://www.cyber.gov.au/resources-business-and-government/essential-cyber-security/essential-eight",
        "implemented_in_demo": False,
        "key_requirements": [
            "Patch applications and operating systems; multi-factor authentication; restrict administrative privileges.",
            "Application control, restrict macros, user application hardening, regular backups.",
        ],
    },
    {
        "id": "irap",
        "name": "Information Security Registered Assessors Program (IRAP)",
        "authority": "Australian Signals Directorate / ACSC",
        "summary": "Independent assessment of cloud and services, often to PROTECTED. This demo has no IRAP report.",
        "link": "https://www.cyber.gov.au/resources-business-and-government/essential-cyber-security/irap",
        "implemented_in_demo": False,
        "key_requirements": [
            "Assess the hosting platform, not the workshop UI.",
            "Do not treat a Sydney region checkbox as an IRAP outcome.",
        ],
    },
    {
        "id": "openscap-host",
        "name": "OpenSCAP / SCAP (host hardening, later)",
        "authority": "OpenSCAP project / NIST SCAP (not an ASD product)",
        "summary": "Machine-hardening scanner for Linux images. Appropriate in a later build pipeline. Not an ISM badge in this UI.",
        "link": "https://www.open-scap.org/",
        "implemented_in_demo": False,
        "key_requirements": [
            "Scan RHEL/Ubuntu images with CIS or vendor content; keep findings in the system security plan.",
            "ASD does not publish an official ISM OpenSCAP datastream.",
        ],
    },
    {
        "id": "ssba-regulatory-framework",
        "name": "Security Sensitive Biological Agents (SSBA)",
        "authority": "Department of Health, Disability and Ageing (National Health Security Act 2007)",
        "summary": "Statutory SSBA reporting and handling. The dashboard does not notify Health or ACDP.",
        "link": "https://www.health.gov.au/our-work/security-sensitive-biological-agents",
        "implemented_in_demo": False,
        "key_requirements": [
            "Presumptive Tier 1 identification has notification duties in a real incident.",
            "This demo only pauses a human gate; it does not send a statutory notice.",
        ],
    },
    {
        "id": "privacy-act-1988",
        "name": "Australian Privacy Principles (Privacy Act 1988)",
        "authority": "Office of the Australian Information Commissioner (OAIC)",
        "summary": "Personal and health information. The demo stores no real personal information and has no privacy controls.",
        "link": "https://www.oaic.gov.au/privacy/australian-privacy-principles",
        "implemented_in_demo": False,
        "key_requirements": [
            "Minimise health data and segregate it from public interfaces in an operational system.",
        ],
    },
]


@router.get("/settings")
def get_governance_settings():
    return {"settings": CURRENT_GOVERNANCE_SETTINGS.model_dump()}


@router.post("/settings")
def update_governance_settings(settings_data: Dict[str, Any]):
    global CURRENT_GOVERNANCE_SETTINGS
    current = CURRENT_GOVERNANCE_SETTINGS.model_dump()
    for key, value in settings_data.items():
        if isinstance(current.get(key), dict) and isinstance(value, dict):
            current[key] = {**current[key], **value}
        else:
            current[key] = value
    try:
        updated = GovernanceSettings.model_validate(current)
    except ValidationError as err:
        raise HTTPException(status_code=422, detail=str(err))
    updated.updated_at = datetime.utcnow().isoformat() + "Z"
    CURRENT_GOVERNANCE_SETTINGS = updated
    return {"status": "success", "settings": updated.model_dump()}


@router.get("/policies")
def list_australian_policies():
    return {"policies": AUSTRALIAN_GOV_POLICIES}

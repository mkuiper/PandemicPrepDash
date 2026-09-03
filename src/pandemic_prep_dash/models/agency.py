from enum import Enum
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class AgencyIdentifier(str, Enum):
    ACDP = "ACDP"                  # Australian Centre for Disease Prevention (formerly AAHL / CSIRO ACDP Geelong)
    ACDC = "ACDP"                  # Backwards compatibility alias to ACDP
    TGA = "TGA"                    # Therapeutic Goods Administration
    DAFF = "DAFF"                  # Department of Agriculture, Fisheries and Forestry
    DSTG = "DSTG"                  # Defence Science and Technology Group (Department of Defence)
    NEMA = "NEMA"                  # National Emergency Management Agency
    DFAT = "DFAT"                  # Department of Foreign Affairs and Trade
    CSIRO = "CSIRO"                # Commonwealth Scientific and Industrial Research Organisation
    OGTR = "OGTR"                  # Office of the Gene Technology Regulator
    ARPANSA = "ARPANSA"            # Australian Radiation Protection and Nuclear Safety Agency
    ANSTO = "ANSTO"                # Australian Nuclear Science and Technology Organisation
    ASNO = "ASNO"                  # Australian Safeguards and Non-Proliferation Office
    HOME_AFFAIRS = "HOME_AFFAIRS"  # Department of Home Affairs (National Counter-Terrorism & Critical Infrastructure)
    CDNA = "CDNA"                  # Communicable Diseases Network Australia
    PHLN = "PHLN"                  # Public Health Laboratory Network


class SecurityClassification(str, Enum):
    UNCLASSIFIED = "UNCLASSIFIED"
    OFFICIAL = "OFFICIAL"
    OFFICIAL_SENSITIVE = "OFFICIAL: Sensitive"
    SECRET = "SECRET - AUSTRALIAN EYES ONLY"


class UrgencyLevel(str, Enum):
    ROUTINE = "ROUTINE"
    PRIORITY = "PRIORITY"
    IMMEDIATE = "IMMEDIATE"
    FLASH = "FLASH / CRITICAL"


class AgencyProfile(BaseModel):
    id: AgencyIdentifier
    full_name: str
    portfolio: str
    mandate_summary: str
    key_responsibilities: List[str]
    statutory_authority: str
    official_website: str = "https://www.australia.gov.au"
    legislation_url: str = "https://www.legislation.gov.au"
    liaison_contact_role: str
    preferred_brief_format: str
    relevant_threat_types: List[str] = Field(default_factory=list)


class AgencyReport(BaseModel):
    report_id: str
    agency_id: AgencyIdentifier
    title: str
    classification: SecurityClassification = SecurityClassification.OFFICIAL_SENSITIVE
    urgency: UrgencyLevel = UrgencyLevel.PRIORITY
    generated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    incident_name: str
    threat_type: str
    is_relevant: bool = True
    relevance_reason: str = "Direct statutory jurisdiction over threat type"
    executive_summary: str
    situation_update: str
    scientific_findings: Dict[str, Any] = Field(default_factory=dict)
    strategic_implications: List[str] = Field(default_factory=list)
    action_items_required: List[str] = Field(default_factory=list)
    cross_agency_dependencies: List[AgencyIdentifier] = Field(default_factory=list)
    signoff_authority: str = "Incident Response Pipeline (Verified by Human-In-The-Loop Lead)"
    dispatched: bool = False
    dispatch_timestamp: Optional[str] = None

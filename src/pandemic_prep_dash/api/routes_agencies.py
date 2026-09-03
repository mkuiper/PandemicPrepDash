"""
Australian Agency and Briefing API routes.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse
from typing import Dict, Any, List
from datetime import datetime

from ..core.state_manager import StateManager
from ..agencies.registry import AUSTRALIAN_AGENCIES
from ..agencies.generator import AgencyReportGenerator
from ..models.agency import AgencyIdentifier

router = APIRouter(prefix="/api/agencies", tags=["Agencies"])


@router.get("")
def list_agencies():
    return {
        "agencies": [
            {
                "id": a.id.value,
                "full_name": a.full_name,
                "portfolio": a.portfolio,
                "mandate_summary": a.mandate_summary,
                "key_responsibilities": a.key_responsibilities,
                "statutory_authority": a.statutory_authority,
                "preferred_brief_format": a.preferred_brief_format,
            }
            for a in AUSTRALIAN_AGENCIES.values()
        ]
    }


@router.get("/{agency_id}/report")
def get_agency_report(agency_id: str):
    try:
        ident = AgencyIdentifier(agency_id)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Agency '{agency_id}' not recognized")

    engine = StateManager.get_engine()
    reports_map = engine.run.node_artifacts.get("agency_reports", {})

    if agency_id in reports_map:
        return reports_map[agency_id]

    # If pipeline hasn't run the reporting node yet, generate on-the-fly preview
    report = AgencyReportGenerator.generate_report_for_agency(
        agency_id=ident,
        incident_name=engine.scenario_data.get("name", "Active Incident"),
        threat_type=str(engine.scenario_data.get("threat_type", "Biological")),
        artifacts=engine.run.node_artifacts,
    )
    return report.model_dump()


@router.get("/{agency_id}/export/markdown", response_class=PlainTextResponse)
def export_agency_report_markdown(agency_id: str):
    try:
        ident = AgencyIdentifier(agency_id)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Agency '{agency_id}' not recognized")

    engine = StateManager.get_engine()
    reports_map = engine.run.node_artifacts.get("agency_reports", {})
    if agency_id in reports_map:
        rep_dict = reports_map[agency_id]
    else:
        rep_dict = AgencyReportGenerator.generate_report_for_agency(
            agency_id=ident,
            incident_name=engine.scenario_data.get("name", "Active Incident"),
            threat_type=str(engine.scenario_data.get("threat_type", "Biological")),
            artifacts=engine.run.node_artifacts,
        ).model_dump()

    md = f"""# {rep_dict['title']}

**Classification:** `{rep_dict['classification']}`  
**Urgency:** `{rep_dict['urgency']}`  
**Generated At:** `{rep_dict['generated_at']}`  
**Report ID:** `{rep_dict['report_id']}`  
**Target Agency:** {rep_dict['agency_id']} ({AUSTRALIAN_AGENCIES[ident].full_name})  
**Statutory Mandate:** {AUSTRALIAN_AGENCIES[ident].statutory_authority}  

---

## Executive Summary
{rep_dict['executive_summary']}

## Situation Update
{rep_dict['situation_update']}

## Strategic Implications for Australia
{chr(10).join(f"- {item}" for item in rep_dict['strategic_implications'])}

## Operational Action Items Required
{chr(10).join(f"1. {item}" for item in rep_dict['action_items_required'])}

## Cross-Agency Dependencies
{chr(10).join(f"- **{dep}**: {AUSTRALIAN_AGENCIES[AgencyIdentifier(dep)].full_name if dep in [a.value for a in AgencyIdentifier] else dep}" for dep in rep_dict['cross_agency_dependencies'])}

---
*Signed off by: {rep_dict['signoff_authority']}*
"""
    return md


@router.post("/{agency_id}/dispatch")
def dispatch_agency_report(agency_id: str):
    engine = StateManager.get_engine()
    reports_map = engine.run.node_artifacts.get("agency_reports", {})
    if agency_id not in reports_map:
        # Generate it now
        try:
            ident = AgencyIdentifier(agency_id)
        except ValueError:
            raise HTTPException(status_code=404, detail=f"Agency '{agency_id}' not recognized")
        rep = AgencyReportGenerator.generate_report_for_agency(
            agency_id=ident,
            incident_name=engine.scenario_data.get("name", "Active Incident"),
            threat_type=str(engine.scenario_data.get("threat_type", "Biological")),
            artifacts=engine.run.node_artifacts,
        )
        reports_map[agency_id] = rep.model_dump()
        engine.run.node_artifacts["agency_reports"] = reports_map

    rep = reports_map[agency_id]
    rep["dispatched"] = True
    rep["dispatch_timestamp"] = datetime.utcnow().isoformat() + "Z"

    return {
        "status": "dispatched",
        "agency_id": agency_id,
        "dispatch_timestamp": rep["dispatch_timestamp"],
        "message": f"Secure briefing successfully transmitted to {agency_id} liaison channel.",
    }

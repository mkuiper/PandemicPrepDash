"""
Scenario API routes.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import uuid

from ..scenarios import list_scenarios, get_scenario, SCENARIO_REGISTRY
from ..core.state_manager import StateManager
from ..models.bio_chem import ThreatType, SampleType, BiologicalSample

router = APIRouter(prefix="/api/scenarios", tags=["Scenarios"])


class CustomScenarioRequest(BaseModel):
    name: str
    threat_type: ThreatType = ThreatType.BIOLOGICAL_VIRUS
    sample_type: SampleType = SampleType.RNA
    raw_payload: str
    source_location: str = "Australia"
    description: str = "User-submitted custom specimen"


@router.get("")
def get_all_scenarios():
    return {"scenarios": list_scenarios()}


@router.get("/{scenario_id}")
def get_single_scenario(scenario_id: str):
    try:
        return get_scenario(scenario_id)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Scenario '{scenario_id}' not found")


@router.post("/select/{scenario_id}")
def select_active_scenario(scenario_id: str):
    engine = StateManager.get_engine()
    try:
        engine.set_scenario(scenario_id)
        return {
            "status": "success",
            "active_scenario_id": scenario_id,
            "message": f"Active scenario switched to {scenario_id}",
        }
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Scenario '{scenario_id}' not found")


@router.post("/custom")
def create_custom_scenario(req: CustomScenarioRequest):
    custom_id = f"scen_custom_{uuid.uuid4().hex[:6]}"
    sample = BiologicalSample(
        sample_id=f"SMP-{uuid.uuid4().hex[:6].upper()}",
        sample_type=req.sample_type,
        name=f"Custom Specimen: {req.name}",
        raw_payload=req.raw_payload,
        source_location=req.source_location,
    )
    
    scenario_data = {
        "scenario_id": custom_id,
        "name": req.name,
        "threat_type": req.threat_type,
        "description": req.description,
        "sample": sample.model_dump(),
        "identification": {
            "agent_name": f"Uncharacterized Specimen ({req.name})",
            "clade_or_lineage": "Novel isolate",
            "taxonomy": "Taxonomic audit pending",
            "host_tropism": "Investigating mammalian affinity",
            "genomic_mutations_detected": ["Custom input - undergoing algorithmic alignment"],
            "alignment_confidence": 95.0,
        },
        "protein_targets": [
            {
                "id": "prot_custom_01",
                "name": "Surface Envelope Glycoprotein Candidate",
                "organism": req.name,
                "function_summary": "Primary host attachment target",
                "sequence_length": 450,
                "plddt_confidence": 88.5,
                "pocket_volume_angstrom3": 750.0,
                "druggability_score": 0.81,
            }
        ],
        "drug_candidates": [
            {
                "id": "drug_broad_spectrum",
                "name": "Broad-Spectrum Antiviral Probe",
                "mechanism_of_action": "Inhibitor of replication complex",
                "target_protein_id": "prot_custom_01",
                "repurposing_indication": "Investigational Countermeasure",
                "binding_affinity_kcal_mol": -8.5,
                "tga_artg_status": "Special Access Scheme",
                "australian_stockpile_status": "Monitoring",
                "clinical_evidence_tier": "In Silico Evaluation",
            }
        ],
        "vaccine_candidates": [
            {
                "id": "vac_custom_mrna",
                "platform": "mRNA-LNP",
                "target_antigen": "Surface Glycoprotein",
                "formulation_details": "Rapid synthesis prototype",
                "stability_profile": "Standard -20°C",
                "predicted_neutralization_titer": "Moderate-High",
                "epitopes": [],
                "local_manufacturing_capability": "CSIRO Pilot Facilities",
            }
        ],
        "threat_assessment": {
            "hazard_class": "Novel Uncharacterized Agent",
            "ssba_tier": "Tier 2 SSBA (Provisional)",
            "aerosol_transmission_feasibility": "Moderate",
            "evidence_of_genetic_manipulation": False,
            "gain_of_function_signatures": ["Under evaluation"],
            "dual_use_concern_rating": "Moderate",
            "containment_level_required": "PC3 Certified Laboratory",
            "who_pandemic_potential": "Provisional Surveillance Trigger",
        },
    }

    SCENARIO_REGISTRY[custom_id] = scenario_data
    engine = StateManager.get_engine()
    engine.set_scenario(custom_id)

    return {
        "status": "success",
        "scenario_id": custom_id,
        "message": f"Custom scenario '{req.name}' registered and set as active.",
    }

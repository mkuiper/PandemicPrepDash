"""
Physical Reference Laboratory & Assay Coordination Engine.
Manages dispatch and ingestion of experimental data from Australian reference facilities.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

from ..models.lab_bridge import (
    PhysicalAssayRequest,
    AssayCategory,
    FacilityIdentifier,
    AssayRequestStatus,
)


class LabBridgeManager:
    """Orchestrates physical assay requests raised by agentic squads to accredited facilities."""

    _REQUESTS: Dict[str, PhysicalAssayRequest] = {}

    @classmethod
    def initialize_scenario_requests(cls, threat_type: str, scenario_id: str):
        """Pre-seeds standard physical experimental requests relevant to the incident."""
        cls._REQUESTS.clear()

        if "h5n1" in scenario_id.lower() or "bio" in threat_type.lower():
            req1 = PhysicalAssayRequest(
                request_id="REQ-ACDP-FERRET-01",
                title="Ferret Direct & Airborne Aerosol Transmission Challenge",
                assay_category=AssayCategory.ANIMAL_CHALLENGE_STUDY,
                target_facility=FacilityIdentifier.ACDP_GEELONG,
                originating_node_id="node_genomic_characterization",
                requesting_agent_role="Genomics Squad Lead (Bioinformatics)",
                hypothesis_to_test="PB2 E627K mutation combined with HA polybasic cleavage facilitates sustained airborne droplet transmission between ferrets.",
                critical_question="Can this avian isolate transmit between naive mammals via ambient room air without direct physical contact?",
                specimen_requirements="1.0 mL viable lung homogenate or MDCK cell passage isolate (>10^6 TCID50/mL).",
                biosafety_level="PC4 Containment (ACDP Geelong)",
                estimated_turnaround_hours=72,
                priority="CRITICAL",
                status=AssayRequestStatus.IN_PROGRESS_AT_LAB,
                authorized_by="Chief Veterinary Officer & ACDP Director",
                dispatched_at="2026-09-03T10:15:00Z",
                impact_on_pipeline="If transmission confirmed, automatically triggers Category 1 pandemic alert across all States and escalates NEMA coordination.",
            )

            req2 = PhysicalAssayRequest(
                request_id="REQ-ACDP-PRNT-02",
                title="Plaque Reduction Neutralization Test (PRNT90) vs National Serum Bank",
                assay_category=AssayCategory.VIROLOGY_NEUTRALIZATION,
                target_facility=FacilityIdentifier.ACDP_GEELONG,
                originating_node_id="node_vaccine_design",
                requesting_agent_role="Vaccine Squad Lead",
                hypothesis_to_test="Seasonal influenza antibodies possess zero neutralizing cross-reactivity against the emerging clade 2.3.4.4b isolate.",
                critical_question="What is the baseline population immune evasion index in the Australian community?",
                specimen_requirements="Reference strain viral stock + pooled sera from Australian Blood Service cohort.",
                biosafety_level="PC3 Enhanced",
                estimated_turnaround_hours=36,
                priority="HIGH",
                status=AssayRequestStatus.AUTHORIZED_BY_DUTY_OFFICER,
                authorized_by="Incident Controller",
                dispatched_at="2026-09-03T11:30:00Z",
                impact_on_pipeline="Determines need for emergency deployment of pre-pandemic H5 vaccine antigen from National Medical Stockpile.",
            )

            req3 = PhysicalAssayRequest(
                request_id="REQ-TGA-POTENCY-03",
                title="In Vitro Neuraminidase & Cap-Dependent Endonuclease Inhibition IC50",
                assay_category=AssayCategory.THERAPEUTIC_POTENCY_IC50,
                target_facility=FacilityIdentifier.TGA_LABS,
                originating_node_id="node_therapeutic_screening",
                requesting_agent_role="Medicinal Chemistry Lead",
                hypothesis_to_test="Computational docking predicts Baloxavir marboxil IC50 < 2.5 nM and Oseltamivir IC50 < 10 nM.",
                critical_question="Are circulating isolates fully susceptible to Commonwealth National Medical Stockpile stockpiled antivirals?",
                specimen_requirements="Purified neuraminidase enzyme extracts or recombinant active proteins.",
                biosafety_level="PC2 / Chemical Laboratory",
                estimated_turnaround_hours=24,
                priority="HIGH",
                status=AssayRequestStatus.PROPOSED_BY_AGENT,
                impact_on_pipeline="Validates computational docking scores before releasing clinical guidelines to hospital emergency departments.",
            )

            cls._REQUESTS[req1.request_id] = req1
            cls._REQUESTS[req2.request_id] = req2
            cls._REQUESTS[req3.request_id] = req3

        elif "cesium" in scenario_id.lower() or "radio" in threat_type.lower():
            req1 = PhysicalAssayRequest(
                request_id="REQ-ANSTO-HPGE-01",
                title="High-Purity Germanium (HPGe) Gamma Spectrometry & Burnup Profiling",
                assay_category=AssayCategory.GAMMA_SPECTROMETRY_ISOTOPES,
                target_facility=FacilityIdentifier.ANSTO_LUCAS_HEIGHTS,
                originating_node_id="node_spectral_characterization",
                requesting_agent_role="Health Physics Lead",
                hypothesis_to_test="Photopeak ratio of Cs-134 (604/795 keV) to Cs-137 (662 keV) indicates aged industrial radiography source from regional disused well-logging device.",
                critical_question="What is the exact isotopic fingerprint and historical registry origin of the dispersed radioactive source?",
                specimen_requirements="Particulate air filter swipe and soil core specimen in lead transport cask.",
                biosafety_level="Hot Cell / Radiochemistry Facility (Lucas Heights)",
                estimated_turnaround_hours=6,
                priority="CRITICAL",
                status=AssayRequestStatus.IN_PROGRESS_AT_LAB,
                authorized_by="ARPANSA Radiation Emergency Delegate",
                dispatched_at="2026-09-03T12:00:00Z",
                impact_on_pipeline="Provides incontrovertible forensic attribution for the Australian Safeguards and Non-Proliferation Office (ASNO) and Home Affairs.",
            )

            req2 = PhysicalAssayRequest(
                request_id="REQ-ARPANSA-BIOASSAY-02",
                title="Emergency In Vivo Whole-Body Counting & Urine Bioassay Protocol",
                assay_category=AssayCategory.IN_VIVO_BIOASSAY,
                target_facility=FacilityIdentifier.ARPANSA_YALLAMBIE,
                originating_node_id="node_health_physics_assessment",
                requesting_agent_role="ARPANSA Liaison Lead",
                hypothesis_to_test="Immediate oral administration of Prussian Blue (500mg TDS) accelerates biological clearance rate by 3.5-fold.",
                critical_question="What is the committed effective dose equivalent (CED) for first responders exposed within the 450m inner hot zone?",
                specimen_requirements="24-hour urine collection and whole-body sodium iodide scintillation scan.",
                biosafety_level="Clinical Radiation Facility (Yallambie)",
                estimated_turnaround_hours=12,
                priority="HIGH",
                status=AssayRequestStatus.AUTHORIZED_BY_DUTY_OFFICER,
                authorized_by="National Situation Centre",
                dispatched_at="2026-09-03T12:30:00Z",
                impact_on_pipeline="Determines mandatory medical decorporation protocols and public sheltering clearance radius.",
            )

            cls._REQUESTS[req1.request_id] = req1
            cls._REQUESTS[req2.request_id] = req2

        elif "nerve" in scenario_id.lower() or "chem" in threat_type.lower():
            req1 = PhysicalAssayRequest(
                request_id="REQ-DSTG-GCMS-01",
                title="High-Resolution GC-MS & LC-MS Fluoride Ion Reactivation Assay",
                assay_category=AssayCategory.CHEMICAL_TOXICOLOGY_GCMS,
                target_facility=FacilityIdentifier.DSTG_FISHERMANS_BEND,
                originating_node_id="node_chemical_identification",
                requesting_agent_role="CBRN Chemical Specialist Lead",
                hypothesis_to_test="Organophosphate compound is a fourth-generation A-series agent with delayed aging kinetics.",
                critical_question="Is the agent a scheduled Chemical Weapons Convention Schedule 1 neurotoxin, and what is the exact oxime reactivation window?",
                specimen_requirements="Decontamination swab in sealed PTFE vial, refrigerated at 4°C.",
                biosafety_level="OPCW-Designated High Security Chemical Defense Lab",
                estimated_turnaround_hours=8,
                priority="CRITICAL",
                status=AssayRequestStatus.IN_PROGRESS_AT_LAB,
                authorized_by="Department of Home Affairs Threat Triage Controller",
                dispatched_at="2026-09-03T11:00:00Z",
                impact_on_pipeline="Mandates immediate whole-of-government referral under the Chemical Weapons (Prohibition) Act 1994.",
            )

            cls._REQUESTS[req1.request_id] = req1

    @classmethod
    def list_requests(cls) -> List[PhysicalAssayRequest]:
        return list(cls._REQUESTS.values())

    @classmethod
    def get_request(cls, request_id: str) -> Optional[PhysicalAssayRequest]:
        return cls._REQUESTS.get(request_id)

    @classmethod
    def propose_request(cls, req: PhysicalAssayRequest) -> PhysicalAssayRequest:
        cls._REQUESTS[req.request_id] = req
        return req

    @classmethod
    def dispatch_request(cls, request_id: str, authorized_by: str) -> bool:
        req = cls._REQUESTS.get(request_id)
        if not req:
            return False
        req.status = AssayRequestStatus.DISPATCHED_TO_FACILITY
        req.authorized_by = authorized_by
        req.dispatched_at = datetime.utcnow().isoformat() + "Z"
        return True

    @classmethod
    def record_results(cls, request_id: str, results_payload: Dict[str, Any], notes: str) -> bool:
        req = cls._REQUESTS.get(request_id)
        if not req:
            return False
        req.status = AssayRequestStatus.RESULTS_RECEIVED
        req.results_received_at = datetime.utcnow().isoformat() + "Z"
        req.results_payload = results_payload
        req.impact_on_pipeline = notes
        return True

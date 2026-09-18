"""
Workshop scenario: East Coast Low over the Hawkesbury–Nepean (simulated).

Numbers, forecasts, and field reports are fiction for agency-feedback sessions.
They are not observations from BOM, SES, or any other agency.
"""

from typing import Dict, Any
from ..models.bio_chem import ThreatType, SampleType, BiologicalSample


FLOOD_SITREP = BiologicalSample(
    sample_id="INC-2026-ECL-HN-01",
    sample_type=SampleType.SITREP_TEXT,
    name="Hawkesbury–Nepean East Coast Low sitrep (simulated)",
    raw_payload=(
        "SIMULATED INCIDENT SITREP — not a live agency product.\n"
        "Hazard: East Coast Low / riverine flood, Hawkesbury–Nepean catchment, NSW.\n"
        "BOM (example): Severe Weather Warning and Flood Watch issued for Hawkesbury, "
        "Nepean and Colo. Forecast peak at Windsor 17.4 m around 04:00 local.\n"
        "Gauge (example): Windsor 16.8 m and rising; major flood classification 12.2 m.\n"
        "SES (example): seepage reported on the Richmond levee; Windsor–Richmond road "
        "closures incomplete; evacuation polygons covering about 25,000 residents.\n"
        "Conflict: hydrology forecast indicates overnight overtopping; field recon "
        "reports a slower rise than the forecast hydrograph."
    ),
    source_location="Hawkesbury–Nepean catchment (Windsor / Richmond), New South Wales",
    collection_date="2026-03-14",
    submitting_lab="NSW SES Hawkesbury Incident Management Team (workshop fiction)",
    metadata={
        "hazard": "East Coast Low / riverine flood",
        "warning_level": "Severe Weather Warning / Flood Watch",
        "catchment": "Hawkesbury–Nepean",
        "windsor_gauge_m": 16.8,
        "forecast_peak_m": 17.4,
        "major_flood_level_m": 12.2,
        "population_at_risk_estimate": 25000,
        "provenance": "simulated",
    },
)


EAST_COAST_LOW_FLOOD_SCENARIO: Dict[str, Any] = {
    "scenario_id": "scen_east_coast_low_flood",
    "name": "East Coast Low — Hawkesbury–Nepean flooding (simulated)",
    "threat_type": ThreatType.SEVERE_WEATHER,
    "description": (
        "Workshop fiction: an East Coast Low produces major flooding on the "
        "Hawkesbury–Nepean. BOM forecast, river gauges, and SES field reports disagree "
        "on overnight overtopping. The Incident Controller must approve evacuation and "
        "road closures. Analysis, gauges, and dispatches are simulated."
    ),
    "sample": FLOOD_SITREP.model_dump(),
    "identification": {
        "agent_name": "East Coast Low / Hawkesbury–Nepean flooding",
        "clade_or_lineage": "Riverine flood — Windsor / Richmond sector",
        "taxonomy": "Severe weather / hydrological hazard",
        "host_tropism": "Communities, roads, hospitals, and levees in the floodplain",
        "genomic_mutations_detected": [],
        "alignment_confidence": None,
        "warning_level": "Severe Weather Warning / Flood Watch",
        "forecast_peak_m": 17.4,
        "gauge_height_m": 16.8,
        "provenance": "simulated",
    },
    "impact_assessment": {
        "population_at_risk_estimate": 25000,
        "critical_sites": [
            "Hawkesbury District Health Service",
            "Windsor–Richmond corridor",
            "Richmond levee",
        ],
        "road_status": "Partial closures; Windsor–Richmond incomplete",
        "levee_status": "Seepage reported (unverified field report)",
        "provenance": "simulated",
    },
    "conflicting_reports": {
        "bom_forecast": "Peak 17.4 m at Windsor around 04:00; overtopping likely overnight.",
        "river_gauge": "16.8 m and rising; rate slower than the previous 3-hour forecast.",
        "ses_recon": "Richmond levee seepage; some residents remaining in evacuation polygons.",
        "provenance": "simulated",
    },
    "threat_assessment": {
        "hazard_class": "Severe weather / major flood",
        "ssba_tier": None,
        "protective_action": "Evacuation and road closure pending Incident Controller approval",
        "containment_level_required": "Not applicable",
        "provenance": "simulated",
    },
}

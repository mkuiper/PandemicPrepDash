from typing import Dict, Any, List
from .h5n1_avian_flu import H5N1_SCENARIO_DATA
from .novel_coronavirus import CORONA_SCENARIO_DATA
from .nerve_agent_toxin import NERVE_AGENT_SCENARIO_DATA
from .radiological_scenario import SCENARIO_RADIOLOGICAL_CESIUM137

SCENARIO_REGISTRY: Dict[str, Dict[str, Any]] = {
    "scen_h5n1_avian_flu": H5N1_SCENARIO_DATA,
    "scen_novel_coronavirus": CORONA_SCENARIO_DATA,
    "scen_nerve_agent_toxin": NERVE_AGENT_SCENARIO_DATA,
    "scen_radiological_cesium137": SCENARIO_RADIOLOGICAL_CESIUM137,
}


def get_scenario(scenario_id: str) -> Dict[str, Any]:
    if scenario_id not in SCENARIO_REGISTRY:
        raise KeyError(f"Scenario '{scenario_id}' not found in registry.")
    return SCENARIO_REGISTRY[scenario_id]


def list_scenarios() -> List[Dict[str, Any]]:
    return [
        {
            "scenario_id": data["scenario_id"],
            "name": data["name"],
            "threat_type": data["threat_type"],
            "description": data["description"],
            "sample_name": data["sample"]["name"],
            "sample_type": data["sample"]["sample_type"],
            "source_location": data["sample"]["source_location"],
        }
        for data in SCENARIO_REGISTRY.values()
    ]


__all__ = ["SCENARIO_REGISTRY", "get_scenario", "list_scenarios"]

"""
Global State Manager for active pathway engine and configuration.
"""

from typing import Optional
from ..core.registry import create_default_biological_pathway, PATHWAY_TEMPLATES
from ..core.engine import PathwayExecutionEngine


class StateManager:
    _engine: Optional[PathwayExecutionEngine] = None

    @classmethod
    def get_engine(cls) -> PathwayExecutionEngine:
        if cls._engine is None:
            pathway = create_default_biological_pathway()
            cls._engine = PathwayExecutionEngine(pathway, "scen_h5n1_avian_flu")
        return cls._engine

    @classmethod
    def set_engine(cls, engine: PathwayExecutionEngine):
        cls._engine = engine

    @classmethod
    def switch_pathway(cls, pathway_key: str, scenario_id: Optional[str] = None):
        if pathway_key not in PATHWAY_TEMPLATES:
            raise KeyError(f"Unknown pathway template: {pathway_key}")
        # Clone or re-instantiate template
        if pathway_key == "pathway_default_chemical":
            from ..core.registry import create_default_chemical_pathway
            pathway = create_default_chemical_pathway()
            scen = scenario_id or "scen_nerve_agent_toxin"
        else:
            from ..core.registry import create_default_biological_pathway
            pathway = create_default_biological_pathway()
            scen = scenario_id or "scen_h5n1_avian_flu"

        cls._engine = PathwayExecutionEngine(pathway, scen)
        return cls._engine

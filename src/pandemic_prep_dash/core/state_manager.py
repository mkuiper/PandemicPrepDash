"""
Global State Manager for active pathway engine and configuration.
"""

from typing import Optional
from ..core.templates import TemplateManager
from ..core.registry import create_default_biological_pathway
from ..core.engine import PathwayExecutionEngine
from ..models.bio_chem import ThreatType


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
        template = TemplateManager.get_template(pathway_key)
        # Deep copy template so active runs don't mutate template definition
        pathway = template.model_copy(deep=True)

        if scenario_id:
            scen = scenario_id
        else:
            if pathway.threat_type == ThreatType.CHEMICAL_NERVE_AGENT:
                scen = "scen_nerve_agent_toxin"
            elif "coronavirus" in pathway_key:
                scen = "scen_novel_coronavirus"
            else:
                scen = "scen_h5n1_avian_flu"

        cls._engine = PathwayExecutionEngine(pathway, scen)
        return cls._engine

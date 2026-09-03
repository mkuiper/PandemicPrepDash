from enum import Enum
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class AgentRole(str, Enum):
    BIOINFORMATICS_LEAD = "Bioinformatics & Genomics Specialist"
    STRUCTURAL_BIOLOGIST = "Structural Biologist & Molecular Modeler"
    MEDICINAL_CHEMIST = "Medicinal Chemist & Therapeutics Scout"
    VACCINE_IMMUNOLOGIST = "Vaccinologist & Epitope Engineer"
    BIOSECURITY_ANALYST = "CBRN & Biosecurity Intelligence Analyst"
    WHOLE_OF_GOV_LIAISON = "Australian Inter-Agency Policy Coordinator"
    CLINICAL_EPIDEMIOLOGIST = "Infectious Disease Epidemiologist"


class AgentPersona(BaseModel):
    id: str
    name: str
    role: AgentRole
    avatar_icon: str = "dna"
    specialization: str
    system_prompt: str
    tools: List[str] = Field(default_factory=list)


class AgentThoughtPhase(str, Enum):
    OBSERVATION = "observation"
    HYPOTHESIS = "hypothesis"
    TOOL_EXECUTION = "tool_execution"
    SYNTHESIS = "synthesis"
    RECOMMENDATION = "recommendation"


class AgentThoughtLog(BaseModel):
    id: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    agent_id: str
    agent_name: str
    agent_role: str
    node_id: str
    phase: AgentThoughtPhase
    message: str
    tool_name: Optional[str] = None
    tool_input: Optional[Dict[str, Any]] = None
    tool_output_summary: Optional[str] = None
    confidence: float = Field(0.95, description="Self-assessed confidence score 0.0 - 1.0")


class AgentTeamConfig(BaseModel):
    team_id: str
    name: str
    description: str
    lead_role: AgentRole
    members: List[AgentPersona]
    collaboration_strategy: str = "consensus"
    max_tool_invocations: int = 10

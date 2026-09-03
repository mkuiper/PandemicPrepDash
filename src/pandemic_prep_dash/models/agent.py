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
    SCIENTIFIC_RESEARCHER = "Scientific Literature & Threat Researcher"
    RADIOLOGICAL_PHYSICIST = "Health Physicist & Radiological Specialist"
    NUCLEAR_FORENSICS_ANALYST = "Nuclear Forensics & Safeguards Analyst"


class ModelProviderType(str, Enum):
    LOCAL_OPEN_WEIGHTS = "local_open_weights"
    SOVEREIGN_AUSTRALIAN_CLOUD = "sovereign_australian_cloud"
    GOOGLE_VERTEX_AUSTRALIA = "google_vertex_australia"
    CUSTOM_ENDPOINT = "custom_endpoint"


class ModelProviderConfig(BaseModel):
    provider_type: ModelProviderType = ModelProviderType.LOCAL_OPEN_WEIGHTS
    model_name: str = "llama-3.3-70b-instruct-q4"
    endpoint_url: str = "http://localhost:11434/v1"
    temperature: float = 0.2
    max_tokens: int = 4096
    is_sovereign_hosted: bool = True
    context_window_tokens: int = 32768


class AgentPersona(BaseModel):
    """
    Synthetic Autonomous Agent Specification.
    Strict AISI AI Safety Rule: Agents must use transparent, functional designations
    and never anthropomorphic human names to avoid confusing them with human officials.
    """
    id: str
    name: str  # e.g. "AGENT-GENOMICS-LEAD-01"
    role: AgentRole
    avatar_icon: str = "robot"
    specialization: str
    system_prompt: str
    is_node_lead: bool = False
    tools: List[str] = Field(default_factory=list)
    enabled_mcp_servers: List[str] = Field(default_factory=list)
    enabled_aus_gov_skills: List[str] = Field(default_factory=list)
    provider_config: ModelProviderConfig = Field(default_factory=ModelProviderConfig)


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


class DialogueMessageType(str, Enum):
    REQUEST_INFO = "request_info"
    DATA_DISPATCH = "data_dispatch"
    STATUS_QUERY = "status_query"
    CLARIFICATION = "clarification"
    STATUTORY_REFERRAL = "statutory_referral"


class InterNodeDialogue(BaseModel):
    """
    Auditable cross-node lead communication log.
    Allows node leads to orchestrate work, query peer node leads, and record exchanges.
    """
    dialogue_id: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    source_node_id: str
    source_agent_id: str
    source_agent_name: str
    target_node_id: str
    target_agent_id: str
    target_agent_name: str
    message_type: DialogueMessageType
    subject: str
    content: str
    response_content: Optional[str] = None
    resolved: bool = True


class AgentTeamConfig(BaseModel):
    team_id: str
    name: str
    description: str
    lead_role: AgentRole
    node_lead: Optional[AgentPersona] = None
    members: List[AgentPersona] = Field(default_factory=list)
    collaboration_strategy: str = "sequential_refinement"
    max_tool_invocations: int = 10
    provider_config: ModelProviderConfig = Field(default_factory=ModelProviderConfig)
    enabled_mcp_servers: List[str] = Field(default_factory=list)
    enabled_aus_gov_skills: List[str] = Field(default_factory=list)

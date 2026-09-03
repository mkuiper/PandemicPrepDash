from enum import Enum
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field, model_validator
from .agent import AgentThoughtLog
from .bio_chem import ThreatType


class NodeCategory(str, Enum):
    INGESTION = "ingestion"
    CHARACTERIZATION = "characterization"
    STRUCTURAL_BIOLOGY = "structural_biology"
    THERAPEUTICS = "therapeutics"
    VACCINOLOGY = "vaccinology"
    BIOSECURITY = "biosecurity"
    AGENCY_REPORTING = "agency_reporting"
    CUSTOM = "custom"


class NodeStatus(str, Enum):
    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    PAUSED = "paused"
    FAILED = "failed"
    SKIPPED = "skipped"


class PathwayNode(BaseModel):
    id: str
    label: str
    category: NodeCategory
    description: str
    status: NodeStatus = NodeStatus.PENDING
    agent_team_id: str = "bioinformatics_squad"
    requires_human_approval: bool = False
    approval_granted: bool = True
    inputs: Dict[str, Any] = Field(default_factory=dict)
    outputs: Dict[str, Any] = Field(default_factory=dict)
    execution_params: Dict[str, Any] = Field(default_factory=dict)
    latency_ms: Optional[float] = None
    error_message: Optional[str] = None
    position_x: float = 0.0
    position_y: float = 0.0

    @model_validator(mode="after")
    def check_approval_default(self):
        if self.requires_human_approval and self.status == NodeStatus.PENDING and not self.outputs:
            self.approval_granted = False
        return self


class PathwayEdge(BaseModel):
    id: str
    source: str = Field(..., description="Source node ID")
    target: str = Field(..., description="Target node ID")
    label: Optional[str] = None
    condition: Optional[str] = None


class Pathway(BaseModel):
    id: str
    name: str
    description: str
    threat_type: ThreatType = ThreatType.BIOLOGICAL_VIRUS
    nodes: List[PathwayNode] = Field(default_factory=list)
    edges: List[PathwayEdge] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


class RunStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class ExecutionRun(BaseModel):
    run_id: str
    pathway_id: str
    scenario_id: Optional[str] = None
    status: RunStatus = RunStatus.IDLE
    current_node_id: Optional[str] = None
    completed_node_ids: List[str] = Field(default_factory=list)
    execution_order: List[str] = Field(default_factory=list)
    node_artifacts: Dict[str, Any] = Field(default_factory=dict)
    thought_logs: List[AgentThoughtLog] = Field(default_factory=list)
    start_time: Optional[str] = None
    end_time: Optional[str] = None

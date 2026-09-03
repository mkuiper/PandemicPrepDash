"""
Situation Version Control & Incident Progression Timeline Models.
Enables immutable checkpoints, situational timeline auditing, and rollback/fork capabilities
for human controllers and statutory duty officers.
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid
from pydantic import BaseModel, Field


class CheckpointTriggerType(str, Enum):
    INITIAL_INGESTION = "INITIAL_INGESTION"
    NODE_STEP_COMPLETED = "NODE_STEP_COMPLETED"
    BLOCKER_ALERT_RAISED = "BLOCKER_ALERT_RAISED"
    LAB_ASSAY_DISPATCHED = "LAB_ASSAY_DISPATCHED"
    LAB_RESULTS_INGESTED = "LAB_RESULTS_INGESTED"
    STATUTORY_BRIEF_DISPATCHED = "STATUTORY_BRIEF_DISPATCHED"
    MANUAL_DUTY_OFFICER_CHECKPOINT = "MANUAL_DUTY_OFFICER_CHECKPOINT"


class SituationSnapshot(BaseModel):
    version_id: str = Field(default_factory=lambda: f"v1.{uuid.uuid4().hex[:4]}")
    version_number: int = 1
    checkpoint_name: str
    trigger_event: str = CheckpointTriggerType.INITIAL_INGESTION
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    created_by: str = "Commonwealth Incident Controller"
    completed_nodes_count: int = 0
    total_nodes_count: int = 0
    open_blockers_count: int = 0
    dispatched_assays_count: int = 0
    change_summary: str
    state_hash: Optional[str] = None
    node_artifacts_preview: Dict[str, Any] = Field(default_factory=dict)

"""
Situation Version Control & Snapshot Engine.
Maintains an immutable timeline of incident progression for human oversight.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import hashlib
import json

from ..models.version_control import SituationSnapshot, CheckpointTriggerType


class VersionControlManager:
    """Manages immutable situational snapshots across the emergency response lifecycle."""

    _TIMELINE: List[SituationSnapshot] = []

    @classmethod
    def initialize_scenario_timeline(cls, scenario_name: str, total_nodes: int = 8):
        """Pre-seeds an initial baseline and progression checkpoints."""
        cls._TIMELINE.clear()

        s0 = SituationSnapshot(
            version_id="v1.0",
            version_number=1,
            checkpoint_name=f"Incident Ingestion Baseline: {scenario_name}",
            trigger_event="INITIAL_INGESTION",
            created_at="2026-09-03T08:00:00Z",
            created_by="National Situation Centre (NSC) Duty Officer",
            completed_nodes_count=0,
            total_nodes_count=total_nodes,
            open_blockers_count=0,
            dispatched_assays_count=0,
            change_summary="Specimen payload registered. Initial DAG response pathway initialized.",
        )

        s1 = SituationSnapshot(
            version_id="v1.1",
            version_number=2,
            checkpoint_name="Pathogen Identification & Mutation Screening",
            trigger_event="NODE_STEP_COMPLETED",
            created_at="2026-09-03T09:30:00Z",
            created_by="Genomics Squad Lead",
            completed_nodes_count=2,
            total_nodes_count=total_nodes,
            open_blockers_count=1,
            dispatched_assays_count=0,
            change_summary="Identified H5N1 Clade 2.3.4.4b with PB2 E627K. Blocker alert raised for mammalian airborne risk.",
        )

        s2 = SituationSnapshot(
            version_id="v1.2",
            version_number=3,
            checkpoint_name="Structural Modeling & Empirical Assay Dispatch",
            trigger_event="LAB_ASSAY_DISPATCHED",
            created_at="2026-09-03T11:15:00Z",
            created_by="Chief Health Officer / ACDP Director",
            completed_nodes_count=4,
            total_nodes_count=total_nodes,
            open_blockers_count=1,
            dispatched_assays_count=2,
            change_summary="AlphaFold 3D target coordinates generated. Ferret airborne transmission study dispatched to ACDP Geelong PC4.",
        )

        cls._TIMELINE.extend([s0, s1, s2])

    @classmethod
    def list_snapshots(cls) -> List[SituationSnapshot]:
        return list(cls._TIMELINE)

    @classmethod
    def capture_snapshot(
        cls,
        checkpoint_name: str,
        trigger_event: str,
        created_by: str,
        completed_nodes_count: int,
        total_nodes_count: int,
        open_blockers_count: int,
        dispatched_assays_count: int,
        change_summary: str,
        artifacts_preview: Optional[Dict[str, Any]] = None,
    ) -> SituationSnapshot:
        ver_num = len(cls._TIMELINE) + 1
        ver_id = f"v1.{ver_num - 1}"

        snapshot = SituationSnapshot(
            version_id=ver_id,
            version_number=ver_num,
            checkpoint_name=checkpoint_name,
            trigger_event=trigger_event,
            created_at=datetime.utcnow().isoformat() + "Z",
            created_by=created_by,
            completed_nodes_count=completed_nodes_count,
            total_nodes_count=total_nodes_count,
            open_blockers_count=open_blockers_count,
            dispatched_assays_count=dispatched_assays_count,
            change_summary=change_summary,
            node_artifacts_preview=artifacts_preview or {},
        )
        cls._TIMELINE.append(snapshot)
        return snapshot

    @classmethod
    def get_snapshot(cls, version_id: str) -> Optional[SituationSnapshot]:
        for s in cls._TIMELINE:
            if s.version_id == version_id:
                return s
        return None

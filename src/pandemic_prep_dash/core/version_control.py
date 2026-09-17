"""
Situation Version Control & Snapshot Engine.
Maintains an immutable timeline of incident progression for human oversight.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import json

from ..models.version_control import SituationSnapshot


class VersionControlManager:
    """Manages immutable situational snapshots across the emergency response lifecycle."""

    _TIMELINE: List[SituationSnapshot] = []

    _RUN_ID: Optional[str] = None

    @classmethod
    def bind_run(cls, run_id: str):
        """Keep checkpoints scoped to the active demo run."""
        if cls._RUN_ID != run_id:
            cls._TIMELINE = []
            cls._RUN_ID = run_id

    @classmethod
    def list_snapshots(cls) -> List[SituationSnapshot]:
        return [s.model_copy(deep=True) for s in cls._TIMELINE]

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
            node_artifacts_preview=json.loads(json.dumps(artifacts_preview or {})),
        )
        cls._TIMELINE.append(snapshot)
        return snapshot.model_copy(deep=True)

    @classmethod
    def get_snapshot(cls, version_id: str) -> Optional[SituationSnapshot]:
        for s in cls._TIMELINE:
            if s.version_id == version_id:
                return s.model_copy(deep=True)
        return None

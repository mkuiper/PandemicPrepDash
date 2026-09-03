"""
Execution control API routes.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional

from ..core.state_manager import StateManager

router = APIRouter(prefix="/api/execution", tags=["Execution"])


class RunOptions(BaseModel):
    auto_approve: bool = False


@router.post("/step")
def execute_step():
    engine = StateManager.get_engine()
    result = engine.execute_next_step()
    return {
        "result": result,
        "run_status": engine.run.status.value,
        "completed_nodes": engine.run.completed_node_ids,
        "current_node_id": engine.run.current_node_id,
        "logs_count": len(engine.run.thought_logs),
    }


@router.post("/run")
def execute_all(options: RunOptions = RunOptions()):
    engine = StateManager.get_engine()
    result = engine.execute_all(auto_approve=options.auto_approve)
    return {
        "result": result,
        "run_status": engine.run.status.value,
        "completed_nodes": engine.run.completed_node_ids,
        "total_nodes": len(engine.pathway.nodes),
    }


@router.post("/reset")
def reset_execution():
    engine = StateManager.get_engine()
    engine.reset()
    return {
        "status": "success",
        "message": "Execution state reset to initial conditions.",
        "run_status": engine.run.status.value,
    }


@router.post("/approve/{node_id}")
def approve_node(node_id: str):
    engine = StateManager.get_engine()
    success = engine.approve_node(node_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Node '{node_id}' not found")
    return {
        "status": "success",
        "node_id": node_id,
        "message": f"Approval granted for node '{node_id}'. Ready to proceed.",
    }


@router.get("/logs")
def get_execution_logs():
    engine = StateManager.get_engine()
    return {"logs": [l.model_dump() for l in engine.run.thought_logs]}


@router.get("/artifacts")
def get_execution_artifacts():
    engine = StateManager.get_engine()
    return {"artifacts": engine.run.node_artifacts}

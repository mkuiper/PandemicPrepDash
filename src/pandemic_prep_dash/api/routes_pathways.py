"""
Pathway manipulation, template management, and DAG inspection API routes.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import uuid

from ..core.state_manager import StateManager
from ..core.templates import TemplateManager
from ..models.pathway import Pathway, PathwayNode, PathwayEdge, NodeCategory, NodeStatus
from ..models.agent import AgentTeamConfig

router = APIRouter(prefix="/api/pathways", tags=["Pathways"])


class AddNodeRequest(BaseModel):
    label: str
    category: NodeCategory
    description: str
    agent_team_id: str = "bioinformatics_squad"
    agent_team_config: Optional[AgentTeamConfig] = None
    requires_human_approval: bool = False
    position_x: float = 400.0
    position_y: float = 300.0


class UpdateNodeRequest(BaseModel):
    label: Optional[str] = None
    description: Optional[str] = None
    agent_team_id: Optional[str] = None
    agent_team_config: Optional[AgentTeamConfig] = None
    requires_human_approval: Optional[bool] = None
    position_x: Optional[float] = None
    position_y: Optional[float] = None


class AddEdgeRequest(BaseModel):
    source: str
    target: str
    label: Optional[str] = None


class SwitchPathwayRequest(BaseModel):
    pathway_key: str
    scenario_id: Optional[str] = None


class SaveTemplateRequest(BaseModel):
    name: str
    description: Optional[str] = "User-saved pathway template"


@router.get("/templates")
def list_pathway_templates():
    return {"templates": TemplateManager.list_all_templates()}


@router.post("/templates/save")
def save_current_as_template(req: SaveTemplateRequest):
    engine = StateManager.get_engine()
    saved_tmpl = TemplateManager.save_template(
        pathway=engine.pathway,
        name=req.name,
        description=req.description,
    )
    return {
        "status": "success",
        "template_id": saved_tmpl.id,
        "name": saved_tmpl.name,
        "message": f"Pathway template '{req.name}' successfully saved.",
    }


@router.post("/templates/load/{template_id}")
def load_template(template_id: str):
    try:
        engine = StateManager.switch_pathway(template_id)
        return {
            "status": "success",
            "active_pathway_id": engine.pathway.id,
            "pathway_name": engine.pathway.name,
            "message": f"Loaded template '{engine.pathway.name}'",
        }
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/templates/{template_id}")
def delete_template(template_id: str):
    success = TemplateManager.delete_template(template_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"User template '{template_id}' not found or cannot be deleted.")
    return {"status": "success", "deleted_template_id": template_id}


@router.post("/switch")
def switch_pathway(req: SwitchPathwayRequest):
    try:
        engine = StateManager.switch_pathway(req.pathway_key, req.scenario_id)
        return {
            "status": "success",
            "active_pathway_id": engine.pathway.id,
            "scenario_id": engine.scenario_id,
        }
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/state")
def get_pathway_state():
    engine = StateManager.get_engine()
    return engine.get_full_state()


@router.get("/export/json")
def export_pathway_json():
    engine = StateManager.get_engine()
    return engine.pathway.model_dump()


@router.post("/import/json")
def import_pathway_json(pathway_data: Dict[str, Any]):
    try:
        new_pathway = Pathway.model_validate(pathway_data)
        from ..core.engine import PathwayExecutionEngine
        engine = PathwayExecutionEngine(new_pathway)
        StateManager.set_engine(engine)
        return {"status": "success", "message": f"Imported pathway '{new_pathway.name}'"}
    except Exception as err:
        raise HTTPException(status_code=400, detail=f"Invalid pathway JSON schema: {err}")


@router.post("/nodes")
def add_pathway_node(req: AddNodeRequest):
    engine = StateManager.get_engine()
    node_id = f"node_custom_{uuid.uuid4().hex[:6]}"
    new_node = PathwayNode(
        id=node_id,
        label=req.label,
        category=req.category,
        description=req.description,
        agent_team_id=req.agent_team_id,
        agent_team_config=req.agent_team_config,
        requires_human_approval=req.requires_human_approval,
        position_x=req.position_x,
        position_y=req.position_y,
    )
    success = engine.add_node(new_node)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to add node (duplicate ID or invalid graph)")
    return {"status": "success", "node": new_node.model_dump()}


@router.put("/nodes/{node_id}")
def update_pathway_node(node_id: str, req: UpdateNodeRequest):
    engine = StateManager.get_engine()
    node = engine.get_node(node_id)
    if not node:
        raise HTTPException(status_code=404, detail=f"Node '{node_id}' not found")
    
    if req.label is not None:
        node.label = req.label
    if req.description is not None:
        node.description = req.description
    if req.agent_team_id is not None:
        node.agent_team_id = req.agent_team_id
    if req.agent_team_config is not None:
        node.agent_team_config = req.agent_team_config
    if req.requires_human_approval is not None:
        node.requires_human_approval = req.requires_human_approval
    if req.position_x is not None:
        node.position_x = req.position_x
    if req.position_y is not None:
        node.position_y = req.position_y

    return {"status": "success", "node": node.model_dump()}


@router.delete("/nodes/{node_id}")
def delete_pathway_node(node_id: str):
    engine = StateManager.get_engine()
    if not engine.get_node(node_id):
        raise HTTPException(status_code=404, detail=f"Node '{node_id}' not found")
    engine.remove_node(node_id)
    return {"status": "success", "deleted_node_id": node_id}


@router.post("/edges")
def add_pathway_edge(req: AddEdgeRequest):
    engine = StateManager.get_engine()
    edge_id = f"edge_{req.source}_to_{req.target}"
    edge = PathwayEdge(id=edge_id, source=req.source, target=req.target, label=req.label)
    try:
        success = engine.add_edge(edge)
        if not success:
            raise HTTPException(status_code=400, detail="Edge already exists")
        return {"status": "success", "edge": edge.model_dump()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/edges/{edge_id}")
def delete_pathway_edge(edge_id: str):
    engine = StateManager.get_engine()
    engine.remove_edge(edge_id)
    return {"status": "success", "deleted_edge_id": edge_id}

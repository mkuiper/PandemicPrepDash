"""
Agent, Team, Skills, Toolbox, and MCP Server API routes.
"""

from fastapi import APIRouter
from typing import Dict, Any, List

from ..agents.teams import AGENT_PERSONAS, AGENT_TEAMS
from ..agents.skills_toolbox import AUS_GOV_SKILLS, SOFTWARE_TOOLBOX, MCP_SERVERS_REGISTRY
from ..models.agent import ModelProviderType
from ..core.state_manager import StateManager

router = APIRouter(prefix="/api/agents", tags=["Agents"])


@router.get("/personas")
def list_personas():
    return {
        "personas": [
            {
                "id": p.id,
                "name": p.name,
                "role": p.role.value,
                "avatar_icon": p.avatar_icon,
                "is_node_lead": p.is_node_lead,
                "specialization": p.specialization,
                "system_prompt": p.system_prompt,
                "tools": p.tools,
                "enabled_mcp_servers": p.enabled_mcp_servers,
                "enabled_aus_gov_skills": p.enabled_aus_gov_skills,
            }
            for p in AGENT_PERSONAS.values()
        ]
    }


@router.get("/teams")
def list_teams():
    return {
        "teams": [
            {
                "team_id": t.team_id,
                "name": t.name,
                "description": t.description,
                "lead_role": t.lead_role.value,
                "node_lead": t.node_lead.name if t.node_lead else None,
                "members": [m.name for m in t.members],
                "collaboration_strategy": t.collaboration_strategy,
                "enabled_mcp_servers": t.enabled_mcp_servers,
                "enabled_aus_gov_skills": t.enabled_aus_gov_skills,
            }
            for t in AGENT_TEAMS.values()
        ]
    }


@router.get("/skills")
def list_aus_gov_skills():
    return {"skills": [s.model_dump() for s in AUS_GOV_SKILLS.values()]}


@router.get("/toolbox")
def list_software_toolbox():
    return {"toolbox": [t.model_dump() for t in SOFTWARE_TOOLBOX]}


@router.get("/mcps")
def list_mcp_servers():
    return {"mcps": [m.model_dump() for m in MCP_SERVERS_REGISTRY]}


@router.get("/providers")
def list_model_providers():
    return {
        "providers": [
            {
                "id": ModelProviderType.LOCAL_OPEN_WEIGHTS.value,
                "name": "Local Sovereign Inference (vLLM / Ollama)",
                "description": "On-premises air-gapped or classified sovereign server hosting open-weight weights (e.g. Llama-3.3-70B, DeepSeek-R1, Qwen-2.5).",
                "is_sovereign": True,
                "default_model": "llama-3.3-70b-instruct-q4",
                "default_endpoint": "http://localhost:11434/v1",
            },
            {
                "id": ModelProviderType.SOVEREIGN_AUSTRALIAN_CLOUD.value,
                "name": "Sovereign Australian Gov Enclave (IRAP Protected)",
                "description": "Australian-hosted protected government enclave cloud for sensitive national security workflows.",
                "is_sovereign": True,
                "default_model": "aus-gov-cbrn-shield-70b",
                "default_endpoint": "https://api.sovereign.defence.gov.au/v1",
            },
            {
                "id": ModelProviderType.GOOGLE_VERTEX_AUSTRALIA.value,
                "name": "Google Vertex AI (Sydney / Australia-Southeast1)",
                "description": "In-region sovereign data boundary deployment for high-throughput macromolecular reasoning.",
                "is_sovereign": False,
                "default_model": "gemini-1.5-pro",
                "default_endpoint": "https://australia-southeast1-aiplatform.googleapis.com",
            },
            {
                "id": ModelProviderType.CUSTOM_ENDPOINT.value,
                "name": "Custom OpenAI-Compatible Endpoint",
                "description": "Configurable endpoint for local testbeds, test runners, or private clusters.",
                "is_sovereign": True,
                "default_model": "custom-model",
                "default_endpoint": "http://127.0.0.1:8000/v1",
            },
        ]
    }


@router.get("/dialogues")
def get_inter_node_dialogues():
    engine = StateManager.get_engine()
    return {"dialogues": [d.model_dump() for d in engine.run.inter_node_dialogues]}

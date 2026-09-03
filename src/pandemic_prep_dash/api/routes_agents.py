"""
Agent and Team configuration API routes.
"""

from fastapi import APIRouter
from typing import Dict, Any, List

from ..agents.teams import AGENT_PERSONAS, AGENT_TEAMS

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
                "specialization": p.specialization,
                "system_prompt": p.system_prompt,
                "tools": p.tools,
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
                "members": [m.name for m in t.members],
                "collaboration_strategy": t.collaboration_strategy,
            }
            for t in AGENT_TEAMS.values()
        ]
    }

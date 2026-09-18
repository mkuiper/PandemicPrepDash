"""
Node-bound agent instances and a simulated Academy.

Role templates (AGENT-BIOINFO-LEAD-01) are the job description.
Each pathway node gets its own instance so genomics intake and genomic
characterization do not share memory, skills currency, or academy history.

Academy attendance does not train model weights. It records a workshop
refresh of Skills, MCP servers, or software Tools for that instance.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
import uuid

from ..agents.teams import AGENT_TEAMS, AGENT_PERSONAS
from ..models.pathway import PathwayNode


ACADEMY_TRACKS = ("skills", "mcp", "tools")

TRACK_NOTES = {
    "skills": "Reviewed assigned government skills pack. Currency is simulated; no live policy feed.",
    "mcp": "Checked MCP server bindings for this instance. Endpoints are not live.",
    "tools": "Looked up tool/version notes for this field. No installer or model weights were updated.",
}


class AcademyManager:
    """Per-process academy log, keyed by node-bound instance id."""

    _RECORDS: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def instance_id(cls, node_id: str, persona_id: str) -> str:
        return f"{node_id}::{persona_id}"

    @classmethod
    def get_record(cls, instance_id: str) -> Dict[str, Any]:
        if instance_id not in cls._RECORDS:
            cls._RECORDS[instance_id] = {
                "instance_id": instance_id,
                "last_skills_at": None,
                "last_mcp_at": None,
                "last_tools_at": None,
                "sessions": [],
            }
        return cls._RECORDS[instance_id]

    @classmethod
    def attend(cls, instance_id: str, track: str, actor: str = "orchestrator") -> Dict[str, Any]:
        if track not in ACADEMY_TRACKS:
            raise ValueError(f"Unknown academy track '{track}'")
        rec = cls.get_record(instance_id)
        now = datetime.utcnow().isoformat() + "Z"
        session = {
            "session_id": f"acad_{uuid.uuid4().hex[:8]}",
            "at": now,
            "track": track,
            "actor": actor,
            "note": TRACK_NOTES[track],
            "provenance": "simulated",
        }
        rec["sessions"].append(session)
        rec[f"last_{track}_at"] = now
        return session

    @classmethod
    def clear(cls) -> None:
        cls._RECORDS = {}


def _persona_payload(persona) -> Dict[str, Any]:
    return {
        "template_id": persona.id,
        "template_name": persona.name,
        "role": persona.role.value if hasattr(persona.role, "value") else str(persona.role),
        "specialization": persona.specialization,
        "purpose": persona.specialization,
        "system_prompt": persona.system_prompt,
        "tools": list(persona.tools or []),
        "enabled_mcp_servers": list(persona.enabled_mcp_servers or []),
        "enabled_aus_gov_skills": list(persona.enabled_aus_gov_skills or []),
    }


def _resolve_team(node: PathwayNode):
    if node.agent_team_config and (node.agent_team_config.node_lead or node.agent_team_config.members):
        return node.agent_team_config
    return AGENT_TEAMS.get(node.agent_team_id)


def list_node_crews(nodes: List[PathwayNode]) -> List[Dict[str, Any]]:
    """One crew card per pathway node, with distinct instance ids."""
    crews = []
    for node in nodes:
        team = _resolve_team(node)
        lead = None
        members = []
        if team:
            lead = team.node_lead
            members = list(team.members or [])
            if lead and lead not in members:
                members = [lead] + members
        if not lead:
            lead = AGENT_PERSONAS.get("agent_woag_policy_lead")
            members = [lead] if lead else []

        instances = []
        for persona in members:
            if persona is None:
                continue
            iid = AcademyManager.instance_id(node.id, persona.id)
            rec = AcademyManager.get_record(iid)
            overdue = not rec["last_skills_at"] or not rec["last_mcp_at"] or not rec["last_tools_at"]
            instances.append({
                **_persona_payload(persona),
                "instance_id": iid,
                "instance_name": f"{persona.name}@{node.id}",
                "is_lead": bool(lead and persona.id == lead.id),
                "academy": {
                    "last_skills_at": rec["last_skills_at"],
                    "last_mcp_at": rec["last_mcp_at"],
                    "last_tools_at": rec["last_tools_at"],
                    "sessions": rec["sessions"][-5:],
                    "overdue": overdue,
                },
            })

        crews.append({
            "node_id": node.id,
            "node_label": node.label,
            "node_category": node.category.value if hasattr(node.category, "value") else str(node.category),
            "team_id": getattr(team, "team_id", node.agent_team_id),
            "team_name": getattr(team, "name", node.agent_team_id),
            "team_description": getattr(team, "description", "") or "",
            "harness_engine": str(getattr(team, "harness_engine", "") or ""),
            "instances": instances,
        })
    return crews


def orchestrator_problems(engine) -> List[Dict[str, Any]]:
    """Issues the control-hub orchestrator should surface (simulated)."""
    problems: List[Dict[str, Any]] = []
    for b in engine.data_hub.blockers:
        if getattr(b, "status", "OPEN") != "OPEN":
            continue
        problems.append({
            "id": b.alert_id,
            "kind": "blocker",
            "severity": b.severity.value if hasattr(b.severity, "value") else str(b.severity),
            "title": b.title,
            "detail": b.description,
            "node_id": b.node_id,
        })
    for crew in list_node_crews(engine.pathway.nodes):
        for inst in crew["instances"]:
            if inst["academy"]["overdue"] and inst["is_lead"]:
                problems.append({
                    "id": f"acad-{inst['instance_id']}",
                    "kind": "academy_overdue",
                    "severity": "INFO",
                    "title": f"{inst['instance_name']} has not attended Academy",
                    "detail": "Skills, MCP, or tool refresh has not been recorded for this node instance.",
                    "node_id": crew["node_id"],
                })
        node = engine.get_node(crew["node_id"])
        ctx = (node.outputs or {}).get("lead_context") if node else None
        if ctx:
            unknowns = [q for q in ctx if q.get("unknown")]
            if unknowns:
                problems.append({
                    "id": f"unk-{crew['node_id']}",
                    "kind": "unknown_evidence",
                    "severity": "WARNING",
                    "title": f"{crew['node_label']}: lead reported unknown evidence",
                    "detail": unknowns[0].get("question", "unknown"),
                    "node_id": crew["node_id"],
                })
    academy = [p for p in problems if p["kind"] == "academy_overdue"]
    others = [p for p in problems if p["kind"] != "academy_overdue"]
    return others + academy[:3]

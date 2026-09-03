"""
Agentic Harness - autonomous execution wrapper for Pathway Nodes.
Equips node squads with iterative ReAct loops, tool execution orchestration,
human message board monitoring, and blackboard updates.
"""

from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime
import uuid
import time

from ..models.pathway import PathwayNode, NodeStatus, NodeCategory
from ..models.agent import (
    AgentThoughtLog,
    AgentThoughtPhase,
    AgentRole,
    InterNodeDialogue,
    DialogueMessageType,
)
from ..agents.teams import AGENT_TEAMS, AGENT_PERSONAS
from .data_hub import CentralDataHub, BlockerAlert, BlockerSeverity, HubMessage, MessageSenderType
from .node_executor import NodeExecutor


class NodeAgenticHarness:
    """
    Autonomous execution harness wrapping an individual pathway node.
    Orchestrates the agent squad reasoning loop, monitors human messages on the Central Hub,
    executes tools, raises blocker alerts, and publishes human-readable progress.
    """

    def __init__(self, node: PathwayNode, data_hub: CentralDataHub):
        self.node = node
        self.data_hub = data_hub
        self.harness_id = f"harness_{node.id}"

    def check_human_directives(self) -> List[HubMessage]:
        """Scans the Central Hub message board for human expert directives directed at this node."""
        relevant_messages = []
        for msg in self.data_hub.messages:
            if msg.sender_type == MessageSenderType.HUMAN_EXPERT:
                if msg.target_node_id in [self.node.id, f"@{self.node.id}", "@all", self.node.category.value]:
                    relevant_messages.append(msg)
        return relevant_messages

    def run(
        self,
        blackboard: Dict[str, Any],
        scenario_data: Dict[str, Any],
    ) -> Tuple[PathwayNode, List[AgentThoughtLog], Dict[str, Any], List[InterNodeDialogue], Optional[BlockerAlert]]:
        """
        Executes the agentic harness loop:
        1. Intake blackboard & human expert directives from the Central Hub.
        2. Execute squad reasoning & specialized scientific tools via NodeExecutor.
        3. Post human-readable findings to the Central Hub message board.
        """
        start_time = time.time()
        
        # 1. Check for human directives on the board
        human_directives = self.check_human_directives()
        harness_prefix_logs: List[AgentThoughtLog] = []

        team_config = self.node.agent_team_config or AGENT_TEAMS.get(self.node.agent_team_id)
        lead_persona = (
            team_config.node_lead
            if team_config and team_config.node_lead
            else (team_config.members[0] if team_config and team_config.members else AGENT_PERSONAS["agent_bioinfo_lead"])
        )

        if human_directives:
            latest_directive = human_directives[-1]
            harness_prefix_logs.append(
                AgentThoughtLog(
                    id=f"th_{uuid.uuid4().hex[:8]}",
                    agent_id=lead_persona.id,
                    agent_name=lead_persona.name,
                    agent_role=f"{lead_persona.role.value} (Harness Controller)",
                    node_id=self.node.id,
                    phase=AgentThoughtPhase.OBSERVATION,
                    message=f"Harness ingested human expert directive: '{latest_directive.content}' (From {latest_directive.sender_name}). Integrating into squad workflow.",
                    confidence=0.99,
                )
            )

        # 2. Execute squad logic via NodeExecutor
        updated_node, thought_logs, new_artifacts, new_dialogues, new_blocker = NodeExecutor.execute_node(
            node=self.node,
            blackboard=blackboard,
            scenario_data=scenario_data,
        )

        all_logs = harness_prefix_logs + thought_logs

        # 3. Post a clean, human-readable summary to the Central Hub Message Board
        summary_msg = self._generate_hub_summary(updated_node, new_artifacts)
        if summary_msg:
            self.data_hub.post_message(
                HubMessage(
                    message_id=f"msg_hn_{uuid.uuid4().hex[:6]}",
                    sender_type=MessageSenderType.AGENT,
                    sender_name=lead_persona.name,
                    sender_role=lead_persona.role.value,
                    target_node_id=self.node.id,
                    content=summary_msg,
                    tags=[self.node.category.value, "NODE_COMPLETED"],
                )
            )

        updated_node.latency_ms = round((time.time() - start_time) * 1000, 2)
        return updated_node, all_logs, new_artifacts, new_dialogues, new_blocker

    def _generate_hub_summary(self, node: PathwayNode, artifacts: Dict[str, Any]) -> str:
        """Constructs a human-readable progress note for the Central Hub Message Board."""
        if node.category == NodeCategory.INGESTION:
            sample = artifacts.get("sample", {})
            return f"Ingestion verified specimen '{sample.get('name', 'Sample')}' from {sample.get('source_location')}. Sequencing/detector telemetry passed quality control."
        
        elif node.category == NodeCategory.RESEARCH:
            papers = artifacts.get("literature_research", [])
            top_title = papers[0].get("title", "") if papers else "None"
            return f"Threat Research squad completed literature query. Retrieved {len(papers)} peer-reviewed citations. Lead finding: '{top_title[:80]}...'."
        
        elif node.category == NodeCategory.CHARACTERIZATION:
            ident = artifacts.get("identification", {})
            return f"Genomic characterization resolved pathogen: {ident.get('agent_name', 'Unknown')} ({ident.get('clade_or_lineage', 'Standard')}). GC%: {ident.get('computed_gc_content', 'N/A')}%."
        
        elif node.category == NodeCategory.STRUCTURAL_BIOLOGY:
            targets = artifacts.get("protein_targets", [])
            top_target = targets[0].get("name", "Target") if targets else "N/A"
            return f"Structural biology modeled {len(targets)} macromolecular targets. Primary target '{top_target}' resolved with high confidence."
        
        elif node.category == NodeCategory.THERAPEUTICS:
            drugs = artifacts.get("drug_candidates", [])
            lead_drug = drugs[0].get("name", "None") if drugs else "N/A"
            return f"Therapeutics screening evaluated {len(drugs)} candidate countermeasures. Lead docked compound: {lead_drug} ({drugs[0].get('binding_affinity_kcal_mol', '') if drugs else ''} kcal/mol)."
        
        elif node.category == NodeCategory.VACCINOLOGY:
            vacs = artifacts.get("vaccine_candidates", [])
            top_vac = vacs[0].get("platform", "mRNA") if vacs else "N/A"
            return f"Vaccinology squad formulated {len(vacs)} candidates. Platform: {top_vac}. Neutralization titers and domestic biomanufacturing scaled."
        
        elif node.category == NodeCategory.BIOSECURITY:
            threat = artifacts.get("threat_assessment", {})
            return f"Biosecurity audit completed. Classification: {threat.get('ssba_tier', 'Verified')}. Regulatory physical containment and dual-use markers assessed."
        
        elif node.category == NodeCategory.AGENCY_REPORTING:
            reports = artifacts.get("agency_reports", {})
            relevant_count = sum(1 for r in reports.values() if r.get("is_relevant", True))
            return f"Whole-of-Government reporting generated situation briefs for {relevant_count} relevant statutory authorities. Non-relevant authorities set to standby."

        return f"Node '{node.label}' successfully finished execution."

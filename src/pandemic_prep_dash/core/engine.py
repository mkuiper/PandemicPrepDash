"""
Execution Engine - orchestrates DAG traversal, manages execution blackboard,
evaluates dependencies, and synchronizes the Central Information Hub.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
import networkx as nx

from ..models.pathway import (
    Pathway,
    PathwayNode,
    PathwayEdge,
    ExecutionRun,
    RunStatus,
    NodeStatus,
)
from ..scenarios import get_scenario, list_scenarios
from .node_executor import NodeExecutor
from .data_hub import CentralDataHub, BlockerAlert, BlockerSeverity, ResearchPaper


class PathwayExecutionEngine:
    """Orchestrates DAG execution, handles dependencies, branching, and human-in-the-loop gates."""

    def __init__(self, pathway: Pathway, scenario_id: Optional[str] = None):
        self.pathway = pathway
        self.scenario_id = scenario_id or "scen_h5n1_avian_flu"
        self.scenario_data = get_scenario(self.scenario_id)
        self.run: ExecutionRun = ExecutionRun(
            run_id=f"run_{uuid.uuid4().hex[:8]}",
            pathway_id=pathway.id,
            scenario_id=self.scenario_id,
            status=RunStatus.IDLE,
        )
        self.data_hub = CentralDataHub(
            incident_name=self.scenario_data.get("name", "CBRN Threat"),
            threat_type=str(self.scenario_data.get("threat_type", "biological_virus")),
        )
        self._build_graph()

    def _build_graph(self) -> nx.DiGraph:
        """Constructs NetworkX representation to validate DAG and resolve dependencies."""
        G = nx.DiGraph()
        for node in self.pathway.nodes:
            G.add_node(node.id, data=node)
        for edge in self.pathway.edges:
            G.add_edge(edge.source, edge.target, data=edge)

        if not nx.is_directed_acyclic_graph(G):
            cycles = list(nx.simple_cycles(G))
            raise ValueError(f"Pathway contains cyclic dependencies: {cycles}")

        self.graph = G
        return G

    def set_scenario(self, scenario_id: str):
        """Switches active scenario, aligns pathway template if needed, and resets execution state."""
        self.scenario_id = scenario_id
        self.scenario_data = get_scenario(scenario_id)
        threat_type = self.scenario_data.get("threat_type")

        # Auto-align pathway threat type if switching between chemical, radiological, and biological
        from ..models.bio_chem import ThreatType
        if threat_type == ThreatType.RADIOLOGICAL_DISPERSAL and self.pathway.threat_type != ThreatType.RADIOLOGICAL_DISPERSAL:
            from .templates import TemplateManager
            self.pathway = TemplateManager.get_template("pathway_default_radiological").model_copy(deep=True)
        elif threat_type == ThreatType.CHEMICAL_NERVE_AGENT and self.pathway.threat_type != ThreatType.CHEMICAL_NERVE_AGENT:
            from .registry import create_default_chemical_pathway
            self.pathway = create_default_chemical_pathway()
        elif threat_type not in [ThreatType.CHEMICAL_NERVE_AGENT, ThreatType.RADIOLOGICAL_DISPERSAL] and self.pathway.threat_type in [ThreatType.CHEMICAL_NERVE_AGENT, ThreatType.RADIOLOGICAL_DISPERSAL]:
            from .registry import create_default_biological_pathway
            self.pathway = create_default_biological_pathway()

        self.data_hub = CentralDataHub(
            incident_name=self.scenario_data.get("name", "CBRN Threat"),
            threat_type=str(threat_type),
        )
        self.reset()
        # Pre-seed initial sample artifact so users can inspect it right away
        if "sample" in self.scenario_data:
            self.run.node_artifacts["sample"] = self.scenario_data["sample"]
            self.data_hub.specimen_intel = self.scenario_data["sample"]

    def reset(self):
        """Resets all nodes and execution state to initial condition."""
        for node in self.pathway.nodes:
            node.status = NodeStatus.PENDING
            node.outputs = {}
            node.latency_ms = None
            node.error_message = None
            if node.requires_human_approval:
                node.approval_granted = False
            else:
                node.approval_granted = True

        self.run = ExecutionRun(
            run_id=f"run_{uuid.uuid4().hex[:8]}",
            pathway_id=self.pathway.id,
            scenario_id=self.scenario_id,
            status=RunStatus.IDLE,
        )
        self.data_hub = CentralDataHub(
            incident_name=self.scenario_data.get("name", "CBRN Threat"),
            threat_type=str(self.scenario_data.get("threat_type", "biological_virus")),
        )
        self._build_graph()

    def get_node(self, node_id: str) -> Optional[PathwayNode]:
        for node in self.pathway.nodes:
            if node.id == node_id:
                return node
        return None

    def get_ready_nodes(self) -> List[PathwayNode]:
        """Identifies nodes whose dependencies are all in COMPLETED state."""
        ready = []
        for node in self.pathway.nodes:
            if node.status not in [NodeStatus.PENDING, NodeStatus.READY]:
                continue

            predecessors = list(self.graph.predecessors(node.id))
            all_preds_completed = True
            for pred_id in predecessors:
                pred_node = self.get_node(pred_id)
                if not pred_node or pred_node.status != NodeStatus.COMPLETED:
                    all_preds_completed = False
                    break

            if all_preds_completed:
                ready.append(node)
        return ready

    def approve_node(self, node_id: str) -> bool:
        """Grants human approval to proceed through a gatekeeper node."""
        node = self.get_node(node_id)
        if not node:
            return False
        node.approval_granted = True
        if node.status == NodeStatus.PAUSED:
            node.status = NodeStatus.READY
            if self.run.status == RunStatus.PAUSED:
                self.run.status = RunStatus.RUNNING
        return True

    def execute_next_step(self) -> Dict[str, Any]:
        """Executes the next available node in DAG order."""
        if self.run.status == RunStatus.IDLE:
            self.run.status = RunStatus.RUNNING
            self.run.start_time = datetime.utcnow().isoformat() + "Z"

        ready_nodes = self.get_ready_nodes()
        if not ready_nodes:
            # Check if all completed or if stalled
            all_completed = all(n.status == NodeStatus.COMPLETED for n in self.pathway.nodes)
            if all_completed:
                self.run.status = RunStatus.COMPLETED
                self.run.end_time = datetime.utcnow().isoformat() + "Z"
                return {"status": "completed", "message": "All pathway nodes successfully executed."}
            
            paused_nodes = [n for n in self.pathway.nodes if n.status == NodeStatus.PAUSED]
            if paused_nodes:
                self.run.status = RunStatus.PAUSED
                return {"status": "paused", "message": f"Paused awaiting approval on {len(paused_nodes)} node(s)."}
            
            return {"status": "blocked", "message": "No nodes currently ready to execute."}

        # Take first ready node
        target_node = ready_nodes[0]

        # Check gatekeeper requirement
        if target_node.requires_human_approval and not target_node.approval_granted:
            target_node.status = NodeStatus.PAUSED
            self.run.status = RunStatus.PAUSED
            self.run.current_node_id = target_node.id
            return {
                "status": "approval_required",
                "node_id": target_node.id,
                "node_label": target_node.label,
                "message": f"Human-In-The-Loop confirmation required for node '{target_node.label}'.",
            }

        self.run.current_node_id = target_node.id
        updated_node, thought_logs, new_artifacts, new_dialogues, new_blocker = NodeExecutor.execute_node(
            node=target_node,
            blackboard=self.run.node_artifacts,
            scenario_data=self.scenario_data,
        )

        # Merge artifacts, thought logs, and auditable inter-node dialogues
        self.run.node_artifacts.update(new_artifacts)
        self.run.thought_logs.extend(thought_logs)
        self.run.inter_node_dialogues.extend(new_dialogues)

        # Synchronize Central Data Hub
        if new_blocker:
            self.data_hub.add_blocker(new_blocker)

        if "sample" in new_artifacts or "identification" in new_artifacts:
            self.data_hub.specimen_intel.update(new_artifacts.get("identification", new_artifacts.get("sample", {})))
        if "literature_research" in new_artifacts:
            self.data_hub.literature_research = [ResearchPaper(**p) for p in new_artifacts["literature_research"]]
        if "protein_targets" in new_artifacts:
            self.data_hub.structural_targets = new_artifacts["protein_targets"]
        if "drug_candidates" in new_artifacts or "vaccine_candidates" in new_artifacts:
            self.data_hub.countermeasures = new_artifacts.get("drug_candidates", []) + new_artifacts.get("vaccine_candidates", [])
        if "plume_model" in new_artifacts:
            self.data_hub.plume_and_environmental = new_artifacts["plume_model"]
        if "threat_assessment" in new_artifacts:
            self.data_hub.statutory_compliance = new_artifacts["threat_assessment"]

        self.run.completed_node_ids.append(target_node.id)
        if target_node.id not in self.run.execution_order:
            self.run.execution_order.append(target_node.id)

        # Check if this completion makes everything completed
        if all(n.status == NodeStatus.COMPLETED for n in self.pathway.nodes):
            self.run.status = RunStatus.COMPLETED
            self.run.end_time = datetime.utcnow().isoformat() + "Z"

        return {
            "status": "step_completed",
            "node_id": target_node.id,
            "node_label": target_node.label,
            "latency_ms": target_node.latency_ms,
            "thought_logs_count": len(thought_logs),
            "artifacts_updated": list(new_artifacts.keys()),
        }

    def execute_all(self, auto_approve: bool = False) -> Dict[str, Any]:
        """Executes all remaining nodes until completion or approval pause."""
        if self.run.status == RunStatus.IDLE:
            self.run.status = RunStatus.RUNNING
            self.run.start_time = datetime.utcnow().isoformat() + "Z"

        max_cycles = 50
        cycles = 0
        while cycles < max_cycles:
            cycles += 1
            ready = self.get_ready_nodes()
            if not ready:
                break

            for node in ready:
                if node.requires_human_approval and not node.approval_granted:
                    if auto_approve:
                        node.approval_granted = True
                    else:
                        node.status = NodeStatus.PAUSED
                        self.run.status = RunStatus.PAUSED
                        return {
                            "status": "approval_required",
                            "node_id": node.id,
                            "node_label": node.label,
                            "message": f"Execution paused: Human verification required for '{node.label}'.",
                        }

                self.execute_next_step()

        all_done = all(n.status == NodeStatus.COMPLETED for n in self.pathway.nodes)
        return {
            "status": "completed" if all_done else "paused",
            "completed_nodes": len(self.run.completed_node_ids),
            "total_nodes": len(self.pathway.nodes),
        }

    def add_node(self, node: PathwayNode) -> bool:
        """Dynamically adds a new node to the active pathway."""
        if any(n.id == node.id for n in self.pathway.nodes):
            return False
        self.pathway.nodes.append(node)
        self.pathway.updated_at = datetime.utcnow().isoformat() + "Z"
        self._build_graph()
        return True

    def remove_node(self, node_id: str) -> bool:
        """Removes a node and associated edges."""
        self.pathway.nodes = [n for n in self.pathway.nodes if n.id != node_id]
        self.pathway.edges = [e for e in self.pathway.edges if e.source != node_id and e.target != node_id]
        self.pathway.updated_at = datetime.utcnow().isoformat() + "Z"
        self._build_graph()
        return True

    def add_edge(self, edge: PathwayEdge) -> bool:
        """Adds an edge, ensuring no cycle is introduced."""
        if any(e.id == edge.id for e in self.pathway.edges):
            return False
        # Test addition on temp graph
        temp_g = self.graph.copy()
        temp_g.add_edge(edge.source, edge.target)
        if not nx.is_directed_acyclic_graph(temp_g):
            raise ValueError(f"Adding edge {edge.source} -> {edge.target} would introduce a cycle!")
        self.pathway.edges.append(edge)
        self.pathway.updated_at = datetime.utcnow().isoformat() + "Z"
        self._build_graph()
        return True

    def remove_edge(self, edge_id: str) -> bool:
        """Removes an edge by ID."""
        self.pathway.edges = [e for e in self.pathway.edges if e.id != edge_id]
        self.pathway.updated_at = datetime.utcnow().isoformat() + "Z"
        self._build_graph()
        return True

    def update_node_position(self, node_id: str, x: float, y: float) -> bool:
        """Updates UI visual coordinates of a node."""
        node = self.get_node(node_id)
        if not node:
            return False
        node.position_x = x
        node.position_y = y
        return True

    def get_full_state(self) -> Dict[str, Any]:
        """Returns entire snapshot of pathway, execution run, logs, artifacts, and Central Data Hub."""
        return {
            "pathway": self.pathway.model_dump(),
            "run": self.run.model_dump(),
            "data_hub": self.data_hub.model_dump(),
            "scenario": {
                "scenario_id": self.scenario_data.get("scenario_id"),
                "name": self.scenario_data.get("name"),
                "threat_type": self.scenario_data.get("threat_type"),
                "description": self.scenario_data.get("description"),
                "sample": self.scenario_data.get("sample"),
            },
            "stats": {
                "total_nodes": len(self.pathway.nodes),
                "completed_nodes": len(self.run.completed_node_ids),
                "total_thought_logs": len(self.run.thought_logs),
                "artifacts_count": len(self.run.node_artifacts),
                "active_blockers": len([b for b in self.data_hub.blockers if b.status == "OPEN"]),
            },
        }

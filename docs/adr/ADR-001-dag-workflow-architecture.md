# ADR-001: Directed Acyclic Graph (DAG) Workflow Architecture

## Status
Accepted

## Context
Traditional incident response tools rely on static linear checklists or hardcoded sequential scripts. However, modern CBRN and biological incident characterization is intrinsically non-linear and concurrently branched:
1. Once a sequence or chemical agent is identified, structural modeling of multiple target proteins and security threat assessments can proceed simultaneously.
2. From structural models, therapeutic small-molecule repurposing (antivirals/antidotes) and prophylactic vaccine candidate design can run in parallel.
3. Information converging from all branches must then feed into synthesis nodes that compile briefings for different government agencies.

Additionally, non-technical users and government liaisons need to inspect, modify, add, or prune workflow nodes dynamically based on available compute resources, laboratory capacity, and incoming field intelligence.

## Decision
We chose a Directed Acyclic Graph (DAG) engine backed by NetworkX for dependency resolution:
- **Nodes (`PathwayNode`)**: Represent modular analytical or response tasks with an assigned specialized agent squad, inputs, outputs, execution status, and position coordinates.
- **Edges (`PathwayEdge`)**: Represent dependencies and data flow between nodes.
- **Topological Invariant**: Any addition or modification of an edge is dynamically validated using NetworkX cycle detection (`nx.is_directed_acyclic_graph`). If a cycle is detected, the operation is immediately rejected.
- **Topological In-Degree Execution**: A node is marked `READY` if and only if all predecessor nodes have achieved `COMPLETED` status.
- **Shared State (Blackboard Pattern)**: All nodes read from and write to a shared execution blackboard (`node_artifacts`).

## Consequences
### Positive
- Enables true concurrency and branching (e.g. therapeutics and vaccine pipelines executing concurrently).
- Flexible for arbitrary biological and chemical workflows (e.g., swapping a viral pipeline for an organophosphate nerve agent pipeline).
- Full auditability: Each node maintains individual latency, error states, and execution outputs.

### Negative / Trade-offs
- Requires nodes to conform to consistent blackboard serialization schemas.
- Requires cycle detection checks upon every runtime modification.

# ADR-004: Human-in-the-Loop Security & Statutory Gating

## Status
Accepted

## Context
Full end-to-end automation poses unacceptable risks in biosecurity and CBRN threat classification:
1. Reclassifying an agent as a **Security Sensitive Biological Agent (SSBA Tier 1)** carries profound legal consequences under the *National Health Security Act 2007*, triggering criminal penalties, strict chain-of-custody protocols, and mandatory law enforcement notification.
2. Formally attributing a pathogen or chemical toxin to intentional state or non-state release involves serious national security and diplomatic implications.
3. Rapid regulatory actions by the TGA or biosecurity quarantines by DAFF must be verified by designated human authorities before operational execution.

## Decision
We implemented first-class **Human-in-the-Loop (HITL) Gatekeepers** at the node level:
- Nodes have a boolean flag: `requires_human_approval: bool`.
- When an execution engine reaches a node with `requires_human_approval=True`, if `approval_granted` is false, the engine automatically halts execution, transitions the node and the run status to `PAUSED`, and alerts the operator.
- An authorized human operator can review the upstream artifacts, agent deliberation trace, and security classification on the Node Inspector.
- Only upon receiving explicit confirmation via `POST /api/execution/approve/{node_id}` does the node transition to `READY` and allow the workflow to resume.
- For automated testing or non-critical demo exploration, an optional `auto_approve: bool = True` override flag is provided.

## Consequences
- Guarantees human sovereign control over statutory, legal, and national security triggers.
- Prevents autonomous runaway dissemination of sensitive CBRN assessments.
- Maintains compliance with the Australian National Health Emergency Response Arrangements (NatHealth).

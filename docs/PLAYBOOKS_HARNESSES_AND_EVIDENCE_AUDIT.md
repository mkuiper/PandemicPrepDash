# Operational Response Playbooks, Multi-Harness Architecture & Evidence Audit Engine

## Executive Overview

In this development cycle, **PandemicPrepDash** was significantly advanced to address critical operational requirements for an Australian Whole-of-Government emergency response platform. The system now supports:
1. **Explicit Agentic Harness Engine Specification**: Configurable execution backends per node (`AGY`, `Claude Code CLI`, `OpenAI Codex CLI`, `OpenCode`, `Sovereign Air-Gapped Podman Containers`).
2. **Interactive Agent Squad & Specialist Customization**: Granular control over squad composition, individual agent roles, permitted computational tools (BLAST+, AlphaFold 3, AutoDock Vina, HYSPLIT-Rad, RDKit, SSBA Scanner), and Australian Government Skills (`AUS-SKILL-*`).
3. **Commonwealth Operational Response Playbooks**: Rebranded and structured response templates into accredited playbooks with trigger criteria, jurisdictional mandates, and escalation pathways.
4. **Central Control Hub Evidence Synthesis & Knowledge Gap Engine**: Real-time analytical auditing that exposes critical knowledge gaps, flags contradictory evidence (e.g., *in silico* binding vs. low-frequency field resistance), and mandates physical laboratory assays.
5. **Situation Progression & Version Control Timeline**: Immutable checkpoints (`v1.0`, `v1.1`, `v1.2`) enabling forensic auditability, situational regression tracking, and royal commission readiness.
6. **Platform System Architecture & Technical Specifications**: Full documentation (Chapter 8) detailing multi-tier topologies, ReAct harness execution loops, and statutory interfaces.

---

## 1. Explicit Agentic Harness Execution Engines

In accordance with Australian Government Protective Security Policy Framework (PSPF) and ISM requirements, nodes can be configured to run on distinct execution harnesses:

| Harness Engine | CLI Command / Runtime | Sandbox Policy | Primary Use Case |
|---|---|---|---|
| **AGY (Antigravity Autonomous Coding Harness)** | `agy exec` | `restricted_fs` | Autonomous code execution, tool invocation, and subagent orchestration within DeepMind environment. |
| **Claude Code CLI** | `claude -p` | `restricted_fs` | Advanced multi-step scientific reasoning, code synthesis, and literature parsing. |
| **OpenAI Codex CLI** | `codex exec` | `restricted_fs` | High-speed deterministic execution and complex bioinformatic pipeline generation. |
| **OpenCode Harness** | `opencode run` | `isolated_container` | Local open-source cluster execution without external cloud connectivity. |
| **Sovereign Containerized Harness** | `podman run --network none` | `isolated_container` | Air-gapped container execution satisfying PSPF INFOSEC-10 for sensitive biological / SSBA data. |

Squad members within each node can be customized with explicit tool permissions (e.g. enabling AlphaFold 3 and AutoDock Vina for structural specialists while restricting public network access).

---

## 2. Commonwealth Operational Response Playbooks

Pre-configured response pathways have been elevated into **Operational Response Playbooks**:

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   COMMONWEALTH OPERATIONAL RESPONSE PLAYBOOKS                           │
├───────────────────────────────────────────────────────────────────┬─────────────────────────────────────┤
│ Playbook Designation                                              │ Lead Authority & Trigger Criteria   │
├───────────────────────────────────────────────────────────────────┼─────────────────────────────────────┤
│ 1. Whole-of-Government Novel Respiratory & Avian Flu Playbook     │ Lead: ACDP / Health / DAFF          │
│    • Scope: HPAI H5N1, Coronavirus spillover, airborne clusters.  │ Trigger: Confirmed novel zoonotic   │
│    • Sequence alignment, structural modeling, antiviral triage.   │ spillover or human cluster.         │
├───────────────────────────────────────────────────────────────────┼─────────────────────────────────────┤
│ 2. CBRN Fourth-Generation Neurotoxin Interdiction Playbook        │ Lead: DSTG CBRN / Home Affairs      │
│    • Scope: Novichok A-series, synthetic organophosphates.        │ Trigger: Sudden cholinergic         │
│    • Mass spec deconvolution, AChE docking, Obidoxime protocols.  │ toxidrome or CWC Schedule 1 match.  │
├───────────────────────────────────────────────────────────────────┼─────────────────────────────────────┤
│ 3. Radiological Dispersal Incident (Dirty Bomb) Emergency Playbook│ Lead: ARPANSA / ANSTO Lucas Heights │
│    • Scope: Industrial Caesium-137 / Cobalt-60 RDD detonation.   │ Trigger: Gamma photopeak >10 mSv/hr │
│    • HYSPLIT plume dispersion, Prussian Blue decorporation.       │ or uncontained radioactive release. │
├───────────────────────────────────────────────────────────────────┼─────────────────────────────────────┤
│ 4. Accelerated Antiviral Repurposing & TGA Section 19A Playbook   │ Lead: Therapeutic Goods Admin (TGA) │
│    • Scope: High-throughput virtual screening of ARTG molecules. │ Trigger: Immediate clinical demand  │
│    • Fast-track Section 19A regulatory exemptions.                │ prior to vaccine manufacturing.     │
├───────────────────────────────────────────────────────────────────┼─────────────────────────────────────┤
│ 5. Sovereign mRNA-LNP Rapid Design Playbook                       │ Lead: CSIRO / CSL Seqirus / Moderna │
│    • Scope: Pre-fusion stabilization, epitope engineering.        │ Trigger: Novel pandemic pathogen    │
│    • Sovereign domestic vaccine formulation and scale-up.         │ requiring on-shore manufacturing.   │
└───────────────────────────────────────────────────────────────────┴─────────────────────────────────────┘
```

---

## 3. Evidence Synthesis & Knowledge Gap Analysis Engine

The **Evidence Analyzer Engine** (`src/pandemic_prep_dash/core/evidence_analyzer.py`) continuously audits computational blackboard outputs to prevent premature operational decisions:

1. **Evidentiary Confidence Breakdown**:
   - Scores confidence across domains (Genomics, Structural Biology, Pharmacology, Transmission Dynamics, Biosecurity Law).
2. **Identification of Conflicting Evidence**:
   - Flags discrepancies between *in silico* predictions and real-world biological signals.
   - *Example*: In silico docking predicts strong Baloxavir binding (-8.6 kcal/mol), yet field deep-sequencing reveals a low-frequency (<3%) `I38T` substitution known to confer a 30- to 50-fold reduction in clinical susceptibility. The engine highlights the operational risk and recommends dual-agent combination therapy pending physical assay verification.
3. **Identification of Critical Knowledge Gaps**:
   - Flags missing empirical parameters required for public health legal orders.
   - *Example*: In silico sequence data cannot prove aerosol droplet transmission half-life; the engine warns that community isolation cordons cannot be legally enforced under the *National Health Security Act 2007* without empirical confirmation.
4. **Mandatory Empirical Validations**:
   - Automatically prescribes required physical tests (e.g. Ferret Airborne Challenge at ACDP Geelong PC4, IC50 Potency Verification at TGA Laboratories) with 1-click dispatch to the **Physical Lab Bridge**.

---

## 4. Situation Version Control & Progression Timeline

To ensure total transparency and retrospective auditability:
- **Immutable Situation Snapshots (`v1.0`, `v1.1`, `v1.2`)**:
  - Captures timestamp, triggering event (`INITIAL_INGESTION`, `NODE_STEP_COMPLETED`, `LAB_ASSAY_DISPATCHED`, `LAB_RESULTS_INGESTED`, `MANUAL_DUTY_OFFICER_CHECKPOINT`), logging officer, change summary, and completed node counts.
  - Guarantees that inquiries and Royal Commissions have a complete, tamper-proof record of what was known, what was predicted by autonomous agents, and what was authorized by human controllers at each juncture.

---

## 5. Automated Verification & Test Coverage

The test suite was expanded to **32 automated unit and integration tests** (`pytest -v`), achieving 100% pass rates:
- `test_evidence_analyzer_audit_endpoint`: Validates conflict detection, gap severity, and confidence scoring.
- `test_situation_version_control_timeline`: Validates checkpoint creation, chronological progression, and retrieval.
- `test_operational_playbooks_metadata`: Validates playbook titles, trigger criteria, and statutory lead authorities.
- `test_architecture_documentation_chapter`: Validates technical specifications and system diagrams in Chapter 8.
- All previous 28 tests for DAG pipelines, physical lab bridges, governance, and agency dispatches remain fully verified.

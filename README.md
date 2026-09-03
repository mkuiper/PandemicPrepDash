# PandemicPrepDash 🛡️🦘

**Adaptive Whole-of-Australian-Government CBRN & Pandemic Preparedness Dashboard with Agentic Workflow Pathways**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)](https://fastapi.tiangolo.com)
[![Tests Passing](https://img.shields.io/badge/tests-11%20passed-brightgreen.svg)](https://pytest.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 1. Executive Summary

**PandemicPrepDash** is an incident preparedness and emergency countermeasure platform designed for the **Australian Whole-of-Government (WoAG)** health security and biosecurity ecosystem.

Unlike static emergency plans or linear scripts, PandemicPrepDash models incident response as an **editable, Directed Acyclic Graph (DAG) response pathway**. Each node in the pathway can be dynamically configured, connected, and assigned to specialized **agentic scientific teams** (Bioinformatics, Structural Biology, Medicinal Chemistry, Vaccinology, CBRN Biosecurity, and Government Liaison).

As data arrives (e.g. a raw nucleotide sequence, chemical SMILES, mass spectrometry peaks, or syndromic records), the agent teams concurrently execute analytical tools, populate a shared intelligence blackboard, and automatically synthesize tailored briefings for statutory Australian agencies—including the **Australian Centre for Disease Control (Interim ACDC)**, **Therapeutic Goods Administration (TGA)**, **Department of Agriculture, Fisheries and Forestry (DAFF)**, **Defence Science and Technology Group (DSTG)**, **National Emergency Management Agency (NEMA)**, and **Department of Foreign Affairs and Trade (DFAT)**.

---

## 2. Key Features

- 🧬 **Adaptive DAG Response Engine**: Non-linear response pathways that fork concurrently (e.g., structural biology and biosecurity running in parallel, followed by simultaneous drug repurposing and vaccine design) and converge into government briefings. Built on NetworkX with strict cycle detection.
- 👥 **Configurable Agentic Teams**: Pre-configured multi-agent squads with specific domain personas (Dr. Elena Rostova, Dr. Marcus Vance, Dr. Priya Sharma, Dr. Liam O'Connor, Cdr. Jack Sterling, Alison Bradley PSM) logging transparent deliberation traces (`Observation` ➔ `Hypothesis` ➔ `Tool Execution` ➔ `Synthesis`).
- 🏛️ **Whole-of-Australian-Government (WoAG) Integration**: Direct statutory alignment with the *National Health Security Act 2007*, *Biosecurity Act 2015*, *Therapeutic Goods Act 1989*, and *Gene Technology Act 2000*. Synthesizes tailored situational reports for 8 Commonwealth agencies with dispatch simulation and Markdown export.
- 🛡️ **Human-in-the-Loop (HITL) Gatekeepers**: Crucial statutory checkpoints (e.g. Tier 1 SSBA classification, dual-use attribution) automatically pause the pipeline until an authorized human operator reviews and approves the findings.
- 🧪 **Multi-Domain CBRN Support**: Ready for both biological and chemical hazards:
  1. **H5N1 Avian Influenza (Clade 2.3.4.4b):** Zoonotic spillover with mammalian adaptation markers (PB2 E627K, HA Q226L), Tamiflu/Xofluza screening, and mRNA vaccine candidate formulation.
  2. **Novel Engineered Coronavirus (Variant Tartarus):** Polybasic furin cleavage insertion, ACE2 hyper-affinity, Paxlovid/Xocova docking, and DSTG synthetic origin forensics.
  3. **Synthetic Organophosphate Nerve Agent (Novichok Analogue):** Chemical SMILES ingestion, human acetylcholinesterase phosphorylation kinetics, and Atropine / Pralidoxime / HI-6 antidote protocols.
  4. **Custom Specimen Ingestion:** Real-time ingestion of arbitrary DNA/RNA/Protein sequences or chemical strings via web modal.
- 🖥️ **Interactive Command Dashboard**: Single-page web UI featuring an SVG DAG visualizer with draggable nodes, active execution status rings, node inspector, agency briefing document reader, molecular countermeasure inventory, and real-time agent thought feed.
- 🧪 **Comprehensive Test Suite**: 100% passing pytest suite covering graph invariants, cycle prevention, gatekeeper pauses, chemical pathways, agency reporting synthesis, and REST API endpoints.

---

## 3. Quickstart Guide

### Prerequisites
- Python 3.11+
- `uv` (recommended) or `pip`

### 3.1. Installation
```bash
# Clone the repository
git clone git@github.com:mkuiper/PandemicPrepDash.git
cd PandemicPrepDash

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

### 3.2. Launch the Application
```bash
# Start the FastAPI server with web frontend
.venv/bin/python -m pandemic_prep_dash.main
```
Open your browser to: **`http://localhost:8000`**

### 3.3. Running the Test Suite
```bash
.venv/bin/pytest -v
```

---

## 4. How to Use the Demo Mode

1. **Select a Threat Scenario:**
   - Use the top dropdown to toggle between **H5N1 Avian Flu**, **Novel Coronavirus**, or **Synthetic Nerve Agent Toxin**.
   - Or click **"+ Custom Specimen"** to ingest your own FASTA sequence or chemical SMILES string.
2. **Execute the Pathway:**
   - Click **"Step"** to watch the workflow advance one analytical stage at a time.
   - Or click **"Execute Pathway"** to run all ready stages.
3. **Inspect the Nodes & Agents:**
   - Click any node on the DAG canvas to inspect its assigned agent squad, latency, and outputs.
   - When the pipeline reaches **"CBRN Threat & SSBA Assessment"**, observe the **Human-in-the-Loop gatekeeper** pause execution until you review and click **"Authorize & Proceed"**.
4. **Review Inter-Agency Briefings:**
   - Navigate to the **"Whole-of-Gov Briefings"** tab.
   - Switch between **ACDC**, **TGA**, **DAFF**, **DSTG**, **NEMA**, **DFAT**, **CSIRO**, and **OGTR** to see tailored situation reports with statutory citations, action items, and cross-dependencies.
   - Click **"Dispatch to Agency"** or **"Export Markdown"** to download the brief.
5. **View Molecular Countermeasures:**
   - In the **"Targets & Countermeasures"** tab, inspect 3D protein targets (with pLDDT scores), repurposed drugs ranked by docking affinity and ARTG status, and candidate vaccine platforms.
6. **Follow the Agent Deliberation Feed:**
   - In the **"Agent Reasoning Feed"** tab, inspect the step-by-step thoughts and tool invocations of the scientific squads.

---

## 5. Australian Whole-of-Government Agency Mapping

| Agency | Portfolio | Primary Statutory Mandate & Alert Focus |
|---|---|---|
| **ACDC** | Health & Aged Care | Real-time genomic surveillance, CDNA national case definitions, R0 projections, and clinical guidance. |
| **TGA** | Health & Aged Care | Medical countermeasure evaluation, Section 19A emergency exemptions, ARTG registration, and batch testing. |
| **DAFF** | Agriculture, Fisheries & Forestry | One-Health zoonotic spillover tracking, ACVO alerts, livestock containment buffers, and BICON border controls. |
| **DSTG** | Defence | CBRN threat intelligence, dual-use gain-of-function screening, aerosolization risk, and attribution. |
| **NEMA** | Home Affairs | COMDISPLAN logistics, National Medical Stockpile burn rates, transport corridors, and Cabinet briefings. |
| **DFAT** | Foreign Affairs & Trade | WHO International Health Regulations (IHR 2005) Article 6 notification, Pacific regional health assistance. |
| **CSIRO ACDP** | Industry, Science & Resources | High-containment PC4 pathogen isolation (Geelong) and sovereign vaccine manufacturing (Clayton). |
| **OGTR** | Health & Aged Care | Gene Technology Act 2000 compliance, GMO viral vector licensing, and laboratory containment certification. |

*For full statutory and operational details, see [docs/australian_agencies.md](docs/australian_agencies.md).*

---

## 6. Architecture & Documentation Directory

- [ARCHITECTURE.md](ARCHITECTURE.md): In-depth software architecture, DAG execution semantics, NetworkX solver, blackboard state machine, and agent contract.
- [docs/australian_agencies.md](docs/australian_agencies.md): Institutional profiles, statutory acts, and cross-agency dependencies.
- [docs/scenarios.md](docs/scenarios.md): Walkthrough of H5N1, Coronavirus, and Nerve Agent reference datasets.
- [docs/adr/](docs/adr/): Architectural Decision Records:
  - [ADR-001: DAG Workflow Architecture](docs/adr/ADR-001-dag-workflow-architecture.md)
  - [ADR-002: Agentic Squad Contract](docs/adr/ADR-002-agentic-team-contract.md)
  - [ADR-003: Multi-Agency Briefing System](docs/adr/ADR-003-multi-agency-briefing-system.md)
  - [ADR-004: Human-in-the-Loop Security Gatekeeper](docs/adr/ADR-004-human-in-the-loop-gatekeeper.md)

---

## 7. Roadmap & Iteration Notes for Future Agents

For subsequent human and AI contributors extending this codebase:
1. **Live LLM Integration:** The `NodeExecutor` class is designed to seamlessly plug in external model providers (Gemini, Claude, OpenAI, or local Ollama) by swapping the reasoning generator in `pandemic_prep_dash/core/node_executor.py`.
2. **External Bioinformatics CLI Connectors:** Add connectors to call local `blastn`/`blastp`, `AlphaFold2`/`ESMFold` API, and `AutoDock Vina` binaries.
3. **Interactive 3D Molecular Viewer:** Integrate Mol* (3D Molstar viewer) into the Targets tab to display `.pdb` files for predicted protein targets directly in the browser.
4. **WebSocket / SSE Live Streaming:** Add real-time SSE push for long-running computational jobs.
5. **Additional Hazard Scenarios:** Add fungal pathogens (*Candida auris*), toxin proteins (Ricin / Botulinum), and industrial chemical leaks.

---

## 8. Git Repository

Repository: `git@github.com:mkuiper/PandemicPrepDash.git`
Branch: `main`
License: MIT

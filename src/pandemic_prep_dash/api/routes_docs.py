"""
Documentation & Operational Guidance API routes.
Serves multi-chapter reference manuals, statutory matrices, and MCP technical specifications.
"""

from fastapi import APIRouter
from typing import Dict, Any, List

router = APIRouter(prefix="/api/docs", tags=["Documentation"])

DOCS_CHAPTERS = [
    {
        "id": "conops-overview",
        "title": "1. Operational Overview & Whole-of-Government CONOPS",
        "icon": "fa-shield-halved",
        "category": "Architecture",
        "summary": "Core operational concepts, incident lifecycle, and autonomous multi-agent pipeline topology.",
        "content": """
# Operational Overview & Whole-of-Government CONOPS

The **PandemicPrepDash** platform is designed to provide Australia with an adaptive, auditable, and whole-of-government emergency response pipeline for emerging biological, chemical, and radiological (CBRN) threats.

### Core Operational Principles
1. **Dynamic Directed Acyclic Graph (DAG) Response Pathways:** Rather than a rigid linear workflow, response operations are represented as a configurable DAG. Analytical nodes (e.g. sequence ingestion, structural modeling, therapeutic docking, plume modeling) execute concurrently whenever their input dependencies are resolved.
2. **Autonomous Specialist Squads with Node Leads:** Each node is assigned an autonomous synthetic agent team led by a designated Node Lead. Squad leads coordinate with upstream and downstream node leads through an auditable inter-agent message protocol.
3. **Strictly Functional Agent Design:** Agents use clear, professional functional designations (such as `Genomics Lead`, `Structural Biology Lead`, `Health Physics Lead`, and `Biosecurity Analyst`) to eliminate any confusion between autonomous synthetic reasoning and human authority.
4. **Universal Human-in-the-Loop (HITL) Oversight:** Every node in the pathway features configurable human oversight controls, allowing Commonwealth statutory duty officers (e.g. ACDP diagnostic controllers, TGA evaluators, or ARPANSA radiation inspectors) to review evidence, input signoff notes, and authorize or hold critical downstream operations.
5. **Targeted Agency Relevance:** Not all Australian authorities require emergency dispatches for every event. The engine automatically filters notifications so that only agencies with statutory jurisdiction receive active situation briefs, while unrelated authorities are placed on automated standby.
        """,
    },
    {
        "id": "central-data-hub",
        "title": "2. Central Information Hub & Blocker Alert System",
        "icon": "fa-server",
        "category": "Data Management",
        "summary": "Real-time blackboard data aggregation, intelligence collation, and operational blocker alerts.",
        "content": """
# Central Information Hub (Blackboard) & Blocker Alerts

The **Central Information Hub** acts as the single source of truth across all pathway operations. As autonomous squads execute tasks, their structured findings stream directly into the Central Data Hub.

### Collated Intelligence Streams
* **Specimen & Threat Identification:** Raw payload inspection, computed GC content, taxonomy classification, and signature mutations (e.g. multi-basic furin cleavage sites, PB2 E627K).
* **Live Literature Surveillance:** Curated and real-time PubMed peer-reviewed papers, PMIDs, journal citations, and corroborated clinical evidence.
* **Macromolecular Targets:** AlphaFold / ESMFold predicted 3D structures, pLDDT confidence metrics, binding pocket volumes (Å³), and druggability indices.
* **Medical Countermeasures:** Candidate antivirals, antidotes, and decorporation agents ranked by binding affinity (kcal/mol), TGA ARTG regulatory status, and National Medical Stockpile (NMS) availability.
* **Atmospheric & Plume Dispersion:** HYSPLIT particulate trajectory modeling, ground deposition contours (Bq/m²), and urgent protective action zones.
* **Statutory Compliance:** Security Sensitive Biological Agent (SSBA) tiers, Chemical Weapons Convention (CWC) schedules, and ARPANSA Emergency Reference Levels (ERL).

### Blocker Alert Mechanism
When a node squad encounters an operational blocker or critical safety threshold:
1. The Node Lead raises a structured `BlockerAlert` with severity (`INFO`, `WARNING`, `CRITICAL`), title, description, and required action.
2. The alert is logged to the Central Orchestrator and displayed prominently on the operator dashboard.
3. Downstream dependent nodes can be automatically gated until the designated human controller reviews the situation and resolves the blocker with timestamped authorization notes.
        """,
    },
    {
        "id": "threat-research-nodes",
        "title": "3. Automated Threat Research & Literature Surveillance",
        "icon": "fa-book-open-reader",
        "category": "Scientific Research",
        "summary": "Real-time query of PubMed / NCBI E-Utilities, BioRxiv, and peer-reviewed clinical literature.",
        "content": """
# Automated Threat Research & Literature Surveillance

A foundational capability of the platform is the **Threat Research & Scientific Intelligence Squad**, which executes automated literature queries at the start of any emerging incident.

### How Research Nodes Function
1. **Target Extraction:** The researcher node extracts the provisional taxonomy, pathogen genus, or chemical/radiological identifier from the ingested specimen.
2. **Live NCBI PubMed Query:** The node invokes the National Center for Biotechnology Information (NCBI) E-Utilities API (`esearch` and `esummary`) to search for peer-reviewed studies, clinical reports, and animal transmission investigations.
3. **Evidence Extraction:** The squad parses returned publications for:
   * Confirmed transmission routes (e.g. airborne droplet, aerosol, waterborne, fomite)
   * Animal reservoir hosts and spillover dynamics (e.g. wild migratory waterfowl to domestic cattle/poultry)
   * Therapeutic sensitivity (e.g. oseltamivir susceptibility, oxime aging kinetics, Prussian Blue decorporation efficacy)
4. **Corroboration Dialogue:** The Research Lead initiates an inter-node dialogue with the Genomics Lead and Structural Biology Lead, transmitting validated mutation coordinates and literature citations to calibrate in silico simulations.
        """,
    },
    {
        "id": "mcp-toolbox-spec",
        "title": "4. Model Context Protocol (MCP) & Software Toolbox",
        "icon": "fa-plug",
        "category": "Integration",
        "summary": "Standard JSON-RPC 2.0 architecture, tool calling interfaces, and external server connection guide.",
        "content": """
# Model Context Protocol (MCP) & Computational Software Toolbox

The platform integrates standard computational bioinformatics and chemical defense executables with the open **Model Context Protocol (MCP)** specification.

### What is Model Context Protocol (MCP)?
MCP is an open standard developed to enable AI models and autonomous squads to securely interact with local tools, scientific databases, and external data sources via standard JSON-RPC 2.0 over standard I/O (stdio) or Server-Sent Events (SSE).

### Standard Toolbox Executables
* **BLAST+ (v2.15.0):** Local or remote NCBI basic local alignment search tool for nucleotide and protein sequence identity.
* **AlphaFold 3 / ESMFold:** Deep learning macromolecular structural prediction engines computing atomic coordinates and residue-level pLDDT confidence scores.
* **AutoDock Vina (v1.2.5):** Molecular docking engine calculating free binding energies (kcal/mol) of small-molecule ligands against macromolecular pockets.
* **RDKit (v2024.03):** Chemoinformatics suite calculating SMILES fingerprints, molecular weights, logP lipophilicity, and CWC Schedule 1/2 functional group alerts.
* **HYSPLIT-Rad:** Hybrid Single-Particle Lagrangian Integrated Trajectory atmospheric plume dispersion model for chemical vapor and radioactive particulate fallout.
* **SSBA Regulatory Checker:** Commonwealth statutory database verifying Security Sensitive Biological Agent (SSBA) schedules under the *National Health Security Act 2007*.

### Connecting Custom External MCP Servers
To connect an external MCP server to a node squad:
1. Launch the server process exposing the MCP JSON-RPC protocol (e.g. `npx -y @modelcontextprotocol/server-ncbi` or `python -m my_custom_mcp_server`).
2. Register the command and arguments in the Node Inspector or Squad Configuration modal.
3. The node squad discovers available tools via `tools/list` and executes queries via `tools/call` with automated parameter validation.
        """,
    },
    {
        "id": "statutory-acts-matrix",
        "title": "5. Australian Statutory Powers & Agency Mandates",
        "icon": "fa-landmark",
        "category": "Governance",
        "summary": "Comprehensive overview of Commonwealth emergency legislation, statutory triggers, and agency roles.",
        "content": """
# Australian Statutory Powers & Agency Activation Matrix

All Whole-of-Government briefs generated by the platform are grounded in specific Commonwealth Acts of Parliament.

### Statutory Authorities & Legislative Basis
1. **Australian Centre for Disease Prevention (ACDP / CSIRO):**
   * *Legislation:* [National Health Security Act 2007 (Cth)](https://www.legislation.gov.au/Details/C2021C00122)
   * *Mandate:* Operates high-containment PC4 laboratories at Geelong. Provides definitive national diagnostic confirmation, pathogen isolation, and SSBA initial notifications.
2. **Therapeutic Goods Administration (TGA):**
   * *Legislation:* [Therapeutic Goods Act 1989 (Cth)](https://www.legislation.gov.au/Details/C2022C00289)
   * *Mandate:* Grants emergency medicine approvals, expedited batch release, and Section 19A emergency exemptions to import unapproved foreign therapeutics.
3. **Department of Agriculture, Fisheries and Forestry (DAFF):**
   * *Legislation:* [Biosecurity Act 2015 (Cth)](https://www.legislation.gov.au/Details/C2021C00424)
   * *Mandate:* Animal and plant biosecurity, border entry points, quarantine zones, and AUSVETPLAN activation for emergency animal diseases.
4. **Australian Radiation Protection and Nuclear Safety Agency (ARPANSA):**
   * *Legislation:* [Australian Radiation Protection and Nuclear Safety Act 1998 (Cth)](https://www.legislation.gov.au/Details/C2016C00965)
   * *Mandate:* Radiation protection regulator. Establishes Emergency Reference Levels (ERLs), conducts plume dose assessments, and advises on public sheltering/evacuation.
5. **Australian Nuclear Science and Technology Organisation (ANSTO):**
   * *Legislation:* [Australian Nuclear Science and Technology Organisation Act 1987 (Cth)](https://www.legislation.gov.au/Details/C2016C00966)
   * *Mandate:* Nuclear forensics at Lucas Heights, HPGe gamma spectrometry, thermal ionization mass spectrometry (TIMS), and radioactive source attribution.
6. **Australian Safeguards and Non-Proliferation Office (ASNO):**
   * *Legislation:* [Nuclear Non-Proliferation (Safeguards) Act 1987 (Cth)](https://www.legislation.gov.au/Details/C2018C00286)
   * *Mandate:* International non-proliferation compliance, IAEA Incident and Trafficking Database (ITDB) reporting, and OPCW chemical weapons declarations.
7. **National Emergency Management Agency (NEMA):**
   * *Legislation:* [National Emergency Declaration Act 2020 (Cth)](https://www.legislation.gov.au/Details/C2020A00128)
   * *Mandate:* Commonwealth disaster coordination, National Situation Room (NSR), National Medical Stockpile logistics, and COMDISPLAN activation.
8. **Defence Science and Technology Group (DSTG):**
   * *Legislation:* [Defence Act 1903 (Cth)](https://www.legislation.gov.au/Details/C2017C00350) & [Weapons of Mass Destruction Act 1995 (Cth)](https://www.legislation.gov.au/Details/C2016C00843)
   * *Mandate:* Sovereign CBRN defense research, chemical/biological weapon forensics, and Australian Defence Force (ADF) force health protection.
9. **Department of Home Affairs:**
   * *Legislation:* [Security of Critical Infrastructure Act 2018 (Cth)](https://www.legislation.gov.au/Details/C2022C00155)
   * *Mandate:* National Counter-Terrorism Plan (NCTP), critical infrastructure security (ports, transport, utilities), and Australian Border Force (ABF) interdiction.
10. **Office of the Gene Technology Regulator (OGTR):**
    * *Legislation:* [Gene Technology Act 2000 (Cth)](https://www.legislation.gov.au/Details/C2021C00201)
    * *Mandate:* Regulation of genetically modified organisms (GMOs) and synthetic biology constructs. Issues Emergency Dealing Determinations (EDD).
        """,
    },
    {
        "id": "cbrn-playbooks",
        "title": "6. CBRN Emergency Response Playbooks",
        "icon": "fa-biohazard",
        "category": "Operations",
        "summary": "Standard operating procedures for Biological, Chemical, and Radiological incidents.",
        "content": """
# CBRN Emergency Response Playbooks

### Playbook A: Highly Pathogenic Avian Influenza (HPAI H5N1 Clade 2.3.4.4b)
1. **Specimen Ingestion:** Collect respiratory or organ swab in viral transport medium. Ingest FASTA sequencing reads.
2. **Literature Surveillance:** Query PubMed for clade 2.3.4.4b mammalian adaptation markers and antiviral resistance mutations.
3. **Genomic Alignment:** Confirm multi-basic furin cleavage motif (PQRESRRKKR*GLF) and PB2 E627K mammalian polymerase adaptation.
4. **Target Resolution & Antivirals:** Model neuraminidase (NA) and RNA-dependent RNA polymerase (RdRp). Screen Oseltamivir and Baloxavir marboxil.
5. **Vaccine Design:** Identify conserved hemagglutinin head epitopes. Design stabilized pre-fusion mRNA-LNP construct for domestic CSL Seqirus / Moderna Victoria production.
6. **Statutory Reporting:** Issue notifications to ACDP, DAFF (animal biosecurity), TGA (vaccines), and NEMA.

### Playbook B: Organophosphate Nerve Agent / Chemical Threat
1. **Hazard Ingestion:** Ingest GC-MS spectral peaks, SMILES chemical structure, and ambient air ppb sensor data.
2. **Toxicology Research:** Retrieve literature on aging half-life and central nervous system reactivation profiles.
3. **Molecular Fingerprinting:** Verify Chemical Weapons Convention (CWC) Schedule 1 listing and phosphorylating core (P=O).
4. **Docking & Antidotes:** Model acetylcholinesterase (AChE) active gorge. Check availability of Pralidoxime (2-PAM), Obidoxime, and Atropine.
5. **Containment Gate:** Calculate volatile plume hazard perimeter and require Police HAZMAT and DSTG signoff.
6. **Reporting:** Dispatch priority alerts to DSTG CBRN, NEMA, TGA, and Home Affairs.

### Playbook C: Radiological Dispersal Incident (Caesium-137 Dirty Bomb)
1. **Detection & Gamma Spectrometry:** Acquire HPGe multichannel spectrum. Confirm 661.7 keV photopeak (Ba-137m) and quantify activity (TBq).
2. **Plume Modeling:** Run HYSPLIT atmospheric dispersion simulation. Map 10 mSv/hr inner cordon and 5 km Urgent Protective Action Planning Zone (UPZ).
3. **Decorporation Countermeasures:** Screen Prussian Blue (ferric hexacyanoferrate) ion-exchanger and Ca-DTPA chelation from National Medical Stockpile.
4. **Statutory Intervention Signoff:** ARPANSA Chief Radiation Health Scientist verifies Emergency Reference Levels under the *ARPANS Act 1998*.
5. **Reporting:** Transmit briefs to ARPANSA, ANSTO (Lucas Heights nuclear forensics), ASNO, and Home Affairs.
        """,
    },
]


@router.get("")
def list_docs():
    return {
        "chapters": [
            {
                "id": c["id"],
                "title": c["title"],
                "icon": c["icon"],
                "category": c["category"],
                "summary": c["summary"],
            }
            for c in DOCS_CHAPTERS
        ]
    }


@router.get("/{chapter_id}")
def get_doc_chapter(chapter_id: str):
    chapter = next((c for c in DOCS_CHAPTERS if c["id"] == chapter_id), None)
    if not chapter:
        return {"error": "Chapter not found"}
    return {"chapter": chapter}

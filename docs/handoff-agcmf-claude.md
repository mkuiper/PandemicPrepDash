# Handoff for Claude: integrate AGCMF into CBRN Rapid Response

You are continuing work on **CBRN Rapid Response**, a **workshop demonstrator**. The product sits **under** the Australian Government Crisis Management Framework (AGCMF). Agent crews **augment** a shared picture and human gates. They **do not replace** state first responders, the Lead Minister, the Coordinating Agency, the LCSO, the NCM, NSR, NSC, or an Incident Controller.

Read first (in this order):

1. `README.md`
2. `docs/agcmf-alignment.md`
3. `docs/reference/agcmf-september-2025.txt` (Appendix A from ~line 1873; Continuum ~405; 4-tier ~822)
4. Help chapter `agcmf-role` in `src/pandemic_prep_dash/api/routes_docs.py`
5. Flood/fire pattern: `scenarios/east_coast_low_flood.py`, `core/registry.py` (`create_default_severe_weather_pathway`), `core/engine.py` `set_scenario`, `static/app.js` `isCivilianIncident` / inspector tabs

Official AGCMF: https://www.pmc.gov.au/resources/australian-government-crisis-management-framework-agcmf  
Local PDF: `docs/reference/agcmf-september-2025.pdf` (v4.1, Sep 2025, CC BY 4.0).

Do **not** claim to be the NCM, NJCOP, or NSR. All new numbers, briefs, and “plans” are **simulated workshop fiction** unless they are quotes of public Framework role names.

---

## Pitch (keep this language)

- Augment AGCMF-style coordination; humans remain in charge.
- States/territories are first responders; the Commonwealth does not replicate them.
- Crisis coordination scope: **near-term preparedness → response → relief → early recovery**. Do not add operational Prevention or Reconstruction nodes.
- 4-tier scale is **Commonwealth coordination scale**, not a bigger BLAST/HYSPLIT job. Tier 4 = NEMA coordinates; PM is Lead Minister (may delegate).
- Playbook AGCMF fields are a **workshop mapping**, not a designation under the Framework.

---

## Current state (already done)

- Built-in playbooks have metadata: `agcmf_hazard`, `agcmf_national_plan`, `agcmf_coordinating_agency`, `agcmf_lead_minister`, `agcmf_lcso`, `agcmf_continuum` in `core/templates.py` `playbook_meta`.
- Pathway toolbar `#agcmfStrip` and playbook cards show plan + coordinating agency.
- Scenarios: H5N1, corona, nerve agent, Cs-137, East Coast Low flood, Erskine Park warehouse fire.
- Flood/fire DAGs already look more AGCMF-like (intake → evidence → HITL → brief → recovery). CBRN DAGs are still lab-heavy (sequence, docking) with a biosecurity HITL.
- Security layers in Cloud & Governance are labelled **NOT IMPLEMENTED**. Do not add fake OpenSCAP/ISM pass badges.

---

## What to implement (in order)

### 1. Shared AGCMF overlay fragment (required)

Add a factory, e.g. `create_agcmf_coordination_nodes(prefix, *, coordinating_agency, lcso_role, national_plan)` in `core/registry.py`, returning nodes + edges that can be **prepended/appended** to hazard-specific DAGs without deleting scientific nodes.

Suggested nodes (ids unique per playbook via prefix):

| Node | Category | HITL? | Purpose |
|---|---|---|---|
| `{prefix}_near_term` | `triage` | No | Near-term preparedness: named plan, Coordinating Agency, LCSO, surge. Simulated. |
| `{prefix}_picture` | `ingestion` or keep existing intake | No | Shared situational awareness sitrep (not NSR). |
| existing scientific / evidence nodes | unchanged | | Hazard picture. |
| existing or `{prefix}_protect` | HITL | **Yes** | Protective action; human is IC / LCSO stand-in. |
| `{prefix}_relief` | `triage` or `recovery` | No | Essential needs (thin, simulated). |
| existing `agency_reporting` | | No | Contributing agencies, not NSC. |
| `{prefix}_early_recovery` | `recovery` | No | Early recovery / stand-down. CBRN playbooks currently lack this. |
| `{prefix}_tier` | HITL optional | Optional | “Remain Coordinating Agency (tiers 1–3) vs note Tier 4 NEMA/PM”. Default **off** or a single non-blocking note unless you can do it cleanly. Prefer a **blocker/lead-context question**, not a second mandatory gate, so demos do not double-pause. |

Wire `set_scenario` / template load so biological, chemical, and radiological playbooks **gain** overlay nodes (especially early recovery + near-term preparedness). Flood/fire already have intake/recovery; add a thin near-term node or metadata-only if the DAG would get too busy.

Keep graphs valid DAGs (`validate_pathway_graph`). One primary HITL unless you have a strong reason.

Executor: new categories already exist (`triage`, `recovery`). Add `is_agcmf` or branch on node id prefix / label. **Do not** run BLAST/GC% on sitrep text. Inspector already hides sequence for `severe_weather` and `industrial_fire`; extend `inspectorToolsForThreat()` / sitrep viewer for any new non-sequence threat types.

Lead context: questions like “Who is Coordinating Agency under Appendix A?” citing `agcmf_coordinating_agency`. Answer **unknown** if missing.

### 2. Playbooks that follow Appendix A scenarios (required)

Add **two** new workshop scenarios that are clearly AGCMF Appendix A hazards we do not already own. Copy the flood/fire pattern (sitrep sample, conflicting reports, HITL, civilian-style UI).

**A. Domestic biosecurity — `scen_ausbioagplan_fmd` (or similar)**

- Hazard: Domestic biosecurity crises  
- Plan: **AUSBIOAGPLAN**  
- Coordinating agency: **DAFF**  
- LCSO: Deputy Secretary responsible for Biosecurity, DAFF  
- Lead minister: Minister responsible for Agriculture  
- Story (fiction): suspected FMD (or similar EAD) in livestock; state is first responder; Commonwealth picture + movement/standstill **recommendation** for human approval.  
- Pathway: intake sitrep → adjacent properties / unknown inventory of movements → evidence conflict → HITL (not a real standstill order) → DAFF/NEMA/Health briefs (Health standby unless zoonotic) → early recovery.  
- `ThreatType`: add something like `BIOSCURITY_ANIMAL` / `agricultural_biosecurity`. Do **not** fall through to H5N1 BLAST.  
- Agencies: DAFF relevant; ACDP as **lab support** not Coordinating Agency; TGA/OGTR standby unless you have a reason.

**B. Second Appendix A pick — choose one:**

- **Cyber** (`AUSCYBERPLAN`, Home Affairs / National Cyber Security Coordinator, NCM + IDETF), **or**
- **Space weather** (NEMA coordinating in Appendix A — confirm in the PDF/txt around “Space weather events”), **or**
- **Domestic energy supply** (DCCEEW; NLFERP / ITGSP / PSEMP).

Prefer **cyber** or **energy** if you want a non-CBRN AGCMF demo that is still “national picture + HITL”. Keep it a coordination DAG, not a SOC product. No live scans, no “we patched the grid”.

Register scenario, pathway, `playbook_meta`, `set_scenario` alignment, `StateManager.switch_pathway`, lab-bridge seeds as **proposals** (or none), evidence analyzer **before** the chemical `else`, `determine_relevance` so TGA does not talk Section 19A.

### 3. Existing CBRN playbooks (required, light)

- Biological default: metadata already NHERA / Health / CMO. Add overlay nodes; recovery node.  
- Radiological: keep **AUSRNEPLAN / ARPANSA** as coordinating agency; Lead Minister remains Health (workshop beat).  
- Chemical: NHERA HAZMAT health path unless the scenario is explicitly terrorism (then do not silently use DSTG as Coordinating Agency).  
- Do not make NEMA the lead on NHERA or AUSRNEPLAN runs.

### 4. Honesty and UI (required)

- Banner and Help already say augment / not NCM. Keep that.  
- New threats: sitrep inspector, not GC%/Oseltamivir defaults (`renderPipelineDataInspector`).  
- Agency briefs: `is_relevant` false → standby copy, no CBRN stockpile language.  
- Never label a node “National Coordination Mechanism” as if this app hosts it. “NCM-style picture (simulated)” is OK.  
- `auto_approve` stays API-only, default false.  
- Security layers stay **not implemented**.

### 5. Tests (required)

- Overlay: biological pathway after change still pauses once for HITL; completes after approve; has a recovery node.  
- New biosecurity scenario: `threat_type` not biological BLAST path; DAFF relevant; ACDP not Coordinating Agency in metadata; TGA not relevant.  
- Switching flood ↔ new scenario does not leak lab requests or hub drugs.  
- Evidence analyzer does not emit Novichok gaps for the new scenario.  
- Templates API: new playbook has `agcmf_national_plan` set.  
- JS: inspector does not invent Oseltamivir/GC% for the new sitrep type.  
- Existing CBRN tests still pass (`pytest -q`, `node --test tests/frontend.test.cjs`).  
- Bump `app.js?v=` in `static/index.html` if you change JS.

### 6. Docs (required)

- Update `docs/agcmf-alignment.md` mapping table.  
- `docs/scenarios.md` for new incidents (fiction + simulated).  
- Glossary if you add threat types.  
- Do not rewrite the whole CONOPS into a fake national plan.

---

## Help vs hinder (design test)

After your change, a facilitator should be able to say:

- “This node is the **hazard picture** (science).”  
- “This node is **near-term preparedness** under the Framework.”  
- “This pause is a **human** standing in for IC/LCSO.”  
- “This brief is a **contributing** agency, not the Coordinating Agency unless Appendix A says so.”

If a screen looks like the app just called out the ADF, closed a motorway, or convened NSC, you have gone too far. Pull it back to a recommendation + HITL + simulated label.

---

## Out of scope

- Live BOM, CAD, PubMed-as-truth, HYSPLIT, NCM/NSR feeds  
- Auth, MFA, OpenSCAP, IRAP  
- Terrorism playbook that looks operational (if you mention terrorism, keep it clearly workshop and do not add kill-chain chrome)  
- Renaming the Python package  
- Prevention/reconstruction programmes

---

## Suggested commit message

```
Add AGCMF overlay nodes and Appendix A workshop playbooks.

Shared near-term preparedness, relief, and early recovery sit under
NHERA / AUSRNEPLAN / AUSBIOAGPLAN mappings. Agents augment the
picture; they do not replace the NCM or state responders.
```

When done, run the full test suite and hard-refresh instructions (`app.js?v=`). Summarize for the human: what Appendix A hazards you added, where HITL maps to LCSO/IC, and what you refused to fake.

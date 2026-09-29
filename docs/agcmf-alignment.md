# Aligning playbooks with the AGCMF

Local copy of the official framework (CC BY 4.0, Commonwealth of Australia):

- PDF: [docs/reference/agcmf-september-2025.pdf](reference/agcmf-september-2025.pdf) (Version 4.1, September 2025)
- Text extract: [docs/reference/agcmf-september-2025.txt](reference/agcmf-september-2025.txt)
- Source: [pmc.gov.au — Australian Government Crisis Management Framework](https://www.pmc.gov.au/resources/australian-government-crisis-management-framework-agcmf)

This demonstrator is **not** the National Coordination Mechanism (NCM), the National Situation Room, or a national plan. It is a workshop sketch of how a CBRN (and related) pathway could **sit under** the Framework.

## What the Framework actually is

The AGCMF is the capstone **all-hazards** policy for how the Australian Government prepares for, responds to, and supports **early recovery** from significant crises. States and territories remain first responders. The Commonwealth does not replicate their capabilities.

**Continuum (7 phases).** The Framework’s crisis-coordination scope is only four of them:

| Phase | In AGCMF crisis coordination? | Demo implication |
|---|---|---|
| Prevention | No | Do not fake prevention programmes in the DAG |
| Preparedness (incl. **near-term preparedness**) | Yes (near-term) | First nodes: sitrep, surge, plans, designated roles |
| Response | Yes | Protective action, HITL, scientific characterisation |
| Relief | Yes | Essential needs (shelter, medical, comms) — thin in current CBRN DAGs |
| Early recovery | Yes | Stand-down / restoration nodes (flood/fire have a start) |
| Reconstruction | No | Out of scope |
| Risk reduction | No | Point to the National Disaster Risk Reduction Framework |

**Roles (do not displace ministers’ existing duties):**

- **Lead Minister** — advice to the Prime Minister and NSC
- **Australian Government Coordinating Agency** — whole-of-government coordination for the designated hazard
- **Lead Coordinating Senior Official (LCSO)** — agency lead supporting the minister

**4-tier coordination** (scale of *Australian Government* coordination, not a scientific severity score):

1. Limited — Coordinating Agency
2. Major — Coordinating Agency
3. Severe — Coordinating Agency
4. Extreme/catastrophic — **NEMA** coordinates; Prime Minister is Lead Minister (may delegate)

**Mechanisms:** NSC (ministers); **NCM** / **NCM-AUSGOV** (senior officials, NEMA secretariat); IDETF (international, DFAT); NSR, NJCOP.

## Appendix A mapping for our playbooks

From AGCMF Appendix A (identified hazards). Workshop labels only.

| Current playbook | AGCMF identified hazard | National plan | Coordinating agency | LCSO (Framework) | Typical demo tier |
|---|---|---|---|---|---|
| Biological / avian flu / corona | Domestic public health crises | NHERA | Department of Health, Disability and Ageing | Chief Medical Officer | 2–3 |
| Rapid antiviral / sovereign vaccine | Support to the same public-health hazard (not a separate national plan) | NHERA (enabling) | Health / TGA as contributing agencies | CMO | 2 |
| Chemical / nerve agent (non-terror) | Public health: hazardous material with nationally significant health consequences | NHERA | Health | CMO | 2–3 |
| Chemical if terrorism | Domestic terrorist incidents | (counter-terrorism arrangements) | Home Affairs | National security lead | 3–4 |
| Radiological / nuclear (non-terror) | Radiological/nuclear incidents | AUSRNEPLAN | **ARPANSA** | Chief Radiation Health Scientist / CEO ARPANSA | 2–3 |
| East Coast Low / flood | Domestic natural hazard disasters | COMDISPLAN | **NEMA** | DCG Emergency Management and Response, NEMA | 2–3 |
| Industrial warehouse fire | Often **state first response** (FRNSW). If nationally significant health/HAZMAT → NHERA; if disaster-scale → COMDISPLAN | NHERA or COMDISPLAN | Health or NEMA | CMO or NEMA DCG | 1–2 unless it scales |
| International CBRN affecting Australians | International crises | ICMF | DFAT | DS Consular and Crisis Management | IDETF, not NCM first |

Lead Minister for public health and radiological/nuclear (non-terror) is the **Minister responsible for Health**. Natural disasters: **Minister responsible for Emergency Management**. That is a useful workshop beat: ARPANSA coordinates AUSRNEPLAN, but the Lead Minister is Health, not a lab director.

## How to remake templates (recommended, not a big-bang rewrite)

Keep the **scientific nodes** (sequence, docking, HYSPLIT-shaped contour). They are the *hazard picture*, not the national plan.

Add an **AGCMF coordination overlay** that every playbook can share:

1. **Near-term preparedness** — designated roles, national plan name, surge, what the Coordinating Agency already owns
2. **Shared situational awareness** — sitrep for NCM-style picture (simulated; we are not the NSR)
3. **Response / protective action (HITL)** — map to LCSO or Incident Controller; states remain first responders
4. **Consequence / relief** — hospitals, shelter, essential services (already stronger on fire/flood)
5. **Agency briefs** — contributing agencies, not a fake NSC
6. **Early recovery / stand-down** — already on flood/fire; add a thin node to CBRN playbooks
7. **Tier review** — optional HITL: stay at Coordinating Agency (1–3) or note NEMA/PM for Tier 4

**Playbook metadata** (now on built-in templates) should carry: AGCMF hazard, national plan, coordinating agency, lead minister, LCSO, continuum focus. The scientific DAG stays hazard-specific.

**Do not**

- Rename the product to NCM or claim NJCOP/NSR connectivity
- Put Prevention or Reconstruction nodes that look operational
- Make NEMA the lead on every CBRN run (wrong for NHERA and AUSRNEPLAN)
- Treat Tier 4 as a bigger BLAST job — it is a change of **coordination scale**

## Opinion

Yes, align with the AGCMF. It is the right capstone for a Commonwealth workshop, and it explains why our flood/fire paths felt more “incident-like” than the lab-heavy CBRN DAGs: they already resemble near-term preparedness → response → recovery.

The high-value remake is **metadata + a shared coordination spine**, not deleting genomics. Next implementation step, if you want it: one shared “AGCMF overlay” pathway fragment merged onto the biological default, with NHERA roles on the inspector, still labelled simulated.

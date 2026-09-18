# Factory fire, dispersal, and designed failure

Workshop design note. The **Erskine Park warehouse fire** pathway is now in the
demonstrator (`scen_industrial_warehouse_fire`). Inventories, winds, contours,
and hospital loads remain fiction.

## Role of this platform (second eyes)

Crews and agencies already have practised protocols (AIIMS, fire, ambulance,
EPA). This dashboard must not replace those. It is a **shared picture and a
second set of eyes** on an evolving event:

- Start from **this site**, not a canned suburb the system already “knew”.
- Look up **adjacent sites and populations** as the next risk, the way a
  planning officer would ask “what’s next door?”
- Offer a **planning contour** (HYSPLIT-shaped, simulated) so the Incident
  Controller can compare model vs field.
- **Record what happened, in order**, so the run can be replayed in an
  after-action review and used to improve the later platform.

Agent squads here are guides: they assemble sitrep, neighbour hazards, weather,
and a contour, then stop for a human. They do not dispatch appliances or close
a motorway.

## Dynamic site-first assessment

The next accident will not be at a pre-written coordinate. The intended loop is:

1. Pin the burning site (address / estate / lat-long later).
2. Simulated cadastral / dangerous-goods lookup of neighbours (tank farm,
   school, hospital). Unknown inventory is a first-class result.
3. Pull met for *that* location and time (BOM product; simulated today).
4. Run a dispersal estimate whose inputs are site + materials + weather.
5. Hold protective action, traffic, and hospital diversion for the IC.

Today the lookup table is in the scenario file. A later platform would geocode
and query real registers, with the same “unknown / stale / conflict” states.
Do not hard-wire only Erskine Park as if that were the product.

## Event recording for diagnostics

Each run appends an **incident event log** (scenario selected, node completed,
approval required, approval granted, failure). It is in-memory with the run,
not a tamper-proof archive. Use it in the workshop to walk “what did we know
when we approved?” After-action use is the requirement for the later platform:
durable, actor-bound, exportable events.

## Why a factory fire

A warehouse or factory fire with a toxic plume is a better civilian coordination
demo than another CBRN set-piece. Agencies already run these: fire service as
combat agency, EPA on air and runoff, health and ambulance on exposure, local
government on shelter and traffic, BOM on meteorology. Participants will
recognize the decisions. The demonstrator’s job is to make those decisions
visible, contested, and pauseable — not to predict a real plume.

Radiological and chemical playbooks already *mention* HYSPLIT. The fire case
reuses that idea for a common hazard: weather in, planning contour out, field
observations that disagree, then a human gate on evacuate / shelter-in-place /
road closure.

## Suggested incident (workshop fiction)

A plastics and solvent warehouse fire on an industrial estate beside a motorway,
with a school and a district hospital within a few kilometres. Adjacent sites
include a tank farm whose inventory is incomplete on first call. Night-time
inversion, light onshore wind that is forecast to shift.

Decisions the session should force:

1. What is burning, and what is next door that might become involved?
2. Where does the plume go in the next 1–6 hours, and how uncertain is that?
3. Shelter-in-place vs evacuate, and which way traffic is allowed to move.
4. Which hospital takes contaminated / smoke-exposed patients, and which is
   downwind and must divert.
5. What the public is told, by whom, and when.

Do not require SSBA, vaccines, or Section 19A. If those appear, the generic
incident model has failed again.

## Pathway slice (in the demonstrator)

Same spine as flood, with an adjacent-risk node instead of hydrology triage.
HYSPLIT is a **named simulated method** on a planning contour; wind is an input
in the sitrep, not a live NOAA run.

| Node | Owner (workshop role) | Produces | Pause? |
|---|---|---|---|
| Incident intake | Fire / IMT watch | Location, time, fuel, first 000 narrative | No |
| Site and adjacent inventory | Fire / EPA / SafeWork | On-site dangerous goods + neighbour unknowns | No |
| Weather input | BOM liaison | Wind, stability, rain; labelled simulated | No |
| Dispersal estimate (HYSPLIT-shaped) | Transport / air-quality squad | Planning contour + assumptions + provenance | No |
| Field vs model | EPA / fire recon | Conflict: monitor or smell reports ≠ contour | No |
| Protective action | Incident Controller | Evacuate, shelter, road/motorway, hospital diversion | **Yes** |
| Agency and hospital briefs | PIO / liaison | Fire, EPA, health, council, BOM, ambulance — different views | No |
| Traffic and population | Police / council / TfNSW-style | Contraflow, do-not-enter-plume, assembly points | After approval |
| Recovery / re-entry | IC + EPA | Air-clearance and re-entry conditions | No |

HYSPLIT in this demonstrator means: **a named method on a simulated contour**,
with wind as an input you can change in the workshop. It does not mean NOAA
HYSPLIT is running. If a later platform wires a real model, tag the artifact
`computed` or `retrieved` and keep the simulated contour available as a fallback
inject.

## Civilian agencies to preview (not authorize)

Combat and consequence, not CBRN leads:

- State fire service (combat agency)
- EPA (air, runoff, advice to IC)
- Ambulance / state health (surge, decon of walk-ins, hospital diversion)
- Local government (shelter, welfare)
- Police / traffic authority (motorway, do-not-drive-into-plume)
- BOM (meteorology only)
- NEMA on standby unless it scales
- SafeWork / dangerous-goods regulator on inventory

ACDP, TGA, OGTR, ARPANSA stay off the primary list unless the inventory
unexpectedly includes a scheduled CBRN material — that itself is an inject.

## Where this demonstrator fails today

These are software and product limits. Say them in the room.

| Failure | What participants will see | Design implication for the later platform |
|---|---|---|
| One shared in-memory incident | Every browser mutates the same run | Incident-scoped durable state |
| No agency identity | Everyone sees every brief | Server-side need-to-know before serialize |
| Scripted science | HYSPLIT, inventory, and gauges do not compute | Provenance: simulated / imported / computed / retrieved |
| Sequential DAG | Fire, EPA, and hospitals cannot “work in parallel” | Concurrent tasks with invalidation rules |
| Checkpoints are summaries | Reset wipes the story | Append-only decision log bound to an actor |
| Auto-approve still exists on the API | A client can skip the IC gate | Approvals are authorized actions, not flags |
| Silent literature/model fallback | A contour or citation can appear with no live source | Fail visibly; never substitute without a label |
| HTML still interpolated in some views | Hostile workshop data can break the UI | Text nodes + sanitizer; browser tests |

A convincing factory-fire UI that hides these is worse than a sparse one that
states them.

## Where a real factory-fire response fails (workshop gold)

Use these as **injects**, not as extra chrome. Each inject should change a
decision, not only a chart.

1. **Unknown inventory** — dangerous-goods manifest is 18 months old; adjacent
   tank farm will not confirm contents in the first hour.
2. **Wrong or shifting wind** — BOM update reverses the contour after traffic
   has already been sent that way.
3. **Model / field disagreement** — EPA handhelds or public smell reports
   outside the planning contour.
4. **Hospital is downwind** — the “receiving” ED is inside the shelter zone;
   ambulance needs a new destination and a decon story for walk-ins.
5. **Motorway still open into the plume** — traffic authority and IC disagree
   on who can close it.
6. **Public message races the IC** — a council or media post uses an old
   contour.
7. **Runoff vs air** — EPA wants bunding and drain closure while fire is still
   in offensive attack; two “correct” actions conflict.
8. **Comms or connector down** — BOM product, hospital bed state, or CAD
   incident number does not arrive; the system must show *unknown*, not last
   week’s value.
9. **Dual-hat authority** — SafeWork wants the site frozen for investigation
   while fire wants overhaul; who wins, and what is recorded.
10. **Re-entry pressure** — businesses want the motorway open; air clearance
    is not yet agreed.

Capture for each inject: who noticed, what they needed, what they must not see,
what would constitute a wrong decision, and an acceptance test for the later
platform.

## Chaos engineering as a design tool

Two layers. Do not conflate them.

### 1. Workshop chaos (tabletop injects)

This is the high-value use **now**. A facilitator toggle or scripted event that
breaks one assumption mid-run:

- Swap the wind vector after the dispersal node has completed.
- Blank the adjacent-site inventory.
- Mark the nearest hospital `unknown` or `divert`.
- Delay or fail the BOM product and force the IC to approve on incomplete met.
- Publish a second, conflicting contour from “EPA field”.

The DAG should **invalidate** downstream artifacts or show them stale. If the
UI still shows the first cordon as current, that is a finding, not a feature.

This is closer to emergency-management injects than to Netflix chaos. It
produces requirements: stale-data rules, dual-source evidence, approval
re-open conditions, and “unknown” as a first-class state.

### 2. Platform chaos (later, against a real system)

Once there is more than one process and a real store, attack the software:

- Concurrent Run / Reset / Approve / Select-scenario.
- Kill the worker mid-briefing export.
- Poison a blackboard artifact and see whether briefs still go out.
- Partition the “BOM connector” and watch fallback labelling.
- Replay an approval token; duplicate a lab/field request id.

Those experiments belong in tests and staging, not in the facilitated demo,
except as stories: “if two operators hit Approve, what should happen?”

A minimal design rule: **every external input has a failure mode that is
visible in the UI** (missing, stale, conflict, simulated). Chaos is how you
check the rule. Adding more agent personas without failure modes makes the
demo less robust, not more.

## What not to build yet

- A live HYSPLIT or meteorological pipeline.
- Real hospital, CAD, or traffic feeds.
- A full multi-agency ICS org chart.
- Auth “because fire is civilian” — the access questions are the workshop;
  enforcement is the later platform.

Build next only if agencies agree the fire story is the session they will
attend: simulated inventory + weather-driven contour + one serious conflict +
IC gate + hospital/traffic briefs, with injects for wind shift and unknown
neighbours.

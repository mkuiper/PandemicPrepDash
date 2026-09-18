# Agency feedback workshop

## Purpose

Use the demonstrator to learn how agencies coordinate decisions and share evidence.
Record requirements for the larger platform, including places where agencies have
different needs. Use synthetic incident data and state explicitly which outputs
and integrations are simulated.

## Suggested 45-minute session

| Time | Activity | What to learn |
|---|---|---|
| 0–5 min | Choose an incident and a decision the agency needs to make | Whether the scenario and outcome are relevant |
| 5–15 min | Follow intake, evidence, and response pathway | Missing inputs, handoffs, ownership, and terminology |
| 15–25 min | Pause for human approval; introduce a conflicting report | Who can decide, evidence thresholds, dissent, and escalation |
| 25–35 min | Compare agency briefing previews | Minimum necessary information, redactions, timeliness, and sharing authority |
| 35–45 min | Review checkpoint and capture feedback | What would make the workflow usable, credible, and auditable |

## Capture each observation

- Agency and participant role (record names only when needed and agreed).
- Decision or task being attempted.
- Information required and information that should be withheld.
- Observed difficulty, missing capability, or unclear assumption.
- Consequence: inconvenience, delay, incorrect decision, or inappropriate disclosure.
- Proposed behavior and an example acceptance test.
- Priority, requirement owner, unresolved question, and follow-up date.

Measure task completion, missed information, approval delays, and uncertainty
understanding. Do not rely only on whether the demo looks convincing.

## Explore information access explicitly

The current app has no agency authorization. Use the table below as a workshop
worksheet, not as an implemented policy or a claim about agency entitlements.

| Resource | Incident controller | Assigned analyst | Agency liaison | Observer |
|---|---|---|---|---|
| Incident summary | Discuss full operational view | Discuss task-relevant view | Discuss approved agency view | Discuss redacted view |
| Raw evidence | Determine need-to-know | Determine assignment and clearance | Determine sharing authority | Usually exclude; validate with participants |
| Draft assessment | Determine review rights | Determine edit rights | Determine collaboration rights | Determine release point |
| Approval | Identify accountable authority | Identify permitted recommendations | Identify agency-specific authority | No approval role unless explicitly assigned |
| Export/share | Identify release authority | Identify restrictions | Identify recipients and onward-sharing rules | Determine whether export is permitted |

For each row ask: who owns the information, who may see it, who may change it,
which incident/purpose grants access, when does access expire, who may release it,
and what record is needed to explain a decision later? Include contractors,
cross-jurisdiction participants, withdrawn access, and emergency access exceptions.

A future design could combine authenticated agency identity, incident membership,
role, information classification, and purpose/need-to-know attributes. Enforce
policy on the backend, including exports and derived summaries. Log denied access
as well as successful disclosure where appropriate. Confirm this design with the
agencies; do not assume existing government classification labels are sufficient.

## Next demonstrator increments

1. **A non-CBRN scenario** — the East Coast Low / Hawkesbury–Nepean flood pathway
   now covers intake, triage, evidence, approval, briefing, and recovery. A service
   outage remains a useful second generic incident.
2. **Artifact provenance and uncertainty**, visibly distinguishing example data,
   uploaded reports, computed values, and verified observations.
3. **Agency view previews**, showing proposed information boundaries using synthetic
   data, clearly labelled as previews until backed by access enforcement.
4. **Decision records**, capturing the evidence considered, accountable reviewer,
   rationale, alternatives, and the conditions that would reopen a decision.
5. **Feedback export**, associating workshop observations with the screen, task,
   incident, and software version so the larger platform has traceable requirements.

For the larger platform, prioritize incident-scoped durable storage, authenticated
identities, enforced disclosure rules, accountable approvals, event history,
connector contracts, and resilience tests. Add integrations only when their evidence
and failure behavior can be demonstrated convincingly.

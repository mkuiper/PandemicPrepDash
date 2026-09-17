# Critical implementation review — 18 September 2026

## Assessment and intended use

The Incident Response Dashboard is useful as a facilitated demonstrator for
agency feedback. It has a functioning graph editor, workflow engine, API, and
briefing UI. It is not yet a general incident platform: domain categories,
scenario logic, evidence scores, and agency mappings remain CBRN-specific.

The strongest demonstration is a traceable decision: show the input, uncertainty,
responsible reviewer, approval, resulting action, and agency-specific information
needs. Production security design should be informed by those workflows.

This review inspected local code and tested software behavior. It did not validate
medical/scientific outputs, legislation, agency mandates, citations, cloud controls,
or external integration contracts. No external agency communications were sent.

## Fixed in this change

| Finding | Change and evidence |
|---|---|
| Radiological playbook silently selected H5N1 | Added matching scenario selection in `core/state_manager.py`; API regression verifies both scenario and threat type. |
| Vaccine execution erased drugs from the hub | Build the combined view from accumulated artifacts; regression compares all drugs and vaccines. |
| Missing edge endpoints and duplicate node IDs accepted | Validate before graph creation/mutation; malformed imports leave the active workflow intact. |
| Selecting an unknown scenario partly changed engine identity | Resolve the scenario before mutation; regression checks the run remains unchanged. |
| Execution mutated the shared scenario catalog | Copy scenario data and execution inputs; regression checks catalog sample data after execution. |
| Connector exceptions left execution state misleading | Mark node/run failed, report the error, and do not append completion or publish returned artifacts. This does not yet make every downstream artifact merge transactional. |
| Paused gates could not be resumed with explicit auto-approval; long workflows stopped at 50 cycles | Drive execution through one step at a time until completion/pause/failure; test a paused gate and a 55-node chain. |
| Imported runtime state could retain completed nodes or approvals | New engines reset runtime state; imported workflows must obtain fresh approval. |
| UI Run button silently auto-approved gates | Run now preserves approval pauses and displays failure/blocking messages. JavaScript behavior test checks the request and pause notification. |
| Hub messages interpolated user text as HTML | Escape message text, sender, role, and target. Markdown escapes raw HTML and limits generated links to HTTP(S). Other HTML templates still need review. |
| Template IDs could refer outside the storage directory | Restrict template identifiers for load/delete. This is not a defense against filesystem manipulation by a local user. |
| Timeline claimed events that had never occurred | Removed prefilled timeline; checkpoints are manual, scoped to the active run, and returned as defensive copies. They remain volatile summaries, not a durable audit log. |
| Governance updates bypassed validation and returned success HTTP status on errors | Validate merged settings and return 422 for invalid data without mutation. This is still demo configuration, not policy enforcement. |
| UI claimed working diagnostics, a secrets vault, and verified compliance | Label diagnostics/storage as simulations, disable credential fields, and default unverified controls/key connections to false. |

Product branding now reads **Incident Response Dashboard**. A persistent demo
notice clarifies simulated analysis and dispatch. The existing import/package
name is preserved, with an additional `incident-response` console entry point.

## Remaining findings, ordered by practical impact

### High: agency isolation and authorization do not exist

`core/state_manager.py` holds one process-global engine. API routes do not identify
an authenticated user or enforce incident membership, agency, classification,
need-to-know, or approval authority. `api/routes_execution.py` still supports
explicit `auto_approve`; changing the UI default is not a security boundary.
`main.py` also enables broad CORS. Multiple browsers see and mutate the same run.

Before any independently accessed agency deployment, introduce authenticated
identity and server-side authorization on reads, writes, exports, approvals, and
search results. Exercise explicit allow/deny cases and ensure redactions happen
before serialization. A role dropdown is only an illustrative view.

### High: results and evidence can imply capabilities that do not exist

`core/node_executor.py` largely assembles scenario data and scripted logs rather
than invoking scientific tools or model providers. `core/evidence_analyzer.py`
uses scenario-dependent predefined claims/scores. `core/data_hub.py` silently
falls back from live literature retrieval to example records. Tool selections,
provider settings, and human directives do not constitute a working autonomous
reasoning system. `core/bio_analyzer.py` uses limited heuristics/reference matching.

Add provenance to each artifact: **simulated**, **imported**, **computed locally**,
or **retrieved**, plus source, timestamp, method/version, and validation status.
Show “unknown” when evidence is missing. Separate retrieval from corroboration;
never treat a source link or a numeric score as proof of correctness.

### High: remaining HTML injection surface

`static/app.js` still has many `innerHTML` templates for node labels, custom
specimens, report content, templates, and other API data. The message and Markdown
fixes do not establish general XSS protection. Migrate user-controlled values to
DOM text/attribute setters and use a reviewed sanitizer for any deliberate rich
content. Include a real-browser test with malicious custom incident input.

### High: laboratory state and lifecycle are misleading

`core/lab_bridge.py` seeds requests with prefilled dispatch/progress and approvals.
Its global registry survives scenario changes and resets. Results can be recorded
without a valid prior dispatch, and supplied identifiers can overwrite requests.
Consequently a lab record from one incident can contaminate another or inflate
checkpoint dispatch counts. These are simulated records, not facility receipts.

Scope requests to incident/run, start examples as proposals, validate transitions,
and distinguish an operator-entered result from verified external evidence. Tests
must cover scenario changes, illegal transitions, duplicates, and replay.

### Medium: execution is neither concurrent-safe nor durable

Synchronous API handlers can mutate the shared engine concurrently. There are no
locks, optimistic version checks, idempotency keys, or transactions. Graph edits
can leave completed results out of date. Dependencies are ordered sequentially;
branches do not execute concurrently. `PathwayEdge.condition` is not evaluated.

Use explicit incident/run ownership, immutable run definitions or invalidation
rules, serialized transitions, and eventually durable storage. Test simultaneous
Run/Reset/Approve operations and failure during artifact publication. Conditional
edges should be implemented with defined semantics or rejected as unsupported.

### Medium: checkpoints are summaries, not audit or recovery

`core/version_control.py` keeps an in-memory list; the API records artifact type
previews, not complete recoverable snapshots. Reset discards checkpoints and
version labels can be reused. There is no authenticated actor binding, append-only
storage, integrity proof, or restore. Do not describe this as a tamper-proof audit.

### Medium: demo reproducibility and packaging

Dependencies have lower bounds without a lockfile. Frontend CSS/icons use CDNs;
PubMed latency/fallback can change demo behavior. Static assets and templates are
located relative to the source checkout, without a tested wheel asset strategy.
The launcher assumes an importable installed environment is sufficiently current;
use `--install` after dependency changes.

Pin a tested environment, vendor/build frontend assets, add an explicit deterministic
demo mode, and test a fresh install on a clean machine. Add browser-level checks
for scenario selection, pause/approve/resume, briefings, import/export, and reset.

## Testing validity

The original 32 tests passed, but did not cover the failures above. Several asserted
only that text/keys existed; one asserted a compliance flag was true by default.
They shared mutable global state, wrote templates into the project, and allowed
live PubMed requests. A passing badge therefore overstated confidence.

Changes:

- Each Python test gets an isolated engine, governance settings, lab registry,
  timeline, restored scenario catalog, and temporary template directory.
- Live urllib HTTP is replaced with an offline transport. This exercises the
  current fallback path; it does **not** validate successful live PubMed parsing.
- Initial regression run: **11 failures and 1 pass** against the pre-fix code.
- Added rejection/atomicity, lifecycle, approval, failure, data retention, long-run,
  snapshot ownership, and path traversal regressions.
- JavaScript tests execute actual frontend functions with a small DOM substitute;
  they test escaping and approval behavior, not browser layout or full DOM behavior.

Final validation: **52 Python tests passed** in deterministic shuffled order
(seed `18092026`), and **3 JavaScript tests passed** under Node 24. The Python run
reported two existing Starlette/TestClient deprecation warnings. Shell/JavaScript
syntax checks and `git diff --check` passed. No full browser or fresh-install test
was performed in this review.

Remaining test work: randomized action sequences, concurrent requests, browser
integration, live-service contract fixtures, clean installation, dependency locking,
and artifact-provenance checks. Agency/scientific validation is a separate activity.

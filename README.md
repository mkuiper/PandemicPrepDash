# Second Eyes

**Incident Response Dashboard** — an all-hazards workshop demonstrator.

A working demonstrator for incident coordination, response pathways, human review,
and shared situational awareness. It is a **second set of eyes** on an evolving
event, not a command system and not a CBRN-only product. Its purpose is to gather
agency feedback and inform the design of a larger platform.

The current example scenarios cover biological, chemical, radiological,
severe-weather (Hawkesbury–Nepean flood), and an industrial warehouse fire with
a simulated toxic plume. Civilian pathways are a **second set of eyes** on an
evolving event — they do not replace fire, EPA, ambulance, or SES protocols.
The fire path starts at the site, looks up adjacent occupancies, offers a
HYSPLIT-shaped planning contour (simulated), and records an in-run event log
for after-action discussion. Agency access controls are planned, not
implemented. The Python package and repository retain their original names
for compatibility.

## What works today

- Editable directed acyclic response pathways, with cycle and endpoint validation.
- Sequential execution of ready nodes, step-by-step or through an entire pathway.
- Human approval pauses, execution status, messages, and generated demo artifacts.
- Scenario switching, pathway template storage, and JSON import/export.
- Agency briefing previews, Markdown export, and simulated dispatch.
- Manual checkpoints that reflect the active run and reset with it.

Scientific analyses, agent deliberations, confidence scores, laboratory operations,
cloud integrations, and agency dispatches are largely simulated. The literature
component can query PubMed and falls back to example records; fallback citations
have not been independently verified. A successful workflow run demonstrates
software behavior, not scientific validity or agency approval. Security settings
are illustrative and do not enforce access control or compliance.

## Start a demo

Requires Python 3.11+; `uv` is optional and can provision a suitable Python.

```bash
./start.sh
```

Open **http://127.0.0.1:8000** and stop with **Ctrl+C**. The launcher works from
any working directory, creates `.venv` if needed, and installs missing application
dependencies with `uv` or `pip`.

```bash
PORT=8080 ./start.sh          # Another port
HOST=0.0.0.0 ./start.sh       # Access from a trusted demonstration network
./start.sh --install         # Refresh dependencies after pyproject.toml changes
```

Initial setup needs internet. The frontend also loads Tailwind CSS and icons from
external CDNs. No model API keys are required. The server uses one worker without
auto-reload. All browser sessions share the active incident; execution state is
in memory and is lost on shutdown. Saved pathway templates remain in `templates/`.
There is no authentication or agency-level authorization; use synthetic workshop data.

For an agency workshop:

1. Select a scenario and identify the decision the participants need to make.
2. Execute the pathway; inspect evidence, messages, and node outputs.
3. At an approval pause, review the node and explicitly authorize it to continue.
4. Compare agency briefing previews and discuss necessary redactions and permissions.
5. Capture a checkpoint and record feedback using the [workshop guide](docs/agency-feedback.md).

## Tests

Install the development dependencies:

```bash
uv pip install --python .venv/bin/python -e '.[dev]'
# Or: .venv/bin/python -m pip install -e '.[dev]'
.venv/bin/python -m pytest -q
node --test tests/frontend.test.cjs
```

The JavaScript tests require a recent Node.js with the built-in test runner
(Node 24 was used for validation). Node is not needed to run the application.
Python tests isolate global state and template storage and replace live HTTP
with an offline transport. They cover behavior and regression cases, including
rejection without mutation, approval gates, failed execution, and retained results.
JavaScript tests execute the message renderer, Markdown formatter, and Run control.
These are not full browser, scientific validation, security certification, or load tests.

See the [critical review](docs/critical-review.md) for findings, validation evidence,
remaining risks, and a proposed development sequence.

## Further documentation

- [Agency feedback and access-design workshop](docs/agency-feedback.md)
- [Architecture notes](ARCHITECTURE.md)
- [Scenario notes](docs/scenarios.md)
- [Design decisions](docs/adr/)

Older architecture and domain documentation contains aspirational capability and
policy descriptions. Treat the critical review as the current implementation
assessment; domain and policy content requires agency review before operational use.

# ADR-003: Whole-of-Government Multi-Agency Reporting Synthesis

## Status
Accepted

## Context
During a national health or biosecurity emergency in Australia, different government agencies have distinct statutory jurisdictions, legal responsibilities, and information requirements:
- The **Australian Centre for Disease Control (ACDC)** requires epidemiological R0 estimates, clinical case definitions, and transmission dynamics.
- The **Therapeutic Goods Administration (TGA)** requires pharmaceutical binding data, ARTG register numbers, Section 19A emergency exemption feasibility, and batch-testing criteria.
- The **Department of Agriculture, Fisheries and Forestry (DAFF)** requires One-Health zoonotic spillover markers, livestock buffer zones, and ACVO movement advisories.
- The **Defence Science and Technology Group (DSTG)** requires dual-use gain-of-function assessments, aerosol dispersion risks, and CBRN attribution.
- The **National Emergency Management Agency (NEMA)** requires critical supply chain stress points (cold-chain, N95 stockpiles) and COMDISPLAN logistics triggers.
- The **Department of Foreign Affairs and Trade (DFAT)** requires WHO International Health Regulations (IHR 2005) Article 6 notification text and Pacific regional assistance plans.

Generating a single generic PDF or email leads to information overload, missed statutory deadlines, and delayed responses.

## Decision
We implemented the `AgencyReportGenerator` which synthesizes bespoke, tailored situation reports (`AgencyReport`) for each statutory Australian agency directly from the shared blackboard:
- **Statutory Alignment**: Every report quotes relevant Commonwealth legislation (e.g., National Health Security Act 2007, Biosecurity Act 2015, Therapeutic Goods Act 1989).
- **Targeted Action Items**: Specific, numbered operational tasks for the receiving department.
- **Cross-Agency Dependencies**: Identifies other departments whose inputs are prerequisites (e.g. TGA depending on CSIRO laboratory assays).
- **Multi-Format Export & Dispatch**: Reports can be previewed in the UI, exported in GitHub Flavored Markdown, or dispatched via simulated secure government communications channels with recorded audit timestamps.

## Consequences
- Eliminates manual transcription bottlenecks between scientific laboratories and policy decision-makers.
- Provides a direct mechanism for departmental feedback and iterative refinement during exercises and live incidents.

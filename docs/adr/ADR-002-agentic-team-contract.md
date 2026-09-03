# ADR-002: Agentic Squad Contract and Deliberation Lifecycle

## Status
Accepted

## Context
Each node in a pandemic response workflow requires specialized scientific domain expertise (e.g., phylogenomics, Cryo-EM structural modeling, medicinal chemistry, immunology, CBRN threat classification, emergency public health policy). Using a single monolithic prompt or a generic assistant results in hallucination, lack of depth, and unstructured output.

Furthermore, human decision-makers need transparency into the reasoning process of AI agents before acting on recommendations.

## Decision
We implemented specialized **Agent Squads** composed of specific domain personas. Each agent squad follows a formal deliberation lifecycle:
1. **Observation**: Agent ingests inputs from preceding nodes in the blackboard and verifies quality metrics.
2. **Hypothesis**: Agent articulates biological/chemical hypotheses (e.g. evaluating furin cleavage sites or mammalian adaptation mutations).
3. **Tool Execution**: Agent invokes domain tools (e.g. `blast_alignment`, `alphafold_structural_predictor`, `autodock_vina_screener`, `iedb_epitope_predictor`, `ssba_regulatory_classifier`). Tool invocations record tool name, input parameters, and structured outputs.
4. **Synthesis & Recommendation**: Agent formulates structured outputs and writes them to the blackboard.

Each step produces an immutable `AgentThoughtLog` entry stamped with timestamps, confidence scores, agent name, and role.

## Pre-Configured Squads
- `bioinformatics_squad`: Led by Dr. Elena Rostova (Phylogenomics, variant calling, NCBI/GISAID BLAST).
- `structural_biology_squad`: Led by Dr. Marcus Vance (AlphaFold/ESMFold 3D coordinates, pocket volume, pLDDT).
- `medicinal_chemistry_squad`: Led by Dr. Priya Sharma (In silico docking, ARTG register lookup, ADMET).
- `vaccine_squad`: Led by Dr. Liam O'Connor (Conserved B/T cell epitopes, mRNA-LNP construct design).
- `biosecurity_squad`: Led by Commander Jack Sterling (SSBA Tier 1/2, dual-use screening, aerosolization risk).
- `policy_squad`: Led by Alison Bradley PSM (Whole-of-Government situational report synthesis).

## Consequences
- Provides full audit trail of agent reasoning for government inquiries and clinical oversight.
- Pluggable backend: Works with simulated realistic outputs for offline/demo operation, and can seamlessly connect to external LLM providers (Gemini, Claude, GPT) and bioinformatic CLI tools.

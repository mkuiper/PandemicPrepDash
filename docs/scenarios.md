# PandemicPrepDash Threat Scenarios Walkthrough

PandemicPrepDash comes equipped with three realistic reference scenarios covering biological, synthetic, and chemical CBRN hazards, as well as a flexible custom specimen ingestion capability.

---

## Scenario 1: H5N1 High-Pathogenicity Avian Influenza (Clade 2.3.4.4b)

### Background & Threat Description
High-Pathogenicity Avian Influenza (HPAI) A(H5N1) clade 2.3.4.4b has caused unprecedented mortality in avian species globally and demonstrated alarming mammalian spillover (dairy cattle, marine mammals, and human dairy workers). In this scenario, an isolate is detected in bulk raw milk and respiratory swabs from an Australian dairy and poultry farming district in Victoria.

### Key Analytical Findings
1. **Genomic Mutations:**
   - `PB2 E627K`: Critical mammalian adaptation substitution enabling efficient polymerase replication at 33°C (human upper respiratory tract temperature).
   - `HA Q226L`: Receptor-binding switch enhancing affinity for human-type alpha-2,6 linked sialic acid receptors.
   - `NA H275Y Absence`: Confirms wild-type susceptibility to neuraminidase inhibitors (Oseltamivir).
2. **Protein Targets Resolved:**
   - Hemagglutinin (HA) pre-fusion trimer (pLDDT: 94.6%).
   - Neuraminidase (NA) tetramer catalytic pocket (pLDDT: 96.1%).
   - Polymerase PB2 host cap-binding subunit (pLDDT: 91.3%).
3. **Medical Countermeasures:**
   - **Oseltamivir Phosphate (Tamiflu):** ARTG registered, binding affinity `-8.9 kcal/mol`, abundant in National Medical Stockpile (NMS).
   - **Baloxavir Marboxil (Xofluza):** Cap-dependent endonuclease inhibitor, binding affinity `-9.7 kcal/mol`.
   - **mRNA-LNP Vaccine:** Conserved neutralizing stem epitope candidate formulated for sovereign Australian manufacture at the Moderna Victoria (Monash) facility.
4. **Whole-of-Government Routing:**
   - **DAFF:** Immediate 50km poultry/livestock containment buffer, ACVO notification.
   - **ACDC:** National CDNA surveillance case definition for emergency departments and dairy workers.
   - **TGA:** Rapid stockpile audit for pediatric oral suspension formulations of oseltamivir.

---

## Scenario 2: Novel Engineered Coronaviral Agent ("Variant Tartarus")

### Background & Threat Description
An acute respiratory distress cluster is identified in a major metropolitan hospital ICU in Sydney, Australia. Sequencing reveals an unclassified Betacoronavirus exhibiting non-natural insertion markers and hyper-affinity for human ACE2.

### Key Analytical Findings
1. **Genomic Mutations & Dual-Use Markers:**
   - Insertion of a polybasic `PRRAR*S` furin cleavage motif utilizing non-canonical tandem `CGG-CGG` codons.
   - Convergent ACE2 hyper-affinity substitutions in the Spike Receptor-Binding Domain (`T478K`, `N501Y`, `E484K`, `Q498R`).
   - Absence of intermediate phylogenetic ancestors in global genomic surveillance repositories.
2. **Protein Targets Resolved:**
   - Spike (S) Trimer (pLDDT: 93.4%).
   - Main Protease (Mpro / 3CLpro, pLDDT: 97.8%).
3. **Medical Countermeasures:**
   - **Nirmatrelvir (Paxlovid):** Binding affinity `-10.4 kcal/mol`, ARTG registered, high national stockpile.
   - **Ensitrelvir (Xocova):** Non-covalent Mpro inhibitor, candidate for TGA Section 19A emergency import.
   - **HexaPro mRNA Vaccine:** Broadly neutralizing S2 stem helix construct.
4. **Whole-of-Government Routing:**
   - **DSTG & Defence CBRN:** Forensic synthetic origin audit, physical containment mandate PC4 (ACDP Geelong).
   - **ACDC:** Immediate NIR Level 2 alert and hospital ICU surge threshold triggers.
   - **DFAT:** Formal WHO International Health Regulations (IHR 2005) Article 6 notification.

---

## Scenario 3: Synthetic Chemical Toxin / Nerve Agent (A-Series Novichok Analogue)

### Background & Threat Description
During routine maritime cargo container inspection at an Australian port, customs hazmat sensors flag an unmanifested toxic residue. GC-MS and high-resolution mass spectrometry isolate a fourth-generation fluorophosphonamidate chemical warfare agent.

### Key Analytical Findings
1. **Chemical Characterization:**
   - Irreversible inhibitor of acetylcholinesterase with high environmental persistence (> 3 weeks on porous surfaces).
   - Rapid catalytic aging half-life (< 3.5 hours).
2. **Protein Targets Resolved:**
   - Human Acetylcholinesterase (AChE Ser203, pLDDT: 98.9%).
   - Human Butyrylcholinesterase (BChE, pLDDT: 98.2%).
3. **Medical Countermeasures:**
   - **Atropine Sulfate:** Immediate muscarinic receptor blockade.
   - **Pralidoxime Chloride (2-PAM) & HI-6:** Nucleophilic oxime reactivators.
   - **Pegylated Recombinant BChE Bioscavenger:** Prophylactic stoichiometric enzyme trap.
4. **Whole-of-Government Routing:**
   - **DSTG CBRN Defence:** Level A Hazmat containment and forensic attribution.
   - **NEMA Hazmat:** Critical port exclusion zone and supply chain redirection.
   - **DFAT:** Immediate declaration under the Chemical Weapons Convention (CWC) to the OPCW.

---

## Custom Specimen Ingestion
Users can ingest arbitrary biological or chemical specimens through the UI ("Custom Specimen" modal) or via `POST /api/scenarios/custom`. The pipeline will automatically parse the input format (DNA, RNA, Protein, SMILES, or Syndromic narrative), instantiate the node graph, and execute the agent squads.

"""
Australian Government SKILLS Repository, Computational Software Toolbox,
and Model Context Protocol (MCP) Server Registry.
Co-developed under Australian AI Safety Institute (AISI) & Department of Home Affairs frameworks.
"""

from typing import Dict, Any, List
from pydantic import BaseModel, Field


class AusGovSkill(BaseModel):
    skill_id: str
    name: str
    authority: str
    statutory_basis: str
    description: str
    operational_playbook: str
    tags: List[str] = Field(default_factory=list)


class SoftwareTool(BaseModel):
    tool_id: str
    name: str
    category: str
    description: str
    version: str
    license: str
    sovereign_australian_hosted: bool = True
    input_format: str
    output_format: str


class McpServer(BaseModel):
    server_id: str
    name: str
    description: str
    transport: str = "stdio"
    command: str
    args: List[str] = Field(default_factory=list)
    capabilities: List[str] = Field(default_factory=list)
    is_active: bool = True


# 1. Curated Australian Government Skills Repository
AUS_GOV_SKILLS: Dict[str, AusGovSkill] = {
    "AUS-SKILL-SSBA-REPORTING": AusGovSkill(
        skill_id="AUS-SKILL-SSBA-REPORTING",
        name="Security Sensitive Biological Agent (SSBA) Statutory Reporting",
        authority="Australian Centre for Disease Control (ACDC) / Department of Health and Aged Care",
        statutory_basis="National Health Security Act 2007 (Part 3) & SSBA Standards v7.1",
        description="Mandatory reporting workflows, initial notification timelines (24-hour rule), Tier 1 transfer logs, and chain-of-custody compliance.",
        operational_playbook=(
            "1. Verify pathogen against Tier 1 / Tier 2 SSBA List.\n"
            "2. Determine whether possession is lawful under Part 3 of the National Health Security Act 2007.\n"
            "3. If presumptive positive, dispatch Urgent Initial Notification (Form SSBA-01) to ACDC within 24 hours.\n"
            "4. Establish biosecurity perimeter, restrict facility access, and trigger electronic transfer manifest."
        ),
        tags=["SSBA", "Tier 1", "National Health Security Act 2007", "ACDC"],
    ),
    "AUS-SKILL-TGA-SECTION19A": AusGovSkill(
        skill_id="AUS-SKILL-TGA-SECTION19A",
        name="TGA Section 19A Emergency Countermeasure Access",
        authority="Therapeutic Goods Administration (TGA)",
        statutory_basis="Therapeutic Goods Act 1989 (Section 19A)",
        description="Expedited regulatory evaluation enabling importation and supply of unapproved overseas therapeutic goods to address national public health emergencies.",
        operational_playbook=(
            "1. Confirm shortage or unavailability of registered ARTG therapeutic alternatives.\n"
            "2. Identify overseas equivalents approved by recognized comparable overseas regulators (FDA, EMA, PMDA).\n"
            "3. Formulate Section 19A emergency determination dossier for the TGA Delegate.\n"
            "4. Cross-reference batch availability with the National Medical Stockpile (NMS)."
        ),
        tags=["TGA", "Section 19A", "Therapeutic Goods Act 1989", "ARTG", "Countermeasures"],
    ),
    "AUS-SKILL-ARPANSA-DOSE-ASSESSMENT": AusGovSkill(
        skill_id="AUS-SKILL-ARPANSA-DOSE-ASSESSMENT",
        name="ARPANSA Radiation Protection & Intervention Dose Assessment",
        authority="Australian Radiation Protection and Nuclear Safety Agency (ARPANSA)",
        statutory_basis="Australian Radiation Protection and Nuclear Safety Act 1998 & Radiation Protection Series C-1",
        description="Standard operating procedure for public dose limitation, emergency reference levels, evacuation perimeter calculation, and decorporation administration.",
        operational_playbook=(
            "1. Acquire gamma spectrometry photopeak data (keV) to identify specific radionuclide(s).\n"
            "2. Compute projected whole-body effective dose (mSv) over 24-hour and 7-day windows.\n"
            "3. Compare against ARPANSA Emergency Reference Levels (100 mSv intervention threshold for urgent protective actions).\n"
            "4. Define Inner Cordons (10 mGy/hr) and Outer Evacuation Radiuses; dispatch potassium iodide or Prussian Blue protocols."
        ),
        tags=["ARPANSA", "ARPANS Act 1998", "Radiation", "Dosimetry", "Dirty Bomb", "CBRN"],
    ),
    "AUS-SKILL-CBRN-FORENSICS": AusGovSkill(
        skill_id="AUS-SKILL-CBRN-FORENSICS",
        name="Whole-of-Government CBRN Attribution & Forensic Triage",
        authority="Department of Home Affairs & Defence Science and Technology Group (DSTG)",
        statutory_basis="Weapons of Mass Destruction Act 1995 & Crimes (Biological Weapons) Act 1976",
        description="Forensic evidentiary protocols for determining state vs non-state actor attribution, synthetic biology dual-use signatures, and Chemical Weapons Convention violations.",
        operational_playbook=(
            "1. Secure chain-of-custody documentation under Commonwealth rules of evidence.\n"
            "2. Execute isotopic and genomic sequence scanning for unnatural scar sites, cloning vectors, or signature precursor impurities.\n"
            "3. Compile technical attribution dossier for the National Security Committee of Cabinet (NSC).\n"
            "4. Coordinate referral to the Organisation for the Prohibition of Chemical Weapons (OPCW) or WHO."
        ),
        tags=["Home Affairs", "DSTG", "Forensics", "Attribution", "WMD Act 1995", "Cabinet"],
    ),
    "AUS-SKILL-ANSTO-SOURCE-ATTRIBUTION": AusGovSkill(
        skill_id="AUS-SKILL-ANSTO-SOURCE-ATTRIBUTION",
        name="ANSTO Radioisotope Forensic Sourcing & Safeguards",
        authority="Australian Nuclear Science and Technology Organisation (ANSTO) & ASNO",
        statutory_basis="ANSTO Act 1987 & Nuclear Non-Proliferation (Safeguards) Act 1987",
        description="High-precision nuclear forensics, mass spectrometry isotopic ratios, origin reactor profiling, and IAEA safeguard compliance reporting.",
        operational_playbook=(
            "1. Isolate particulate samples for High-Purity Germanium (HPGe) and Thermal Ionization Mass Spectrometry (TIMS).\n"
            "2. Determine isotopic ratios (e.g. Cs-134/Cs-137 or Pu-239/Pu-240) to deduce reactor burnup and enrichment.\n"
            "3. Cross-reference against the Australian Safeguards and Non-Proliferation Office (ASNO) domestic inventory.\n"
            "4. Transmit verification findings to the International Atomic Energy Agency (IAEA) Illicit Trafficking Database."
        ),
        tags=["ANSTO", "ASNO", "Nuclear Forensics", "Isotopes", "IAEA", "Lucas Heights"],
    ),
}

# 2. Computational Software Toolbox
SOFTWARE_TOOLBOX: List[SoftwareTool] = [
    SoftwareTool(
        tool_id="blast_plus",
        name="NCBI BLAST+ Suite",
        category="Bioinformatics",
        description="High-sensitivity local sequence alignment for nucleotide and protein homology searches.",
        version="2.15.0",
        license="Public Domain",
        input_format="FASTA / Raw String",
        output_format="JSON / XML / Tabular Alignment",
    ),
    SoftwareTool(
        tool_id="alphafold_3",
        name="AlphaFold 3 Inference Engine",
        category="Structural Biology",
        description="Diffusion-based macromolecular structure prediction for proteins, nucleic acids, and small-molecule complexes.",
        version="3.0.1",
        license="DeepMind Research License",
        input_format="Amino Acid Sequence",
        output_format="PDB / mmCIF Coordinates & pLDDT Matrix",
    ),
    SoftwareTool(
        tool_id="autodock_vina",
        name="AutoDock Vina",
        category="Chemoinformatics",
        description="Molecular docking and virtual screening for small-molecule therapeutic candidates.",
        version="1.2.5",
        license="Apache 2.0",
        input_format="PDBQT / SMILES",
        output_format="Binding Affinity (kcal/mol) & Conformation Poses",
    ),
    SoftwareTool(
        tool_id="rdkit",
        name="RDKit Cheminformatics",
        category="Chemoinformatics",
        description="Chemical structure validation, fingerprinting, SMILES parsing, and physicochemical descriptor calculation.",
        version="2024.03.1",
        license="BSD 3-Clause",
        input_format="SMILES / InChI",
        output_format="Molecular Descriptors & Substructure Match",
    ),
    SoftwareTool(
        tool_id="hysplit_rad_plume",
        name="HYSPLIT-Rad Atmospheric Dispersion Code",
        category="Health Physics",
        description="NOAA/Bureau of Meteorology hybrid single-particle Lagrangian integrated trajectory model for radioactive plume tracking.",
        version="5.3.0",
        license="Australian Bureau of Meteorology Licensed",
        input_format="Source Release (Bq) & Gridded Meteorological Data",
        output_format="Air Concentration Contours & Ground Deposition (Bq/m²)",
    ),
    SoftwareTool(
        tool_id="hotspot_health_physics",
        name="HOTSPOT Health Physics Code",
        category="Health Physics",
        description="Atmospheric dispersion and radiation dose calculation for dirty bomb (RDD) and industrial radionuclide releases.",
        version="3.1.2",
        license="Public Domain (LLNL)",
        input_format="Radionuclide, Activity (Ci/TBq), Wind Speed",
        output_format="TEDE (Total Effective Dose Equivalent) vs Distance Curves",
    ),
    SoftwareTool(
        tool_id="aus_ssba_checker",
        name="Australian SSBA Regulatory Scanner",
        category="Biosecurity",
        description="Automated deterministic matching of genomic/protein signatures against the Commonwealth SSBA List.",
        version="2.0.0",
        license="Commonwealth Copyright (AISI/Home Affairs)",
        input_format="Taxonomy / Mutation Profile",
        output_format="SSBA Tier Classification & Statutory Obligations",
    ),
]

# 3. Model Context Protocol (MCP) Server Registry
MCP_SERVERS_REGISTRY: List[McpServer] = [
    McpServer(
        server_id="mcp-server-ncbi-blast",
        name="NCBI GenBank & BLAST MCP Server",
        description="Enables agentic squads to execute real-time NCBI GenBank queries and BLAST+ alignments.",
        command="python",
        args=["-m", "mcp_blast_server", "--database", "refseq"],
        capabilities=["resources", "tools"],
    ),
    McpServer(
        server_id="mcp-server-arpansa-rad",
        name="ARPANSA Radiation Monitoring & Intervention MCP",
        description="Connects agents to ARPANSA national radiation monitoring network data and RPS C-1 safety guidelines.",
        command="python",
        args=["-m", "mcp_arpansa_server", "--network", "australian_rad_net"],
        capabilities=["tools", "prompts"],
    ),
    McpServer(
        server_id="mcp-server-tga-artg",
        name="TGA Australian Register of Therapeutic Goods (ARTG) MCP",
        description="Live lookup of ARTG registration, indications, black box warnings, and Section 19A emergency exemption history.",
        command="python",
        args=["-m", "mcp_tga_server", "--register", "artg_prescriptions"],
        capabilities=["resources", "tools"],
    ),
    McpServer(
        server_id="mcp-server-alphafold-db",
        name="AlphaFold DB & PDB-REDO MCP Server",
        description="Retrieves pre-computed AlphaFold structures and experimental crystallography models.",
        command="python",
        args=["-m", "mcp_alphafold_server"],
        capabilities=["resources", "tools"],
    ),
    McpServer(
        server_id="mcp-server-ansto-forensics",
        name="ANSTO Lucas Heights Nuclear Forensics MCP",
        description="Connects agents to ANSTO radioisotope spectral libraries and mass spectrometry databases.",
        command="python",
        args=["-m", "mcp_ansto_server", "--facility", "lucas_heights"],
        capabilities=["tools"],
    ),
    McpServer(
        server_id="mcp-server-aus-legislation",
        name="Australian Federal Legislation & Emergency Acts MCP",
        description="Provides agents with validated semantic search across Commonwealth Acts: National Health Security Act, Biosecurity Act, ARPANS Act, and TGA Act.",
        command="python",
        args=["-m", "mcp_legislation_server", "--corpus", "commonwealth_acts"],
        capabilities=["resources", "prompts"],
    ),
]

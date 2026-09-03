"""
Pathway Template Management & Storage.
Allows saving, loading, importing, and exporting custom and pre-configured response pathways.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import json
import uuid

from ..models.pathway import Pathway, PathwayNode, PathwayEdge, NodeCategory, NodeStatus
from ..models.bio_chem import ThreatType
from .registry import create_default_biological_pathway, create_default_chemical_pathway

TEMPLATES_DIR = Path(__file__).resolve().parent.parent.parent.parent / "templates"
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)


def create_rapid_antiviral_pathway() -> Pathway:
    """Streamlined response pathway focusing specifically on rapid drug repurposing."""
    nodes = [
        PathwayNode(
            id="node_antiviral_ingestion",
            label="Pathogen Specimen Ingestion",
            category=NodeCategory.INGESTION,
            description="Ingests sequence reads and checks phylogenetic markers.",
            agent_team_id="bioinformatics_squad",
            position_x=100.0,
            position_y=220.0,
        ),
        PathwayNode(
            id="node_antiviral_target",
            label="Catalytic Target Identification",
            category=NodeCategory.STRUCTURAL_BIOLOGY,
            description="AlphaFold active site mapping for viral proteases and polymerases.",
            agent_team_id="structural_biology_squad",
            position_x=380.0,
            position_y=220.0,
        ),
        PathwayNode(
            id="node_antiviral_screening",
            label="High-Throughput Repurposing Docking",
            category=NodeCategory.THERAPEUTICS,
            description="Screens ARTG-listed small molecules against target binding pockets.",
            agent_team_id="medicinal_chemistry_squad",
            position_x=660.0,
            position_y=220.0,
        ),
        PathwayNode(
            id="node_antiviral_regulatory",
            label="TGA Section 19A Exemption Briefing",
            category=NodeCategory.AGENCY_REPORTING,
            description="Synthesizes expedited regulatory access dossier for TGA and ACDP.",
            agent_team_id="policy_squad",
            position_x=940.0,
            position_y=220.0,
        ),
    ]
    edges = [
        PathwayEdge(id="av_edge_1", source="node_antiviral_ingestion", target="node_antiviral_target", label="Sequence Validated"),
        PathwayEdge(id="av_edge_2", source="node_antiviral_target", target="node_antiviral_screening", label="Pockets Mapped"),
        PathwayEdge(id="av_edge_3", source="node_antiviral_screening", target="node_antiviral_regulatory", label="Lead Candidates Ranked"),
    ]
    return Pathway(
        id="pathway_rapid_antiviral",
        name="Rapid Therapeutic & Antiviral Repurposing Pathway",
        description="Streamlined response pipeline for fast-tracking repurposed medicines and TGA Section 19A exemptions.",
        threat_type=ThreatType.BIOLOGICAL_VIRUS,
        nodes=nodes,
        edges=edges,
    )


def create_sovereign_vaccine_pathway() -> Pathway:
    """Accelerated vaccine design and sovereign biomanufacturing pathway."""
    nodes = [
        PathwayNode(
            id="node_vac_ingestion",
            label="Viral Antigen Sequence Ingestion",
            category=NodeCategory.INGESTION,
            description="Ingests surface glycoprotein sequence and confirms variant clade.",
            agent_team_id="bioinformatics_squad",
            position_x=100.0,
            position_y=220.0,
        ),
        PathwayNode(
            id="node_vac_epitopes",
            label="Epitope Mapping & Neutralization Profiling",
            category=NodeCategory.VACCINOLOGY,
            description="Identifies conserved B/T-cell epitopes and models pre-fusion conformation.",
            agent_team_id="vaccine_squad",
            position_x=380.0,
            position_y=220.0,
        ),
        PathwayNode(
            id="node_vac_mrna_design",
            label="mRNA-LNP Construct Formulation",
            category=NodeCategory.VACCINOLOGY,
            description="Optimizes codon bias, 5'/3' UTR stability, and lipid nanoparticle ratio.",
            agent_team_id="vaccine_squad",
            position_x=660.0,
            position_y=220.0,
        ),
        PathwayNode(
            id="node_vac_csiro_manufacture",
            label="CSIRO & Domestic Manufacturing Dispatch",
            category=NodeCategory.AGENCY_REPORTING,
            description="Dispatches technical production dossiers to CSIRO ACDP and Moderna Victoria.",
            agent_team_id="policy_squad",
            position_x=940.0,
            position_y=220.0,
        ),
    ]
    edges = [
        PathwayEdge(id="vac_edge_1", source="node_vac_ingestion", target="node_vac_epitopes", label="Antigen Confirmed"),
        PathwayEdge(id="vac_edge_2", source="node_vac_epitopes", target="node_vac_mrna_design", label="Epitopes Mapped"),
        PathwayEdge(id="vac_edge_3", source="node_vac_mrna_design", target="node_vac_csiro_manufacture", label="Construct Finalized"),
    ]
    return Pathway(
        id="pathway_sovereign_vaccine",
        name="Sovereign mRNA Vaccine Accelerated Pathway",
        description="Focused pipeline for rapid domestic antigen design, epitope mapping, and CSIRO/Moderna manufacturing handoff.",
        threat_type=ThreatType.BIOLOGICAL_VIRUS,
        nodes=nodes,
        edges=edges,
    )


def create_default_radiological_pathway() -> Pathway:
    """Default Australian radiological / nuclear emergency response pathway."""
    nodes = [
        PathwayNode(
            id="node_rad_detection",
            label="Radiation Detection & Gamma Spectrometry",
            category=NodeCategory.INGESTION,
            description="Acquires HPGe gamma photopeak data, identifies radioisotopes, and measures activity.",
            agent_team_id="radiological_defense_squad",
            human_oversight_role="ARPANSA Radiation Monitoring Duty Officer",
            position_x=100.0,
            position_y=220.0,
        ),
        PathwayNode(
            id="node_rad_plume",
            label="HYSPLIT Plume & Dispersion Modeling",
            category=NodeCategory.CHARACTERIZATION,
            description="Simulates atmospheric dispersion, ground deposition (Bq/m²), and public dose rate.",
            agent_team_id="radiological_defense_squad",
            human_oversight_role="Bureau of Meteorology & ARPANSA Modeler",
            position_x=380.0,
            position_y=140.0,
        ),
        PathwayNode(
            id="node_rad_decorporation",
            label="Decorporation Countermeasures (Prussian Blue)",
            category=NodeCategory.THERAPEUTICS,
            description="Screens ion-exchange decorporation antidotes and authorizes National Medical Stockpile release.",
            agent_team_id="medicinal_chemistry_squad",
            human_oversight_role="TGA & Chief Medical Officer Evaluator",
            position_x=660.0,
            position_y=140.0,
        ),
        PathwayNode(
            id="node_rad_arpansa_approval",
            label="ARPANSA Emergency Intervention Signoff",
            category=NodeCategory.BIOSECURITY,
            description="Statutory review of Emergency Reference Levels under the ARPANS Act 1998.",
            agent_team_id="biosecurity_squad",
            requires_human_approval=True,
            human_oversight_role="ARPANSA Chief Radiation Health Scientist & Home Affairs Delegate",
            position_x=660.0,
            position_y=300.0,
        ),
        PathwayNode(
            id="node_rad_agency_reports",
            label="Whole-of-Government Radiological Dispatches",
            category=NodeCategory.AGENCY_REPORTING,
            description="Dispatches briefings to ARPANSA, ANSTO, ASNO, Home Affairs, NEMA, and Cabinet.",
            agent_team_id="policy_squad",
            human_oversight_role="Home Affairs Crisis Centre Director",
            position_x=960.0,
            position_y=220.0,
        ),
    ]
    edges = [
        PathwayEdge(id="rad_e1", source="node_rad_detection", target="node_rad_plume", label="Isotope Confirmed"),
        PathwayEdge(id="rad_e2", source="node_rad_plume", target="node_rad_decorporation", label="Dose Projected"),
        PathwayEdge(id="rad_e3", source="node_rad_detection", target="node_rad_arpansa_approval", label="Activity Measured"),
        PathwayEdge(id="rad_e4", source="node_rad_decorporation", target="node_rad_agency_reports", label="Medical Antidotes Ready"),
        PathwayEdge(id="rad_e5", source="node_rad_arpansa_approval", target="node_rad_agency_reports", label="Statutory Signoff"),
    ]
    return Pathway(
        id="pathway_default_radiological",
        name="Radiological & Nuclear CBRN Response Pathway",
        description="Whole-of-government emergency pathway for radiological dispersal devices (RDD / dirty bombs), atmospheric plume dispersion, decorporation medical countermeasures, and ARPANSA/ANSTO statutory dispatches.",
        threat_type=ThreatType.RADIOLOGICAL_DISPERSAL,
        nodes=nodes,
        edges=edges,
    )


class TemplateManager:
    """Manages built-in and user-persisted response pathway templates."""

    @classmethod
    def get_builtin_templates(cls) -> Dict[str, Pathway]:
        return {
            "pathway_default_biological": create_default_biological_pathway(),
            "pathway_default_chemical": create_default_chemical_pathway(),
            "pathway_default_radiological": create_default_radiological_pathway(),
            "pathway_rapid_antiviral": create_rapid_antiviral_pathway(),
            "pathway_sovereign_vaccine": create_sovereign_vaccine_pathway(),
        }

    @classmethod
    def list_all_templates(cls) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []

        # Built-in templates
        for k, p in cls.get_builtin_templates().items():
            results.append({
                "id": k,
                "name": p.name,
                "description": p.description,
                "threat_type": p.threat_type.value if hasattr(p.threat_type, "value") else str(p.threat_type),
                "node_count": len(p.nodes),
                "edge_count": len(p.edges),
                "is_builtin": True,
            })

        # User saved templates from directory
        for f in TEMPLATES_DIR.glob("*.json"):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                results.append({
                    "id": data.get("id", f.stem),
                    "name": data.get("name", f.stem),
                    "description": data.get("description", "User-saved custom template"),
                    "threat_type": data.get("threat_type", "biological_virus"),
                    "node_count": len(data.get("nodes", [])),
                    "edge_count": len(data.get("edges", [])),
                    "is_builtin": False,
                })
            except Exception as err:
                print(f"Failed to load template file {f}: {err}")

        return results

    @classmethod
    def get_template(cls, template_id: str) -> Pathway:
        # Check built-in
        builtins = cls.get_builtin_templates()
        if template_id in builtins:
            return builtins[template_id]

        # Check user templates
        target_file = TEMPLATES_DIR / f"{template_id}.json"
        if target_file.exists():
            data = json.loads(target_file.read_text(encoding="utf-8"))
            return Pathway.model_validate(data)

        raise KeyError(f"Template '{template_id}' not found.")

    @classmethod
    def save_template(cls, pathway: Pathway, name: Optional[str] = None, description: Optional[str] = None) -> Pathway:
        template_id = f"tmpl_{uuid.uuid4().hex[:8]}"
        saved_pathway = pathway.model_copy(deep=True)
        saved_pathway.id = template_id
        if name:
            saved_pathway.name = name
        if description:
            saved_pathway.description = description

        # Reset runtime statuses in saved template
        for n in saved_pathway.nodes:
            n.status = NodeStatus.PENDING
            n.outputs = {}
            n.latency_ms = None
            n.error_message = None

        target_file = TEMPLATES_DIR / f"{template_id}.json"
        target_file.write_text(saved_pathway.model_dump_json(indent=2), encoding="utf-8")
        return saved_pathway

    @classmethod
    def delete_template(cls, template_id: str) -> bool:
        target_file = TEMPLATES_DIR / f"{template_id}.json"
        if target_file.exists():
            target_file.unlink()
            return True
        return False

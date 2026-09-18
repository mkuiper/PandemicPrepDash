"""
Grounded lead-agent questions. Second eyes only; unknown is a valid answer.
"""

from typing import Any, Dict, List, Optional
from ..models.pathway import PathwayNode


def _cite(artifacts: Dict[str, Any], key: str) -> Any:
    return artifacts.get(key)


def _unknown(question: str, cite: str) -> Dict[str, Any]:
    return {
        "question": question,
        "answer": "unknown",
        "cites": [cite],
        "unknown": True,
        "provenance": "simulated",
    }


def _known(question: str, answer: str, cites: List[str]) -> Dict[str, Any]:
    return {
        "question": question,
        "answer": answer,
        "cites": cites,
        "unknown": False,
        "provenance": "simulated",
    }


def build_lead_context(
    node: PathwayNode,
    artifacts: Dict[str, Any],
    pathway_node_ids: Optional[List[str]] = None,
    threat_type: str = "",
) -> List[Dict[str, Any]]:
    """Return 2–4 artifact-grounded questions for the node lead."""
    nid = node.id
    threat = str(threat_type).lower()
    items: List[Dict[str, Any]] = []

    if nid == "node_ff_intake" or nid == "node_wx_intake":
        sample = artifacts.get("sample") or {}
        loc = sample.get("source_location")
        q = "What site or catchment is this sitrep actually about?"
        items.append(
            _known(q, loc, ["sample.source_location"]) if loc else _unknown(q, "sample.source_location")
        )
        items.append(
            _known(
                "Is this a live agency product or a workshop sitrep?",
                "Workshop fiction — second eyes only; not CAD, BOM, or FRNSW live feed.",
                ["sample.raw_payload"],
            )
        )
    elif nid == "node_ff_adjacent":
        neighbours = artifacts.get("adjacent_sites") or []
        unknown = [n.get("name") for n in neighbours if n.get("inventory_status") == "unknown"]
        if not neighbours:
            items.append(_unknown("What occupancies sit next to this fire?", "adjacent_sites"))
        else:
            items.append(
                _known(
                    "Can we model without the neighbour inventory?",
                    (
                        f"Unknown inventory: {', '.join(unknown)}. Treat unknown as a result, not a gap to invent."
                        if unknown
                        else "Declared neighbour inventories are on the blackboard."
                    ),
                    ["adjacent_sites"],
                )
            )
        items.append(
            _known(
                "Which populations sit on the example plume axis?",
                "School and example district hospital are listed in the adjacent lookup (simulated).",
                ["adjacent_sites"],
            )
        )
    elif nid == "node_ff_dispersal":
        plume = artifacts.get("plume_model") or {}
        conflict = artifacts.get("conflicting_reports") or {}
        if plume.get("planning_distance_km"):
            items.append(
                _known(
                    "What planning contour are we offering the IC?",
                    f"{plume.get('planning_distance_km')} km {plume.get('direction')} "
                    f"({plume.get('method', 'simulated contour')}).",
                    ["plume_model"],
                )
            )
        else:
            items.append(_unknown("What planning contour are we offering the IC?", "plume_model"))
        items.append(
            _known(
                "Does field reporting match the contour?",
                conflict.get("field") or "Field comparison not yet on the blackboard.",
                ["conflicting_reports"],
            )
        )
        items.append(
            _known(
                "If the wind shifts, what must happen?",
                "Mark the contour stale and re-open the Incident Controller decision. Do not dispatch from this app.",
                ["weather"],
            )
        )
    elif nid == "node_ff_approval":
        items.append(
            _known(
                "Is the receiving ED inside the field-report axis?",
                (artifacts.get("impact_assessment") or {}).get("hospital_status")
                or "Hospital status not yet recorded.",
                ["impact_assessment"],
            )
        )
        items.append(
            _known(
                "What is not in force until you approve?",
                "Shelter-in-place, M7 do-not-enter, and ambulance diversion — second eyes, not fireground command.",
                ["threat_assessment"],
            )
        )
    elif nid in ("node_wx_triage", "node_wx_evidence"):
        impact = artifacts.get("impact_assessment") or {}
        items.append(
            _known(
                "Which critical sites are in the example flood picture?",
                ", ".join(impact.get("critical_sites") or []) or "not yet ranked",
                ["impact_assessment"],
            )
        )
        conflict = artifacts.get("conflicting_reports") or {}
        items.append(
            _known(
                "Which source should the IC privilege — forecast or gauge?",
                f"Forecast: {conflict.get('bom_forecast', 'unknown')}. Gauge: {conflict.get('river_gauge', 'unknown')}.",
                ["conflicting_reports"],
            )
        )
    elif nid in ("node_wx_approval",):
        items.append(
            _known(
                "What would reopen evacuation?",
                "A gauge rise that matches the overnight forecast, or a confirmed levee failure — record the condition.",
                ["threat_assessment"],
            )
        )
    elif nid in ("node_wx_recovery", "node_ff_recovery"):
        items.append(
            _known(
                "What did we know at stand-down?",
                "Replay the in-run event log. It is not a durable audit archive.",
                ["recovery"],
            )
        )
    elif nid in ("node_sample_ingestion", "node_rad_detection", "node_chem_sample_ingestion"):
        sample = artifacts.get("sample") or {}
        items.append(
            _known(
                "What was ingested, and from where?",
                f"{sample.get('name', 'unspecified')} @ {sample.get('source_location', 'unknown')}",
                ["sample"],
            )
        )
    elif nid == "node_genomic_characterization":
        ident = artifacts.get("identification") or {}
        items.append(
            _known(
                "Which identity are downstream nodes allowed to assume?",
                ident.get("agent_name") or "identification not on the blackboard",
                ["identification"],
            )
        )
    elif nid == "node_biosecurity_assessment":
        ta = artifacts.get("threat_assessment") or {}
        items.append(
            _known(
                "What would reopen this classification?",
                f"Current label: {ta.get('ssba_tier') or ta.get('hazard_class') or 'unset'}. Change of identity or dual-use evidence.",
                ["threat_assessment"],
            )
        )
    elif nid in ("node_therapeutic_screening", "node_chem_target_docking"):
        drugs = artifacts.get("drug_candidates") or []
        if not drugs:
            items.append(_unknown("Is there a stockpile candidate, or only in-silico scoring?", "drug_candidates"))
        else:
            items.append(
                _known(
                    "Stockpile vs in-silico only?",
                    f"Lead on blackboard: {drugs[0].get('name')} ({drugs[0].get('tga_artg_status', 'status unset')}).",
                    ["drug_candidates"],
                )
            )
    elif nid.endswith("briefing") or "agency" in nid:
        reports = artifacts.get("agency_reports") or {}
        relevant = [k for k, v in reports.items() if isinstance(v, dict) and v.get("is_relevant")]
        items.append(
            _known(
                "Who is on the active brief list, and who is standby?",
                f"Relevant: {', '.join(relevant) or 'none yet'}.",
                ["agency_reports"],
            )
        )
    else:
        items.append(
            _known(
                "What is on the blackboard for this node?",
                "See node outputs. Ask the IC before assuming missing evidence.",
                ["outputs"],
            )
        )

    return items[:4]


def filter_dialogues(dialogues: List[Any], pathway_node_ids: List[str]) -> List[Any]:
    allowed = set(pathway_node_ids)
    return [d for d in dialogues if getattr(d, "target_node_id", None) in allowed]

"""
Evidence Synthesis & Knowledge Gap Analyzer.
Performs critical audits across computational blackboard artifacts, highlights conflicting evidence,
identifies knowledge gaps, and maps necessary physical validations to Commonwealth reference laboratories.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

from ..models.evidence import (
    EvidenceDomain,
    GapSeverity,
    KnowledgeGap,
    ConflictingEvidence,
    ExperimentalValidationNeed,
    EvidenceAnalysisReport,
)
from .lab_bridge import LabBridgeManager


class EvidenceAnalyzer:
    """Evaluates the integrity, gaps, and discrepancies in current incident intelligence."""

    @classmethod
    def analyze_incident_evidence(
        cls,
        scenario_id: str,
        threat_type: str,
        node_artifacts: Dict[str, Any],
        completed_node_ids: List[str],
    ) -> EvidenceAnalysisReport:
        threat_lower = threat_type.lower()
        scen_lower = scenario_id.lower()

        gaps: List[KnowledgeGap] = []
        conflicts: List[ConflictingEvidence] = []
        validations: List[ExperimentalValidationNeed] = []
        domain_scores: Dict[str, float] = {}

        if "bio" in threat_lower or "h5n1" in scen_lower:
            # Domain Confidence Scores
            domain_scores = {
                "Genomics & Phylogenetics": 0.94 if "node_genomic_characterization" in completed_node_ids else 0.45,
                "Structural Biology & Targets": 0.89 if "node_structural_modeling" in completed_node_ids else 0.30,
                "Pharmacology & Therapeutics": 0.72 if "node_therapeutic_screening" in completed_node_ids else 0.20,
                "Transmission & Epidemiology": 0.40,  # low until physical animal challenge
                "Statutory & Biosecurity Law": 0.95 if "node_biosecurity_assessment" in completed_node_ids else 0.60,
            }

            # Knowledge Gaps
            gaps.append(
                KnowledgeGap(
                    domain=EvidenceDomain.EPIDEMIOLOGY,
                    title="Mammalian Aerosol Droplet Transmission Half-Life in Ambient Air",
                    description="While genomics identifies PB2 E627K and HA multi-basic cleavage, in silico sequence data cannot determine whether the virus replicates efficiently in the mammalian upper respiratory tract to sustain ambient airborne transmission without direct contact.",
                    severity=GapSeverity.CRITICAL,
                    related_node_ids=["node_genomic_characterization", "node_biosecurity_assessment"],
                    impact_if_unresolved="Inability to determine whether community isolation cordons or Level 4 airborne PPE standards are legally mandated for public transport.",
                    suggested_investigation="High-containment airborne transmission challenge with ferrets housed in adjoining cages with directional airflow at ACDP Geelong PC4.",
                )
            )

            gaps.append(
                KnowledgeGap(
                    domain=EvidenceDomain.PHARMACOLOGY,
                    title="Antiviral Susceptibility Phenotype Against Rare Secondary Neuraminidase Variants",
                    description="AutoDock Vina predicted strong binding for Oseltamivir and Baloxavir, but deep sequencing reads detect low-frequency (<3%) sub-clonal neuraminidase substitutions (such as I38T or H274Y) whose clinical IC50 shifts remain unquantified.",
                    severity=GapSeverity.HIGH,
                    related_node_ids=["node_therapeutic_screening"],
                    impact_if_unresolved="Risk of deploying National Medical Stockpile therapeutics that face rapid clinical resistance during patient treatment.",
                    suggested_investigation="Direct in vitro enzymatic IC50 inhibition assay using purified recombinant neuraminidase at TGA Laboratories Division.",
                )
            )

            # Conflicting Evidence
            conflicts.append(
                ConflictingEvidence(
                    domain=EvidenceDomain.PHARMACOLOGY,
                    title="In Silico Docking Potency vs. Emerging Phenotypic Resistance Signature",
                    source_a="In Silico AutoDock Vina & AlphaFold Target",
                    claim_a="Predicted Baloxavir binding energy is -8.6 kcal/mol with complete catalytic pocket occlusion (druggability index 0.94).",
                    source_b="Field Deep-Sequencing Read Frequency (<3% I38T)",
                    claim_b="Minority sub-population carries I38T substitution documented in literature to produce a 30- to 50-fold shift in clinical Baloxavir IC50.",
                    discrepancy_explanation="Computational docking evaluated the consensus wild-type consensus structure, missing low-frequency quasi-species that can rapidly become dominant under pharmaceutical selection pressure.",
                    operational_risk="Premature clinical reliance on single-agent therapy risking widespread treatment failure in intensive care units.",
                    recommended_arbitration="Mandate combination therapy protocol (Baloxavir + Oseltamivir) until physical TGA enzymatic IC50 confirmation.",
                )
            )

            # Required Validations
            validations.append(
                ExperimentalValidationNeed(
                    assay_title="Ferret Direct Contact & Airborne Aerosol Transmission Study",
                    target_facility="ACDP (CSIRO Australian Centre for Disease Prevention - PC4)",
                    critical_question="Can naive ferrets contract the virus through ambient air at 1.0 m separation without direct physical contact?",
                    urgency="CRITICAL",
                    specimen_spec="1.0 mL viable lung homogenate (>10^6 TCID50/mL)",
                    unblocks_decision="Legally confirms human-to-human transmission potential under National Health Security Act 2007 Section 11.",
                )
            )

            validations.append(
                ExperimentalValidationNeed(
                    assay_title="In Vitro Neuraminidase & Endonuclease IC50 Potency Verification",
                    target_facility="TGA Laboratories Division (Symonston, ACT)",
                    critical_question="What is the exact IC50 concentration of Commonwealth Stockpile antivirals against the emergent field isolate?",
                    urgency="HIGH",
                    specimen_spec="50 ug recombinant HA/NA glycoprotein extract",
                    unblocks_decision="Unblocks Section 19A emergency distribution guidelines for intensive care emergency departments.",
                )
            )

            overall_conf = sum(domain_scores.values()) / len(domain_scores)
            summary = (
                "Computational analysis provides high confidence in taxonomic identity (H5N1 Clade 2.3.4.4b) "
                "and molecular targets. However, an empirical transmission gap (aerosol droplet mechanics) "
                "and conflicting pharmacological signals (in silico docking vs minority I38T resistance reads) "
                "require physical confirmation at ACDP Geelong PC4 and TGA Laboratories."
            )

        elif "radio" in threat_lower or "cesium" in scen_lower:
            domain_scores = {
                "Health Physics & Plume Dynamics": 0.91 if "node_plume_dispersion_modeling" in completed_node_ids else 0.40,
                "Nuclear Forensics & Safeguards": 0.85 if "node_spectral_characterization" in completed_node_ids else 0.35,
                "Pharmacology & Therapeutics": 0.78,
                "Transmission & Epidemiology": 0.95,  # deterministic dose geometry
                "Statutory & Biosecurity Law": 0.95,
            }

            gaps.append(
                KnowledgeGap(
                    domain=EvidenceDomain.HEALTH_PHYSICS,
                    title="Urban Micro-Climate Particulate Resuspension & Inhalation Coefficient",
                    description="Standard Gaussian and Lagrangian plume modeling assumes uniform surface roughness. Heavy vehicle turbulence along highway corridors may resuspend sub-micron CsCl particulates, extending the inhalation hazard beyond the initial 450m cordon.",
                    severity=GapSeverity.HIGH,
                    related_node_ids=["node_plume_dispersion_modeling"],
                    impact_if_unresolved="Unprotected transport corridor workers may inhale resuspendable aerosols outside the cordoned zone.",
                    suggested_investigation="High-volume cascade impactor air sampling across Sydney orbital freight corridors.",
                )
            )

            conflicts.append(
                ConflictingEvidence(
                    domain=EvidenceDomain.HEALTH_PHYSICS,
                    title="HYSPLIT Simulated Contours vs. Field Mobile Gamma Swab Readings",
                    source_a="HYSPLIT Lagrangian Particulate Simulation",
                    claim_a="Predicted inner exclusion hot zone (>10 mSv/hr) is strictly confined to a 450 m radial perimeter.",
                    source_b="Police HAZMAT / ARPANSA First Responder Mobile Detectors",
                    claim_b="Intermittent elevated micro-R readings (up to 12.4 mSv/hr) detected at 680 m along railway drainage swales.",
                    discrepancy_explanation="Drainage swales acted as stormwater collection conduits, concentrating water-soluble Caesium Chloride (CsCl) slurry downwind of the initial blast epicenter.",
                    operational_risk="First responders and rail maintenance personnel entering an un-cordoned stormwater zone with lethal exposure risk.",
                    recommended_arbitration="Expand physical outer cordon to 1.0 km along stormwater corridors pending ANSTO gamma mapping.",
                )
            )

            validations.append(
                ExperimentalValidationNeed(
                    assay_title="High-Purity Germanium (HPGe) Spectrometry & Isotopic Burnup Profiling",
                    target_facility="ANSTO Nuclear Science (Lucas Heights)",
                    critical_question="What is the precise Cs-134/Cs-137 activity ratio, and does it match domestic Australian ASNO disused source registry?",
                    urgency="CRITICAL",
                    specimen_spec="Air filter swipe and soil specimen in lead cask",
                    unblocks_decision="Attribution of state vs stolen domestic source under Nuclear Non-Proliferation (Safeguards) Act 1987.",
                )
            )

            overall_conf = sum(domain_scores.values()) / len(domain_scores)
            summary = (
                "Radiological identification of Caesium-137 is robustly established. Critical conflicting evidence "
                "between simulated plume contours and field drainage swale readings requires expanding the inner perimeter. "
                "Physical HPGe spectrometry at ANSTO is essential for attribution."
            )

        elif "weather" in threat_lower or "flood" in scen_lower:
            domain_scores = {
                "Hydrology & Forecast": 0.72 if "node_wx_evidence" in completed_node_ids else 0.35,
                "Operations & Impact Assessment": 0.68 if "node_wx_triage" in completed_node_ids else 0.30,
                "Statutory & Biosecurity Law": 0.55 if "node_wx_approval" in completed_node_ids else 0.20,
            }
            gaps.append(
                KnowledgeGap(
                    domain=EvidenceDomain.HYDROLOGY,
                    title="Overnight hydrograph versus gauge rise (simulated)",
                    description=(
                        "The example BOM forecast peaks at 17.4 m at Windsor while the example gauge is 16.8 m "
                        "and rising more slowly than the previous three-hour forecast. These figures are workshop fiction."
                    ),
                    severity=GapSeverity.CRITICAL,
                    related_node_ids=["node_wx_evidence", "node_wx_intake"],
                    impact_if_unresolved="Evacuation timing may be too early or too late relative to actual overtopping.",
                    suggested_investigation="Audit the Windsor gauge and compare with an independent hydrology run (simulated field task).",
                )
            )
            conflicts.append(
                ConflictingEvidence(
                    domain=EvidenceDomain.HYDROLOGY,
                    title="Forecast overtopping versus field reconnaissance (simulated)",
                    source_a="BOM hydrology example product",
                    claim_a="Overtopping at Windsor/Richmond is likely overnight.",
                    source_b="SES field recon example",
                    claim_b="Rise is slower than forecast; levee seepage is reported but not confirmed as failure.",
                    discrepancy_explanation="Example products were generated independently for the workshop and are not reconciled observations.",
                    operational_risk="An evacuation order based on only one source will be hard to justify later.",
                    recommended_arbitration="Incident Controller records which sources were used and the conditions that would reopen the decision.",
                )
            )
            validations.append(
                ExperimentalValidationNeed(
                    assay_title="Windsor gauge audit (simulated field task)",
                    target_facility="Bureau of Meteorology Observing Network (NSW)",
                    critical_question="Does the Windsor gauge still match the independent staff gauge within 0.05 m?",
                    urgency="HIGH",
                    specimen_spec="Gauge log extract and photographs (workshop fiction)",
                    unblocks_decision="Whether overnight overtopping is treated as likely or uncertain.",
                )
            )
            overall_conf = sum(domain_scores.values()) / len(domain_scores)
            summary = (
                "Simulated flood evidence is incomplete: the forecast, gauge, and field recon do not agree. "
                "This is a workshop conflict, not a live hydrology assessment."
            )

        elif "industrial_fire" in threat_lower or "warehouse_fire" in scen_lower:
            domain_scores = {
                "Hydrology & Forecast": 0.0,
                "Operations & Impact Assessment": 0.7 if "node_ff_adjacent" in completed_node_ids else 0.3,
                "Health Physics & Plume Dynamics": 0.62 if "node_ff_dispersal" in completed_node_ids else 0.28,
                "Statutory & Biosecurity Law": 0.5 if "node_ff_approval" in completed_node_ids else 0.2,
            }
            gaps.append(
                KnowledgeGap(
                    domain=EvidenceDomain.OPERATIONS,
                    title="Adjacent tank-farm inventory unknown (simulated)",
                    description="The neighbour bulk-liquids site has not confirmed contents in the first hour. Domino risk cannot be bounded.",
                    severity=GapSeverity.CRITICAL,
                    related_node_ids=["node_ff_adjacent", "node_ff_intake"],
                    impact_if_unresolved="Protective action may understate a BLEVE or secondary toxic release.",
                    suggested_investigation="SafeWork / EPA dangerous-goods request to the tank-farm operator (simulated field task).",
                )
            )
            conflicts.append(
                ConflictingEvidence(
                    domain=EvidenceDomain.HEALTH_PHYSICS,
                    title="HYSPLIT-shaped contour versus creek-line field reports (simulated)",
                    source_a="Planning contour (simulated HYSPLIT-shaped method)",
                    claim_a="3.2 km ENE from the warehouse under SW 8 kt night inversion.",
                    source_b="EPA handheld / public smell reports (example)",
                    claim_b="Odour and elevated readings along a drainage line at about 4.5 km.",
                    discrepancy_explanation="Example products are not reconciled. Creek drainage can channel dense smoke.",
                    operational_risk="School and example hospital sit on the field-report axis; M7 still open.",
                    recommended_arbitration="IC records which contour was used and the wind-shift that would reopen the decision.",
                )
            )
            validations.append(
                ExperimentalValidationNeed(
                    assay_title="Downwind air monitoring transect (simulated)",
                    target_facility="NSW Environment Protection Authority field team",
                    critical_question="Do handheld readings support extending the planning contour along the creek?",
                    urgency="HIGH",
                    specimen_spec="Air-quality transect notes (workshop fiction)",
                    unblocks_decision="Shelter vs evacuate east of site, and whether the example hospital must divert.",
                )
            )
            overall_conf = sum(v for v in domain_scores.values() if v) / max(1, len([v for v in domain_scores.values() if v]))
            summary = (
                "Simulated industrial-fire evidence is incomplete: neighbour inventory is unknown and "
                "the planning contour disagrees with field reports. Second eyes only — not a live plume model."
            )

        else:
            # Chemical / Generic Threat
            domain_scores = {
                "Genomics & Phylogenetics": 0.50,
                "Structural Biology & Targets": 0.85,
                "Pharmacology & Therapeutics": 0.70,
                "Transmission & Epidemiology": 0.80,
                "Statutory & Biosecurity Law": 0.95,
            }

            gaps.append(
                KnowledgeGap(
                    domain=EvidenceDomain.PHARMACOLOGY,
                    title="In Vivo Human Erythrocyte Acetylcholinesterase Aging Half-Life",
                    description="Fourth-generation organophosphate nerve agents (Novichoks) feature phosphonamidofluoridate structures with accelerated covalent aging, rendering standard oxime reactivators ineffective if delayed.",
                    severity=GapSeverity.CRITICAL,
                    related_node_ids=["node_therapeutic_screening", "node_chemical_identification"],
                    impact_if_unresolved="Failure to administer oximes within the therapeutic window leads to permanent neurological damage.",
                    suggested_investigation="High-resolution LC-MS/MS fluoride regeneration assay at DSTG Fishermans Bend.",
                )
            )

            conflicts.append(
                ConflictingEvidence(
                    domain=EvidenceDomain.PHARMACOLOGY,
                    title="Standard Chemical Defense Playbook vs. A-Series Resistance",
                    source_a="Standard Clinical Toxicological Playbook",
                    claim_a="Standard Pralidoxime (2-PAM) dosing is the front-line oxime reactivator.",
                    source_b="DSTG Chemical Threat Intelligence Dossier",
                    claim_b="A-234 forms bulky steric hindrance in AChE active gorge, rendering 2-PAM ineffective; requires Obidoxime or HI-6.",
                    discrepancy_explanation="Traditional stockpiles are optimized for classic G-series/V-series agents, not modern fourth-generation organophosphates.",
                    operational_risk="Depleting 2-PAM without reversing neuromuscular blockade in critical patients.",
                    recommended_arbitration="Direct TGA and NMS to release Obidoxime and high-dose Atropine exclusively.",
                )
            )

            validations.append(
                ExperimentalValidationNeed(
                    assay_title="OPCW-Accredited LC-MS/MS Fluoride Reactivation Assay",
                    target_facility="DSTG CBRN Defence Laboratories (Fishermans Bend)",
                    critical_question="Confirm exact chemical structure and determine AChE reactivation kinetics with Obidoxime.",
                    urgency="CRITICAL",
                    specimen_spec="Container swipe sample in sealed PTFE vial",
                    unblocks_decision="Statutory notification under Chemical Weapons (Prohibition) Act 1994.",
                )
            )

            overall_conf = 0.76
            summary = (
                "Chemical identification indicates fourth-generation neurotoxin. Conflicting evidence regarding oxime efficacy "
                "mandates substituting standard 2-PAM with Obidoxime. Urgent DSTG LC-MS/MS assay required."
            )

        return EvidenceAnalysisReport(
            incident_name=scenario_id.replace("scen_", "").replace("_", " ").title(),
            overall_confidence_score=round(overall_conf, 2),
            domain_scores=domain_scores,
            knowledge_gaps=gaps,
            conflicting_evidence=conflicts,
            required_validations=validations,
            synthesis_summary=summary,
        )

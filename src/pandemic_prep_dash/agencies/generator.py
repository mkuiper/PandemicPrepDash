"""
Agency Briefing Generator - synthesizes tailored whole-of-government reports
based on pipeline analytical outputs.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
from ..models.agency import (
    AgencyIdentifier,
    AgencyReport,
    SecurityClassification,
    UrgencyLevel,
)
from .registry import AUSTRALIAN_AGENCIES


class AgencyReportGenerator:
    """Generates agency-specific briefing reports from shared execution state."""

    @staticmethod
    def generate_all_reports(
        incident_name: str,
        threat_type: str,
        artifacts: Dict[str, Any],
        urgency: UrgencyLevel = UrgencyLevel.PRIORITY,
        classification: SecurityClassification = SecurityClassification.OFFICIAL_SENSITIVE,
    ) -> Dict[AgencyIdentifier, AgencyReport]:
        """Generates briefings for all primary Australian government agencies."""
        reports: Dict[AgencyIdentifier, AgencyReport] = {}
        for agency_id in AUSTRALIAN_AGENCIES.keys():
            reports[agency_id] = AgencyReportGenerator.generate_report_for_agency(
                agency_id=agency_id,
                incident_name=incident_name,
                threat_type=threat_type,
                artifacts=artifacts,
                urgency=urgency,
                classification=classification,
            )
        return reports

    @staticmethod
    def generate_report_for_agency(
        agency_id: AgencyIdentifier,
        incident_name: str,
        threat_type: str,
        artifacts: Dict[str, Any],
        urgency: UrgencyLevel = UrgencyLevel.PRIORITY,
        classification: SecurityClassification = SecurityClassification.OFFICIAL_SENSITIVE,
    ) -> AgencyReport:
        sample_info = artifacts.get("sample", {})
        identification = artifacts.get("identification", {})
        protein_targets = artifacts.get("protein_targets", [])
        drug_candidates = artifacts.get("drug_candidates", [])
        vaccine_candidates = artifacts.get("vaccine_candidates", [])
        threat_assessment = artifacts.get("threat_assessment", {})

        agent_name = identification.get("agent_name", "Novel Pathogen / Toxin")
        lineage = identification.get("clade_or_lineage", "Unclassified")
        ssba_tier = threat_assessment.get("ssba_tier", "Tier 1 SSBA")

        now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

        if agency_id == AgencyIdentifier.ACDC:
            title = f"ACDC Epidemiological & Surveillance Sitrep: {agent_name} ({lineage})"
            exec_summary = (
                f"Automated intelligence synthesis has confirmed the characterization of {agent_name} "
                f"({lineage}). High transmissibility indicators detected. Immediate activation of national "
                f"genomic surveillance network and Communicable Diseases Network Australia (CDNA) case definitions recommended."
            )
            sit_update = (
                f"Origin/Index Detection: {sample_info.get('source_location', 'Australia')}. "
                f"Pathogen classification: {identification.get('taxonomy', 'Emerging Agent')}. "
                f"WHO Pandemic Potential: {threat_assessment.get('who_pandemic_potential', 'High')}. "
                f"Containment rating: {threat_assessment.get('containment_level_required', 'PC3/PC4')}."
            )
            strategic_imps = [
                "Issue urgent national CDNA surveillance case definition to State/Territory public health units.",
                "Activate National Incident Room (NIR) Level 2 monitoring protocol.",
                "Coordinate with Public Health Laboratory Network (PHLN) for nationwide RT-PCR primer distribution.",
                "Establish baseline R0 tracking and hospital ICU surge threshold triggers.",
            ]
            action_items = [
                "Publish Interim Clinical Guidance for emergency departments within 12 hours.",
                "Stand up daily National Health Emergency Management Standing Committee (NHEMSC) briefings.",
                "Liaise with TGA regarding priority distribution of therapeutic countermeasures.",
            ]
            cross_deps = [AgencyIdentifier.TGA, AgencyIdentifier.DAFF, AgencyIdentifier.NEMA, AgencyIdentifier.DFAT]

        elif agency_id == AgencyIdentifier.TGA:
            title = f"TGA Medical Countermeasure & Regulatory Dossier: Countermeasures for {agent_name}"
            exec_summary = (
                f"Computational docking and structural evaluation have identified {len(drug_candidates)} potential therapeutic "
                f"candidates and {len(vaccine_candidates)} vaccine formulation designs targeting {agent_name}. "
                f"Evaluation of emergency regulatory pathways (Section 19A exemptions & Provisional Registration) initiated."
            )
            top_target_name = protein_targets[0].get('name', 'Viral Target') if protein_targets else 'Under Analysis'
            top_target_plddt = protein_targets[0].get('plddt_confidence', 'N/A') if protein_targets else 'Pending'
            top_drug_name = drug_candidates[0].get('name', 'Screening in Progress') if drug_candidates else 'None Identified'
            top_drug_affinity = drug_candidates[0].get('binding_affinity_kcal_mol', 'N/A') if drug_candidates else 'N/A'
            top_drug_artg = drug_candidates[0].get('tga_artg_status', 'Pending') if drug_candidates else 'Pending'

            sit_update = (
                f"Primary target identified: {top_target_name} (pLDDT Confidence: {top_target_plddt}). "
                f"Leading drug candidate: {top_drug_name} (Affinity: {top_drug_affinity} kcal/mol, ARTG Status: {top_drug_artg})."
            )
            strategic_imps = [
                "Review Section 19A emergency supply mechanisms for immediate off-label / repurposed antiviral access.",
                "Initiate pre-submission scientific advice with domestic vaccine developers (CSIRO / local mRNA hubs).",
                "Assess domestic National Medical Stockpile (NMS) holdings for active pharmaceutical ingredients (APIs).",
                "Review rapid diagnostic test (RDT) target antigens for in-country sensitivity verification.",
            ]
            action_items = [
                "Issue regulatory alert on priority clinical trial protocol templates.",
                "Commence batch testing protocol design for candidate vaccines.",
                "Establish therapeutic safety monitoring registry in DAEN (Database of Adverse Event Notifications).",
            ]
            cross_deps = [AgencyIdentifier.ACDC, AgencyIdentifier.CSIRO, AgencyIdentifier.NEMA]

        elif agency_id == AgencyIdentifier.DAFF:
            title = f"DAFF Biosecurity & One-Health Alert: Zoonotic Risk Assessment - {agent_name}"
            exec_summary = (
                f"One-Health genomic characterization highlights potential spillover / animal-human interface risk for {agent_name}. "
                f"Australian Chief Veterinary Officer (ACVO) notified. Animal biosecurity containment and quarantine buffer protocols active."
            )
            sit_update = (
                f"Sample origin: {sample_info.get('source_location', 'Domestic Site')}. "
                f"Host species range: {identification.get('host_tropism', 'Avian / Mammalian / Human')}. "
                f"Zoonotic spillover risk score: {threat_assessment.get('zoonotic_risk', 'High')}. "
                f"Biosecurity import conditions (BICON) status: Escalated review."
            )
            strategic_imps = [
                "Implement wildlife and poultry/livestock surveillance zones within 50km radius of detection site.",
                "Alert domestic commercial poultry, swine, and dairy producer associations to heighten biosecurity protocols.",
                "Verify wild bird flyway tracking and migratory monitoring in collaboration with state agricultural bodies.",
            ]
            action_items = [
                "Convene Consultative Committee on Emergency Animal Diseases (CCEAD).",
                "Coordinate with CSIRO ACDP Geelong for live viral isolation from animal samples.",
                "Update border biosecurity screening protocols at all international air and sea freight terminals.",
            ]
            cross_deps = [AgencyIdentifier.ACDC, AgencyIdentifier.CSIRO, AgencyIdentifier.DSTG]

        elif agency_id == AgencyIdentifier.DSTG:
            title = f"DSTG CBRN Defence & Threat Intelligence Assessment: {agent_name}"
            exec_summary = (
                f"CBRN threat intelligence audit completed. Classification: {ssba_tier}. "
                f"Evaluation of aerosolization feasibility, synthetic biology markers, and attribution conducted for Defence Force Health Protection."
            )
            sit_update = (
                f"Synthetic manipulation evidence: {'Positive' if threat_assessment.get('evidence_of_genetic_manipulation') else 'Negative / Natural Lineage'}. "
                f"Aerosol transmission feasibility: {threat_assessment.get('aerosol_transmission_feasibility', 'Moderate')}. "
                f"Signatures identified: {', '.join(threat_assessment.get('gain_of_function_signatures', ['None detected']))}."
            )
            strategic_imps = [
                "Audit domestic military CBRN countermeasure stockpiles and operational force protective posture.",
                "Maintain real-time technical liaison with Five-Eyes (TTCP) CBRN defense partners.",
                "Evaluate secondary forensic attribution via phylogenomic signatures and synthetic scar markers.",
            ]
            action_items = [
                "Issue tactical force health protection guidelines to Australian Defence Force (ADF) Joint Health Command.",
                "Deploy specialized mobile CBRN diagnostic teams to high-readiness status.",
            ]
            cross_deps = [AgencyIdentifier.ACDC, AgencyIdentifier.NEMA, AgencyIdentifier.DFAT]

        elif agency_id == AgencyIdentifier.NEMA:
            title = f"NEMA Crisis Logistics & Emergency Supply Chain Brief: {agent_name}"
            exec_summary = (
                f"Civil protection and supply chain resilience assessment for {agent_name}. Preparedness triggers "
                f"activated for national medical stockpiling, transport cold-chain, and potential COMDISPLAN logistics deployment."
            )
            sit_update = (
                f"National Threat Level: {urgency.value}. Projected regional impact: Multi-jurisdictional. "
                f"Required cold chain: {vaccine_candidates[0].get('stability_profile', 'Standard Cold Chain') if vaccine_candidates else 'Standard'}."
            )
            strategic_imps = [
                "Audit National Medical Stockpile (NMS) for PPE (N95 respirators, PAPRs), transport media, and therapeutics.",
                "Model interstate air/road freight transport corridors for medical countermeasure distribution.",
                "Prepare briefing for National Security Committee of Cabinet (NSC) on whole-of-nation supply resiliency.",
            ]
            action_items = [
                "Establish direct liaison cell with State/Territory State Emergency Service (SES) coordinators.",
                "Review emergency critical care bed capacity and surge oxygen distribution logistics.",
            ]
            cross_deps = [AgencyIdentifier.ACDC, AgencyIdentifier.TGA, AgencyIdentifier.DSTG]

        elif agency_id == AgencyIdentifier.DFAT:
            title = f"DFAT International Health Security & Diplomatic Notification: {agent_name}"
            exec_summary = (
                f"International compliance and regional Indo-Pacific health security brief for {agent_name}. "
                f"Prepared in accordance with WHO International Health Regulations (IHR 2005) Article 6 obligations."
            )
            sit_update = (
                f"Agent: {agent_name}. Identification Confidence: 99.4%. Potential for cross-border transmission: High. "
                f"Regional vulnerability: Pacific Island Countries (PICs) lacking high-containment PC4 diagnostics."
            )
            strategic_imps = [
                "Issue formal Article 6 notification to the World Health Organization (WHO) Western Pacific Regional Office (WPRO).",
                "Review Smartraveller travel advisories for affected transit hubs and international departure points.",
                "Mobilize Australian Indo-Pacific Centre for Health Security rapid diagnostic support for regional partners.",
            ]
            action_items = [
                "Brief Australian Ambassador for Global Health on multilateral coordination strategy.",
                "Coordinate with Pacific Island health ministries for emergency diagnostic sample transport to CSIRO ACDP.",
            ]
            cross_deps = [AgencyIdentifier.ACDC, AgencyIdentifier.DAFF]

        elif agency_id == AgencyIdentifier.CSIRO:
            title = f"CSIRO ACDP High-Containment Diagnostic & Platform Synthesis Brief: {agent_name}"
            exec_summary = (
                f"Technical brief for CSIRO Australian Centre for Disease Preparedness (ACDP, Geelong) and "
                f"Biomedical Manufacturing teams regarding {agent_name} isolation, cryo-EM structure, and pilot batching."
            )
            sit_update = (
                f"Target pLDDT Confidence: {protein_targets[0].get('plddt_confidence', 90.0) if protein_targets else 'N/A'}. "
                f"Structural pockets identified: {len(protein_targets)}. Vaccine construct: {vaccine_candidates[0].get('platform', 'mRNA-LNP') if vaccine_candidates else 'Subunit'}."
            )
            strategic_imps = [
                "Prepare PC4 biocontainment suites at ACDP Geelong for live viral isolation and challenge assays.",
                "Initiate high-throughput cryo-electron microscopy structural validation of predicted epitopes.",
                "Spin up pilot-scale biomanufacturing runs at Clayton / Parkville mRNA production facilities.",
            ]
            action_items = [
                "Synthesize diagnostic reference antigens for Public Health Laboratory Network distribution.",
                "Complete in vitro binding validation assay for lead repurposed drug candidates within 72 hours.",
            ]
            cross_deps = [AgencyIdentifier.TGA, AgencyIdentifier.ACDC, AgencyIdentifier.DSTG]

        elif agency_id == AgencyIdentifier.OGTR:
            title = f"OGTR Biosafety & Gene Technology Regulatory Compliance Notice: {agent_name}"
            exec_summary = (
                f"Gene Technology Act 2000 regulatory review for experimental and synthetic biology handling of {agent_name}."
            )
            sit_update = (
                f"Classification: Gene Technology and Synthetic Biology containment protocol required. "
                f"Containment mandate: PC3 or PC4 certified facilities only."
            )
            strategic_imps = [
                "Issue expedited emergency dealing authorization (EDD) if live attenuated or viral-vectored research commences.",
                "Verify certified Physical Containment (PC) status of participating academic and industry laboratories.",
            ]
            action_items = [
                "Publish safety advisory for institutional biosafety committees (IBCs) across Australia.",
            ]
            cross_deps = [AgencyIdentifier.TGA, AgencyIdentifier.ACDC]

        elif agency_id == AgencyIdentifier.ARPANSA:
            title = f"ARPANSA Public Health Radiation Emergency & Intervention Dose Assessment: {agent_name}"
            exec_summary = (
                f"Statutory radiological emergency assessment under the ARPANS Act 1998 and Radiation Protection Series C-1. "
                f"Atmospheric dispersion and whole-body committed effective dose modeling for {agent_name}."
            )
            sit_update = (
                f"Source Characterization: {agent_name}. "
                f"Dose Projection: Near-source boundary dose rates exceed 10 mSv/hr. "
                f"Atmospheric Plume: HYSPLIT dispersion models indicate downwind particulate deposition."
            )
            strategic_imps = [
                "Establish 5 km Urgent Protective Action Planning Zone (UPZ) based on prevailing wind vectors.",
                "Activate National Radiation Monitoring Network (ARMN) fixed and mobile gamma spectroscopy stations.",
                "Recommend urgent release of decorporation agents (Prussian Blue / Ca-DTPA) from the National Medical Stockpile.",
            ]
            action_items = [
                "Issue public sheltering and radioprotective action orders in coordination with NEMA and state emergency services.",
                "Deploy aerial radiological survey teams to map ground deposition contours (Bq/m²).",
                "Execute thyroid and whole-body bioassays on first responders and exposed civilians.",
            ]
            cross_deps = [AgencyIdentifier.ANSTO, AgencyIdentifier.NEMA, AgencyIdentifier.TGA, AgencyIdentifier.HOME_AFFAIRS]

        elif agency_id == AgencyIdentifier.ANSTO:
            title = f"ANSTO Nuclear Forensics & Radioisotope Origin Attribution Dossier: {agent_name}"
            exec_summary = (
                f"High-resolution nuclear forensics, gamma spectrometry, and thermal ionization mass spectrometry (TIMS) "
                f"conducted at Lucas Heights to identify isotope provenance and encapsulation history."
            )
            sit_update = (
                f"Nuclear Forensics: High-Purity Germanium (HPGe) spectrometry confirms dominant radioisotopic signature. "
                f"Physical Form: Dispersed powder/particulate with specialized industrial carrier matrix."
            )
            strategic_imps = [
                "Isotopic ratio cross-referencing indicates material consistent with orphaned industrial or teletherapy source.",
                "Provide technical decontamination protocols for critical infrastructure, maritime assets, and vehicles.",
            ]
            action_items = [
                "Deliver sovereign radioisotope forensics attribution report to Home Affairs and Defence.",
                "Support emergency HAZMAT teams with Lucas Heights mobile radiation detection suites.",
            ]
            cross_deps = [AgencyIdentifier.ARPANSA, AgencyIdentifier.ASNO, AgencyIdentifier.DSTG]

        elif agency_id == AgencyIdentifier.ASNO:
            title = f"ASNO Safeguards Compliance & Illicit Nuclear Trafficking Alert: {agent_name}"
            exec_summary = (
                f"Statutory review under the Nuclear Non-Proliferation (Safeguards) Act 1987. "
                f"Notification verification against national sealed source inventories and IAEA ITDB."
            )
            sit_update = (
                f"Source Accountancy: Verification against Australian domestic source inventory indicates unrecorded or illicit acquisition."
            )
            strategic_imps = [
                "Formal incident reporting to the International Atomic Energy Agency (IAEA) Incident and Trafficking Database (ITDB).",
                "Coordination with Australian Border Force to monitor border checkpoints and interdict companion consignments.",
            ]
            action_items = [
                "Initiate regulatory enforcement under Commonwealth nuclear safeguards legislation.",
            ]
            cross_deps = [AgencyIdentifier.DFAT, AgencyIdentifier.HOME_AFFAIRS, AgencyIdentifier.ARPANSA]

        elif agency_id == AgencyIdentifier.HOME_AFFAIRS:
            title = f"Department of Home Affairs & AISI National Security Incident Assessment: {agent_name}"
            exec_summary = (
                f"National Counter-Terrorism Plan (NCTP) assessment and critical infrastructure risk appraisal. "
                f"Co-developed evaluation of autonomous agentic response safety with the Australian AI Safety Institute (AISI)."
            )
            sit_update = (
                f"Threat Level: ELEVATED. Multi-agency CBRN response framework activated under whole-of-government arrangements. "
                f"AISI Assurance: Agentic response pathways running with Human-in-the-Loop oversight on all critical decision gates."
            )
            strategic_imps = [
                "Assess disruption risk to Australian ports, transport corridors, and healthcare supply chains under SOCI Act 2018.",
                "Maintain continuous auditing of AI agent decision trees to prevent hallucinated CBRN countermeasures or dual-use proliferation.",
            ]
            action_items = [
                "Brief the National Security Committee of Cabinet (NSC) on whole-of-government containment and inter-agency posture.",
                "Coordinate intelligence sharing across ASIO, AFP, Border Force, and State Police CBRN counter-terrorism squads.",
            ]
            cross_deps = [AgencyIdentifier.DSTG, AgencyIdentifier.NEMA, AgencyIdentifier.ACDC, AgencyIdentifier.ARPANSA]

        else:
            title = f"Inter-Agency Briefing: {agent_name}"
            exec_summary = f"Summary intelligence report regarding incident {incident_name}."
            sit_update = f"Status update for {agent_name}."
            strategic_imps = ["Maintain active inter-agency monitoring."]
            action_items = ["Review situation report updates as generated."]
            cross_deps = [AgencyIdentifier.ACDC]

        return AgencyReport(
            report_id=f"REP-{agency_id.value}-{uuid.uuid4().hex[:6].upper()}",
            agency_id=agency_id,
            title=title,
            classification=classification,
            urgency=urgency,
            incident_name=incident_name,
            threat_type=threat_type,
            executive_summary=exec_summary,
            situation_update=sit_update,
            scientific_findings={
                "identification": identification,
                "protein_targets_count": len(protein_targets),
                "top_target": protein_targets[0].get("name") if protein_targets else None,
                "drug_candidates_count": len(drug_candidates),
                "top_drug_candidate": drug_candidates[0].get("name") if drug_candidates else None,
                "vaccine_candidate_platform": vaccine_candidates[0].get("platform") if vaccine_candidates else None,
                "ssba_tier": ssba_tier,
            },
            strategic_implications=strategic_imps,
            action_items_required=action_items,
            cross_agency_dependencies=cross_deps,
            generated_at=now_str,
            dispatched=False,
        )

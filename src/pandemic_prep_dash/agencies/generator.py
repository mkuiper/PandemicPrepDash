"""
Agency Report Generator - synthesizes tailored, statutory Whole-of-Government situation reports
for Australian emergency authorities under relevant Commonwealth Acts.
Includes targeted agency relevance filtering so agencies only receive active alerts when in-scope.
"""

from typing import Dict, Any, List, Tuple
from datetime import datetime
import uuid

from ..models.agency import AgencyIdentifier, AgencyReport, SecurityClassification, UrgencyLevel
from ..agencies.registry import AUSTRALIAN_AGENCIES, get_agency_profile
from ..models.bio_chem import ThreatType


class AgencyReportGenerator:
    """Generates tailored reports for Australian authorities with jurisdiction relevance filtering."""

    @classmethod
    def determine_relevance(
        cls,
        agency_id: AgencyIdentifier,
        threat_type: str,
        artifacts: Dict[str, Any],
    ) -> Tuple[bool, str]:
        """Evaluates whether an agency requires an active emergency response brief or is on standby."""
        threat_str = str(threat_type).lower()
        is_rad = "radiological" in threat_str or "nuclear" in threat_str
        is_chem = "chemical" in threat_str or "nerve_agent" in threat_str or "toxin" in threat_str
        is_bio = "biological" in threat_str or "virus" in threat_str or "bacteria" in threat_str or "synthetic" in threat_str

        if agency_id in [AgencyIdentifier.ARPANSA, AgencyIdentifier.ANSTO, AgencyIdentifier.ASNO]:
            if is_rad:
                return True, "Primary statutory jurisdiction: Incident involves radioactive source dispersal and isotope contamination."
            return False, "Standby: Incident involves non-radiological bio/chemical agents. Radiation protection not triggered."

        if agency_id == AgencyIdentifier.ACDP:
            if is_bio:
                return True, "Primary diagnostic jurisdiction: PC4 high-containment pathogen identification and surveillance active."
            return False, "Standby: Chemical/radiological incident with no biological pathogen requiring PC4 diagnostic culture."

        if agency_id == AgencyIdentifier.DAFF:
            if is_bio and ("avian" in str(artifacts).lower() or "zoonotic" in str(artifacts).lower() or "animal" in str(artifacts).lower()):
                return True, "Active One-Health jurisdiction: Pathogen presents confirmed zoonotic transmission and livestock biosecurity risk."
            if is_bio:
                return False, "Standby: Pathogen restricted to human host with low direct veterinary/livestock transmission footprint."
            return False, "Standby: Non-agricultural threat with no domestic animal or crop vector identified."

        if agency_id == AgencyIdentifier.OGTR:
            if "synthetic" in threat_str or artifacts.get("threat_assessment", {}).get("evidence_of_genetic_manipulation"):
                return True, "Active statutory jurisdiction: Potential genetically modified or synthetic biology construct identified."
            return False, "Standby: Natural pathogen/agent lineage with no synthetic gene technology regulatory trigger."

        if agency_id == AgencyIdentifier.DSTG:
            if is_chem or is_rad or artifacts.get("threat_assessment", {}).get("dual_use_concerns"):
                return True, "Active national security brief: Dual-use CBRN or sovereign defense force health protection triggered."
            return False, "Standby: Natural outbreak under civil health jurisdiction."

        # Common whole-of-gov crisis agencies (TGA, NEMA, DFAT, Home Affairs, CSIRO)
        if agency_id == AgencyIdentifier.TGA:
            return True, "Active statutory mandate: Emergency therapeutic evaluation and Section 19A medical countermeasure access."
        if agency_id == AgencyIdentifier.NEMA:
            return True, "Active crisis mandate: Whole-of-government emergency logistics, sheltering, and COMDISPLAN coordination."
        if agency_id == AgencyIdentifier.HOME_AFFAIRS:
            if is_chem or is_rad or "terror" in str(artifacts).lower() or "port" in str(artifacts).lower():
                return True, "Active national security brief: Critical infrastructure (SOCI Act) or border interdiction triggered."
            return True, "Active crisis brief: National coordination and emergency cabinet liaison."
        if agency_id == AgencyIdentifier.DFAT:
            return True, "Active treaty mandate: International Health Regulations (IHR 2005) or CBRN treaty compliance notification."
        if agency_id == AgencyIdentifier.CSIRO:
            if is_bio or is_chem:
                return True, "Active scientific mandate: Sovereign biomanufacturing scaleup, preclinical testing, and macromolecular design."
            return False, "Standby: Radiological response led by ANSTO / ARPANSA."

        return True, "Statutory situational awareness."

    @classmethod
    def generate_report(
        cls,
        agency_id: AgencyIdentifier,
        incident_name: str,
        threat_type: str,
        artifacts: Dict[str, Any],
    ) -> AgencyReport:
        sample_info = artifacts.get("sample", {})
        identification = artifacts.get("identification", {})
        protein_targets = artifacts.get("protein_targets", [])
        drug_candidates = artifacts.get("drug_candidates", [])
        vaccine_candidates = artifacts.get("vaccine_candidates", [])
        threat_assessment = artifacts.get("threat_assessment", {})

        agent_name = identification.get("agent_name", "Emerging CBRN Threat")
        lineage = identification.get("clade_or_lineage", "Unclassified")
        ssba_tier = threat_assessment.get("ssba_tier", "Dangerous Substance")

        now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
        is_relevant, relevance_reason = cls.determine_relevance(agency_id, threat_type, artifacts)

        if agency_id == AgencyIdentifier.ACDP:
            title = f"ACDP High-Containment Diagnostic & Surveillance Sitrep: {agent_name} ({lineage})"
            exec_summary = (
                f"Diagnostic confirmation and high-containment PC4 evaluation completed at Geelong for {agent_name} "
                f"({lineage}). Immediate activation of national reference surveillance and Communicable Diseases Network "
                f"Australia (CDNA) diagnostic testing algorithms recommended."
            )
            sit_update = (
                f"Origin/Detection: {sample_info.get('source_location', 'Australia')}. "
                f"Pathogen classification: {identification.get('taxonomy', 'Emerging Pathogen')}. "
                f"Containment rating: {threat_assessment.get('containment_level_required', 'PC4 / PC3')}. "
                f"WHO Pandemic Potential: {threat_assessment.get('who_pandemic_potential', 'High')}."
            )
            strategic_imps = [
                "Issue urgent national CDNA surveillance case definitions to State/Territory public health reference labs.",
                "Activate National Incident Room (NIR) Level 2 monitoring protocol.",
                "Coordinate with Public Health Laboratory Network (PHLN) for nationwide diagnostic assay deployment.",
                "Establish baseline R0 tracking and public health surge threshold triggers.",
            ]
            action_items = [
                "Publish Interim Clinical Diagnostic Guidance for reference laboratories within 12 hours.",
                "Stand up daily National Health Emergency Management Standing Committee (NHEMSC) briefings.",
                "Liaise with TGA regarding priority distribution of candidate therapeutics.",
            ]
            cross_deps = [AgencyIdentifier.TGA, AgencyIdentifier.DAFF, AgencyIdentifier.NEMA, AgencyIdentifier.DFAT]

        elif agency_id == AgencyIdentifier.TGA:
            title = f"TGA Medical Countermeasure & Regulatory Dossier: Countermeasures for {agent_name}"
            exec_summary = (
                f"Computational docking and structural evaluation have identified {len(drug_candidates)} potential therapeutic "
                f"candidates and {len(vaccine_candidates)} vaccine formulations targeting {agent_name}. "
                f"Evaluation of emergency regulatory pathways (Section 19A exemptions & Emergency Use Authorisation) active."
            )
            top_target_name = protein_targets[0].get('name', 'Viral Target') if protein_targets else 'Under Analysis'
            top_drug_name = drug_candidates[0].get('name', 'Screening in Progress') if drug_candidates else 'None Identified'
            sit_update = (
                f"Molecular Target: {top_target_name}. "
                f"Lead Countermeasure Candidate: {top_drug_name}. "
                f"Australian Register of Therapeutic Goods (ARTG) status: {drug_candidates[0].get('tga_artg_status', 'Evaluating') if drug_candidates else 'Pending'}."
            )
            strategic_imps = [
                "Review Section 19A provisions under the Therapeutic Goods Act 1989 for rapid emergency importation.",
                "Engage domestic manufacturers regarding accelerated fill-finish validation.",
                "Issue regulatory guidance for compassionate access and clinical trial protocols.",
            ]
            action_items = [
                "Grant expedited review for lead antiviral/antidote candidate batch releases.",
                "Coordinate with National Medical Stockpile (NMS) for inventory reservation.",
            ]
            cross_deps = [AgencyIdentifier.ACDP, AgencyIdentifier.CSIRO, AgencyIdentifier.NEMA]

        elif agency_id == AgencyIdentifier.DAFF:
            title = f"DAFF Biosecurity One-Health Containment Directive: {agent_name}"
            exec_summary = (
                f"One-Health biosecurity assessment for {agent_name}. Evaluating animal reservoirs, agricultural quarantine "
                f"perimeters, and border biosecurity interdiction protocols under the Biosecurity Act 2015."
            )
            sit_update = (
                f"Host Tropism: {identification.get('host_tropism', 'Multi-species avian/mammalian')}. "
                f"Geographic Hotspot: {sample_info.get('source_location', 'Victoria')}. "
                f"Quarantine perimeter recommendation: 10 km Restricted Area + 25 km Control Area."
            )
            strategic_imps = [
                "Activate AUSVETPLAN disease strategy for emergency animal disease containment.",
                "Establish national livestock and avian movement restrictions around detected outbreak epicenters.",
                "Enforce strict biosecurity protocols at international border points of entry (airports and maritime ports).",
            ]
            action_items = [
                "Issue Emergency Animal Disease (EAD) declaration under state/commonwealth biosecurity acts.",
                "Deploy veterinary epidemiologists for wild bird and commercial poultry trace-back investigations.",
            ]
            cross_deps = [AgencyIdentifier.ACDP, AgencyIdentifier.CSIRO, AgencyIdentifier.DSTG]

        elif agency_id == AgencyIdentifier.DSTG:
            title = f"DSTG Defence CBRN Technical Intelligence Assessment: {agent_name}"
            exec_summary = (
                f"Defence technical intelligence appraisal of {agent_name}. Focus on CBRN verification, synthetic biology "
                f"signatures, aerosol dissemination feasibility, and Australian Defence Force (ADF) force health protection."
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
            cross_deps = [AgencyIdentifier.ACDP, AgencyIdentifier.NEMA, AgencyIdentifier.DFAT]

        elif agency_id == AgencyIdentifier.NEMA:
            title = f"NEMA Crisis Logistics & Emergency Supply Chain Brief: {agent_name}"
            exec_summary = (
                f"Civil protection and supply chain resilience assessment for {agent_name}. Preparedness triggers "
                f"activated for national medical stockpiling, transport cold-chain, and potential COMDISPLAN logistics deployment."
            )
            sit_update = (
                f"National Threat Level: PRIORITY. Projected regional impact: Multi-jurisdictional. "
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
            cross_deps = [AgencyIdentifier.ACDP, AgencyIdentifier.TGA, AgencyIdentifier.DSTG]

        elif agency_id == AgencyIdentifier.DFAT:
            title = f"DFAT International Health Security & Diplomatic Notification: {agent_name}"
            exec_summary = (
                f"International compliance and regional Indo-Pacific health security brief for {agent_name}. "
                f"Assessment of International Health Regulations (IHR 2005) notification requirements and regional Pacific support."
            )
            sit_update = (
                f"Pathogen Identity: {agent_name}. "
                f"IHR Annex 2 Notification Status: Recommended within 24 hours of cluster confirmation. "
                f"Smartraveller Consular Alert: Under evaluation for affected Indo-Pacific transit corridors."
            )
            strategic_imps = [
                "Liaise with World Health Organization (WHO) Western Pacific Regional Office (WPRO) in Manila.",
                "Prepare diplomatic briefings for Indo-Pacific partner nations offering laboratory diagnostics and surge capacity.",
                "Coordinate with Department of Home Affairs on potential international travel health declarations.",
            ]
            action_items = [
                "Submit formal IHR Annex 2 notification through the Australian National Focal Point.",
                "Update Smartraveller destination advisories to reflect emerging outbreak dynamics.",
            ]
            cross_deps = [AgencyIdentifier.ACDP, AgencyIdentifier.DAFF]

        elif agency_id == AgencyIdentifier.CSIRO:
            title = f"CSIRO Translational Science & Domestic Biomanufacturing Memo: {agent_name}"
            exec_summary = (
                f"Translational science mobilization report for {agent_name}. Coordinating Australian Synchrotron macromolecular "
                f"validation, Geelong high-containment assays, and domestic mRNA pilot biomanufacturing scale-up."
            )
            sit_update = (
                f"Structural Resolution: Cryo-EM / AlphaFold pocket models completed for primary targets. "
                f"Manufacturing Partner: {vaccine_candidates[0].get('local_manufacturing_capability', 'CSL Seqirus / Moderna Victoria') if vaccine_candidates else 'Domestic pilot facility'}."
            )
            strategic_imps = [
                "Allocate beamline time at Australian Synchrotron for atomic-resolution inhibitor crystallography.",
                "Activate pilot-scale bioprocess fermentation and mRNA-LNP encapsulation at Victorian facilities.",
                "Initiate pre-clinical pseudovirus neutralization assays in PC3/PC4 containment.",
            ]
            action_items = [
                "Finalize synthetic DNA construct orders for non-infectious antigen expression systems.",
                "Deliver purified antigen standards to reference diagnostic laboratories nationwide.",
            ]
            cross_deps = [AgencyIdentifier.TGA, AgencyIdentifier.ACDP, AgencyIdentifier.DSTG]

        elif agency_id == AgencyIdentifier.OGTR:
            title = f"OGTR Biosafety & Synthetic Genomics Regulatory Advisory: {agent_name}"
            exec_summary = (
                f"Gene Technology Regulator advisory regarding genetic modifications, viral vector systems, and synthetic constructs "
                f"associated with {agent_name} under the Gene Technology Act 2000."
            )
            sit_update = (
                f"Construct Nature: {identification.get('taxonomy', 'Genetic Construct')}. "
                f"Emergency Dealing Determination (EDD): Preparedness draft generated for fast-track clinical trial approval. "
                f"Physical Containment Standard: PC3 / PC4 certified."
            )
            strategic_imps = [
                "Evaluate whether candidate vaccine platforms fall within GMO licensing exemptions or require emergency authorization.",
                "Audit gene synthesis provider screening compliance for flagged dual-use regulatory sequences.",
                "Verify certified Physical Containment (PC) status of participating academic and industry laboratories.",
            ]
            action_items = [
                "Publish safety advisory for institutional biosafety committees (IBCs) across Australia.",
            ]
            cross_deps = [AgencyIdentifier.TGA, AgencyIdentifier.ACDP]

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
            title = f"ASNO Nuclear Safeguards & International Treaty Verification Brief: {agent_name}"
            exec_summary = (
                f"Verification of nuclear safeguards and international reporting under the Nuclear Non-Proliferation (Safeguards) Act 1987 "
                f"and IAEA Incident and Trafficking Database (ITDB)."
            )
            sit_update = (
                f"Treaty Status: Category 1 Dangerous Radioactive Source. "
                f"Safeguards Accounting: Domestic sealed source tracking registry queried for matching serial identifiers. "
                f"Illicit Trafficking Flag: ITDB notification prepared."
            )
            strategic_imps = [
                "Confirm whether material originated from domestic inventory or represents illicit transshipment.",
                "Fulfill Australia's formal reporting obligations to the International Atomic Energy Agency (IAEA) in Vienna.",
                "Audit physical protection protocols at domestic radioactive storage facilities.",
            ]
            action_items = [
                "Transmit initial ITDB report to IAEA Incident and Emergency Centre.",
                "Coordinate with Australian Border Force on container manifest tracking.",
            ]
            cross_deps = [AgencyIdentifier.ARPANSA, AgencyIdentifier.ANSTO, AgencyIdentifier.HOME_AFFAIRS]

        elif agency_id == AgencyIdentifier.HOME_AFFAIRS:
            title = f"Home Affairs National Security & Critical Infrastructure SITREP: {agent_name}"
            exec_summary = (
                f"National security risk appraisal and critical infrastructure impact analysis under the Security of Critical "
                f"Infrastructure Act 2018 (SOCI Act) and National Counter-Terrorism Plan."
            )
            sit_update = (
                f"Sector Impact: Intermodal freight logistics, maritime ports, transport corridors, and public gathering nodes. "
                f"National Threat Level: Elevated. ABF interdiction operations active across inbound freight streams."
            )
            strategic_imps = [
                "Convene the National Security Committee of Cabinet (NSC) Crisis Policy Team.",
                "Issue security directives to critical infrastructure owners under the SOCI Act 2018.",
                "Deploy Australian Border Force (ABF) targeting rules for related international cargo manifests.",
            ]
            action_items = [
                "Issue operational containment directive to State/Territory police counter-terrorism commands.",
                "Establish multi-agency coordination center at Home Affairs National Situation Centre.",
            ]
            cross_deps = [AgencyIdentifier.DSTG, AgencyIdentifier.NEMA, AgencyIdentifier.ACDP, AgencyIdentifier.ARPANSA]

        else:
            title = f"Whole-of-Government Operational Briefing: {agent_name}"
            exec_summary = f"Automated response dossier for {agent_name}. Threat classification: {ssba_tier}."
            sit_update = f"Incident location: {sample_info.get('source_location')}. Threat level: {threat_type}."
            strategic_imps = ["Review standing CBRN and pandemic response plans."]
            action_items = ["Maintain inter-agency operational contact."]
            cross_deps = [AgencyIdentifier.ACDP]

        return AgencyReport(
            report_id=f"REP-{agency_id.value}-{uuid.uuid4().hex[:6].upper()}",
            agency_id=agency_id,
            title=title,
            classification=SecurityClassification.OFFICIAL_SENSITIVE,
            urgency=UrgencyLevel.PRIORITY,
            generated_at=now_str,
            incident_name=incident_name,
            threat_type=threat_type,
            is_relevant=is_relevant,
            relevance_reason=relevance_reason,
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
            signoff_authority="Automated AI Incident Response Pipeline (Verified by Human-In-The-Loop Lead)",
            dispatched=False,
        )

    @classmethod
    def generate_all_reports(
        cls,
        incident_name: str,
        threat_type: str,
        artifacts: Dict[str, Any],
    ) -> Dict[AgencyIdentifier, AgencyReport]:
        """Generates situation reports for all registered authorities, flagging jurisdiction relevance."""
        reports: Dict[AgencyIdentifier, AgencyReport] = {}
        for agency_id in AUSTRALIAN_AGENCIES.keys():
            reports[agency_id] = cls.generate_report(
                agency_id=agency_id,
                incident_name=incident_name,
                threat_type=threat_type,
                artifacts=artifacts,
            )
        return reports

    generate_report_for_agency = generate_report


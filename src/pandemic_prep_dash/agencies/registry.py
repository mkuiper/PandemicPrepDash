"""
Registry of Australian Whole-of-Government agencies involved in CBRN & Pandemic Response.
"""

from typing import Dict
from ..models.agency import AgencyIdentifier, AgencyProfile

AUSTRALIAN_AGENCIES: Dict[AgencyIdentifier, AgencyProfile] = {
    AgencyIdentifier.ACDC: AgencyProfile(
        id=AgencyIdentifier.ACDC,
        full_name="Australian Centre for Disease Control (Interim ACDC)",
        portfolio="Department of Health and Aged Care",
        mandate_summary="National leadership on public health emergency preparedness, disease surveillance, epidemiological risk analysis, and public health communication.",
        key_responsibilities=[
            "Real-time epidemic surveillance and genomic epidemiology",
            "National risk assessment and public health advice to Chief Medical Officer (CMO)",
            "Epidemic forecasting and mathematical transmission modeling",
            "National Incident Room (NIR) coordination and coordination with state CDNA units",
        ],
        statutory_authority="National Health Security Act 2007 (Cth)",
        liaison_contact_role="ACDC Chief Medical Advisor & Public Health Intelligence Lead",
        preferred_brief_format="Epidemiological Situation Report (SITREP) with R0, transmission vectors, and clinical case definitions."
    ),
    AgencyIdentifier.TGA: AgencyProfile(
        id=AgencyIdentifier.TGA,
        full_name="Therapeutic Goods Administration",
        portfolio="Department of Health and Aged Care",
        mandate_summary="Evaluating and regulating medicines, vaccines, medical devices, and rapid diagnostic tests for safety, quality, and efficacy.",
        key_responsibilities=[
            "Emergency Use Authorisations (EUA) and Section 19A emergency medicine import exemptions",
            "Expedited scientific evaluation of repurposed antivirals and novel vaccine candidates",
            "Batch testing, GMP release protocols, and cold-chain supply compliance",
            "Post-market safety surveillance and adverse event monitoring (DAEN)",
        ],
        statutory_authority="Therapeutic Goods Act 1989 (Cth)",
        liaison_contact_role="TGA Medical Countermeasures Regulatory Taskforce Director",
        preferred_brief_format="Regulatory & Medical Countermeasure Readiness Dossier (ARTG status, binding affinity, safety alerts, manufacturing timeline)."
    ),
    AgencyIdentifier.DAFF: AgencyProfile(
        id=AgencyIdentifier.DAFF,
        full_name="Department of Agriculture, Fisheries and Forestry (Biosecurity)",
        portfolio="Department of Agriculture, Fisheries and Forestry",
        mandate_summary="National border biosecurity, animal and plant health, surveillance of zoonotic spillovers, and agricultural economic protection.",
        key_responsibilities=[
            "Zoonotic spillover surveillance (e.g., Avian Influenza H5N1, Swine Flu, Henipavirus)",
            "Livestock and wildlife containment zones and quarantine movement controls",
            "Border biosecurity risk screening (BICON, air/sea ports of entry)",
            "Liaison with Australian Chief Veterinary Officer (ACVO) and World Organisation for Animal Health (WOAH)",
        ],
        statutory_authority="Biosecurity Act 2015 (Cth)",
        liaison_contact_role="Australian Chief Veterinary Officer (ACVO) & Biosecurity Operations Commander",
        preferred_brief_format="One-Health Zoonotic Alert (Species susceptibility, spillover risk, geographic quarantine bounds, livestock impact)."
    ),
    AgencyIdentifier.DSTG: AgencyProfile(
        id=AgencyIdentifier.DSTG,
        full_name="Defence Science and Technology Group & Defence CBRN",
        portfolio="Department of Defence",
        mandate_summary="National security science, CBRN defence counter-measures, dual-use pathogen forensics, and sovereign defence readiness.",
        key_responsibilities=[
            "Dual-use research and gain-of-function molecular forensics",
            "Physical and biological threat characterization and signature attribution",
            "Force health protection and military CBRN countermeasure stockpiles",
            "Aerosol dispersion modeling and decontamination protocol verification",
        ],
        statutory_authority="Defence Act 1903 (Cth) & Weapons of Mass Destruction Act 1995 (Cth)",
        liaison_contact_role="Director of Defence CBRN Scientific Counter-Measures",
        preferred_brief_format="CBRN Threat Intelligence Assessment (Synthetic origin markers, aerosolization potential, attribution, tactical countermeasures)."
    ),
    AgencyIdentifier.NEMA: AgencyProfile(
        id=AgencyIdentifier.NEMA,
        full_name="National Emergency Management Agency",
        portfolio="Department of Home Affairs",
        mandate_summary="Coordinating non-health national disaster and emergency operational response, crisis logistics, and cross-government civil defense.",
        key_responsibilities=[
            "Coordination of Australian Government Disaster Response Plan (COMDISPLAN)",
            "Critical supply chain stress testing (PPE, cold-chain distribution, oxygen supplies)",
            "Critical infrastructure protection and state/territory logistics surge support",
            "Crisis coordination briefings for the National Security Committee (NSC) of Cabinet",
        ],
        statutory_authority="Executive Order & Emergency Management Framework",
        liaison_contact_role="NEMA National Crisis Operations Duty Director",
        preferred_brief_format="Crisis Logistics & Supply Chain Impact Assessment (Resource burn rates, transport bottlenecks, stockpile thresholds)."
    ),
    AgencyIdentifier.DFAT: AgencyProfile(
        id=AgencyIdentifier.DFAT,
        full_name="Department of Foreign Affairs and Trade",
        portfolio="Department of Foreign Affairs and Trade",
        mandate_summary="International diplomatic coordination, consular travel advisories, global health security partnerships, and multilateral notification.",
        key_responsibilities=[
            "Formal notification to World Health Organization (WHO) under IHR (2005) Article 6",
            "Smartraveller travel advisories and consular assistance to Australians abroad",
            "Indo-Pacific Centre for Health Security coordination and regional partner support",
            "Coordination of international medical supplies and cross-border vaccine diplomacy",
        ],
        statutory_authority="International Health Regulations (2005) & Diplomatic Mandate",
        liaison_contact_role="First Assistant Secretary, Global Health & Humanitarian Division",
        preferred_brief_format="Diplomatic & International Health Security Brief (WHO IHR compliance, regional Pacific risk, border travel advice)."
    ),
    AgencyIdentifier.CSIRO: AgencyProfile(
        id=AgencyIdentifier.CSIRO,
        full_name="CSIRO - Australian Centre for Disease Preparedness (ACDP)",
        portfolio="Industry, Science and Resources",
        mandate_summary="Australia's national high-containment (PC4) laboratory and science agency for pathogen isolation, structural biology, and pilot manufacturing.",
        key_responsibilities=[
            "High-containment PC4 diagnostic confirmation and live pathogen isolation",
            "Cryo-EM structural biology and molecular modeling of novel targets",
            "In vivo challenge animal models for vaccine and therapeutic evaluation",
            "Pilot-scale biological countermeasure synthesis and formulation development",
        ],
        statutory_authority="Science and Industry Research Act 1949 (Cth)",
        liaison_contact_role="ACDP Director of High Containment Diagnostics & Bio-Platforms",
        preferred_brief_format="Laboratory Diagnostic & Countermeasure Synthesis Technical Brief (Cryo-EM, structural metrics, challenge model protocols)."
    ),
    AgencyIdentifier.OGTR: AgencyProfile(
        id=AgencyIdentifier.OGTR,
        full_name="Office of the Gene Technology Regulator",
        portfolio="Department of Health and Aged Care",
        mandate_summary="Protecting the health and safety of people and the environment by identifying and managing risks posed by gene technology.",
        key_responsibilities=[
            "Regulation of genetically modified organisms (GMOs) and synthetic biology constructs",
            "Licensing of viral-vectored vaccines and modified viral platforms",
            "Physical containment certification for experimental laboratories",
            "Audit of synthetic gene synthesis orders and dual-use biotechnology vectors",
        ],
        statutory_authority="Gene Technology Act 2000 (Cth)",
        liaison_contact_role="Gene Technology Regulator & Chief Biosafety Assessor",
        preferred_brief_format="Biosafety & Gene Technology Compliance Notice (GMO classification, containment requirements, licensing schedule)."
    ),
}

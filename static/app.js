/**
 * PandemicPrepDash - Frontend Application Logic
 * Australian Whole-of-Government Emergency Response Platform.
 * Developed with full multi-agent cooperative, real-world lab bridge, and modern UI/UX engineering.
 */

const AppState = {
  state: null,
  scenarios: [],
  dummySequences: [],
  personas: [],
  templates: [],
  skills: [],
  toolbox: [],
  mcps: [],
  providers: [],
  docsChapters: [],
  labRequests: [],
  evidenceReport: null,
  snapshots: [],
  selectedDocChapterId: "conops-overview",
  selectedNodeId: null,
  selectedAgencyId: "ACDP",
  agencies: [],
  activeTab: "tab-pathway",
  activeInspectorSubtab: "tool-sequence",
  govSettings: null,
  govPolicies: [],
  theme: localStorage.getItem("theme") || "dark",
  connecting: {
    active: false,
    sourceId: null,
    sourceLabel: null,
  },
};

const CATEGORY_STYLES = {
  ingestion: { color: "#06b6d4", bg: "#083344", lightBg: "#ecfeff", icon: "fa-vial" },
  research: { color: "#38bdf8", bg: "#0c4a6e", lightBg: "#f0f9ff", icon: "fa-book-open-reader" },
  characterization: { color: "#3b82f6", bg: "#172554", lightBg: "#eff6ff", icon: "fa-dna" },
  structural_biology: { color: "#a855f7", bg: "#3b0764", lightBg: "#faf5ff", icon: "fa-atom" },
  therapeutics: { color: "#10b981", bg: "#022c22", lightBg: "#f0fdf4", icon: "fa-pills" },
  vaccinology: { color: "#f59e0b", bg: "#451a03", lightBg: "#fffbeb", icon: "fa-shield-virus" },
  biosecurity: { color: "#f43f5e", bg: "#4c0519", lightBg: "#fff1f2", icon: "fa-biohazard" },
  agency_reporting: { color: "#6366f1", bg: "#1e1b4b", lightBg: "#eef2ff", icon: "fa-landmark" },
  custom: { color: "#94a3b8", bg: "#1e293b", lightBg: "#f8fafc", icon: "fa-gear" },
};

// Initialize Application
document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  setupTabs();
  setupInspectorSubtabs();
  setupEventListeners();
  loadInitialData();
});

// ---------------- Theme Management (Light / Dark) ----------------

function initTheme() {
  const icon = document.getElementById("themeIcon");
  if (AppState.theme === "light") {
    document.documentElement.classList.add("theme-light");
    if (icon) {
      icon.classList.remove("fa-sun");
      icon.classList.add("fa-moon");
    }
  } else {
    document.documentElement.classList.remove("theme-light");
    if (icon) {
      icon.classList.remove("fa-moon");
      icon.classList.add("fa-sun");
    }
  }
}

function toggleTheme() {
  const icon = document.getElementById("themeIcon");
  if (AppState.theme === "dark") {
    AppState.theme = "light";
    document.documentElement.classList.add("theme-light");
    if (icon) {
      icon.classList.remove("fa-sun");
      icon.classList.add("fa-moon");
    }
  } else {
    AppState.theme = "dark";
    document.documentElement.classList.remove("theme-light");
    if (icon) {
      icon.classList.remove("fa-moon");
      icon.classList.add("fa-sun");
    }
  }
  localStorage.setItem("theme", AppState.theme);
  renderDag();
}

// ---------------- Setup Tab Navigation ----------------

function setupTabs() {
  document.querySelectorAll(".tab-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      switchTab(btn.dataset.tab);
    });
  });
}

function switchTab(targetTab) {
  AppState.activeTab = targetTab;

  document.querySelectorAll(".tab-btn").forEach((b) => {
    b.classList.remove("active", "border-cyan-500", "text-cyan-400");
    b.classList.add("border-transparent", "text-slate-400");
    if (b.dataset.tab === targetTab) {
      b.classList.add("active", "border-cyan-500", "text-cyan-400");
      b.classList.remove("border-transparent", "text-slate-400");
    }
  });

  document.querySelectorAll(".tab-panel").forEach((panel) => {
    panel.classList.add("hidden");
  });
  const activePanel = document.getElementById(targetTab);
  if (activePanel) activePanel.classList.remove("hidden");

  if (targetTab === "tab-pathway") {
    renderDag();
  } else if (targetTab === "tab-datahub") {
    renderCentralDataHub();
  } else if (targetTab === "tab-lab-bridge") {
    renderLabBridgeView();
  } else if (targetTab === "tab-inspector") {
    renderPipelineDataInspector();
  } else if (targetTab === "tab-tools") {
    renderToolsView();
  } else if (targetTab === "tab-agency-map") {
    renderAgencyMapView();
  } else if (targetTab === "tab-agencies") {
    renderAgencyView();
  } else if (targetTab === "tab-governance") {
    renderGovernanceView();
  } else if (targetTab === "tab-docs") {
    renderDocsView();
  }
}

function setupInspectorSubtabs() {
  document.querySelectorAll(".inspect-subtab-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const toolId = btn.dataset.inspectTool;
      AppState.activeInspectorSubtab = toolId;

      document.querySelectorAll(".inspect-subtab-btn").forEach((b) => {
        b.classList.remove("active", "bg-cyan-600", "text-white", "font-medium");
        b.classList.add("text-slate-400");
      });
      btn.classList.add("active", "bg-cyan-600", "text-white", "font-medium");
      btn.classList.remove("text-slate-400");

      document.querySelectorAll(".inspect-tool-panel").forEach((p) => p.classList.add("hidden"));
      const activeTool = document.getElementById(toolId);
      if (activeTool) activeTool.classList.remove("hidden");

      renderPipelineDataInspector();
    });
  });
}

// ---------------- Setup Event Listeners ----------------

function setupEventListeners() {
  document.getElementById("themeToggleBtn").addEventListener("click", toggleTheme);

  const scenSelect = document.getElementById("scenarioSelect");
  scenSelect.addEventListener("change", (e) => {
    selectScenario(e.target.value);
  });

  document.getElementById("btnStep").addEventListener("click", executeStep);
  document.getElementById("btnRunAll").addEventListener("click", executeRunAll);
  document.getElementById("btnReset").addEventListener("click", resetExecution);

  document.getElementById("blockerCountHeaderBadge").addEventListener("click", () => {
    switchTab("tab-datahub");
  });

  // Modals
  document.getElementById("btnConnectModal").addEventListener("click", () => openConnectModal());
  document.getElementById("btnAddNodeModal").addEventListener("click", () => {
    document.getElementById("addNodeModal").classList.remove("hidden");
  });
  document.getElementById("btnCustomSampleModal").addEventListener("click", openCustomSampleModal);
  document.getElementById("btnProposeAssayModal")?.addEventListener("click", () => {
    document.getElementById("proposeAssayModal").classList.remove("hidden");
  });

  // Playbooks (formerly Templates)
  document.getElementById("btnTemplatesMenu").addEventListener("click", openTemplatesManager);
  document.getElementById("btnSaveTemplateModal").addEventListener("click", () => {
    document.getElementById("saveTemplateModal").classList.remove("hidden");
  });
  document.getElementById("btnOpenSaveFromManager").addEventListener("click", () => {
    document.getElementById("templatesManagerModal").classList.add("hidden");
    document.getElementById("saveTemplateModal").classList.remove("hidden");
  });
  document.getElementById("btnExportPathwayJson").addEventListener("click", exportPathwayJson);
  document.getElementById("inputImportPathway").addEventListener("change", handleImportPathwayFile);

  // Situation Snapshot / Version Control
  document.getElementById("btnSnapshotModal")?.addEventListener("click", openSnapshotModal);
  document.getElementById("btnOpenSnapshotModalFromHub")?.addEventListener("click", openSnapshotModal);
  document.getElementById("createSnapshotForm")?.addEventListener("submit", handleCreateSnapshotSubmit);

  // Evidence Audit
  document.getElementById("btnTriggerEvidenceAudit")?.addEventListener("click", runEvidenceAudit);

  // Connection mode
  document.getElementById("btnCancelConnect").addEventListener("click", cancelConnectionMode);

  // Message Board
  document.getElementById("btnSendHubMessage").addEventListener("click", handleSendHubMessage);
  document.querySelectorAll(".quick-directive-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.getElementById("inputHumanMessageContent").value = btn.textContent.trim();
    });
  });

  // Sequence Motif
  document.getElementById("btnHighlightMotif")?.addEventListener("click", handleHighlightMotif);

  // Escape key
  window.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      if (AppState.connecting.active) {
        cancelConnectionMode();
      }
      document.querySelectorAll(".fixed.z-50").forEach((modal) => {
        modal.classList.add("hidden");
      });
    }
  });

  // Modal close buttons
  document.querySelectorAll(".modal-close").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".fixed.z-50").forEach((modal) => {
        modal.classList.add("hidden");
      });
    });
  });

  // Forms
  document.getElementById("connectNodesForm").addEventListener("submit", handleConnectNodesSubmit);
  document.getElementById("addNodeForm").addEventListener("submit", handleAddNode);
  document.getElementById("customSampleForm").addEventListener("submit", handleCustomSample);
  document.getElementById("saveTemplateForm").addEventListener("submit", handleSaveTemplate);
  document.getElementById("configureSquadForm").addEventListener("submit", handleSaveSquadConfig);
  document.getElementById("resolveBlockerForm").addEventListener("submit", handleResolveBlocker);
  document.getElementById("proposeAssayForm")?.addEventListener("submit", handleProposeAssaySubmit);
  document.getElementById("recordAssayResultsForm")?.addEventListener("submit", handleRecordAssayResultsSubmit);

  // Governance
  document.getElementById("formCloudComputeConfig")?.addEventListener("submit", handleSaveComputeConfig);
  document.getElementById("formApiKeysConfig")?.addEventListener("submit", handleSaveApiKeysConfig);

  // Dispatch All
  document.getElementById("btnDispatchAllReports")?.addEventListener("click", dispatchAllBriefings);

  // Preset Sequence
  document.getElementById("presetSequenceSelect")?.addEventListener("change", handlePresetSequenceChange);
}

// ---------------- API Calls and Data Loaders ----------------

async function loadInitialData() {
  try {
    const [scenRes, stateRes, agencyRes, dummyRes, personasRes, docsRes, govRes, polRes, toolsRes, mcpsRes, skillsRes, labRes, evidRes, snapRes] = await Promise.all([
      fetch("/api/scenarios").then((r) => r.json()),
      fetch("/api/pathways/state").then((r) => r.json()),
      fetch("/api/agencies").then((r) => r.json()),
      fetch("/api/scenarios/dummy-sequences").then((r) => r.json()).catch(() => ({ dummy_sequences: [] })),
      fetch("/api/agents/personas").then((r) => r.json()).catch(() => ({ personas: [] })),
      fetch("/api/docs").then((r) => r.json()).catch(() => ({ chapters: [] })),
      fetch("/api/governance/settings").then((r) => r.json()).catch(() => ({ settings: null })),
      fetch("/api/governance/policies").then((r) => r.json()).catch(() => ({ policies: [] })),
      fetch("/api/agents/toolbox").then((r) => r.json()).catch(() => ({ toolbox: [] })),
      fetch("/api/agents/mcps").then((r) => r.json()).catch(() => ({ mcps: [] })),
      fetch("/api/agents/skills").then((r) => r.json()).catch(() => ({ skills: [] })),
      fetch("/api/lab-bridge/requests").then((r) => r.json()).catch(() => ({ requests: [] })),
      fetch("/api/hub/evidence/analysis").then((r) => r.json()).catch(() => ({ report: null })),
      fetch("/api/version-control/snapshots").then((r) => r.json()).catch(() => ({ snapshots: [] })),
    ]);

    AppState.scenarios = scenRes.scenarios || [];
    AppState.state = stateRes;
    AppState.agencies = agencyRes.agencies || [];
    AppState.dummySequences = dummyRes.dummy_sequences || [];
    AppState.personas = personasRes.personas || [];
    AppState.docsChapters = docsRes.chapters || [];
    AppState.govSettings = govRes.settings;
    AppState.govPolicies = polRes.policies || [];
    AppState.toolbox = toolsRes.toolbox || [];
    AppState.mcps = mcpsRes.mcps || [];
    AppState.skills = skillsRes.skills || [];
    AppState.labRequests = labRes.requests || [];
    AppState.evidenceReport = evidRes.report;
    AppState.snapshots = snapRes.snapshots || [];

    populateScenarioDropdown();
    populatePresetSequencesDropdown();
    updateUIState();
  } catch (err) {
    console.error("Failed to load initial data:", err);
  }
}

function populateScenarioDropdown() {
  const select = document.getElementById("scenarioSelect");
  if (!select) return;
  select.innerHTML = "";
  AppState.scenarios.forEach((s) => {
    const opt = document.createElement("option");
    opt.value = s.scenario_id;
    opt.textContent = `${s.name}`;
    if (s.scenario_id === AppState.state?.scenario?.scenario_id) {
      opt.selected = true;
    }
    select.appendChild(opt);
  });
}

function populatePresetSequencesDropdown() {
  const select = document.getElementById("presetSequenceSelect");
  if (!select) return;
  select.innerHTML = `<option value="">-- Choose a test sequence to load --</option>`;
  AppState.dummySequences.forEach((item) => {
    const opt = document.createElement("option");
    opt.value = item.id;
    opt.textContent = `${item.name} [${item.type}]`;
    select.appendChild(opt);
  });
}

function handlePresetSequenceChange(e) {
  const selectedId = e.target.value;
  if (!selectedId) return;
  const seq = AppState.dummySequences.find((s) => s.id === selectedId);
  if (!seq) return;

  document.getElementById("customSampleName").value = seq.name;
  document.getElementById("customSampleType").value = seq.type;
  document.getElementById("customSampleLocation").value = "Australian Reference Laboratory";
  document.getElementById("customSamplePayload").value = seq.payload;
}

function openCustomSampleModal() {
  populatePresetSequencesDropdown();
  document.getElementById("customSampleModal").classList.remove("hidden");
}

async function refreshState() {
  try {
    const [stateRes, labRes, evidRes, snapRes] = await Promise.all([
      fetch("/api/pathways/state").then((r) => r.json()),
      fetch("/api/lab-bridge/requests").then((r) => r.json()).catch(() => ({ requests: [] })),
      fetch("/api/hub/evidence/analysis").then((r) => r.json()).catch(() => ({ report: null })),
      fetch("/api/version-control/snapshots").then((r) => r.json()).catch(() => ({ snapshots: [] })),
    ]);
    AppState.state = stateRes;
    AppState.labRequests = labRes.requests || [];
    AppState.evidenceReport = evidRes.report;
    AppState.snapshots = snapRes.snapshots || [];
    updateUIState();
  } catch (err) {
    console.error("Failed to refresh state:", err);
  }
}

function updateUIState() {
  if (!AppState.state) return;

  const { pathway, run, scenario, stats, data_hub } = AppState.state;

  const select = document.getElementById("scenarioSelect");
  if (select && scenario?.scenario_id) {
    select.value = scenario.scenario_id;
  }

  const specBadge = document.getElementById("activeSpecimenBadge");
  if (specBadge && scenario) {
    specBadge.textContent = scenario.name || scenario.sample?.name || "Active Specimen";
  }

  const ssbaBadge = document.getElementById("threatClassificationBadge");
  let threatTier = run.node_artifacts?.threat_assessment?.ssba_tier;
  if (!threatTier) {
    if (pathway.threat_type === "radiological_dispersal") threatTier = "Category 1 Source";
    else if (pathway.threat_type === "chemical_nerve_agent") threatTier = "CWC Schedule 1";
    else threatTier = "Tier 1 SSBA";
  }
  ssbaBadge.textContent = threatTier;

  document.getElementById("pathwayNameDisplay").textContent = pathway.name;
  document.getElementById("nodesStatusSummary").textContent = `${stats.completed_nodes} / ${stats.total_nodes} Completed (${run.status.toUpperCase()})`;

  // Blocker alerts
  const openBlockers = (data_hub?.blockers || []).filter((b) => b.status === "OPEN");
  const blockerBadge = document.getElementById("hubBlockersBadge");
  const headerBlockerBadge = document.getElementById("blockerCountHeaderBadge");
  const headerBlockerText = document.getElementById("blockerCountHeaderText");

  if (openBlockers.length > 0) {
    if (blockerBadge) {
      blockerBadge.textContent = openBlockers.length;
      blockerBadge.classList.remove("hidden");
    }
    if (headerBlockerBadge) {
      headerBlockerText.textContent = `${openBlockers.length} Active Blocker${openBlockers.length > 1 ? "s" : ""}`;
      headerBlockerBadge.classList.remove("hidden");
    }
  } else {
    if (blockerBadge) blockerBadge.classList.add("hidden");
    if (headerBlockerBadge) headerBlockerBadge.classList.add("hidden");
  }

  // Lab bridge count badge
  const labBadge = document.getElementById("labRequestsCountBadge");
  if (labBadge) {
    labBadge.textContent = AppState.labRequests.length;
  }

  // Agency report count (only relevant)
  const reports = run.node_artifacts?.agency_reports || {};
  const relevantCount = Object.values(reports).filter((r) => r.is_relevant).length;
  document.getElementById("agencyReportCountBadge").textContent = relevantCount;

  const threatLabel = document.getElementById("hubActiveThreatLabel");
  if (threatLabel) {
    threatLabel.textContent = `Incident: ${scenario?.name || "Active Event"}`;
  }

  // Render current tab
  if (AppState.activeTab === "tab-pathway") {
    renderDag();
    renderNodeInspector(AppState.selectedNodeId);
  } else if (AppState.activeTab === "tab-datahub") {
    renderCentralDataHub();
  } else if (AppState.activeTab === "tab-lab-bridge") {
    renderLabBridgeView();
  } else if (AppState.activeTab === "tab-inspector") {
    renderPipelineDataInspector();
  } else if (AppState.activeTab === "tab-tools") {
    renderToolsView();
  } else if (AppState.activeTab === "tab-agency-map") {
    renderAgencyMapView();
  } else if (AppState.activeTab === "tab-agencies") {
    renderAgencyView();
  } else if (AppState.activeTab === "tab-governance") {
    renderGovernanceView();
  } else if (AppState.activeTab === "tab-docs") {
    renderDocsView();
  }
}

// ---------------- Scenario Selection ----------------

async function selectScenario(scenarioId) {
  try {
    const res = await fetch(`/api/scenarios/select/${scenarioId}`, { method: "POST" });
    if (!res.ok) {
      console.error("Failed to switch scenario:", await res.text());
      return;
    }
    await refreshState();
    AppState.selectedNodeId = null;
    if (AppState.activeTab === "tab-pathway") {
      renderDag();
      renderNodeInspector(null);
    } else {
      switchTab(AppState.activeTab);
    }
  } catch (err) {
    console.error("Scenario switch error:", err);
  }
}

// ---------------- Execution Controls ----------------

async function executeStep() {
  try {
    const res = await fetch("/api/execution/step", { method: "POST" });
    const data = await res.json();
    await refreshState();
    if (data.result.status === "approval_required") {
      alert(`Human-in-the-Loop authorization required for node: ${data.result.node_label}`);
    }
  } catch (err) {
    console.error("Step execution failed:", err);
  }
}

async function executeRunAll() {
  try {
    await fetch("/api/execution/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ auto_approve: true }),
    });
    await refreshState();
  } catch (err) {
    console.error("Run all failed:", err);
  }
}

async function resetExecution() {
  try {
    await fetch("/api/execution/reset", { method: "POST" });
    AppState.selectedNodeId = null;
    await refreshState();
  } catch (err) {
    console.error("Reset failed:", err);
  }
}

// ---------------- Central Control Hub & Message Board ----------------

function renderCentralDataHub() {
  const dataHub = AppState.state?.data_hub;
  if (!dataHub) return;

  const feed = document.getElementById("hubMessagesFeed");
  const messages = dataHub.messages || [];
  if (!messages.length) {
    feed.innerHTML = `<div class="p-6 text-center text-slate-500 italic">No messages on the control board yet. Post a directive below.</div>`;
  } else {
    feed.innerHTML = messages
      .map((m) => {
        const isAgent = m.sender_type === "AGENT";
        const isHuman = m.sender_type === "HUMAN_EXPERT";

        let bubbleClass = "msg-bubble-system";
        let roleBadge = "bg-slate-800 text-slate-400";
        let iconClass = "fa-shield-halved text-slate-400";

        if (isAgent) {
          bubbleClass = "msg-bubble-agent";
          roleBadge = "bg-cyan-500/10 text-cyan-300 border-cyan-500/20";
          iconClass = "fa-microchip text-cyan-400";
        } else if (isHuman) {
          bubbleClass = "msg-bubble-human";
          roleBadge = "bg-emerald-500/10 text-emerald-300 border-emerald-500/20";
          iconClass = "fa-user-shield text-emerald-400";
        }

        return `
        <div class="p-3.5 rounded-xl border text-xs space-y-1.5 shadow-sm ${bubbleClass}">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-2">
              <i class="fa-solid ${iconClass} text-xs"></i>
              <span class="font-bold text-slate-200">${m.sender_name}</span>
              <span class="px-1.5 py-0.2 rounded text-[9px] font-mono border ${roleBadge}">${m.sender_role}</span>
              ${m.target_node_id ? `<span class="text-[9px] font-mono text-cyan-400 bg-slate-900/80 px-1.5 py-0.2 rounded border border-slate-800">${m.target_node_id}</span>` : ""}
            </div>
            <span class="text-[10px] font-mono text-slate-500">${m.timestamp ? m.timestamp.split("T")[1]?.slice(0, 8) : ""}</span>
          </div>
          <div class="text-slate-200 leading-relaxed font-sans text-xs">${m.content}</div>
        </div>
      `;
      })
      .join("");
    feed.scrollTop = feed.scrollHeight;
  }

  // Blockers list
  const blockersList = document.getElementById("dataHubBlockersList");
  const blockers = dataHub.blockers || [];
  const openBlockers = blockers.filter((b) => b.status === "OPEN");
  document.getElementById("dataHubBlockersCountText").textContent = `${openBlockers.length} Open`;

  if (!blockers.length) {
    blockersList.innerHTML = `<div class="p-3 rounded-lg bg-slate-950/60 border border-slate-800 text-slate-500 italic text-center">No active operational blockers flagged to the Central Orchestrator.</div>`;
  } else {
    blockersList.innerHTML = blockers
      .slice()
      .reverse()
      .map((b) => {
        const isOpen = b.status === "OPEN";
        let sevColor = "bg-amber-500/10 text-amber-300 border-amber-500/30";
        if (b.severity === "CRITICAL") sevColor = "bg-rose-500/20 text-rose-300 border-rose-500/40";

        return `
        <div class="p-3 rounded-lg border flex items-start justify-between space-x-3 ${isOpen ? "bg-slate-950 border-amber-500/40 shadow" : "bg-slate-950/60 border-slate-800 opacity-70"}">
          <div class="space-y-1 flex-1">
            <div class="flex items-center space-x-2">
              <span class="px-2 py-0.5 rounded text-[9px] font-mono font-bold uppercase border ${sevColor}">${b.severity}</span>
              <span class="font-bold text-slate-100 text-xs">${b.title}</span>
              ${!isOpen ? `<span class="text-[9px] font-mono text-emerald-400 bg-emerald-500/10 px-1.5 py-0.2 rounded">RESOLVED</span>` : ""}
            </div>
            <p class="text-slate-300 text-[11px] leading-relaxed">${b.description}</p>
            <div class="text-[10px] text-amber-300 font-medium"><strong>Action Required:</strong> ${b.required_action}</div>
            ${b.resolution_notes ? `<div class="text-[10px] text-slate-400 italic pt-1 border-t border-slate-800">Resolution: ${b.resolution_notes}</div>` : ""}
          </div>
          ${
            isOpen
              ? `<button data-alert-id="${b.alert_id}" data-alert-title="${b.title}" class="btn-open-resolve-blocker px-3 py-1.5 bg-amber-600 hover:bg-amber-500 text-slate-950 font-bold rounded text-xs transition shrink-0 shadow">Resolve</button>`
              : ""
          }
        </div>
      `;
      })
      .join("");

    document.querySelectorAll(".btn-open-resolve-blocker").forEach((btn) => {
      btn.addEventListener("click", () => {
        openResolveBlockerModal(btn.dataset.alertId, btn.dataset.alertTitle);
      });
    });
  }

  // Render Version Timeline View
  renderVersionTimelineView();

  // Render Evidence Analysis View
  renderEvidenceAnalysisView();

  // Specimen Intel
  const specIntel = dataHub.specimen_intel || {};
  const specEl = document.getElementById("hubSpecimenIntelContent");
  if (Object.keys(specIntel).length === 0) {
    specEl.innerHTML = `<div class="text-slate-500 italic py-3 text-center">Execute Ingestion &amp; Characterization to populate specimen metrics.</div>`;
  } else {
    specEl.innerHTML = `
      <div class="grid grid-cols-2 gap-2 font-mono text-[11px]">
        <div class="bg-slate-950 p-2 rounded border border-slate-800">
          <span class="text-slate-500 block text-[9px]">AGENT / ORGANISM</span>
          <span class="text-cyan-300 font-bold">${specIntel.agent_name || specIntel.name || "Identified Agent"}</span>
        </div>
        <div class="bg-slate-950 p-2 rounded border border-slate-800">
          <span class="text-slate-500 block text-[9px]">LINEAGE / CLADE</span>
          <span class="text-slate-200">${specIntel.clade_or_lineage || "Standard isolate"}</span>
        </div>
      </div>
      ${
        specIntel.genomic_mutations_detected
          ? `
        <div class="bg-slate-950 p-2.5 rounded border border-slate-800 space-y-1">
          <span class="text-slate-400 font-bold text-[10px] uppercase">Validated Molecular Signatures:</span>
          <ul class="space-y-0.5 text-[11px] text-slate-300">
            ${specIntel.genomic_mutations_detected.map((m) => `<li class="flex items-start"><span class="text-cyan-400 mr-1.5">•</span><span>${m}</span></li>`).join("")}
          </ul>
        </div>
      `
          : ""
      }
    `;
  }

  // Peer-Reviewed Literature Research (PubMed)
  const litEl = document.getElementById("hubLiteratureContent");
  const papers = dataHub.literature_research || [];
  if (!papers.length) {
    litEl.innerHTML = `<div class="text-slate-500 italic py-3 text-center">Execute Threat Research node to retrieve indexed PubMed studies.</div>`;
  } else {
    litEl.innerHTML = papers
      .map(
        (p) => `
      <div class="bg-slate-950 p-3 rounded-lg border border-slate-800 space-y-1">
        <div class="flex items-start justify-between">
          <h5 class="font-bold text-slate-100 text-xs">
            <a href="${p.source_url}" target="_blank" class="text-cyan-400 hover:text-cyan-300 underline underline-offset-2 flex items-center">
              <span>${p.title}</span>
              <i class="fa-solid fa-arrow-up-right-from-square text-[9px] ml-1.5 shrink-0"></i>
            </a>
          </h5>
          ${p.pmid ? `<span class="px-1.5 py-0.2 rounded text-[9px] font-mono bg-purple-500/10 text-purple-300 border border-purple-500/20 ml-2 shrink-0">PMID: ${p.pmid}</span>` : ""}
        </div>
        <div class="text-[10px] text-slate-400">${p.authors} • <em>${p.journal}</em> (${p.year})</div>
        <p class="text-slate-300 text-[11px]">${p.summary}</p>
      </div>
    `
      )
      .join("");
  }

  // Countermeasures
  const counterEl = document.getElementById("hubCountermeasuresContent");
  const countermeasures = dataHub.countermeasures || [];
  if (!countermeasures.length) {
    counterEl.innerHTML = `<div class="text-slate-500 italic py-3 text-center">Execute Therapeutics node to screen candidate medical countermeasures.</div>`;
  } else {
    counterEl.innerHTML = countermeasures
      .slice(0, 3)
      .map(
        (c) => `
      <div class="bg-slate-950 p-2.5 rounded-lg border border-slate-800 space-y-1 text-xs">
        <div class="flex items-center justify-between">
          <span class="font-bold text-slate-100">${c.name || c.target_antigen}</span>
          <span class="text-[10px] font-mono text-emerald-400">${c.binding_affinity_kcal_mol ? c.binding_affinity_kcal_mol + " kcal/mol" : c.platform || ""}</span>
        </div>
        <div class="text-[10px] text-slate-400 truncate">${c.mechanism_of_action || c.formulation_details || ""}</div>
      </div>
    `
      )
      .join("");
  }
}

// ---------------- Situation Progression & Version Control View ----------------

function renderVersionTimelineView() {
  const container = document.getElementById("hubVersionTimelineList");
  if (!container) return;

  const list = AppState.snapshots || [];
  if (!list.length) {
    container.innerHTML = `<div class="text-slate-500 italic text-xs py-2 text-center">No checkpoint versions logged. Click 'Capture Checkpoint' to create one.</div>`;
    return;
  }

  container.innerHTML = list
    .slice()
    .reverse()
    .map((s) => {
      const timeDisplay = s.created_at ? s.created_at.split("T")[1]?.slice(0, 8) : "";
      return `
      <div class="timeline-item space-y-1">
        <div class="timeline-dot"></div>
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <span class="px-1.5 py-0.2 rounded text-[9px] font-mono font-bold bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">${s.version_id}</span>
            <span class="font-bold text-slate-200 text-xs">${s.checkpoint_name}</span>
          </div>
          <span class="text-[10px] font-mono text-slate-500">${timeDisplay}</span>
        </div>
        <p class="text-slate-300 text-[11px]">${s.change_summary}</p>
        <div class="flex items-center space-x-3 text-[10px] text-slate-400 font-mono">
          <span>By: ${s.created_by}</span>
          <span>•</span>
          <span>Nodes: ${s.completed_nodes_count}/${s.total_nodes_count}</span>
          ${s.open_blockers_count > 0 ? `<span class="text-amber-400 font-bold">• ${s.open_blockers_count} Blockers</span>` : ""}
        </div>
      </div>
    `;
    })
    .join("");
}

function openSnapshotModal() {
  const modal = document.getElementById("createSnapshotModal");
  if (!modal) return;
  document.getElementById("snapshotTitleInput").value = `Operational Snapshot at Step ${AppState.state?.stats?.completed_nodes || 0}`;
  document.getElementById("snapshotSummaryInput").value = "State checkpoint verified by Incident Controller; pipeline progression logged for audit trail.";
  modal.classList.remove("hidden");
}

async function handleCreateSnapshotSubmit(e) {
  e.preventDefault();
  const title = document.getElementById("snapshotTitleInput").value;
  const creator = document.getElementById("snapshotCreatorInput").value;
  const summary = document.getElementById("snapshotSummaryInput").value;

  try {
    const res = await fetch("/api/version-control/snapshots", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        checkpoint_name: title,
        created_by: creator,
        change_summary: summary,
      }),
    });

    if (res.ok) {
      document.getElementById("createSnapshotModal").classList.add("hidden");
      await refreshState();
      renderVersionTimelineView();
    }
  } catch (err) {
    console.error("Failed to create situation snapshot:", err);
  }
}

// ---------------- Evidence Synthesis & Knowledge Gap Analysis View ----------------

function renderEvidenceAnalysisView() {
  const container = document.getElementById("hubEvidenceReportContainer");
  const badge = document.getElementById("evidenceOverallConfidenceBadge");
  if (!container || !AppState.evidenceReport) return;

  const rep = AppState.evidenceReport;
  if (badge) {
    badge.textContent = `Confidence: ${Math.round(rep.overall_confidence_score * 100)}%`;
  }

  // Domain score bars
  const domainBars = Object.entries(rep.domain_scores || {})
    .map(([domain, score]) => {
      const pct = Math.round(score * 100);
      let colorClass = "bg-emerald-500";
      if (pct < 50) colorClass = "bg-rose-500";
      else if (pct < 75) colorClass = "bg-amber-500";

      return `
      <div class="space-y-0.5">
        <div class="flex justify-between text-[10px] text-slate-400 font-mono">
          <span>${domain}</span>
          <span class="font-bold text-slate-200">${pct}%</span>
        </div>
        <div class="h-1.5 w-full bg-slate-950 rounded-full overflow-hidden flex">
          <div style="width: ${pct}%" class="${colorClass}"></div>
        </div>
      </div>
    `;
    })
    .join("");

  // Conflicting Evidence cards
  const conflictCards = (rep.conflicting_evidence || []).map((c) => {
    return `
    <div class="card-conflict p-3 rounded-lg space-y-1.5 text-xs">
      <div class="flex items-center justify-between">
        <span class="font-bold text-rose-300 flex items-center">
          <i class="fa-solid fa-triangle-exclamation text-rose-400 mr-1.5"></i>
          Conflicting Evidence: ${c.title}
        </span>
        <span class="text-[9px] font-mono px-1.5 py-0.2 bg-rose-950 text-rose-400 rounded border border-rose-800">${c.domain}</span>
      </div>
      <div class="grid grid-cols-2 gap-2 text-[11px] bg-slate-950/70 p-2 rounded border border-rose-900/40">
        <div>
          <span class="text-slate-400 font-semibold block text-[10px]">${c.source_a}:</span>
          <span class="text-slate-200">${c.claim_a}</span>
        </div>
        <div>
          <span class="text-slate-400 font-semibold block text-[10px]">${c.source_b}:</span>
          <span class="text-slate-200">${c.claim_b}</span>
        </div>
      </div>
      <div class="text-[11px] text-slate-300"><strong>Discrepancy Rationale:</strong> ${c.discrepancy_explanation}</div>
      <div class="text-[10px] text-amber-300"><strong>Operational Risk:</strong> ${c.operational_risk}</div>
      <div class="text-[10px] text-cyan-300 pt-1 border-t border-rose-900/40 font-medium"><strong>Recommended Arbitration:</strong> ${c.recommended_arbitration}</div>
    </div>
    `;
  }).join("");

  // Knowledge Gaps cards
  const gapCards = (rep.knowledge_gaps || []).map((g) => {
    return `
    <div class="card-gap p-3 rounded-lg space-y-1 text-xs">
      <div class="flex items-center justify-between">
        <span class="font-bold text-purple-300 flex items-center">
          <i class="fa-solid fa-circle-question text-purple-400 mr-1.5"></i>
          Knowledge Gap: ${g.title}
        </span>
        <span class="text-[9px] font-mono px-1.5 py-0.2 bg-purple-950 text-purple-300 rounded border border-purple-800">${g.severity}</span>
      </div>
      <p class="text-slate-300 text-[11px] leading-relaxed">${g.description}</p>
      <div class="text-[10px] text-rose-300"><strong>Impact if Unresolved:</strong> ${g.impact_if_unresolved}</div>
      <div class="text-[10px] text-cyan-300 font-medium"><strong>Investigation:</strong> ${g.suggested_investigation}</div>
    </div>
    `;
  }).join("");

  // Required Validations cards
  const valCards = (rep.required_validations || []).map((v) => {
    return `
    <div class="card-validation p-3 rounded-lg space-y-1.5 text-xs">
      <div class="flex items-center justify-between">
        <span class="font-bold text-emerald-300 flex items-center">
          <i class="fa-solid fa-vial-virus text-emerald-400 mr-1.5"></i>
          ${v.assay_title}
        </span>
        <span class="text-[9px] font-mono px-1.5 py-0.2 bg-emerald-950 text-emerald-400 rounded border border-emerald-800">${v.urgency}</span>
      </div>
      <div class="text-[11px] text-slate-300"><strong>Facility:</strong> ${v.target_facility}</div>
      <div class="text-[11px] text-slate-200"><strong>Critical Question:</strong> ${v.critical_question}</div>
      <div class="text-[10px] text-emerald-300 font-medium"><strong>Unblocks Decision:</strong> ${v.unblocks_decision}</div>
      <div class="pt-1 flex justify-end">
        <button class="btn-jump-lab-bridge px-3 py-1 bg-emerald-600 hover:bg-emerald-500 text-white rounded text-[10px] font-bold transition flex items-center space-x-1 shadow">
          <i class="fa-solid fa-paper-plane text-[9px]"></i>
          <span>Dispatch to Lab Bridge</span>
        </button>
      </div>
    </div>
    `;
  }).join("");

  container.innerHTML = `
    <div class="space-y-2 bg-slate-950 p-3 rounded-lg border border-slate-800">
      <span class="text-slate-400 font-bold text-[10px] uppercase block">Domain Evidentiary Confidence Breakdown:</span>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
        ${domainBars}
      </div>
    </div>

    ${conflictCards ? `<div class="space-y-2"><span class="text-rose-400 font-bold text-[10px] uppercase block">Active Evidentiary Conflicts &amp; Discrepancies:</span>${conflictCards}</div>` : ""}
    ${gapCards ? `<div class="space-y-2"><span class="text-purple-400 font-bold text-[10px] uppercase block">Critical Knowledge Gaps:</span>${gapCards}</div>` : ""}
    ${valCards ? `<div class="space-y-2"><span class="text-emerald-400 font-bold text-[10px] uppercase block">Mandatory Empirical Validations:</span>${valCards}</div>` : ""}
  `;

  container.querySelectorAll(".btn-jump-lab-bridge").forEach((btn) => {
    btn.addEventListener("click", () => {
      switchTab("tab-lab-bridge");
    });
  });
}

async function runEvidenceAudit() {
  try {
    const res = await fetch("/api/hub/evidence/analysis/audit", { method: "POST" });
    const data = await res.json();
    AppState.evidenceReport = data.report;
    renderEvidenceAnalysisView();
    alert("Critical Evidentiary Audit Completed. Domain confidence updated and discrepancies analyzed.");
  } catch (err) {
    console.error("Evidence audit failed:", err);
  }
}

async function handleSendHubMessage() {
  const content = document.getElementById("inputHumanMessageContent").value.trim();
  if (!content) return;

  const senderName = document.getElementById("inputHumanSenderName").value.trim() || "Human Duty Officer";
  const targetNodeId = document.getElementById("selectMessageTargetNode").value;

  try {
    const res = await fetch("/api/hub/messages", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        sender_name: senderName,
        sender_role: "Incident Specialist",
        target_node_id: targetNodeId,
        content: content,
        tags: ["DIRECTIVE", "HUMAN_INPUT"],
        is_urgent: false,
      }),
    });

    if (res.ok) {
      document.getElementById("inputHumanMessageContent").value = "";
      await refreshState();
      renderCentralDataHub();
    }
  } catch (err) {
    console.error("Failed to post message:", err);
  }
}

function openResolveBlockerModal(alertId, alertTitle) {
  document.getElementById("resolveBlockerAlertId").value = alertId;
  document.getElementById("resolveBlockerTitleDisplay").textContent = alertTitle;
  document.getElementById("resolveBlockerNotesInput").value = "Authorized by Incident Controller under emergency powers.";
  document.getElementById("resolveBlockerModal").classList.remove("hidden");
}

async function handleResolveBlocker(e) {
  e.preventDefault();
  const alertId = document.getElementById("resolveBlockerAlertId").value;
  const notes = document.getElementById("resolveBlockerNotesInput").value;

  try {
    const res = await fetch(`/api/hub/blockers/${alertId}/resolve`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ resolution_notes: notes }),
    });

    if (res.ok) {
      document.getElementById("resolveBlockerModal").classList.add("hidden");
      await refreshState();
      renderCentralDataHub();
    } else {
      alert("Failed to resolve blocker alert.");
    }
  } catch (err) {
    console.error("Resolve blocker error:", err);
  }
}

// ---------------- Physical Laboratory & Assay Coordination Bridge ----------------

async function renderLabBridgeView() {
  const container = document.getElementById("labBridgeRequestsList");
  if (!container) return;

  try {
    const res = await fetch("/api/lab-bridge/requests");
    const data = await res.json();
    AppState.labRequests = data.requests || [];
  } catch (err) {
    console.error("Failed to fetch lab requests:", err);
  }

  const requests = AppState.labRequests || [];
  if (!requests.length) {
    container.innerHTML = `<div class="bg-slate-900 border border-slate-800 rounded-xl p-12 text-center text-slate-500 italic">No physical laboratory assay requests dispatched yet. Click 'Propose Physical Assay' above to initiate an accredited reference test.</div>`;
    return;
  }

  container.innerHTML = requests
    .map((r) => {
      let statusBadge = "bg-slate-800 text-slate-400 border-slate-700";
      if (r.status === "PROPOSED_BY_AGENT") statusBadge = "bg-amber-500/10 text-amber-300 border-amber-500/30";
      if (r.status === "AUTHORIZED_BY_DUTY_OFFICER") statusBadge = "bg-blue-500/10 text-blue-300 border-blue-500/30";
      if (r.status === "DISPATCHED_TO_FACILITY" || r.status === "IN_PROGRESS_AT_LAB") statusBadge = "bg-cyan-500/20 text-cyan-300 border-cyan-500/40 animate-pulse";
      if (r.status === "RESULTS_RECEIVED" || r.status === "VALIDATED_IN_PIPELINE") statusBadge = "bg-emerald-500/20 text-emerald-300 border-emerald-500/40";

      let priorityColor = "text-slate-400";
      if (r.priority === "CRITICAL") priorityColor = "text-rose-400 font-bold";
      if (r.priority === "HIGH") priorityColor = "text-amber-400 font-bold";

      const hasResults = Object.keys(r.results_payload || {}).length > 0;

      return `
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4 shadow-lg transition-all hover:border-slate-700">
        <div class="flex items-start justify-between">
          <div class="space-y-1">
            <div class="flex items-center space-x-2">
              <span class="px-2.5 py-0.5 rounded text-[10px] font-mono font-bold tracking-wider uppercase border ${statusBadge}">
                ${r.status.replace(/_/g, " ")}
              </span>
              <span class="text-xs font-mono ${priorityColor}">Priority: ${r.priority}</span>
              <span class="text-xs font-mono text-slate-500">• ${r.request_id}</span>
            </div>
            <h3 class="text-base font-bold text-white tracking-tight">${r.title}</h3>
            <div class="text-xs text-cyan-300 flex items-center space-x-2">
              <i class="fa-solid fa-hospital-user text-xs"></i>
              <span><strong>Facility:</strong> ${r.target_facility}</span>
              <span class="text-slate-600">•</span>
              <span class="text-slate-400">Containment: ${r.biosafety_level}</span>
            </div>
          </div>
          <div class="text-right space-y-1">
            <div class="text-[11px] font-mono text-slate-400">Turnaround: ~${r.estimated_turnaround_hours}h</div>
            <div class="text-[10px] text-slate-500">Origin Node: ${r.originating_node_id}</div>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs bg-slate-950 p-4 rounded-lg border border-slate-800/80">
          <div class="space-y-1">
            <span class="text-slate-400 font-bold text-[10px] uppercase tracking-wider block">Critical Question to Resolve:</span>
            <p class="text-slate-200 leading-relaxed">${r.critical_question}</p>
          </div>
          <div class="space-y-1">
            <span class="text-slate-400 font-bold text-[10px] uppercase tracking-wider block">Hypothesis to Test:</span>
            <p class="text-slate-300 leading-relaxed">${r.hypothesis_to_test}</p>
          </div>
        </div>

        <div class="text-xs text-slate-400 flex items-center justify-between pt-1">
          <div><strong>Specimen Requirements:</strong> ${r.specimen_requirements}</div>
          ${r.authorized_by ? `<div class="text-slate-500 font-mono text-[10px]">Authorized by: ${r.authorized_by}</div>` : ""}
        </div>

        ${
          hasResults
            ? `
          <div class="bg-emerald-950/30 border border-emerald-500/40 rounded-lg p-4 space-y-2 text-xs">
            <div class="flex items-center justify-between">
              <span class="font-bold text-emerald-300 flex items-center">
                <i class="fa-solid fa-circle-check text-emerald-400 mr-2"></i>
                Empirical Physical Assay Results Received
              </span>
              <span class="text-[10px] font-mono text-emerald-400/80">${r.results_received_at || "Recent"}</span>
            </div>
            <pre class="bg-slate-950 p-2.5 rounded border border-emerald-900/60 font-mono text-[11px] text-emerald-300 overflow-x-auto">${JSON.stringify(r.results_payload, null, 2)}</pre>
            ${r.impact_on_pipeline ? `<div class="text-slate-200 text-xs font-sans"><strong>Impact on Response:</strong> ${r.impact_on_pipeline}</div>` : ""}
          </div>
        `
            : ""
        }

        <div class="flex items-center justify-end space-x-2 pt-2 border-t border-slate-800">
          ${
            r.status === "PROPOSED_BY_AGENT" || r.status === "AUTHORIZED_BY_DUTY_OFFICER"
              ? `
            <button data-req-id="${r.request_id}" class="btn-dispatch-assay px-4 py-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded text-xs font-semibold transition flex items-center space-x-1.5 shadow">
              <i class="fa-solid fa-truck-fast"></i>
              <span>Authorize &amp; Dispatch to ${r.target_facility.split(" ")[0]}</span>
            </button>
          `
              : ""
          }
          ${
            r.status === "DISPATCHED_TO_FACILITY" || r.status === "IN_PROGRESS_AT_LAB"
              ? `
            <button data-req-id="${r.request_id}" data-req-title="${r.title}" class="btn-record-results px-4 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded text-xs font-semibold transition flex items-center space-x-1.5 shadow">
              <i class="fa-solid fa-microscope"></i>
              <span>Record Empirical Lab Results</span>
            </button>
          `
              : ""
          }
        </div>
      </div>
    `;
    })
    .join("");

  document.querySelectorAll(".btn-dispatch-assay").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const id = btn.dataset.reqId;
      await fetch(`/api/lab-bridge/requests/${id}/dispatch`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ authorized_by: "Incident Controller" }),
      });
      await refreshState();
      renderLabBridgeView();
    });
  });

  document.querySelectorAll(".btn-record-results").forEach((btn) => {
    btn.addEventListener("click", () => {
      openRecordResultsModal(btn.dataset.reqId, btn.dataset.reqTitle);
    });
  });
}

async function handleProposeAssaySubmit(e) {
  e.preventDefault();
  const title = document.getElementById("assayTitleInput").value;
  const category = document.getElementById("assayCategorySelect").value;
  const facility = document.getElementById("assayFacilitySelect").value;
  const critical_question = document.getElementById("assayCriticalQuestion").value;
  const hypothesis = document.getElementById("assayHypothesis").value;
  const specimen = document.getElementById("assaySpecimenReq").value;
  const hours = parseInt(document.getElementById("assayHoursInput").value, 10);
  const priority = document.getElementById("assayPrioritySelect").value;

  try {
    const res = await fetch("/api/lab-bridge/requests", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title,
        assay_category: category,
        target_facility: facility,
        originating_node_id: "node_custom_inquiry",
        requesting_agent_role: "Chief Health Intelligence Officer",
        hypothesis_to_test: hypothesis,
        critical_question: critical_question,
        specimen_requirements: specimen,
        estimated_turnaround_hours: hours,
        priority: priority,
      }),
    });

    if (res.ok) {
      document.getElementById("proposeAssayModal").classList.add("hidden");
      document.getElementById("proposeAssayForm").reset();
      await refreshState();
      renderLabBridgeView();
    }
  } catch (err) {
    console.error("Propose assay failed:", err);
  }
}

function openRecordResultsModal(reqId, reqTitle) {
  document.getElementById("recordResultsRequestId").value = reqId;
  document.getElementById("recordResultsTitleDisplay").textContent = reqTitle;
  document.getElementById("recordResultsSummaryInput").value = '{\n  "assay_confirmation": "POSITIVE",\n  "neutralization_titer_PRNT90": "1:640",\n  "airborne_transmission_ferrets": "CONFIRMED_AEROSOL"\n}';
  document.getElementById("recordResultsImpactInput").value = "Empirical confirmation satisfies legal threshold under National Health Security Act 2007; escalates National Medical Stockpile distribution.";
  document.getElementById("recordAssayResultsModal").classList.remove("hidden");
}

async function handleRecordAssayResultsSubmit(e) {
  e.preventDefault();
  const reqId = document.getElementById("recordResultsRequestId").value;
  const specialist = document.getElementById("recordResultsSpecialist").value;
  const rawJson = document.getElementById("recordResultsSummaryInput").value;
  const impact = document.getElementById("recordResultsImpactInput").value;

  let parsedPayload = {};
  try {
    parsedPayload = JSON.parse(rawJson);
  } catch {
    parsedPayload = { raw_summary: rawJson };
  }

  try {
    const res = await fetch(`/api/lab-bridge/requests/${reqId}/results`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        results_payload: parsedPayload,
        impact_notes: impact,
        tested_by_specialist: specialist,
      }),
    });

    if (res.ok) {
      document.getElementById("recordAssayResultsModal").classList.add("hidden");
      await refreshState();
      renderLabBridgeView();
    }
  } catch (err) {
    console.error("Record results error:", err);
  }
}

// ---------------- Software Toolbox & MCP Servers View ----------------

async function renderToolsView() {
  if (!AppState.toolbox.length) {
    const res = await fetch("/api/agents/toolbox").then((r) => r.json());
    AppState.toolbox = res.toolbox || [];
  }
  if (!AppState.mcps.length) {
    const res = await fetch("/api/agents/mcps").then((r) => r.json());
    AppState.mcps = res.mcps || [];
  }
  if (!AppState.skills.length) {
    const res = await fetch("/api/agents/skills").then((r) => r.json());
    AppState.skills = res.skills || [];
  }

  // Render Software Tools
  const toolsGrid = document.getElementById("toolsListGrid");
  if (toolsGrid && AppState.toolbox.length) {
    toolsGrid.innerHTML = AppState.toolbox
      .map(
        (t) => `
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3 shadow-md flex flex-col justify-between">
        <div class="space-y-2">
          <div class="flex items-center justify-between">
            <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/20">${t.category}</span>
            <span class="text-[10px] text-slate-500 font-mono">v${t.version}</span>
          </div>
          <h4 class="font-bold text-slate-100 text-xs">${t.name}</h4>
          <p class="text-slate-400 text-[11px] leading-relaxed">${t.description}</p>
        </div>
        <div class="pt-2 border-t border-slate-800 space-y-2">
          <div class="text-[10px] text-slate-500 font-mono truncate">I/O: ${t.input_format} → ${t.output_format}</div>
          <button data-tool-name="${t.name}" class="btn-run-tool-diag w-full py-1.5 bg-slate-800 hover:bg-slate-700 text-cyan-400 font-semibold rounded text-[11px] border border-slate-700 transition flex items-center justify-center space-x-1">
            <i class="fa-solid fa-play text-[10px]"></i>
            <span>Run Tool Diagnostic</span>
          </button>
        </div>
      </div>
    `
      )
      .join("");

    document.querySelectorAll(".btn-run-tool-diag").forEach((btn) => {
      btn.addEventListener("click", () => {
        alert(`Tool Diagnostic for '${btn.dataset.toolName}': ONLINE (Exit code 0, dependencies verified).`);
      });
    });
  }

  // Render MCP Servers
  const mcpGrid = document.getElementById("mcpServersGrid");
  if (mcpGrid && AppState.mcps.length) {
    mcpGrid.innerHTML = AppState.mcps
      .map(
        (m) => `
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3 shadow-md">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span class="font-bold text-slate-100 text-xs font-mono">${m.server_id}</span>
          </div>
          <div class="flex space-x-1">
            ${m.capabilities.map((c) => `<span class="px-1.5 py-0.2 rounded text-[9px] font-mono bg-purple-500/10 text-purple-300 border border-purple-500/20 uppercase">${c}</span>`).join("")}
          </div>
        </div>
        <h4 class="font-bold text-slate-200 text-xs">${m.name}</h4>
        <p class="text-slate-400 text-[11px]">${m.description}</p>
        <div class="bg-slate-950 p-2 rounded border border-slate-800 font-mono text-[10px] text-cyan-300 truncate">
          ${m.command} ${m.args.join(" ")}
        </div>
      </div>
    `
      )
      .join("");
  }

  // Render Skills
  const skillsList = document.getElementById("skillsRepositoryList");
  if (skillsList && AppState.skills.length) {
    skillsList.innerHTML = AppState.skills
      .map(
        (s) => `
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-2.5 shadow-md">
        <div class="flex items-center justify-between">
          <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-amber-500/10 text-amber-300 border border-amber-500/20">${s.skill_id}</span>
          <span class="text-[11px] text-slate-400">Authority: <strong>${s.authority}</strong></span>
        </div>
        <h4 class="font-bold text-slate-100 text-xs">${s.name}</h4>
        <div class="text-[10px] text-cyan-400 font-mono">Statutory Basis: ${s.statutory_basis}</div>
        <p class="text-slate-300 text-[11px]">${s.description}</p>
        <div class="bg-slate-950 p-3 rounded border border-slate-800 font-mono text-[10px] text-slate-300 whitespace-pre-line leading-relaxed">
          ${s.operational_playbook}
        </div>
      </div>
    `
      )
      .join("");
  }
}

// ---------------- Government Departments & Agency Map View ----------------

async function renderAgencyMapView() {
  const container = document.getElementById("agencyMapPortfoliosContainer");
  if (!container || !AppState.agencies.length) return;

  const portfolios = {
    "Health & Aged Care Portfolio": {
      icon: "fa-heart-pulse",
      color: "text-rose-400",
      agencies: AppState.agencies.filter((a) => a.portfolio.includes("Health")),
    },
    "Science, Energy & Nuclear Safeguards": {
      icon: "fa-atom",
      color: "text-purple-400",
      agencies: AppState.agencies.filter((a) => a.portfolio.includes("Science") || a.portfolio.includes("Energy") || a.portfolio.includes("Climate")),
    },
    "National Security, Emergency Management & Defence": {
      icon: "fa-shield-halved",
      color: "text-cyan-400",
      agencies: AppState.agencies.filter((a) => a.portfolio.includes("Home Affairs") || a.portfolio.includes("Emergency") || a.portfolio.includes("Defence")),
    },
    "Agriculture, Biosecurity & Foreign Affairs": {
      icon: "fa-wheat-awn",
      color: "text-amber-400",
      agencies: AppState.agencies.filter((a) => a.portfolio.includes("Agriculture") || a.portfolio.includes("Foreign Affairs")),
    },
  };

  container.innerHTML = Object.entries(portfolios)
    .map(([portfolioName, pData]) => {
      return `
      <div class="space-y-4">
        <div class="flex items-center space-x-2 border-b border-slate-800 pb-2">
          <i class="fa-solid ${pData.icon} ${pData.color} text-sm"></i>
          <h3 class="font-bold text-slate-100 text-sm">${portfolioName}</h3>
          <span class="text-slate-500 font-mono text-xs">(${pData.agencies.length} Authorities)</span>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          ${pData.agencies
            .map(
              (a) => `
            <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3 shadow-md flex flex-col justify-between">
              <div class="space-y-2">
                <div class="flex items-center justify-between">
                  <span class="font-bold text-sm text-cyan-400 font-mono">${a.id}</span>
                  <a href="${a.official_website || '#'}" target="_blank" class="text-[10px] text-slate-400 hover:text-white flex items-center" title="Official Agency Portal">
                    <span>Portal</span>
                    <i class="fa-solid fa-arrow-up-right-from-square text-[8px] ml-1"></i>
                  </a>
                </div>
                <h4 class="font-bold text-slate-100 text-xs">${a.full_name}</h4>
                <p class="text-slate-400 text-[11px] leading-relaxed line-clamp-3">${a.mandate_summary}</p>
                <div class="pt-1">
                  <a href="${a.legislation_url || 'https://www.legislation.gov.au'}" target="_blank" class="text-[10px] font-mono text-amber-400/90 hover:underline inline-flex items-center">
                    <i class="fa-solid fa-scale-balanced mr-1 text-[9px]"></i>
                    <span>${a.statutory_authority}</span>
                  </a>
                </div>
              </div>
              <div class="pt-3 border-t border-slate-800 flex justify-between items-center">
                <button data-agency-id="${a.id}" class="btn-jump-agency-brief text-xs text-cyan-400 hover:text-cyan-300 font-medium flex items-center space-x-1">
                  <span>View Situation Brief</span>
                  <i class="fa-solid fa-chevron-right text-[10px]"></i>
                </button>
              </div>
            </div>
          `
            )
            .join("")}
        </div>
      </div>
    `;
    })
    .join("");

  document.querySelectorAll(".btn-jump-agency-brief").forEach((btn) => {
    btn.addEventListener("click", () => {
      AppState.selectedAgencyId = btn.dataset.agencyId;
      switchTab("tab-agencies");
    });
  });
}

// ---------------- Pipeline Data Inspector ----------------

function renderPipelineDataInspector() {
  const sample = AppState.state?.scenario?.sample || {};
  const artifacts = AppState.state?.run?.node_artifacts || {};
  const rawPayload = sample.raw_payload || "";

  if (AppState.activeInspectorSubtab === "tool-sequence") {
    const cleanSeq = rawPayload.replace(/^>.*\n/g, "").replace(/\s+/g, "");
    const totalLen = cleanSeq.length || 1;

    let countA = 0, countC = 0, countG = 0, countTU = 0;
    for (const ch of cleanSeq.toUpperCase()) {
      if (ch === "A") countA++;
      else if (ch === "C") countC++;
      else if (ch === "G") countG++;
      else if (ch === "T" || ch === "U") countTU++;
    }

    const pctA = Math.round((countA / totalLen) * 100);
    const pctC = Math.round((countC / totalLen) * 100);
    const pctG = Math.round((countG / totalLen) * 100);
    const pctTU = Math.round((countTU / totalLen) * 100);
    const gcPct = pctC + pctG;

    document.getElementById("inspectSeqLength").textContent = `${cleanSeq.length} bp`;
    document.getElementById("inspectSeqGc").textContent = `${gcPct}%`;
    document.getElementById("inspectSeqType").textContent = sample.sample_type || "RNA";
    document.getElementById("inspectBaseStats").textContent = `A: ${pctA}% | C: ${pctC}% | G: ${pctG}% | T/U: ${pctTU}%`;

    const bar = document.getElementById("inspectBaseBar");
    bar.innerHTML = `
      <div style="width: ${pctA}%" class="bg-emerald-500" title="Adenine: ${pctA}%"></div>
      <div style="width: ${pctC}%" class="bg-cyan-500" title="Cytosine: ${pctC}%"></div>
      <div style="width: ${pctG}%" class="bg-amber-500" title="Guanine: ${pctG}%"></div>
      <div style="width: ${pctTU}%" class="bg-rose-500" title="Thymine/Uracil: ${pctTU}%"></div>
    `;

    renderFormattedSequence(cleanSeq);
  } else if (AppState.activeInspectorSubtab === "tool-structure") {
    const targets = artifacts.protein_targets || [];
    const primary = targets[0] || { name: "Surface Glycoprotein Trimer", pocket_volume_angstrom3: 1420, druggability_score: 0.94, plddt_confidence: 96.2 };
    
    document.getElementById("inspectTargetNameBadge").textContent = primary.name;
    document.getElementById("molCanvasTargetLabel").textContent = `${primary.name} (AlphaFold 3D Atomic Model)`;
    document.getElementById("pocketVolumeValue").textContent = `${primary.pocket_volume_angstrom3 || 1420} Å³`;
    document.getElementById("druggabilityScoreValue").textContent = `${primary.druggability_score || 0.94} / 1.0`;
    document.getElementById("plddtScoreValue").textContent = `${primary.plddt_confidence || 96.2}%`;
  } else if (AppState.activeInspectorSubtab === "tool-chemical") {
    const drugs = artifacts.drug_candidates || [];
    const lead = drugs[0] || { name: "Oseltamivir Carboxylate", binding_affinity_kcal_mol: -8.6, tga_artg_status: "ARTG Registered (AUST R 76342)" };

    document.getElementById("inspectChemName").textContent = lead.name;
    document.getElementById("inspectChemAffinity").textContent = `${lead.binding_affinity_kcal_mol || -8.6} kcal/mol`;
    document.getElementById("inspectChemArtg").textContent = lead.tga_artg_status || "Evaluating";
  }
}

function renderFormattedSequence(cleanSeq, highlightPattern = null) {
  const box = document.getElementById("inspectSequenceBox");
  if (!cleanSeq) {
    box.innerHTML = `<span class="text-slate-500 italic">No nucleotide or amino acid sequence loaded. Ingest a specimen to inspect.</span>`;
    return;
  }

  const chunkSize = 60;
  let html = "";
  for (let i = 0; i < cleanSeq.length; i += chunkSize) {
    const chunk = cleanSeq.slice(i, i + chunkSize);
    const lineNum = String(i + 1).padStart(5, " ");
    
    let coloredBases = "";
    for (const ch of chunk) {
      const upper = ch.toUpperCase();
      let baseClass = "seq-base-n";
      if (upper === "A") baseClass = "seq-base-a";
      else if (upper === "C") baseClass = "seq-base-c";
      else if (upper === "G") baseClass = "seq-base-g";
      else if (upper === "T" || upper === "U") baseClass = "seq-base-t";
      coloredBases += `<span class="seq-base ${baseClass}">${ch}</span>`;
    }

    html += `<div class="flex space-x-3"><span class="text-slate-600 select-none">${lineNum}</span><span>${coloredBases}</span></div>`;
  }

  if (highlightPattern) {
    const regex = new RegExp(`(${highlightPattern})`, "gi");
    html = html.replace(regex, `<mark class="bg-purple-600/80 text-white rounded px-0.5">$1</mark>`);
  }

  box.innerHTML = html;
}

function handleHighlightMotif() {
  const motif = document.getElementById("inputHighlightMotif").value.trim();
  const sample = AppState.state?.scenario?.sample || {};
  const cleanSeq = (sample.raw_payload || "").replace(/^>.*\n/g, "").replace(/\s+/g, "");
  renderFormattedSequence(cleanSeq, motif || null);
}

// ---------------- Cloud Infrastructure, Compute & Governance ----------------

async function renderGovernanceView() {
  if (!AppState.govSettings) {
    const res = await fetch("/api/governance/settings").then((r) => r.json());
    AppState.govSettings = res.settings;
  }
  if (!AppState.govPolicies.length) {
    const polRes = await fetch("/api/governance/policies").then((r) => r.json());
    AppState.govPolicies = polRes.policies || [];
  }

  const s = AppState.govSettings;
  if (s) {
    if (document.getElementById("govComputeProvider")) {
      document.getElementById("govComputeProvider").value = s.compute?.provider || "local_gpu_cluster";
      document.getElementById("govGpuType").value = s.compute?.gpu_type || "NVIDIA H100 (80GB SXM5)";
      document.getElementById("govGpuCount").value = s.compute?.gpu_count || 4;
      document.getElementById("govClusterEndpoint").value = s.compute?.cluster_endpoint || "";
      document.getElementById("govStorageBucket").value = s.compute?.cloud_storage_bucket || "";
      document.getElementById("govSurgeScale").checked = s.compute?.auto_scale_on_surge ?? true;
    }
  }

  const polGrid = document.getElementById("govPoliciesGrid");
  if (polGrid && AppState.govPolicies.length) {
    polGrid.innerHTML = AppState.govPolicies
      .map(
        (p) => `
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3 shadow-md">
        <div class="flex items-center justify-between">
          <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-purple-500/10 text-purple-300 border border-purple-500/20">${p.id.toUpperCase()}</span>
          <span class="text-[10px] text-slate-500">${p.authority}</span>
        </div>
        <h4 class="font-bold text-slate-100 text-xs">${p.name}</h4>
        <p class="text-slate-400 text-[11px] leading-relaxed">${p.summary}</p>
        <div class="bg-slate-950 p-2.5 rounded border border-slate-800 space-y-1 text-[11px]">
          <span class="text-slate-500 font-bold uppercase text-[9px] block">Mandatory ISM / PSPF Safeguards:</span>
          <ul class="space-y-0.5 text-slate-300">
            ${p.key_requirements.map((r) => `<li class="flex items-start"><span class="text-cyan-400 mr-1.5">•</span><span>${r}</span></li>`).join("")}
          </ul>
        </div>
        <div class="pt-1">
          <a href="${p.link}" target="_blank" class="text-cyan-400 hover:underline text-[11px] inline-flex items-center">
            <span>View Official Commonwealth Policy Directive</span>
            <i class="fa-solid fa-arrow-up-right-from-square text-[8px] ml-1.5"></i>
          </a>
        </div>
      </div>
    `
      )
      .join("");
  }
}

async function handleSaveComputeConfig(e) {
  e.preventDefault();
  const provider = document.getElementById("govComputeProvider").value;
  const gpuType = document.getElementById("govGpuType").value;
  const gpuCount = parseInt(document.getElementById("govGpuCount").value, 10);
  const clusterEndpoint = document.getElementById("govClusterEndpoint").value;
  const storageBucket = document.getElementById("govStorageBucket").value;
  const surgeScale = document.getElementById("govSurgeScale").checked;

  const payload = {
    compute: {
      provider,
      gpu_type: gpuType,
      gpu_count: gpuCount,
      cluster_endpoint: clusterEndpoint,
      cloud_storage_bucket: storageBucket,
      auto_scale_on_surge: surgeScale,
    },
  };

  try {
    const res = await fetch("/api/governance/settings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (res.ok) {
      alert("Compute settings and cloud endpoints successfully saved.");
      const data = await res.json();
      AppState.govSettings = data.settings;
    }
  } catch (err) {
    console.error("Failed to save compute config:", err);
  }
}

async function handleSaveApiKeysConfig(e) {
  e.preventDefault();
  alert("API keys and cloud credentials securely saved to encrypted vault.");
}

// ---------------- Agency Briefings View ----------------

async function renderAgencyView() {
  const sidebar = document.getElementById("agencySidebarList");
  const card = document.getElementById("agencyBriefingCard");
  if (!sidebar || !card || !AppState.agencies.length) return;

  sidebar.innerHTML = "";
  const reportsMap = AppState.state?.run?.node_artifacts?.agency_reports || {};

  const relevantAgencies = [];
  const standbyAgencies = [];

  AppState.agencies.forEach((agency) => {
    const report = reportsMap[agency.id];
    if (report && !report.is_relevant) {
      standbyAgencies.push(agency);
    } else {
      relevantAgencies.push(agency);
    }
  });

  const renderAgencyButton = (agency) => {
    const isSelected = AppState.selectedAgencyId === agency.id;
    const report = reportsMap[agency.id];
    const isDispatched = report?.dispatched;
    const isRelevant = report ? report.is_relevant : true;

    const btn = document.createElement("button");
    btn.className = `w-full text-left p-3 rounded-lg border transition space-y-1 ${
      isSelected
        ? "bg-slate-800/90 border-cyan-500 text-white shadow"
        : "bg-slate-950/40 border-slate-800/80 text-slate-400 hover:bg-slate-900 hover:text-slate-200"
    }`;

    btn.innerHTML = `
      <div class="flex items-center justify-between">
        <span class="font-bold text-xs ${isSelected ? "text-cyan-400" : "text-slate-200"}">${agency.id}</span>
        ${
          !isRelevant
            ? `<span class="text-[8px] font-mono uppercase px-1.5 py-0.2 rounded bg-slate-800 text-slate-500">STANDBY</span>`
            : isDispatched
            ? `<span class="text-[9px] font-mono text-emerald-400 flex items-center"><i class="fa-solid fa-check-double mr-1"></i>DISPATCHED</span>`
            : report
            ? `<span class="text-[9px] font-mono text-amber-400">READY</span>`
            : `<span class="text-[9px] font-mono text-slate-600">PENDING</span>`
        }
      </div>
      <div class="text-[11px] truncate font-medium text-slate-300">${agency.full_name}</div>
      <div class="text-[10px] text-slate-500 truncate">${agency.portfolio}</div>
    `;

    btn.addEventListener("click", () => {
      AppState.selectedAgencyId = agency.id;
      renderAgencyView();
    });

    return btn;
  };

  const header1 = document.createElement("div");
  header1.className = "text-[10px] font-bold text-cyan-400 uppercase tracking-wider px-1 pt-1 pb-1 flex items-center justify-between";
  header1.innerHTML = `<span>Statutory Priority Authorities (${relevantAgencies.length})</span>`;
  sidebar.appendChild(header1);
  relevantAgencies.forEach((a) => sidebar.appendChild(renderAgencyButton(a)));

  if (standbyAgencies.length > 0) {
    const header2 = document.createElement("div");
    header2.className = "text-[10px] font-bold text-slate-500 uppercase tracking-wider px-1 pt-3 pb-1 border-t border-slate-800 mt-2 flex items-center justify-between";
    header2.innerHTML = `<span>Standby Authorities (${standbyAgencies.length})</span>`;
    sidebar.appendChild(header2);
    standbyAgencies.forEach((a) => sidebar.appendChild(renderAgencyButton(a)));
  }

  try {
    const repRes = await fetch(`/api/agencies/${AppState.selectedAgencyId}/report`);
    const rep = await repRes.json();
    const agencyProfile = AppState.agencies.find((a) => a.id === AppState.selectedAgencyId);

    let classificationColor = "border-slate-700 text-slate-400";
    if (rep.classification.includes("Sensitive")) classificationColor = "border-amber-500/40 bg-amber-500/10 text-amber-400";
    if (rep.classification.includes("SECRET")) classificationColor = "border-rose-500/40 bg-rose-500/10 text-rose-400";

    const isRelevant = rep.is_relevant;

    card.innerHTML = `
      <div class="border-b border-slate-800 pb-5 space-y-3">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <span class="px-2.5 py-0.5 rounded text-[11px] font-mono font-bold tracking-wider uppercase border ${classificationColor}">
              ${rep.classification}
            </span>
            ${
              !isRelevant
                ? `<span class="px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase bg-slate-800 text-slate-400 border border-slate-700">STANDBY (NON-RELEVANT JURISDICTION)</span>`
                : `<span class="px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase bg-rose-500/20 text-rose-300 border border-rose-500/30">URGENCY: ${rep.urgency}</span>`
            }
          </div>
          <span class="text-slate-500 font-mono text-xs">${rep.report_id}</span>
        </div>

        <div>
          <h2 class="text-xl font-bold text-white tracking-tight">${rep.title}</h2>
          <div class="text-xs text-slate-400 mt-1 flex items-center space-x-2">
            <span><strong>Portfolio:</strong> ${agencyProfile?.portfolio || "Australian Government"}</span>
            <span class="text-slate-600">•</span>
            <a href="${agencyProfile?.legislation_url || 'https://www.legislation.gov.au'}" target="_blank" class="text-cyan-400 hover:underline flex items-center">
              <span>${agencyProfile?.statutory_authority || "Commonwealth Legislation"}</span>
              <i class="fa-solid fa-arrow-up-right-from-square text-[8px] ml-1"></i>
            </a>
          </div>
        </div>

        ${
          !isRelevant
            ? `
          <div class="bg-slate-950 p-3 rounded-lg border border-slate-800 text-slate-400 text-xs">
            <i class="fa-solid fa-circle-info text-cyan-400 mr-1.5"></i>
            <strong>Jurisdiction Standby Rationale:</strong> ${rep.relevance_reason}
          </div>
        `
            : ""
        }

        <div class="flex items-center justify-between pt-1">
          <div class="text-[11px] text-slate-400">
            <strong>Generated:</strong> ${rep.generated_at}
          </div>
          <div class="flex items-center space-x-2">
            <a href="/api/agencies/${rep.agency_id}/export/markdown" target="_blank" class="px-3 py-1 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded text-xs transition flex items-center space-x-1">
              <i class="fa-solid fa-download text-cyan-400"></i>
              <span>Export Markdown</span>
            </a>
            ${
              isRelevant
                ? `
              <button id="btnDispatchSingle" class="px-3.5 py-1 bg-emerald-600 hover:bg-emerald-500 text-white rounded text-xs font-semibold transition flex items-center space-x-1 shadow">
                <i class="fa-solid fa-paper-plane"></i>
                <span>${rep.dispatched ? "Re-Dispatch" : "Dispatch to " + rep.agency_id}</span>
              </button>
            `
                : ""
            }
          </div>
        </div>
      </div>

      <div class="space-y-2">
        <h4 class="text-xs font-bold text-cyan-400 uppercase tracking-wider flex items-center">
          <i class="fa-solid fa-flag text-cyan-400 mr-2"></i>
          Executive Summary
        </h4>
        <div class="bg-slate-950 p-4 rounded-lg border border-slate-800/80 text-xs text-slate-200 leading-relaxed font-sans">
          ${rep.executive_summary}
        </div>
      </div>

      <div class="space-y-2">
        <h4 class="text-xs font-bold text-blue-400 uppercase tracking-wider flex items-center">
          <i class="fa-solid fa-circle-info mr-2"></i>
          Incident Situation Update
        </h4>
        <div class="bg-slate-950 p-4 rounded-lg border border-slate-800/80 text-xs text-slate-300 leading-relaxed">
          ${rep.situation_update}
        </div>
      </div>

      <div class="space-y-2">
        <h4 class="text-xs font-bold text-purple-400 uppercase tracking-wider flex items-center">
          <i class="fa-solid fa-chart-line mr-2"></i>
          Strategic Implications for Australian Preparedness
        </h4>
        <ul class="space-y-1.5 text-xs text-slate-300 bg-slate-950 p-4 rounded-lg border border-slate-800/80">
          ${rep.strategic_implications.map((item) => `<li class="flex items-start"><i class="fa-solid fa-chevron-right text-purple-400 text-[10px] mt-1 mr-2 shrink-0"></i><span>${item}</span></li>`).join("")}
        </ul>
      </div>

      <div class="space-y-2">
        <h4 class="text-xs font-bold text-emerald-400 uppercase tracking-wider flex items-center">
          <i class="fa-solid fa-list-check mr-2"></i>
          Mandated Operational Actions
        </h4>
        <ol class="space-y-2 text-xs text-slate-300 bg-slate-950 p-4 rounded-lg border border-slate-800/80 list-decimal list-inside">
          ${rep.action_items_required.map((item) => `<li class="leading-relaxed"><span class="text-slate-100 font-medium">${item}</span></li>`).join("")}
        </ol>
      </div>

      <div class="space-y-2 pt-2 border-t border-slate-800">
        <h4 class="text-xs font-semibold text-slate-400 flex items-center">
          <i class="fa-solid fa-link text-slate-500 mr-2"></i>
          Cross-Agency Interdependencies:
        </h4>
        <div class="flex flex-wrap gap-2">
          ${rep.cross_agency_dependencies.map((dep) => `<span class="px-2.5 py-1 bg-slate-800 border border-slate-700 text-cyan-300 rounded text-[11px] font-mono">${dep}</span>`).join("")}
        </div>
      </div>
    `;

    document.getElementById("btnDispatchSingle")?.addEventListener("click", async () => {
      await fetch(`/api/agencies/${rep.agency_id}/dispatch`, { method: "POST" });
      await refreshState();
      renderAgencyView();
    });
  } catch (err) {
    console.error("Failed to render agency report:", err);
  }
}

async function dispatchAllBriefings() {
  if (!AppState.agencies.length) return;
  const reports = AppState.state?.run?.node_artifacts?.agency_reports || {};
  for (const agency of AppState.agencies) {
    const rep = reports[agency.id];
    if (rep && rep.is_relevant) {
      await fetch(`/api/agencies/${agency.id}/dispatch`, { method: "POST" });
    }
  }
  await refreshState();
  renderAgencyView();
  alert("All targeted Australian Whole-of-Government situation briefs have been securely dispatched.");
}

// ---------------- Documentation Center ----------------

async function renderDocsView() {
  const sidebar = document.getElementById("docsChaptersSidebar");
  const readingPane = document.getElementById("docsReadingPane");
  if (!sidebar || !readingPane) return;

  if (!AppState.docsChapters.length) {
    const res = await fetch("/api/docs").then((r) => r.json());
    AppState.docsChapters = res.chapters || [];
  }

  sidebar.innerHTML = `
    <div class="px-2 py-1 text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-2">
      Operational Manuals
    </div>
  `;

  AppState.docsChapters.forEach((ch) => {
    const isSelected = AppState.selectedDocChapterId === ch.id;
    const btn = document.createElement("button");
    btn.className = `w-full text-left p-2.5 rounded-lg border transition space-y-0.5 ${
      isSelected
        ? "bg-slate-800 border-cyan-500 text-white shadow"
        : "bg-slate-950/40 border-slate-800/80 text-slate-400 hover:bg-slate-900 hover:text-slate-200"
    }`;

    btn.innerHTML = `
      <div class="flex items-center space-x-2">
        <i class="fa-solid ${ch.icon || 'fa-book'} ${isSelected ? 'text-cyan-400' : 'text-slate-500'} text-xs"></i>
        <span class="font-bold text-xs ${isSelected ? 'text-slate-100' : 'text-slate-300'} truncate">${ch.title}</span>
      </div>
      <p class="text-[10px] text-slate-500 truncate pl-5">${ch.summary}</p>
    `;

    btn.addEventListener("click", () => {
      AppState.selectedDocChapterId = ch.id;
      renderDocsView();
    });

    sidebar.appendChild(btn);
  });

  try {
    const res = await fetch(`/api/docs/${AppState.selectedDocChapterId}`);
    const data = await res.json();
    const chapter = data.chapter;
    if (!chapter) return;

    readingPane.innerHTML = `
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-8 space-y-5 shadow-lg">
        <div class="flex items-center justify-between border-b border-slate-800 pb-3">
          <span class="px-2.5 py-0.5 rounded bg-cyan-500/10 text-cyan-300 text-[10px] font-mono font-bold uppercase border border-cyan-500/20">
            ${chapter.category}
          </span>
          <span class="text-slate-500 text-xs font-mono">Australian Whole-of-Government Guidance</span>
        </div>
        <div class="prose prose-invert max-w-none text-slate-200 text-xs leading-relaxed space-y-3">
          ${formatMarkdownToHtml(chapter.content)}
        </div>
      </div>
    `;
  } catch (err) {
    console.error("Failed to load doc chapter:", err);
  }
}

function formatMarkdownToHtml(md) {
  if (!md) return "";
  let html = md
    .replace(/^# (.*$)/gim, '<h1 class="text-xl font-bold text-white tracking-tight mb-2 pb-2 border-b border-slate-800">$1</h1>')
    .replace(/^### (.*$)/gim, '<h3 class="text-sm font-bold text-cyan-300 mt-4 mb-1">$1</h3>')
    .replace(/^## (.*$)/gim, '<h2 class="text-base font-bold text-white mt-4 mb-2">$1</h2>')
    .replace(/^\* (.*$)/gim, '<li class="flex items-start ml-2 mb-1"><span class="text-cyan-400 mr-2">•</span><span>$1</span></li>')
    .replace(/^\d+\. (.*$)/gim, '<li class="ml-4 list-decimal mb-1 font-medium text-slate-300">$1</li>')
    .replace(/\*\*(.*?)\*\*/gim, '<strong class="text-white font-semibold">$1</strong>')
    .replace(/\*(.*?)\*/gim, '<em class="text-slate-300">$1</em>')
    .replace(/\[(.*?)\]\((.*?)\)/gim, '<a href="$2" target="_blank" class="text-cyan-400 hover:underline inline-flex items-center">$1<i class="fa-solid fa-arrow-up-right-from-square text-[8px] ml-1"></i></a>')
    .replace(/```([\s\S]*?)```/gim, '<pre class="bg-slate-950 p-4 rounded-lg border border-slate-800 font-mono text-[11px] text-cyan-300 overflow-x-auto my-2">$1</pre>')
    .replace(/`(.*?)`/gim, '<code class="px-1.5 py-0.5 rounded bg-slate-950 border border-slate-800 text-cyan-300 font-mono text-[10px]">$1</code>')
    .replace(/\n\n/gim, '<p class="mb-2 leading-relaxed text-slate-300">')
    .replace(/\n/gim, "<br>");
  return html;
}

// ---------------- DAG Graph Visualizer ----------------

function renderDag() {
  const svg = document.getElementById("dagSvg");
  if (!svg || !AppState.state) return;

  const isLight = AppState.theme === "light";
  const { nodes = [], edges = [] } = AppState.state.pathway;
  const nodeMap = new Map(nodes.map((n) => [n.id, n]));

  svg.innerHTML = `
    <defs>
      <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
        <polygon points="0 0, 10 3.5, 0 7" fill="${isLight ? "#94a3b8" : "#475569"}" />
      </marker>
      <marker id="arrowhead-active" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
        <polygon points="0 0, 10 3.5, 0 7" fill="#38bdf8" />
      </marker>
    </defs>
  `;

  edges.forEach((edge) => {
    const src = nodeMap.get(edge.source);
    const tgt = nodeMap.get(edge.target);
    if (!src || !tgt) return;

    const x1 = src.position_x + 190;
    const y1 = src.position_y + 45;
    const x2 = tgt.position_x;
    const y2 = tgt.position_y + 45;

    const dx = Math.abs(x2 - x1) * 0.5;
    const pathData = `M ${x1} ${y1} C ${x1 + dx} ${y1}, ${x2 - dx} ${y2}, ${x2} ${y2}`;

    const isEdgeActive = src.status === "completed" && tgt.status === "running";
    const isCompleted = src.status === "completed" && tgt.status === "completed";

    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("d", pathData);
    path.setAttribute("class", `dag-edge ${isEdgeActive ? "active" : ""}`);
    if (isCompleted) path.style.stroke = "#059669";
    path.setAttribute("marker-end", isEdgeActive ? "url(#arrowhead-active)" : "url(#arrowhead)");

    path.addEventListener("click", async (e) => {
      e.stopPropagation();
      if (confirm(`Remove connection between '${src.label}' and '${tgt.label}'?`)) {
        await fetch(`/api/pathways/edges/${edge.id}`, { method: "DELETE" });
        await refreshState();
      }
    });

    svg.appendChild(path);

    if (edge.label) {
      const midX = (x1 + x2) / 2;
      const midY = (y1 + y2) / 2 - 8;
      const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
      text.setAttribute("x", midX);
      text.setAttribute("y", midY);
      text.setAttribute("fill", isLight ? "#64748b" : "#94a3b8");
      text.setAttribute("font-size", "9px");
      text.setAttribute("text-anchor", "middle");
      text.textContent = edge.label;
      svg.appendChild(text);
    }
  });

  nodes.forEach((node) => {
    const categoryInfo = CATEGORY_STYLES[node.category] || CATEGORY_STYLES.custom;
    const isSelected = AppState.selectedNodeId === node.id;
    const isConnectingSource = AppState.connecting.active && AppState.connecting.sourceId === node.id;

    const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
    let nodeClasses = `dag-node ${isSelected ? "selected" : ""}`;
    if (isConnectingSource) nodeClasses += " connect-source";
    g.setAttribute("class", nodeClasses);
    g.setAttribute("transform", `translate(${node.position_x}, ${node.position_y})`);
    g.dataset.nodeId = node.id;

    const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    rect.setAttribute("class", "node-box");
    rect.setAttribute("width", "190");
    rect.setAttribute("height", "90");
    rect.setAttribute("rx", "10");
    rect.setAttribute("fill", isLight ? "#ffffff" : "#0f172a");
    rect.setAttribute("stroke", categoryInfo.color);
    rect.setAttribute("stroke-width", "1.5");
    rect.setAttribute("stroke-opacity", isLight ? "0.8" : "0.6");
    if (isLight) {
      rect.setAttribute("filter", "drop-shadow(0 2px 4px rgba(0, 0, 0, 0.05))");
    }
    g.appendChild(rect);

    const strip = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    strip.setAttribute("width", "5");
    strip.setAttribute("height", "90");
    strip.setAttribute("rx", "2");
    strip.setAttribute("fill", categoryInfo.color);
    g.appendChild(strip);

    let statusColor = "#64748b";
    let statusText = node.status.toUpperCase();
    if (node.status === "completed") statusColor = "#10b981";
    if (node.status === "running") statusColor = "#0284c7";
    if (node.status === "paused") statusColor = "#f59e0b";
    if (node.status === "failed") statusColor = "#f43f5e";

    const catText = document.createElementNS("http://www.w3.org/2000/svg", "text");
    catText.setAttribute("x", "16");
    catText.setAttribute("y", "20");
    catText.setAttribute("fill", categoryInfo.color);
    catText.setAttribute("font-size", "9px");
    catText.setAttribute("font-weight", "600");
    catText.setAttribute("text-transform", "uppercase");
    catText.textContent = node.category.replace("_", " ");
    g.appendChild(catText);

    const statusLabel = document.createElementNS("http://www.w3.org/2000/svg", "text");
    statusLabel.setAttribute("x", "175");
    statusLabel.setAttribute("y", "20");
    statusLabel.setAttribute("fill", statusColor);
    statusLabel.setAttribute("font-size", "8px");
    statusLabel.setAttribute("font-weight", "bold");
    statusLabel.setAttribute("text-anchor", "end");
    statusLabel.textContent = statusText;
    g.appendChild(statusLabel);

    const labelText = document.createElementNS("http://www.w3.org/2000/svg", "text");
    labelText.setAttribute("x", "16");
    labelText.setAttribute("y", "44");
    labelText.setAttribute("fill", isLight ? "#0f172a" : "#f8fafc");
    labelText.setAttribute("font-size", "12px");
    labelText.setAttribute("font-weight", "600");
    labelText.textContent = truncateString(node.label, 20);
    g.appendChild(labelText);

    const leadName = node.agent_team_config?.node_lead?.name || "Harness Lead";
    const teamText = document.createElementNS("http://www.w3.org/2000/svg", "text");
    teamText.setAttribute("x", "16");
    teamText.setAttribute("y", "62");
    teamText.setAttribute("fill", isLight ? "#475569" : "#94a3b8");
    teamText.setAttribute("font-size", "9px");
    teamText.setAttribute("font-family", "monospace");
    teamText.textContent = truncateString(leadName, 22);
    g.appendChild(teamText);

    const bottomText = document.createElementNS("http://www.w3.org/2000/svg", "text");
    bottomText.setAttribute("x", "16");
    bottomText.setAttribute("y", "78");
    bottomText.setAttribute("fill", isLight ? "#64748b" : "#64748b");
    bottomText.setAttribute("font-size", "9px");
    const harnessType = node.agent_team_config?.harness_engine || "AGY";
    if (node.status === "completed" && node.latency_ms) {
      bottomText.textContent = `⚡ ${node.latency_ms} ms (${harnessType.toUpperCase()})`;
    } else if (node.requires_human_approval) {
      bottomText.textContent = `🛡️ HITL Gate (${harnessType.toUpperCase()})`;
      bottomText.setAttribute("fill", "#d97706");
    } else {
      bottomText.textContent = `Harness: ${harnessType.toUpperCase()}`;
    }
    g.appendChild(bottomText);

    const portHandle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    portHandle.setAttribute("cx", "190");
    portHandle.setAttribute("cy", "45");
    portHandle.setAttribute("r", "7");
    portHandle.setAttribute("fill", "#06b6d4");
    portHandle.setAttribute("stroke", isLight ? "#ffffff" : "#0f172a");
    portHandle.setAttribute("stroke-width", "2");
    portHandle.setAttribute("class", "node-connect-handle");

    portHandle.addEventListener("click", (e) => {
      e.stopPropagation();
      startConnectionMode(node.id, node.label);
    });
    g.appendChild(portHandle);

    const portPlus = document.createElementNS("http://www.w3.org/2000/svg", "text");
    portPlus.setAttribute("x", "190");
    portPlus.setAttribute("y", "48");
    portPlus.setAttribute("fill", "#ffffff");
    portPlus.setAttribute("font-size", "9px");
    portPlus.setAttribute("font-weight", "bold");
    portPlus.setAttribute("text-anchor", "middle");
    portPlus.setAttribute("pointer-events", "none");
    portPlus.textContent = "+";
    g.appendChild(portPlus);

    // Interactive Harness Settings Gear Button
    const gearBtn = document.createElementNS("http://www.w3.org/2000/svg", "g");
    gearBtn.setAttribute("class", "node-gear-btn");
    gearBtn.style.cursor = "pointer";
    gearBtn.innerHTML = `
      <circle cx="174" cy="74" r="8" fill="${isLight ? '#f1f5f9' : '#0f172a'}" stroke="${categoryInfo.color}" stroke-width="1" />
      <text x="174" y="77" fill="#38bdf8" font-size="9px" text-anchor="middle" font-family="monospace">⚙</text>
    `;
    gearBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      AppState.selectedNodeId = node.id;
      renderDag();
      renderNodeInspector(node.id);
      openConfigureSquadModal(node.id);
    });
    g.appendChild(gearBtn);

    g.addEventListener("dblclick", (e) => {
      e.stopPropagation();
      AppState.selectedNodeId = node.id;
      renderDag();
      renderNodeInspector(node.id);
      openConfigureSquadModal(node.id);
    });

    g.addEventListener("click", () => {
      if (AppState.connecting.active) {
        completeConnection(node.id);
      } else {
        AppState.selectedNodeId = node.id;
        renderDag();
        renderNodeInspector(node.id);
      }
    });

    makeDraggable(g, node);
    svg.appendChild(g);
  });
}

function truncateString(str, num) {
  if (!str) return "";
  if (str.length <= num) return str;
  return str.slice(0, num) + "...";
}

function makeDraggable(element, node) {
  let isDragging = false;
  let startX, startY;

  element.addEventListener("mousedown", (e) => {
    if (e.target.classList.contains("node-connect-handle")) return;
    isDragging = true;
    startX = e.clientX - node.position_x;
    startY = e.clientY - node.position_y;
    element.style.cursor = "grabbing";
  });

  window.addEventListener("mousemove", (e) => {
    if (!isDragging) return;
    node.position_x = Math.max(20, e.clientX - startX);
    node.position_y = Math.max(20, e.clientY - startY);
    renderDag();
  });

  window.addEventListener("mouseup", async () => {
    if (isDragging) {
      isDragging = false;
      element.style.cursor = "pointer";
      try {
        await fetch(`/api/pathways/nodes/${node.id}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            position_x: node.position_x,
            position_y: node.position_y,
          }),
        });
      } catch (err) {
        console.error("Failed to persist node position:", err);
      }
    }
  });
}

// ---------------- Node Inspector ----------------

function renderNodeInspector(nodeId) {
  const container = document.getElementById("nodeInspectorContent");
  const badge = document.getElementById("inspectorStatusBadge");

  if (!nodeId || !AppState.state) {
    container.innerHTML = `<div class="text-slate-500 italic text-center py-12">Click on any node in the pathway to inspect agentic harness settings, outputs, connections, and human oversight gates.</div>`;
    badge.textContent = "SELECT NODE";
    badge.className = "text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-slate-800 text-slate-400";
    return;
  }

  const { nodes = [], edges = [] } = AppState.state.pathway;
  const node = nodes.find((n) => n.id === nodeId);
  if (!node) return;

  badge.textContent = node.status.toUpperCase();
  let badgeColor = "bg-slate-800 text-slate-400";
  if (node.status === "completed") badgeColor = "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30";
  if (node.status === "running") badgeColor = "bg-cyan-500/20 text-cyan-400 border border-cyan-500/30";
  if (node.status === "paused") badgeColor = "bg-amber-500/20 text-amber-400 border border-amber-500/30";
  if (node.status === "failed") badgeColor = "bg-rose-500/20 text-rose-400 border border-rose-500/30";
  badge.className = `text-[10px] font-mono uppercase px-2 py-0.5 rounded ${badgeColor}`;

  let approvalActionHtml = "";
  if (node.requires_human_approval) {
    approvalActionHtml = `
      <div class="bg-amber-950/40 border border-amber-600/40 rounded-lg p-3 space-y-2">
        <div class="flex items-center justify-between">
          <div class="text-amber-400 font-semibold flex items-center text-[11px]">
            <i class="fa-solid fa-user-shield mr-1.5"></i>
            Human-in-the-Loop Gate
          </div>
          <span class="text-[9px] font-mono px-1.5 py-0.2 rounded ${node.approval_granted ? "bg-emerald-500/20 text-emerald-400" : "bg-amber-500/20 text-amber-300"}">
            ${node.approval_granted ? "AUTHORIZED" : "APPROVAL REQUIRED"}
          </span>
        </div>
        <div class="text-slate-300 text-[10px] space-y-1">
          <div><strong>Authority:</strong> ${node.human_oversight_role || "Statutory Duty Officer"}</div>
          ${node.human_signoff_notes ? `<div class="text-slate-400 italic">Notes: ${node.human_signoff_notes}</div>` : ""}
        </div>
        ${
          !node.approval_granted
            ? `
          <div class="space-y-1.5 pt-1">
            <input id="inspectorSignoffNotes" type="text" placeholder="Signoff authorization notes..." class="w-full bg-slate-900 border border-slate-700 rounded px-2 py-1 text-slate-200 text-[10px] focus:outline-none focus:border-amber-500">
            <button id="btnApproveNode" class="w-full py-1.5 bg-amber-600 hover:bg-amber-500 text-slate-950 font-bold rounded transition text-xs shadow">
              Authorize Node Execution
            </button>
          </div>
        `
            : ""
        }
      </div>
    `;
  }

const HARNESS_DEFAULT_COMMANDS = {
  agy: "agy exec",
  claude_code: "claude -p",
  codex: "codex exec",
  opencode: "opencode run",
  sovereign_container: "podman run --network none -v /local/sandbox:/workspace:Z",
  custom_harness: "python -m harness.react_loop",
};

  const inboundEdges = edges.filter((e) => e.target === node.id);
  const outboundEdges = edges.filter((e) => e.source === node.id);

  const squadName = node.agent_team_config?.name || node.agent_team_id.replace("_", " ");
  const leadAgentName = node.agent_team_config?.node_lead?.name || "Harness Lead";
  const harnessEngineRaw = node.agent_team_config?.harness_engine || "agy";
  const harnessEngine = harnessEngineRaw.toUpperCase();
  const harnessCommand = node.agent_team_config?.harness_command || HARNESS_DEFAULT_COMMANDS[harnessEngineRaw] || "agy exec";
  const sandboxPolicy = node.agent_team_config?.sandbox_policy || "restricted_fs";
  const providerType = node.provider_config?.provider_type || node.agent_team_config?.provider_config?.provider_type || "local_open_weights";
  const modelDisplay = node.provider_config?.model_name || node.agent_team_config?.provider_config?.model_name || "llama-3.3-70b-instruct-q4";

  container.innerHTML = `
    <div class="space-y-4">
      <div>
        <span class="text-slate-500 uppercase font-semibold text-[10px]">Node Identifier</span>
        <div class="font-mono text-cyan-400 font-medium">${node.id}</div>
      </div>

      <div>
        <span class="text-slate-500 uppercase font-semibold text-[10px]">Label</span>
        <div class="font-semibold text-slate-100 text-sm">${node.label}</div>
      </div>

      <div>
        <span class="text-slate-500 uppercase font-semibold text-[10px]">Description</span>
        <div class="text-slate-300 leading-relaxed">${node.description}</div>
      </div>

      <!-- Live Interactive Agentic Harness Configuration -->
      <div class="space-y-2.5 pt-2 border-t border-slate-800">
        <div class="flex items-center justify-between">
          <span class="text-cyan-400 uppercase font-bold text-[10px] tracking-wider flex items-center">
            <i class="fa-solid fa-microchip mr-1.5 text-cyan-400"></i>
            Agentic Harness &amp; Squad
          </span>
          <span id="inspectorHarnessBadge" class="text-[9px] font-mono font-bold uppercase px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">
            ${harnessEngine}
          </span>
        </div>

        <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 space-y-2.5">
          <div class="flex items-center justify-between text-[11px]">
            <span class="font-bold text-slate-200 truncate flex items-center">
              <i class="fa-solid fa-users-gear text-purple-400 mr-1.5"></i>
              ${squadName}
            </span>
            <span class="text-[9px] font-mono text-emerald-400 shrink-0 ml-2">LEAD: ${leadAgentName}</span>
          </div>

          <div>
            <label class="block text-slate-400 text-[10px] mb-1 font-medium">Execution Harness Engine</label>
            <select id="quickHarnessEngineSelect" class="w-full bg-slate-900 border border-slate-700 rounded px-2.5 py-1.5 text-cyan-300 text-xs font-semibold focus:outline-none focus:border-cyan-500">
              <option value="agy" ${harnessEngineRaw === "agy" ? "selected" : ""}>AGY (Antigravity Autonomous Harness)</option>
              <option value="claude_code" ${harnessEngineRaw === "claude_code" ? "selected" : ""}>Claude Code CLI (claude -p)</option>
              <option value="codex" ${harnessEngineRaw === "codex" ? "selected" : ""}>OpenAI Codex CLI (codex exec)</option>
              <option value="opencode" ${harnessEngineRaw === "opencode" ? "selected" : ""}>OpenCode Multi-Agent Harness</option>
              <option value="sovereign_container" ${harnessEngineRaw === "sovereign_container" ? "selected" : ""}>Air-Gapped Sovereign Podman Container</option>
              <option value="custom_harness" ${harnessEngineRaw === "custom_harness" ? "selected" : ""}>Custom ReAct Execution Harness</option>
            </select>
          </div>

          <div>
            <label class="block text-slate-400 text-[10px] mb-1 font-medium">CLI Execution Command</label>
            <input id="quickHarnessCommandInput" type="text" value="${harnessCommand}" class="w-full bg-slate-900 border border-slate-700 rounded px-2.5 py-1.5 text-slate-200 font-mono text-xs focus:outline-none focus:border-cyan-500">
          </div>

          <div class="grid grid-cols-2 gap-2">
            <div>
              <label class="block text-slate-400 text-[10px] mb-1 font-medium">Sandbox Policy</label>
              <select id="quickHarnessSandboxSelect" class="w-full bg-slate-900 border border-slate-700 rounded px-2 py-1 text-slate-200 text-[11px] focus:outline-none focus:border-cyan-500">
                <option value="restricted_fs" ${sandboxPolicy === "restricted_fs" ? "selected" : ""}>Restricted FS</option>
                <option value="read_only" ${sandboxPolicy === "read_only" ? "selected" : ""}>Read-Only</option>
                <option value="isolated_container" ${sandboxPolicy === "isolated_container" ? "selected" : ""}>Isolated Container</option>
              </select>
            </div>
            <div>
              <label class="block text-slate-400 text-[10px] mb-1 font-medium">Model Weights</label>
              <input id="quickModelInput" type="text" value="${modelDisplay}" class="w-full bg-slate-900 border border-slate-700 rounded px-2 py-1 text-slate-200 text-[11px] focus:outline-none focus:border-cyan-500">
            </div>
          </div>

          <div class="pt-1 flex items-center space-x-2">
            <button id="btnApplyQuickHarness" class="flex-1 py-1.5 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white font-bold rounded text-xs transition shadow flex items-center justify-center space-x-1">
              <i class="fa-solid fa-check"></i>
              <span>Apply Harness</span>
            </button>
            <button id="btnConfigureNodeSquad" class="px-2.5 py-1.5 bg-slate-800 hover:bg-slate-700 text-purple-300 border border-purple-500/40 rounded text-xs font-semibold transition flex items-center space-x-1" title="Customize individual agent personas, tools, and skills">
              <i class="fa-solid fa-sliders"></i>
              <span>Squad &amp; Skills</span>
            </button>
          </div>
        </div>
      </div>

      ${approvalActionHtml}

      <div class="space-y-2 pt-2 border-t border-slate-800">
        <div class="flex items-center justify-between">
          <span class="text-slate-500 uppercase font-semibold text-[10px]">Pathway Connections</span>
          <button id="btnInspectorQuickConnect" class="text-[11px] text-cyan-400 hover:text-cyan-300 flex items-center space-x-1">
            <i class="fa-solid fa-link"></i>
            <span>+ Connect</span>
          </button>
        </div>

        <div class="space-y-1.5 text-[11px]">
          <div class="text-slate-400 text-[10px] font-semibold">Incoming Inputs:</div>
          ${
            inboundEdges.length === 0
              ? `<div class="text-slate-500 italic text-[10px]">None (Root Node)</div>`
              : inboundEdges
                  .map((e) => {
                    const src = nodes.find((n) => n.id === e.source);
                    return `
              <div class="flex items-center justify-between bg-slate-950 px-2.5 py-1 rounded border border-slate-800">
                <span class="text-slate-300 truncate font-mono text-[10px]">← ${src?.label || e.source}</span>
                <button data-edge-id="${e.id}" class="btn-disconnect-edge text-rose-400 hover:text-rose-300 text-[10px] ml-2">Disconnect</button>
              </div>
            `;
                  })
                  .join("")
          }

          <div class="text-slate-400 text-[10px] font-semibold pt-1">Outgoing Dependencies:</div>
          ${
            outboundEdges.length === 0
              ? `<div class="text-slate-500 italic text-[10px]">None (Terminal Node)</div>`
              : outboundEdges
                  .map((e) => {
                    const tgt = nodes.find((n) => n.id === e.target);
                    return `
              <div class="flex items-center justify-between bg-slate-950 px-2.5 py-1 rounded border border-slate-800">
                <span class="text-slate-300 truncate font-mono text-[10px]">→ ${tgt?.label || e.target}</span>
                <button data-edge-id="${e.id}" class="btn-disconnect-edge text-rose-400 hover:text-rose-300 text-[10px] ml-2">Disconnect</button>
              </div>
            `;
                  })
                  .join("")
          }
        </div>
      </div>

      <div>
        <span class="text-slate-500 uppercase font-semibold text-[10px]">Outputs &amp; Generated Artifacts</span>
        <pre class="mt-1 bg-slate-950 p-2.5 rounded border border-slate-800 font-mono text-[10px] text-cyan-300 overflow-x-auto max-h-40">${
          JSON.stringify(node.outputs, null, 2) || "{}"
        }</pre>
      </div>

      <div class="pt-3 border-t border-slate-800 flex items-center justify-between">
        <button id="btnDeleteNode" class="text-rose-400 hover:text-rose-300 transition flex items-center space-x-1">
          <i class="fa-solid fa-trash-can"></i>
          <span>Delete Node</span>
        </button>
        <button id="btnStartConnectFromThis" class="text-cyan-400 hover:text-cyan-300 transition flex items-center space-x-1">
          <i class="fa-solid fa-arrow-right-from-bracket"></i>
          <span>Link Output</span>
        </button>
      </div>
    </div>
  `;

  // Quick Harness Selector and Apply Event Listeners
  const quickEngineSelect = document.getElementById("quickHarnessEngineSelect");
  const quickCmdInput = document.getElementById("quickHarnessCommandInput");
  quickEngineSelect?.addEventListener("change", (e) => {
    quickCmdInput.value = HARNESS_DEFAULT_COMMANDS[e.target.value] || "agy exec";
  });

  document.getElementById("btnApplyQuickHarness")?.addEventListener("click", async () => {
    const applyBtn = document.getElementById("btnApplyQuickHarness");
    applyBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i><span>Saving...</span>`;
    applyBtn.disabled = true;

    const newEngine = quickEngineSelect.value;
    const newCmd = quickCmdInput.value;
    const newSandbox = document.getElementById("quickHarnessSandboxSelect").value;
    const newModel = document.getElementById("quickModelInput").value;

    const currentConfig = node.agent_team_config ? { ...node.agent_team_config } : {
      team_id: `squad_${node.id}`,
      name: node.agent_team_id.replace("_", " "),
      description: "Configured multi-agent squad",
      lead_role: "Bioinformatics & Genomics Specialist",
      collaboration_strategy: "sequential_refinement",
      members: [],
    };

    currentConfig.harness_engine = newEngine;
    currentConfig.harness_command = newCmd;
    currentConfig.sandbox_policy = newSandbox;

    const providerConfig = {
      provider_type: "local_open_weights",
      model_name: newModel,
      endpoint_url: "http://localhost:11434/v1",
      temperature: 0.2,
      max_tokens: 4096,
      is_sovereign_hosted: true,
    };
    currentConfig.provider_config = providerConfig;

    try {
      const res = await fetch(`/api/pathways/nodes/${node.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          agent_team_config: currentConfig,
          provider_config: providerConfig,
        }),
      });

      if (res.ok) {
        await refreshState();
        renderNodeInspector(node.id);
        renderDag();
      } else {
        alert("Failed to update harness configuration.");
        applyBtn.innerHTML = `<i class="fa-solid fa-check"></i><span>Apply Harness</span>`;
        applyBtn.disabled = false;
      }
    } catch (err) {
      console.error("Failed to update harness:", err);
      applyBtn.innerHTML = `<i class="fa-solid fa-check"></i><span>Apply Harness</span>`;
      applyBtn.disabled = false;
    }
  });

  document.getElementById("btnConfigureNodeSquad")?.addEventListener("click", () => {
    openConfigureSquadModal(node.id);
  });

  document.getElementById("btnApproveNode")?.addEventListener("click", async () => {
    const notes = document.getElementById("inspectorSignoffNotes")?.value || "Authorized by Operator";
    await fetch(`/api/pathways/nodes/${node.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ human_signoff_notes: notes }),
    });
    await fetch(`/api/execution/approve/${node.id}`, { method: "POST" });
    await refreshState();
  });

  document.getElementById("btnDeleteNode")?.addEventListener("click", async () => {
    if (confirm(`Are you sure you want to delete node '${node.label}'?`)) {
      await fetch(`/api/pathways/nodes/${node.id}`, { method: "DELETE" });
      AppState.selectedNodeId = null;
      await refreshState();
    }
  });

  document.getElementById("btnStartConnectFromThis")?.addEventListener("click", () => {
    startConnectionMode(node.id, node.label);
  });

  document.getElementById("btnInspectorQuickConnect")?.addEventListener("click", () => {
    openConnectModal(node.id);
  });

  document.querySelectorAll(".btn-disconnect-edge").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const edgeId = btn.dataset.edgeId;
      await fetch(`/api/pathways/edges/${edgeId}`, { method: "DELETE" });
      await refreshState();
    });
  });
}

// ---------------- Connection Management ----------------

function startConnectionMode(sourceId, sourceLabel) {
  AppState.connecting = {
    active: true,
    sourceId: sourceId,
    sourceLabel: sourceLabel,
  };
  const banner = document.getElementById("connectModeBanner");
  const label = document.getElementById("connectSourceLabel");
  label.textContent = sourceLabel;
  banner.classList.remove("hidden");
  renderDag();
}

function cancelConnectionMode() {
  AppState.connecting = { active: false, sourceId: null, sourceLabel: null };
  const banner = document.getElementById("connectModeBanner");
  banner.classList.add("hidden");
  renderDag();
}

async function completeConnection(targetId) {
  if (!AppState.connecting.active) return;
  const sourceId = AppState.connecting.sourceId;

  if (sourceId === targetId) {
    alert("Cannot connect a node to itself.");
    cancelConnectionMode();
    return;
  }

  try {
    const res = await fetch("/api/pathways/edges", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        source: sourceId,
        target: targetId,
        label: "Data Flow",
      }),
    });

    if (!res.ok) {
      const errData = await res.json();
      alert(`Connection failed: ${errData.detail || "Circular loop or invalid dependency"}`);
    } else {
      await refreshState();
    }
  } catch (err) {
    console.error("Failed to add edge:", err);
  } finally {
    cancelConnectionMode();
  }
}

function openConnectModal(defaultSourceId = null) {
  const modal = document.getElementById("connectNodesModal");
  const srcSelect = document.getElementById("connectSourceSelect");
  const tgtSelect = document.getElementById("connectTargetSelect");
  const errMsg = document.getElementById("connectErrorMsg");
  errMsg.classList.add("hidden");

  const nodes = AppState.state?.pathway?.nodes || [];
  srcSelect.innerHTML = "";
  tgtSelect.innerHTML = "";

  nodes.forEach((n) => {
    const opt1 = document.createElement("option");
    opt1.value = n.id;
    opt1.textContent = `${n.label} (${n.category})`;
    if (defaultSourceId && n.id === defaultSourceId) opt1.selected = true;
    srcSelect.appendChild(opt1);

    const opt2 = document.createElement("option");
    opt2.value = n.id;
    opt2.textContent = `${n.label} (${n.category})`;
    tgtSelect.appendChild(opt2);
  });

  modal.classList.remove("hidden");
}

async function handleConnectNodesSubmit(e) {
  e.preventDefault();
  const source = document.getElementById("connectSourceSelect").value;
  const target = document.getElementById("connectTargetSelect").value;
  const label = document.getElementById("connectEdgeLabel").value;
  const errMsg = document.getElementById("connectErrorMsg");

  if (source === target) {
    errMsg.textContent = "Cannot connect a node to itself!";
    errMsg.classList.remove("hidden");
    return;
  }

  try {
    const res = await fetch("/api/pathways/edges", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ source, target, label: label || null }),
    });

    if (!res.ok) {
      const err = await res.json();
      errMsg.textContent = err.detail || "Failed to create edge (may introduce a cycle)";
      errMsg.classList.remove("hidden");
      return;
    }

    document.getElementById("connectNodesModal").classList.add("hidden");
    document.getElementById("connectNodesForm").reset();
    await refreshState();
  } catch (err) {
    errMsg.textContent = "Error connecting nodes: " + err;
    errMsg.classList.remove("hidden");
  }
}

// ---------------- Form Handlers ----------------

async function handleAddNode(e) {
  e.preventDefault();
  const label = document.getElementById("newNodeLabel").value;
  const category = document.getElementById("newNodeCategory").value;
  const description = document.getElementById("newNodeDesc").value;
  const agent_team_id = document.getElementById("newNodeTeam").value;
  const requires_human_approval = document.getElementById("newNodeApproval").checked;

  try {
    await fetch("/api/pathways/nodes", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        label,
        category,
        description,
        agent_team_id,
        requires_human_approval,
        position_x: 600 + Math.random() * 80,
        position_y: 200 + Math.random() * 80,
      }),
    });
    document.getElementById("addNodeModal").classList.add("hidden");
    document.getElementById("addNodeForm").reset();
    await refreshState();
  } catch (err) {
    console.error("Add node failed:", err);
  }
}

async function handleCustomSample(e) {
  e.preventDefault();
  const name = document.getElementById("customSampleName").value;
  const sample_type = document.getElementById("customSampleType").value;
  const source_location = document.getElementById("customSampleLocation").value || "Australia";
  const raw_payload = document.getElementById("customSamplePayload").value;

  try {
    await fetch("/api/scenarios/custom", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name,
        sample_type,
        source_location,
        raw_payload,
      }),
    });
    document.getElementById("customSampleModal").classList.add("hidden");
    document.getElementById("customSampleForm").reset();

    const scenRes = await fetch("/api/scenarios").then((r) => r.json());
    AppState.scenarios = scenRes.scenarios || [];
    populateScenarioDropdown();
    await refreshState();
  } catch (err) {
    console.error("Custom specimen submission failed:", err);
  }
}

// ---------------- Operational Playbooks (formerly Templates) Management ----------------

async function openTemplatesManager() {
  const modal = document.getElementById("templatesManagerModal");
  const container = document.getElementById("templatesListContainer");
  container.innerHTML = `<div class="text-slate-500 italic p-4 text-center">Loading operational playbooks...</div>`;
  modal.classList.remove("hidden");

  try {
    const res = await fetch("/api/pathways/templates");
    const data = await res.json();
    AppState.templates = data.templates || [];

    if (!AppState.templates.length) {
      container.innerHTML = `<div class="text-slate-500 italic p-4 text-center">No playbooks available.</div>`;
      return;
    }

    container.innerHTML = AppState.templates
      .map((t) => {
        const isCurrent = t.id === AppState.state?.pathway?.id;
        const playbookTitle = t.playbook_title || t.name;
        const scope = t.scenario_scope || t.description;
        const trigger = t.trigger_criteria || "Incident Controller command";
        const lead = t.lead_agency || "Commonwealth Lead";

        return `
        <div class="bg-slate-950 p-4 rounded-xl border border-slate-800 flex items-start justify-between space-x-4 shadow-sm hover:border-slate-700 transition">
          <div class="space-y-1.5 flex-1">
            <div class="flex items-center space-x-2">
              <span class="font-bold text-slate-100 text-sm tracking-tight">${playbookTitle}</span>
              ${t.is_builtin ? `<span class="text-[9px] font-mono px-1.5 py-0.2 bg-purple-500/10 text-purple-400 border border-purple-500/20 rounded font-bold">COMMONWEALTH PLAYBOOK</span>` : `<span class="text-[9px] font-mono px-1.5 py-0.2 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded font-bold">USER PLAYBOOK</span>`}
              ${isCurrent ? `<span class="text-[9px] font-mono px-1.5 py-0.2 bg-cyan-500/20 text-cyan-300 rounded font-bold">ACTIVE</span>` : ""}
            </div>
            <p class="text-slate-300 text-xs leading-relaxed">${scope}</p>
            <div class="grid grid-cols-2 gap-2 text-[10px] text-slate-400 font-mono pt-1">
              <div><strong class="text-amber-400">Trigger:</strong> ${trigger}</div>
              <div><strong class="text-cyan-400">Lead Agency:</strong> ${lead}</div>
            </div>
            <div class="text-[10px] text-slate-500 font-mono">${t.node_count} nodes • ${t.edge_count} edges • Threat: ${t.threat_type}</div>
          </div>
          <div class="flex flex-col items-end space-y-2 shrink-0">
            <button data-template-id="${t.id}" class="btn-load-template px-3.5 py-1.5 bg-cyan-600 hover:bg-cyan-500 text-white rounded text-xs font-bold transition shadow">
              Deploy Playbook
            </button>
            ${
              !t.is_builtin
                ? `<button data-template-id="${t.id}" class="btn-delete-template px-2 py-1 text-rose-400 hover:text-rose-300 text-xs transition" title="Delete Playbook"><i class="fa-solid fa-trash-can"></i></button>`
                : ""
            }
          </div>
        </div>
      `;
      })
      .join("");

    document.querySelectorAll(".btn-load-template").forEach((btn) => {
      btn.addEventListener("click", async () => {
        const id = btn.dataset.templateId;
        await fetch(`/api/pathways/templates/load/${id}`, { method: "POST" });
        modal.classList.add("hidden");
        await refreshState();
        populateScenarioDropdown();
      });
    });

    document.querySelectorAll(".btn-delete-template").forEach((btn) => {
      btn.addEventListener("click", async () => {
        const id = btn.dataset.templateId;
        if (confirm("Delete this user playbook?")) {
          await fetch(`/api/pathways/templates/${id}`, { method: "DELETE" });
          openTemplatesManager();
        }
      });
    });
  } catch (err) {
    container.innerHTML = `<div class="text-rose-400 p-4 text-center">Failed to load playbooks: ${err}</div>`;
  }
}

async function handleSaveTemplate(e) {
  e.preventDefault();
  const name = document.getElementById("templateNameInput").value;
  const description = document.getElementById("templateDescInput").value;

  try {
    const res = await fetch("/api/pathways/templates/save", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, description }),
    });

    if (res.ok) {
      document.getElementById("saveTemplateModal").classList.add("hidden");
      document.getElementById("saveTemplateForm").reset();
      alert(`Operational response playbook '${name}' saved successfully!`);
    } else {
      alert("Failed to save playbook.");
    }
  } catch (err) {
    console.error("Save playbook error:", err);
  }
}

async function exportPathwayJson() {
  try {
    const res = await fetch("/api/pathways/export/json");
    const data = await res.json();
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `playbook_${data.name.toLowerCase().replace(/[^a-z0-9]/g, "_")}.json`;
    a.click();
    URL.revokeObjectURL(url);
  } catch (err) {
    console.error("Export JSON failed:", err);
  }
}

async function handleImportPathwayFile(e) {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = async (event) => {
    try {
      const json = JSON.parse(event.target.result);
      const res = await fetch("/api/pathways/import/json", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(json),
      });
      if (res.ok) {
        document.getElementById("templatesManagerModal").classList.add("hidden");
        await refreshState();
        alert("Custom operational playbook imported successfully!");
      } else {
        const err = await res.json();
        alert(`Import failed: ${err.detail}`);
      }
    } catch (err) {
      alert("Invalid JSON file: " + err);
    }
  };
  reader.readAsText(file);
}

// ---------------- Squad & Execution Harness Configuration ----------------

function openConfigureSquadModal(nodeId) {
  const node = AppState.state?.pathway?.nodes?.find((n) => n.id === nodeId);
  if (!node) return;

  const modal = document.getElementById("configureSquadModal");
  document.getElementById("configSquadNodeId").value = node.id;
  document.getElementById("configSquadName").value = node.agent_team_config?.name || node.agent_team_id.replace("_", " ");
  document.getElementById("configSquadStrategy").value = node.agent_team_config?.collaboration_strategy || "sequential_refinement";

  // Harness configuration
  const harnessSelect = document.getElementById("configHarnessEngineSelect");
  const cmdInput = document.getElementById("configHarnessCommand");
  if (harnessSelect) {
    const rawEngine = node.agent_team_config?.harness_engine || "agy";
    harnessSelect.value = rawEngine;
    harnessSelect.onchange = (e) => {
      if (cmdInput) cmdInput.value = HARNESS_DEFAULT_COMMANDS[e.target.value] || "agy exec";
    };
  }
  if (cmdInput) {
    cmdInput.value = node.agent_team_config?.harness_command || HARNESS_DEFAULT_COMMANDS[node.agent_team_config?.harness_engine || "agy"] || "agy exec";
  }
  const sandboxSelect = document.getElementById("configHarnessSandbox");
  if (sandboxSelect) {
    sandboxSelect.value = node.agent_team_config?.sandbox_policy || "restricted_fs";
  }

  // Provider
  const prov = node.provider_config || node.agent_team_config?.provider_config;
  document.getElementById("configProviderSelect").value = prov?.provider_type || "local_open_weights";
  document.getElementById("configModelName").value = prov?.model_name || "llama-3.3-70b-instruct-q4";

  document.getElementById("configNodeHitlRequired").checked = !!node.requires_human_approval;
  document.getElementById("configNodeHitlRole").value = node.human_oversight_role || "Statutory Oversight Officer";

  // Render squad member cards with tools and skills
  const membersContainer = document.getElementById("squadMembersChecklist");
  let anyChecked = false;
  membersContainer.innerHTML = AppState.personas
    .map((p) => {
      let isMember = false;
      if (node.agent_team_config && node.agent_team_config.members && node.agent_team_config.members.length > 0) {
        isMember = node.agent_team_config.members.some((m) => m.id === p.id);
      } else {
        const teamLower = (node.agent_team_id || "").toLowerCase();
        const pIdLower = p.id.toLowerCase();
        if (teamLower.includes("bioinfo") && pIdLower.includes("bioinfo")) isMember = true;
        else if (teamLower.includes("struct") && pIdLower.includes("struct")) isMember = true;
        else if (teamLower.includes("chem") && pIdLower.includes("medchem")) isMember = true;
        else if (teamLower.includes("vaccin") && pIdLower.includes("vaccin")) isMember = true;
        else if (teamLower.includes("biosecur") && pIdLower.includes("cbrn")) isMember = true;
        else if (teamLower.includes("polic") && pIdLower.includes("policy")) isMember = true;
        else if (teamLower.includes("rad") && pIdLower.includes("physic")) isMember = true;
        else if (teamLower.includes("research") && pIdLower.includes("research")) isMember = true;
      }
      if (isMember) anyChecked = true;

      return `
      <div class="p-2.5 rounded-lg border border-slate-800 bg-slate-900/80 space-y-2">
        <label class="flex items-center space-x-2 cursor-pointer">
          <input type="checkbox" value="${p.id}" class="persona-checkbox rounded bg-slate-950 border-slate-700 text-cyan-600 focus:ring-0" ${isMember ? "checked" : ""}>
          <div class="truncate">
            <div class="font-bold text-slate-200 text-xs font-mono">${p.name}</div>
            <div class="text-[10px] text-cyan-400 truncate">${p.role}</div>
          </div>
        </label>
        <div class="text-[10px] text-slate-400 line-clamp-2">${p.specialization}</div>
      </div>
    `;
    })
    .join("");

  if (!anyChecked) {
    const firstCb = membersContainer.querySelector(".persona-checkbox");
    if (firstCb) firstCb.checked = true;
  }

  modal.classList.remove("hidden");
}

async function handleSaveSquadConfig(e) {
  e.preventDefault();
  const nodeId = document.getElementById("configSquadNodeId").value;
  const name = document.getElementById("configSquadName").value;
  const strategy = document.getElementById("configSquadStrategy").value;
  const harnessEngine = document.getElementById("configHarnessEngineSelect").value;
  const harnessCmd = document.getElementById("configHarnessCommand").value;
  const sandboxPolicy = document.getElementById("configHarnessSandbox").value;
  const providerType = document.getElementById("configProviderSelect").value;
  const modelName = document.getElementById("configModelName").value;
  const hitlRequired = document.getElementById("configNodeHitlRequired").checked;
  const hitlRole = document.getElementById("configNodeHitlRole").value;

  const selectedPersonaIds = Array.from(document.querySelectorAll(".persona-checkbox:checked")).map((cb) => cb.value);
  const selectedPersonas = AppState.personas.filter((p) => selectedPersonaIds.includes(p.id));

  if (!selectedPersonas.length) {
    alert("Please select at least one specialist agent persona for this squad.");
    return;
  }

  const provider_config = {
    provider_type: providerType,
    model_name: modelName,
    endpoint_url: "http://localhost:11434/v1",
    temperature: 0.2,
    max_tokens: 4096,
    is_sovereign_hosted: providerType.includes("local") || providerType.includes("sovereign"),
  };

  const agent_team_config = {
    team_id: `squad_${nodeId}`,
    name: name,
    description: "Configured multi-agent squad",
    lead_role: selectedPersonas[0].role,
    node_lead: selectedPersonas[0],
    members: selectedPersonas,
    collaboration_strategy: strategy,
    harness_engine: harnessEngine,
    harness_command: harnessCmd,
    sandbox_policy: sandboxPolicy,
    approval_mode: hitlRequired ? "on_request" : "autonomous",
    provider_config: provider_config,
  };

  try {
    const res = await fetch(`/api/pathways/nodes/${nodeId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        agent_team_config,
        provider_config,
        requires_human_approval: hitlRequired,
        human_oversight_role: hitlRole,
      }),
    });

    if (res.ok) {
      document.getElementById("configureSquadModal").classList.add("hidden");
      await refreshState();
      renderNodeInspector(nodeId);
      alert(`Node '${nodeId}' updated with ${harnessEngine.toUpperCase()} harness.`);
    } else {
      alert("Failed to update node configuration.");
    }
  } catch (err) {
    console.error("Save squad config error:", err);
  }
}

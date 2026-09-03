/**
 * PandemicPrepDash - Frontend Application Logic
 */

const AppState = {
  state: null,
  scenarios: [],
  selectedNodeId: null,
  selectedAgencyId: "ACDC",
  agencies: [],
  activeTab: "tab-pathway",
};

const CATEGORY_STYLES = {
  ingestion: { color: "#06b6d4", bg: "#083344", icon: "fa-vial" },
  characterization: { color: "#3b82f6", bg: "#172554", icon: "fa-dna" },
  structural_biology: { color: "#a855f7", bg: "#3b0764", icon: "fa-atom" },
  therapeutics: { color: "#10b981", bg: "#022c22", icon: "fa-pills" },
  vaccinology: { color: "#f59e0b", bg: "#451a03", icon: "fa-shield-virus" },
  biosecurity: { color: "#f43f5e", bg: "#4c0519", icon: "fa-biohazard" },
  agency_reporting: { color: "#6366f1", bg: "#1e1b4b", icon: "fa-landmark" },
  custom: { color: "#94a3b8", bg: "#1e293b", icon: "fa-gear" },
};

// Initialize Application
document.addEventListener("DOMContentLoaded", () => {
  setupTabs();
  setupEventListeners();
  loadInitialData();
});

// Setup Tab Navigation
function setupTabs() {
  document.querySelectorAll(".tab-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const targetTab = btn.dataset.tab;
      AppState.activeTab = targetTab;

      document.querySelectorAll(".tab-btn").forEach((b) => {
        b.classList.remove("active", "border-cyan-500", "text-cyan-400");
        b.classList.add("border-transparent", "text-slate-400");
      });
      btn.classList.add("active", "border-cyan-500", "text-cyan-400");
      btn.classList.remove("border-transparent", "text-slate-400");

      document.querySelectorAll(".tab-panel").forEach((panel) => {
        panel.classList.add("hidden");
      });
      const activePanel = document.getElementById(targetTab);
      if (activePanel) activePanel.classList.remove("hidden");

      if (targetTab === "tab-pathway") {
        renderDag();
      } else if (targetTab === "tab-agencies") {
        renderAgencyView();
      } else if (targetTab === "tab-countermeasures") {
        renderCountermeasures();
      } else if (targetTab === "tab-agentfeed") {
        renderAgentFeed();
      }
    });
  });
}

// Setup Event Listeners
function setupEventListeners() {
  // Scenario select
  const scenSelect = document.getElementById("scenarioSelect");
  scenSelect.addEventListener("change", (e) => {
    selectScenario(e.target.value);
  });

  // Action Buttons
  document.getElementById("btnStep").addEventListener("click", executeStep);
  document.getElementById("btnRunAll").addEventListener("click", executeRunAll);
  document.getElementById("btnReset").addEventListener("click", resetExecution);

  // Template switch
  document.getElementById("btnSwitchPathway").addEventListener("click", () => {
    const currentType = AppState.state?.pathway?.threat_type;
    const newKey = currentType === "chemical_nerve_agent" ? "pathway_default_biological" : "pathway_default_chemical";
    switchPathwayTemplate(newKey);
  });

  // Modal Triggers
  document.getElementById("btnAddNodeModal").addEventListener("click", () => {
    document.getElementById("addNodeModal").classList.remove("hidden");
  });
  document.getElementById("btnCustomSampleModal").addEventListener("click", () => {
    document.getElementById("customSampleModal").classList.remove("hidden");
  });

  // Modal Closers
  document.querySelectorAll(".modal-close").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.getElementById("addNodeModal").classList.add("hidden");
      document.getElementById("customSampleModal").classList.add("hidden");
    });
  });

  // Form Submissions
  document.getElementById("addNodeForm").addEventListener("submit", handleAddNode);
  document.getElementById("customSampleForm").addEventListener("submit", handleCustomSample);

  // Dispatch All Briefings
  document.getElementById("btnDispatchAllReports").addEventListener("click", dispatchAllBriefings);
}

// API Calls and Data Loaders
async function loadInitialData() {
  try {
    const [scenRes, stateRes, agencyRes] = await Promise.all([
      fetch("/api/scenarios").then((r) => r.json()),
      fetch("/api/pathways/state").then((r) => r.json()),
      fetch("/api/agencies").then((r) => r.json()),
    ]);

    AppState.scenarios = scenRes.scenarios || [];
    AppState.state = stateRes;
    AppState.agencies = agencyRes.agencies || [];

    populateScenarioDropdown();
    updateUIState();
  } catch (err) {
    console.error("Failed to load initial data:", err);
  }
}

function populateScenarioDropdown() {
  const select = document.getElementById("scenarioSelect");
  select.innerHTML = "";
  AppState.scenarios.forEach((s) => {
    const opt = document.createElement("option");
    opt.value = s.scenario_id;
    opt.textContent = `${s.name} (${s.threat_type})`;
    if (s.scenario_id === AppState.state?.scenario?.scenario_id) {
      opt.selected = true;
    }
    select.appendChild(opt);
  });
}

async function refreshState() {
  try {
    const res = await fetch("/api/pathways/state");
    AppState.state = await res.json();
    updateUIState();
  } catch (err) {
    console.error("Failed to refresh state:", err);
  }
}

function updateUIState() {
  if (!AppState.state) return;

  const { pathway, run, scenario, stats } = AppState.state;

  // Header badges
  const ssbaBadge = document.getElementById("threatClassificationBadge");
  const threatTier = run.node_artifacts?.threat_assessment?.ssba_tier || "Tier 1 SSBA";
  ssbaBadge.textContent = threatTier;

  // Pathway summary
  document.getElementById("pathwayNameDisplay").textContent = pathway.name;
  document.getElementById("nodesStatusSummary").textContent = `${stats.completed_nodes} / ${stats.total_nodes} Completed (${run.status.toUpperCase()})`;

  // Badges
  const reportCount = Object.keys(run.node_artifacts?.agency_reports || {}).length;
  document.getElementById("agencyReportCountBadge").textContent = reportCount;
  document.getElementById("thoughtLogCountBadge").textContent = stats.total_thought_logs;

  // Render current tab
  if (AppState.activeTab === "tab-pathway") {
    renderDag();
    renderNodeInspector(AppState.selectedNodeId);
  } else if (AppState.activeTab === "tab-agencies") {
    renderAgencyView();
  } else if (AppState.activeTab === "tab-countermeasures") {
    renderCountermeasures();
  } else if (AppState.activeTab === "tab-agentfeed") {
    renderAgentFeed();
  }
}

// Execution Controls
async function executeStep() {
  try {
    const res = await fetch("/api/execution/step", { method: "POST" });
    const data = await res.json();
    await refreshState();
    if (data.result.status === "approval_required") {
      alert(`Human-in-the-Loop approval required for node: ${data.result.node_label}`);
    }
  } catch (err) {
    console.error("Step execution failed:", err);
  }
}

async function executeRunAll() {
  try {
    const res = await fetch("/api/execution/run", {
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

async function selectScenario(scenarioId) {
  try {
    await fetch(`/api/scenarios/select/${scenarioId}`, { method: "POST" });
    await refreshState();
  } catch (err) {
    console.error("Scenario switch failed:", err);
  }
}

async function switchPathwayTemplate(pathwayKey) {
  try {
    await fetch("/api/pathways/switch", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pathway_key: pathwayKey }),
    });
    await refreshState();
    populateScenarioDropdown();
  } catch (err) {
    console.error("Pathway template switch failed:", err);
  }
}

// Form Handlers
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
        position_x: 600 + Math.random() * 100,
        position_y: 200 + Math.random() * 100,
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
    const res = await fetch("/api/scenarios/custom", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name,
        sample_type,
        source_location,
        raw_payload,
      }),
    });
    const data = await res.json();
    document.getElementById("customSampleModal").classList.add("hidden");
    document.getElementById("customSampleForm").reset();

    // Reload scenarios and state
    const scenRes = await fetch("/api/scenarios").then((r) => r.json());
    AppState.scenarios = scenRes.scenarios || [];
    populateScenarioDropdown();
    await refreshState();
  } catch (err) {
    console.error("Custom specimen submission failed:", err);
  }
}

// ---------------- DAG Graph Visualizer ----------------

function renderDag() {
  const svg = document.getElementById("dagSvg");
  if (!svg || !AppState.state) return;

  const { nodes = [], edges = [] } = AppState.state.pathway;
  const nodeMap = new Map(nodes.map((n) => [n.id, n]));

  svg.innerHTML = `
    <defs>
      <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
        <polygon points="0 0, 10 3.5, 0 7" fill="#475569" />
      </marker>
      <marker id="arrowhead-active" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
        <polygon points="0 0, 10 3.5, 0 7" fill="#38bdf8" />
      </marker>
    </defs>
  `;

  // Draw Edges (Smooth Bezier curves)
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
    svg.appendChild(path);

    // Edge label if present
    if (edge.label) {
      const midX = (x1 + x2) / 2;
      const midY = (y1 + y2) / 2 - 8;
      const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
      text.setAttribute("x", midX);
      text.setAttribute("y", midY);
      text.setAttribute("fill", "#64748b");
      text.setAttribute("font-size", "9px");
      text.setAttribute("text-anchor", "middle");
      text.textContent = edge.label;
      svg.appendChild(text);
    }
  });

  // Draw Nodes
  nodes.forEach((node) => {
    const categoryInfo = CATEGORY_STYLES[node.category] || CATEGORY_STYLES.custom;
    const isSelected = AppState.selectedNodeId === node.id;

    const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
    g.setAttribute("class", `dag-node ${isSelected ? "selected" : ""}`);
    g.setAttribute("transform", `translate(${node.position_x}, ${node.position_y})`);
    g.dataset.nodeId = node.id;

    // Node Box
    const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    rect.setAttribute("width", "190");
    rect.setAttribute("height", "90");
    rect.setAttribute("rx", "10");
    rect.setAttribute("fill", "#0f172a");
    rect.setAttribute("stroke", categoryInfo.color);
    rect.setAttribute("stroke-width", "1.5");
    rect.setAttribute("stroke-opacity", "0.6");
    g.appendChild(rect);

    // Left category color strip
    const strip = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    strip.setAttribute("width", "5");
    strip.setAttribute("height", "90");
    strip.setAttribute("rx", "2");
    strip.setAttribute("fill", categoryInfo.color);
    g.appendChild(strip);

    // Status Indicator Dot / Badge
    let statusColor = "#64748b";
    let statusText = node.status.toUpperCase();
    if (node.status === "completed") statusColor = "#10b981";
    if (node.status === "running") statusColor = "#38bdf8";
    if (node.status === "paused") statusColor = "#f59e0b";
    if (node.status === "failed") statusColor = "#f43f5e";

    // Category Text
    const catText = document.createElementNS("http://www.w3.org/2000/svg", "text");
    catText.setAttribute("x", "16");
    catText.setAttribute("y", "20");
    catText.setAttribute("fill", categoryInfo.color);
    catText.setAttribute("font-size", "9px");
    catText.setAttribute("font-weight", "600");
    catText.setAttribute("text-transform", "uppercase");
    catText.textContent = node.category.replace("_", " ");
    g.appendChild(catText);

    // Status Badge text
    const statusLabel = document.createElementNS("http://www.w3.org/2000/svg", "text");
    statusLabel.setAttribute("x", "175");
    statusLabel.setAttribute("y", "20");
    statusLabel.setAttribute("fill", statusColor);
    statusLabel.setAttribute("font-size", "8px");
    statusLabel.setAttribute("font-weight", "bold");
    statusLabel.setAttribute("text-anchor", "end");
    statusLabel.textContent = statusText;
    g.appendChild(statusLabel);

    // Node Title / Label
    const labelText = document.createElementNS("http://www.w3.org/2000/svg", "text");
    labelText.setAttribute("x", "16");
    labelText.setAttribute("y", "44");
    labelText.setAttribute("fill", "#f8fafc");
    labelText.setAttribute("font-size", "12px");
    labelText.setAttribute("font-weight", "600");
    labelText.textContent = truncateString(node.label, 22);
    g.appendChild(labelText);

    // Subtitle / Agent Team
    const teamText = document.createElementNS("http://www.w3.org/2000/svg", "text");
    teamText.setAttribute("x", "16");
    teamText.setAttribute("y", "62");
    teamText.setAttribute("fill", "#94a3b8");
    teamText.setAttribute("font-size", "10px");
    teamText.textContent = truncateString(node.agent_team_id.replace("_", " "), 24);
    g.appendChild(teamText);

    // Latency or Gatekeeper status bottom
    const bottomText = document.createElementNS("http://www.w3.org/2000/svg", "text");
    bottomText.setAttribute("x", "16");
    bottomText.setAttribute("y", "78");
    bottomText.setAttribute("fill", "#64748b");
    bottomText.setAttribute("font-size", "9px");
    if (node.status === "completed" && node.latency_ms) {
      bottomText.textContent = `⚡ ${node.latency_ms} ms`;
    } else if (node.requires_human_approval) {
      bottomText.textContent = `🛡️ Human Gatekeeper`;
      bottomText.setAttribute("fill", "#f59e0b");
    } else {
      bottomText.textContent = `ID: ${node.id}`;
    }
    g.appendChild(bottomText);

    // Click handler
    g.addEventListener("click", () => {
      AppState.selectedNodeId = node.id;
      renderDag();
      renderNodeInspector(node.id);
    });

    // Simple Drag to Reposition
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
      // Persist node position to backend
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
    container.innerHTML = `<div class="text-slate-500 italic text-center py-12">Click on any node in the pathway to inspect agent configurations, execution outputs, and approval status.</div>`;
    badge.textContent = "SELECT NODE";
    badge.className = "text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-slate-800 text-slate-400";
    return;
  }

  const node = AppState.state.pathway.nodes.find((n) => n.id === nodeId);
  if (!node) return;

  badge.textContent = node.status.toUpperCase();
  let badgeColor = "bg-slate-800 text-slate-400";
  if (node.status === "completed") badgeColor = "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30";
  if (node.status === "running") badgeColor = "bg-cyan-500/20 text-cyan-400 border border-cyan-500/30";
  if (node.status === "paused") badgeColor = "bg-amber-500/20 text-amber-400 border border-amber-500/30";
  badge.className = `text-[10px] font-mono uppercase px-2 py-0.5 rounded ${badgeColor}`;

  let approvalActionHtml = "";
  if (node.status === "paused" && node.requires_human_approval) {
    approvalActionHtml = `
      <div class="bg-amber-950/40 border border-amber-600/40 rounded-lg p-3 space-y-2">
        <div class="text-amber-400 font-semibold flex items-center">
          <i class="fa-solid fa-triangle-exclamation mr-1.5"></i>
          Human-in-the-Loop Signoff Required
        </div>
        <p class="text-slate-300 text-[11px]">This node represents a critical statutory or security checkpoint. Operator authorization is required before continuing.</p>
        <button id="btnApproveNode" class="w-full py-1.5 bg-amber-600 hover:bg-amber-500 text-slate-950 font-bold rounded transition">
          Authorize & Proceed
        </button>
      </div>
    `;
  }

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

      <div>
        <span class="text-slate-500 uppercase font-semibold text-[10px]">Assigned Agent Squad</span>
        <div class="mt-1 bg-slate-950 p-2.5 rounded border border-slate-800 flex items-center space-x-2">
          <i class="fa-solid fa-users-gear text-purple-400"></i>
          <span class="font-medium text-slate-200">${node.agent_team_id.replace("_", " ")}</span>
        </div>
      </div>

      ${approvalActionHtml}

      <div>
        <span class="text-slate-500 uppercase font-semibold text-[10px]">Outputs & Generated Artifacts</span>
        <pre class="mt-1 bg-slate-950 p-2.5 rounded border border-slate-800 font-mono text-[10px] text-cyan-300 overflow-x-auto max-h-48">${
          JSON.stringify(node.outputs, null, 2) || "{}"
        }</pre>
      </div>

      <div class="pt-3 border-t border-slate-800 flex items-center justify-between">
        <button id="btnDeleteNode" class="text-rose-400 hover:text-rose-300 transition flex items-center space-x-1">
          <i class="fa-solid fa-trash-can"></i>
          <span>Delete Node</span>
        </button>
      </div>
    </div>
  `;

  // Attach button events
  const btnApprove = document.getElementById("btnApproveNode");
  if (btnApprove) {
    btnApprove.addEventListener("click", async () => {
      await fetch(`/api/execution/approve/${node.id}`, { method: "POST" });
      await refreshState();
    });
  }

  const btnDelete = document.getElementById("btnDeleteNode");
  if (btnDelete) {
    btnDelete.addEventListener("click", async () => {
      if (confirm(`Are you sure you want to delete node '${node.label}'?`)) {
        await fetch(`/api/pathways/nodes/${node.id}`, { method: "DELETE" });
        AppState.selectedNodeId = null;
        await refreshState();
      }
    });
  }
}

// ---------------- Agency Briefings View ----------------

async function renderAgencyView() {
  const sidebar = document.getElementById("agencySidebarList");
  const card = document.getElementById("agencyBriefingCard");
  if (!sidebar || !card || !AppState.agencies.length) return;

  sidebar.innerHTML = "";
  const reportsMap = AppState.state?.run?.node_artifacts?.agency_reports || {};

  AppState.agencies.forEach((agency) => {
    const isSelected = AppState.selectedAgencyId === agency.id;
    const report = reportsMap[agency.id];
    const isDispatched = report?.dispatched;

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
          isDispatched
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

    sidebar.appendChild(btn);
  });

  // Fetch report for selected agency
  try {
    const repRes = await fetch(`/api/agencies/${AppState.selectedAgencyId}/report`);
    const rep = await repRes.json();
    const agencyProfile = AppState.agencies.find((a) => a.id === AppState.selectedAgencyId);

    let classificationColor = "border-slate-700 text-slate-400";
    if (rep.classification.includes("Sensitive")) classificationColor = "border-amber-500/40 bg-amber-500/10 text-amber-400";
    if (rep.classification.includes("SECRET")) classificationColor = "border-rose-500/40 bg-rose-500/10 text-rose-400";

    card.innerHTML = `
      <!-- Briefing Header -->
      <div class="border-b border-slate-800 pb-5 space-y-3">
        <div class="flex items-center justify-between">
          <span class="px-2.5 py-0.5 rounded text-[11px] font-mono font-bold tracking-wider uppercase border ${classificationColor}">
            ${rep.classification}
          </span>
          <div class="flex items-center space-x-2">
            <span class="px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase bg-rose-500/20 text-rose-300 border border-rose-500/30">
              URGENCY: ${rep.urgency}
            </span>
            <span class="text-slate-500 font-mono text-xs">${rep.report_id}</span>
          </div>
        </div>

        <div>
          <h2 class="text-xl font-bold text-white tracking-tight">${rep.title}</h2>
          <div class="text-xs text-slate-400 mt-1 flex items-center space-x-2">
            <span><strong>Portfolio:</strong> ${agencyProfile?.portfolio || "Australian Government"}</span>
            <span class="text-slate-600">•</span>
            <span><strong>Statutory Authority:</strong> ${agencyProfile?.statutory_authority || "Commonwealth Acts"}</span>
          </div>
        </div>

        <div class="flex items-center justify-between pt-1">
          <div class="text-[11px] text-slate-400">
            <strong>Generated:</strong> ${rep.generated_at}
          </div>
          <div class="flex items-center space-x-2">
            <a href="/api/agencies/${rep.agency_id}/export/markdown" target="_blank" class="px-3 py-1 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded text-xs transition flex items-center space-x-1">
              <i class="fa-solid fa-download text-cyan-400"></i>
              <span>Export Markdown</span>
            </a>
            <button id="btnDispatchSingle" class="px-3.5 py-1 bg-emerald-600 hover:bg-emerald-500 text-white rounded text-xs font-semibold transition flex items-center space-x-1 shadow">
              <i class="fa-solid fa-paper-plane"></i>
              <span>${rep.dispatched ? "Re-Dispatch" : "Dispatch to " + rep.agency_id}</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Executive Summary -->
      <div class="space-y-2">
        <h4 class="text-xs font-bold text-cyan-400 uppercase tracking-wider flex items-center">
          <i class="fa-solid fa-flag text-cyan-400 mr-2"></i>
          Executive Summary
        </h4>
        <div class="bg-slate-950 p-4 rounded-lg border border-slate-800/80 text-xs text-slate-200 leading-relaxed font-sans">
          ${rep.executive_summary}
        </div>
      </div>

      <!-- Situation Update -->
      <div class="space-y-2">
        <h4 class="text-xs font-bold text-blue-400 uppercase tracking-wider flex items-center">
          <i class="fa-solid fa-circle-info mr-2"></i>
          Incident Situation Update
        </h4>
        <div class="bg-slate-950 p-4 rounded-lg border border-slate-800/80 text-xs text-slate-300 leading-relaxed">
          ${rep.situation_update}
        </div>
      </div>

      <!-- Strategic Implications -->
      <div class="space-y-2">
        <h4 class="text-xs font-bold text-purple-400 uppercase tracking-wider flex items-center">
          <i class="fa-solid fa-chart-line mr-2"></i>
          Strategic Implications for Australian Preparedness
        </h4>
        <ul class="space-y-1.5 text-xs text-slate-300 bg-slate-950 p-4 rounded-lg border border-slate-800/80">
          ${rep.strategic_implications.map((item) => `<li class="flex items-start"><i class="fa-solid fa-chevron-right text-purple-400 text-[10px] mt-1 mr-2 shrink-0"></i><span>${item}</span></li>`).join("")}
        </ul>
      </div>

      <!-- Operational Action Items -->
      <div class="space-y-2">
        <h4 class="text-xs font-bold text-emerald-400 uppercase tracking-wider flex items-center">
          <i class="fa-solid fa-list-check mr-2"></i>
          Mandated Operational Actions
        </h4>
        <ol class="space-y-2 text-xs text-slate-300 bg-slate-950 p-4 rounded-lg border border-slate-800/80 list-decimal list-inside">
          ${rep.action_items_required.map((item) => `<li class="leading-relaxed"><span class="text-slate-100 font-medium">${item}</span></li>`).join("")}
        </ol>
      </div>

      <!-- Cross Agency Dependencies -->
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
  for (const agency of AppState.agencies) {
    await fetch(`/api/agencies/${agency.id}/dispatch`, { method: "POST" });
  }
  await refreshState();
  renderAgencyView();
  alert("All Australian Whole-of-Government situation briefs have been securely dispatched.");
}

// ---------------- Countermeasures & Intelligence View ----------------

function renderCountermeasures() {
  const artifacts = AppState.state?.run?.node_artifacts || {};
  const targets = artifacts.protein_targets || [];
  const drugs = artifacts.drug_candidates || [];
  const vaccines = artifacts.vaccine_candidates || [];

  // 1. Protein Targets Grid
  const targetGrid = document.getElementById("proteinTargetsGrid");
  if (!targets.length) {
    targetGrid.innerHTML = `<div class="col-span-3 text-slate-500 italic p-4 bg-slate-900/50 rounded-lg border border-slate-800 text-center">Execute the Response Pathway to resolve macromolecular protein targets.</div>`;
  } else {
    targetGrid.innerHTML = targets
      .map(
        (t) => `
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-3 shadow-md">
        <div class="flex items-start justify-between">
          <div>
            <span class="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-purple-500/10 text-purple-400 border border-purple-500/20">${t.gene_symbol || "Target"}</span>
            <h4 class="font-bold text-slate-100 text-xs mt-1">${t.name}</h4>
          </div>
          <span class="text-xs font-mono font-semibold text-emerald-400">${t.plddt_confidence}% pLDDT</span>
        </div>
        <p class="text-slate-400 text-[11px] line-clamp-2">${t.function_summary}</p>
        <div class="pt-2 border-t border-slate-800/80 flex items-center justify-between text-[10px] text-slate-400 font-mono">
          <span>Active Pocket: ${t.pocket_volume_angstrom3 || "N/A"} Å³</span>
          <span class="text-cyan-400">Druggability: ${t.druggability_score || "N/A"}</span>
        </div>
      </div>
    `
      )
      .join("");
  }

  // 2. Therapeutics Table
  const tbody = document.getElementById("therapeuticsTableBody");
  if (!drugs.length) {
    tbody.innerHTML = `<tr><td colspan="6" class="px-4 py-8 text-center text-slate-500 italic">No therapeutic docking candidates resolved yet. Run the Therapeutics node to generate candidates.</td></tr>`;
  } else {
    tbody.innerHTML = drugs
      .map(
        (d) => `
      <tr class="hover:bg-slate-800/40 transition">
        <td class="px-4 py-3 font-semibold text-slate-100">${d.name}</td>
        <td class="px-4 py-3 text-slate-300 max-w-xs truncate">${d.mechanism_of_action}</td>
        <td class="px-4 py-3 font-mono font-bold text-emerald-400">${d.binding_affinity_kcal_mol} kcal/mol</td>
        <td class="px-4 py-3">
          <span class="px-2 py-0.5 rounded text-[10px] font-medium bg-blue-500/10 text-blue-300 border border-blue-500/20">
            ${d.tga_artg_status}
          </span>
        </td>
        <td class="px-4 py-3 text-slate-400">${d.australian_stockpile_status}</td>
        <td class="px-4 py-3">
          <span class="text-cyan-400 font-mono text-[10px]">${d.clinical_evidence_tier}</span>
        </td>
      </tr>
    `
      )
      .join("");
  }

  // 3. Vaccine Candidates Grid
  const vacGrid = document.getElementById("vaccineCandidatesGrid");
  if (!vaccines.length) {
    vacGrid.innerHTML = `<div class="col-span-2 text-slate-500 italic p-4 bg-slate-900/50 rounded-lg border border-slate-800 text-center">Execute the Vaccinology node to generate candidate antigen designs.</div>`;
  } else {
    vacGrid.innerHTML = vaccines
      .map(
        (v) => `
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4 shadow-md">
        <div class="flex items-center justify-between">
          <span class="px-2.5 py-0.5 rounded text-[10px] font-mono font-bold bg-amber-500/10 text-amber-400 border border-amber-500/20">
            ${v.platform}
          </span>
          <span class="text-[11px] font-medium text-emerald-400">${v.predicted_neutralization_titer}</span>
        </div>
        <div>
          <h4 class="font-bold text-sm text-slate-100">${v.target_antigen}</h4>
          <p class="text-xs text-slate-400 mt-1">${v.formulation_details}</p>
        </div>
        <div class="bg-slate-950 p-3 rounded-lg border border-slate-800 space-y-1 text-[11px]">
          <div class="text-slate-400 font-medium">Domestic Manufacturing Facility:</div>
          <div class="text-cyan-300 font-mono">${v.local_manufacturing_capability}</div>
        </div>
      </div>
    `
      )
      .join("");
  }
}

// ---------------- Agent Thought Feed View ----------------

function renderAgentFeed() {
  const container = document.getElementById("agentThoughtFeedList");
  const countBadge = document.getElementById("feedLogsCount");
  if (!container || !AppState.state) return;

  const logs = AppState.state.run?.thought_logs || [];
  countBadge.textContent = `${logs.length} deliberation steps`;

  if (!logs.length) {
    container.innerHTML = `<div class="text-center text-slate-500 italic py-16">No agent deliberation logs yet. Click 'Step' or 'Execute Pathway' to trigger agent reasoning squads.</div>`;
    return;
  }

  container.innerHTML = logs
    .slice()
    .reverse()
    .map((log) => {
      let phaseColor = "bg-slate-800 text-slate-400 border-slate-700";
      if (log.phase === "observation") phaseColor = "bg-blue-500/10 text-blue-400 border-blue-500/30";
      if (log.phase === "hypothesis") phaseColor = "bg-purple-500/10 text-purple-400 border-purple-500/30";
      if (log.phase === "tool_execution") phaseColor = "bg-cyan-500/10 text-cyan-400 border-cyan-500/30";
      if (log.phase === "synthesis") phaseColor = "bg-emerald-500/10 text-emerald-400 border-emerald-500/30";

      return `
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-2.5 shadow-sm">
        <div class="flex items-center justify-between text-xs">
          <div class="flex items-center space-x-2.5">
            <div class="w-7 h-7 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-cyan-400 font-bold text-xs">
              ${log.agent_name.charAt(0)}
            </div>
            <div>
              <span class="font-bold text-slate-100">${log.agent_name}</span>
              <span class="text-slate-500 text-[11px] ml-1.5">• ${log.agent_role}</span>
            </div>
          </div>
          <div class="flex items-center space-x-2">
            <span class="px-2 py-0.5 rounded text-[9px] font-mono uppercase font-bold border ${phaseColor}">
              ${log.phase}
            </span>
            <span class="text-[10px] text-slate-500 font-mono">${log.timestamp.split("T")[1]?.slice(0, 8) || ""}</span>
          </div>
        </div>

        <div class="text-xs text-slate-300 leading-relaxed font-sans pl-9">
          ${log.message}
        </div>

        ${
          log.tool_name
            ? `
          <div class="ml-9 bg-slate-950 p-2.5 rounded-lg border border-slate-800/80 text-[11px] font-mono space-y-1">
            <div class="text-cyan-400 font-semibold flex items-center">
              <i class="fa-solid fa-wrench mr-1.5 text-[10px]"></i>
              Tool Call: ${log.tool_name}
            </div>
            ${log.tool_output_summary ? `<div class="text-slate-400 text-[10px]">Result: ${log.tool_output_summary}</div>` : ""}
          </div>
        `
            : ""
        }
      </div>
    `;
    })
    .join("");
}

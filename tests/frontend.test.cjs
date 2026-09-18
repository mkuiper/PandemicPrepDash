// Run with: node --test tests/frontend.test.cjs
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');

function loadApp() {
  const elements = new Map();
  const context = vm.createContext({
    localStorage: { getItem: () => null },
    document: {
      addEventListener() {},
      querySelectorAll() { return []; },
      getElementById(id) {
        if (!elements.has(id)) elements.set(id, { innerHTML: '', textContent: '', classList: { add() {}, remove() {} } });
        return elements.get(id);
      },
    },
  });
  vm.runInContext(fs.readFileSync(path.join(__dirname, '../static/app.js'), 'utf8'), context);
  return { context, elements };
}

test('hub renders untrusted message text without HTML injection', () => {
  const { context, elements } = loadApp();
  vm.runInContext(`
    AppState.state = { data_hub: { messages: [{
      sender_name: '<img src=x onerror=alert(1)>', sender_role: '<svg onload=alert(1)>',
      content: '<script>alert(1)</script>', target_node_id: '<b>target</b>'
    }] } };
    renderCentralDataHub();
  `, context);
  const html = elements.get('hubMessagesFeed').innerHTML;
  assert.ok(html.includes('&lt;script&gt;alert(1)&lt;/script&gt;'));
  assert.ok(html.includes('&lt;img'));
  assert.ok(html.includes('&lt;svg'));
  assert.ok(!html.includes('<script>'));
  assert.ok(!html.includes('<img'));
});

test('markdown escapes HTML and does not create javascript links', () => {
  const { context } = loadApp();
  const html = vm.runInContext('formatMarkdownToHtml(\'<img src=x onerror=alert(1)> [bad](javascript:alert(1)) [good](https://example.com)\')', context);
  assert.ok(!html.includes('<img'));
  assert.ok(!html.includes('href="javascript:'));
  assert.ok(html.includes('href="https://example.com"'));
});

test('hub escapes specimen, blocker, and literature fields', () => {
  const { context, elements } = loadApp();
  vm.runInContext(`
    AppState.state = {
      scenario: { threat_type: 'severe_weather' },
      pathway: { threat_type: 'severe_weather' },
      data_hub: {
        messages: [],
        blockers: [{
          alert_id: 'blk-1', status: 'OPEN', severity: 'HIGH',
          title: '<img src=x onerror=alert(1)>',
          description: '<script>alert(1)</script>',
          required_action: '<b>act</b>'
        }],
        specimen_intel: {
          name: '<img src=x onerror=alert(1)>',
          source_location: '<svg onload=alert(1)>',
          metadata: { warning_level: '<iframe>', windsor_gauge_m: '16.8' }
        },
        literature_research: [{
          title: '<img src=x onerror=alert(1)>',
          source_url: 'javascript:alert(1)',
          authors: '<b>bad</b>', journal: 'J', year: '2026', summary: '<script>x</script>'
        }]
      }
    };
    renderCentralDataHub();
  `, context);
  const intel = elements.get('hubSpecimenIntelContent').innerHTML;
  const blockers = elements.get('dataHubBlockersList').innerHTML;
  const lit = elements.get('hubLiteratureContent').innerHTML;
  assert.ok(intel.includes('&lt;img'));
  assert.ok(!intel.includes('<img'));
  assert.ok(blockers.includes('&lt;script&gt;'));
  assert.ok(!blockers.includes('<script>'));
  assert.ok(!lit.includes('href="javascript:'));
  assert.ok(lit.includes('&lt;img'));
});

test('lab list and playbooks escape titles', async () => {
  const { context, elements } = loadApp();
  context.fetch = async (url) => {
    if (String(url).includes('lab-bridge')) {
      return {
        ok: true,
        json: async () => ({
          requests: [{
            request_id: 'REQ-1', status: 'PROPOSED_BY_AGENT', priority: 'HIGH',
            title: '<img src=x onerror=alert(1)>', target_facility: 'BOM <b>x</b>',
            biosafety_level: '<svg>', originating_node_id: '<i>n</i>',
            estimated_turnaround_hours: 4, critical_question: '<script>alert(1)</script>',
            hypothesis_to_test: '<b>h</b>', specimen_requirements: '<img>',
            results_payload: {},
          }],
        }),
      };
    }
    return {
      ok: true,
      json: async () => ({
        templates: [{
          id: 't1', playbook_title: '<img src=x onerror=alert(1)>',
          scenario_scope: '<script>x</script>', trigger_criteria: '<b>t</b>',
          lead_agency: '<svg>', node_count: 1, edge_count: 0,
          threat_type: 'severe_weather', is_builtin: true,
        }],
      }),
    };
  };
  await vm.runInContext('renderLabBridgeView()', context);
  const labHtml = elements.get('labBridgeRequestsList').innerHTML;
  assert.ok(labHtml.includes('&lt;img'));
  assert.ok(!labHtml.includes('<img'));
  assert.ok(labHtml.includes('&lt;script&gt;'));

  await vm.runInContext('openTemplatesManager()', context);
  const playbookHtml = elements.get('templatesListContainer').innerHTML;
  assert.ok(playbookHtml.includes('&lt;img'));
  assert.ok(!playbookHtml.includes('<img src=x'));
});

test('inspector does not invent CBRN artifacts on a factory fire', () => {
  const { context, elements } = loadApp();
  vm.runInContext(`
    AppState.state = {
      scenario: { threat_type: 'industrial_fire', sample: { sample_type: 'SITREP_TEXT', name: 'Fire', source_location: 'Erskine Park', raw_payload: 'SIMULATED sitrep styrene' } },
      pathway: { threat_type: 'industrial_fire' },
      run: { node_artifacts: { adjacent_sites: [{ name: 'Tank farm', inventory_status: 'unknown', bearing: 'SSW', occupancy: 'liquids', note: 'unconfirmed' }] }, event_log: [] },
      data_hub: {}
    };
    AppState.activeInspectorSubtab = 'tool-sitrep';
    renderPipelineDataInspector();
  `, context);
  assert.ok(elements.get('inspectSitrepText').textContent.includes('SIMULATED'));
  vm.runInContext(`AppState.activeInspectorSubtab = 'tool-adjacent'; renderPipelineDataInspector();`, context);
  const adj = elements.get('inspectAdjacentList').innerHTML;
  assert.ok(adj.includes('Tank farm'));
  assert.ok(!adj.includes('<img'));
  vm.runInContext(`
    AppState.state.scenario.threat_type = 'biological_virus';
    AppState.state.pathway.threat_type = 'biological_virus';
    AppState.state.run.node_artifacts = {};
    AppState.activeInspectorSubtab = 'tool-chemical';
    renderPipelineDataInspector();
  `, context);
  assert.equal(elements.get('inspectChemName').textContent, 'Not produced');
  assert.ok(!String(elements.get('inspectChemArtg').textContent).includes('Oseltamivir'));
});

test('Execute Pathway preserves human approval gates and reports pause', async () => {
  const { context } = loadApp();
  const alerts = [];
  let request;
  context.fetch = async (url, options) => {
    request = { url, options };
    return { ok: true, json: async () => ({ result: { status: 'approval_required', node_label: 'Review' } }) };
  };
  context.alert = text => alerts.push(text);
  vm.runInContext('refreshState = async () => {}', context);
  await vm.runInContext('executeRunAll()', context);
  assert.equal(request.url, '/api/execution/run');
  assert.equal(JSON.parse(request.options.body).auto_approve, false);
  assert.deepEqual(alerts, ['Authorization required for: Review']);
});

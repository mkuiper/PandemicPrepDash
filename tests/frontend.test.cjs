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

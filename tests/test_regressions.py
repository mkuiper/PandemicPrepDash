"""Behavioral regressions found during the incident-dashboard review."""
import pytest
from fastapi.testclient import TestClient
from pandemic_prep_dash.main import app
from pandemic_prep_dash.core.engine import PathwayExecutionEngine
from pandemic_prep_dash.core.registry import create_default_biological_pathway
from pandemic_prep_dash.core.state_manager import StateManager
from pandemic_prep_dash.core.harness import NodeAgenticHarness
from pandemic_prep_dash.models.pathway import PathwayEdge, NodeStatus, RunStatus
from pandemic_prep_dash.scenarios import get_scenario


def test_radiological_playbook_selects_matching_data():
    with TestClient(app) as client:
        response = client.post('/api/pathways/templates/load/pathway_default_radiological')
        assert response.status_code == 200
        state = client.get('/api/pathways/state').json()
    assert state['run']['scenario_id'] == 'scen_radiological_cesium137'
    assert state['scenario']['threat_type'] == 'radiological_dispersal'


def test_hub_retains_drugs_and_vaccines():
    engine = StateManager.get_engine()
    assert engine.execute_all(auto_approve=True)['status'] == 'completed'
    artifacts = engine.run.node_artifacts
    assert engine.data_hub.countermeasures == artifacts['drug_candidates'] + artifacts['vaccine_candidates']


@pytest.mark.parametrize('missing', ['source', 'target'])
def test_invalid_edge_rejected_without_mutation(missing):
    engine = StateManager.get_engine()
    before = engine.pathway.model_dump()
    endpoints = dict(source=engine.pathway.nodes[0].id, target=engine.pathway.nodes[-1].id)
    endpoints[missing] = 'missing-node'
    with pytest.raises(ValueError, match='exist'):
        engine.add_edge(PathwayEdge(id='invalid', **endpoints))
    assert engine.pathway.model_dump() == before


def test_invalid_scenario_does_not_mutate_active_run():
    engine = StateManager.get_engine()
    before = engine.get_full_state()
    with pytest.raises(KeyError):
        engine.set_scenario('missing')
    assert engine.get_full_state() == before
    assert engine.scenario_id == before['run']['scenario_id']


def test_execution_does_not_mutate_scenario_catalog():
    engine = StateManager.get_engine()
    before = get_scenario(engine.scenario_id)['sample'].copy()
    engine.execute_next_step()
    assert get_scenario(engine.scenario_id)['sample'] == before


def test_execution_failure_is_not_reported_as_completion(monkeypatch):
    engine = StateManager.get_engine()
    def fail(*args, **kwargs):
        raise RuntimeError('test connector unavailable')
    monkeypatch.setattr(NodeAgenticHarness, 'run', fail)
    result = engine.execute_all()
    assert result['status'] == 'failed'
    assert engine.run.status == RunStatus.FAILED
    assert engine.pathway.nodes[0].status == NodeStatus.FAILED
    assert engine.pathway.nodes[0].error_message == 'test connector unavailable'
    assert engine.run.completed_node_ids == []
    assert not engine.run.node_artifacts


@pytest.mark.parametrize('corruption', ['duplicate_node', 'missing_endpoint', 'cycle'])
def test_bad_import_preserves_existing_workflow(corruption):
    with TestClient(app) as client:
        before = client.get('/api/pathways/state').json()
        data = create_default_biological_pathway().model_dump(mode='json')
        if corruption == 'duplicate_node':
            data['nodes'].append(data['nodes'][0])
        else:
            source = 'missing' if corruption == 'missing_endpoint' else data['nodes'][-1]['id']
            data['edges'].append(dict(id='bad', source=source, target=data['nodes'][0]['id']))
        assert client.post('/api/pathways/import/json', json=data).status_code == 400
        assert client.get('/api/pathways/state').json() == before


def test_run_can_auto_approve_an_already_paused_gate():
    engine = StateManager.get_engine()
    assert engine.execute_all()['status'] == 'approval_required'
    assert engine.execute_all(auto_approve=True)['status'] == 'completed'
    assert len(set(engine.run.completed_node_ids)) == len(engine.pathway.nodes)


def test_imported_completion_and_approvals_are_reset():
    engine = StateManager.get_engine()
    engine.execute_all(auto_approve=True)
    imported = PathwayExecutionEngine(engine.pathway.model_copy(deep=True))
    assert all(n.status == NodeStatus.PENDING and not n.outputs for n in imported.pathway.nodes)
    assert all(not n.approval_granted for n in imported.pathway.nodes if n.requires_human_approval)
    assert imported.execute_all()['status'] == 'approval_required'


def test_snapshots_only_record_real_actions_and_reset_with_run():
    with TestClient(app) as client:
        assert client.get('/api/version-control/snapshots').json()['snapshots'] == []
        client.post('/api/execution/step').raise_for_status()
        response = client.post('/api/version-control/snapshots', json={
            'checkpoint_name': 'Ingestion complete', 'change_summary': 'Operator checkpoint'})
        snapshot = response.json()['snapshot']
        assert snapshot['completed_nodes_count'] == 1
        assert snapshot['dispatched_assays_count'] == 0
        client.post('/api/execution/reset').raise_for_status()
        assert client.get('/api/version-control/snapshots').json()['snapshots'] == []
        assert client.get('/api/version-control/snapshots/' + snapshot['version_id']).status_code == 404


def test_snapshot_return_value_cannot_mutate_stored_checkpoint():
    from pandemic_prep_dash.core.version_control import VersionControlManager
    snapshot = VersionControlManager.capture_snapshot(
        'test', 'MANUAL', 'tester', 0, 8, 0, 0, 'test', {'nested': {'value': 1}})
    snapshot.node_artifacts_preview['nested']['value'] = 2
    listed = VersionControlManager.list_snapshots()
    listed[0].checkpoint_name = 'tampered'
    stored = VersionControlManager.get_snapshot(snapshot.version_id)
    assert stored.checkpoint_name == 'test'
    assert stored.node_artifacts_preview == {'nested': {'value': 1}}


@pytest.mark.parametrize('template_id', ['../outside', '/tmp/outside', '..\\outside'])
def test_template_paths_cannot_escape_storage(template_id):
    from pandemic_prep_dash.core.templates import TemplateManager
    with pytest.raises(KeyError):
        TemplateManager.get_template(template_id)
    assert TemplateManager.delete_template(template_id) is False


def test_long_workflow_is_not_silently_truncated():
    from pandemic_prep_dash.models.pathway import Pathway, PathwayNode, NodeCategory
    nodes = [PathwayNode(id=str(i), label=str(i), description='Demo step', category=NodeCategory.CUSTOM)
             for i in range(55)]
    edges = [PathwayEdge(id=str(i), source=str(i), target=str(i+1)) for i in range(54)]
    engine = PathwayExecutionEngine(Pathway(id='long', name='Long', description='Test', nodes=nodes, edges=edges))
    assert engine.execute_all()['status'] == 'completed'
    assert engine.run.completed_node_ids == [str(i) for i in range(55)]


def test_invalid_governance_update_is_rejected_atomically():
    with TestClient(app) as client:
        before = client.get('/api/governance/settings').json()
        assert client.post('/api/governance/settings', json={'classification': 'NOT_A_CLASSIFICATION'}).status_code == 422
        assert client.get('/api/governance/settings').json() == before
        result = client.post('/api/governance/settings', json={'compute': {'gpu_count': 2}})
        assert result.status_code == 200
        compute = result.json()['settings']['compute']
        assert compute['gpu_count'] == 2
        assert compute['cluster_endpoint'] == before['settings']['compute']['cluster_endpoint']


def test_demo_does_not_claim_verified_security_or_connected_keys():
    with TestClient(app) as client:
        settings = client.get('/api/governance/settings').json()['settings']
        assert settings['compliance']['ism_controls_verified'] is False
        assert settings['api_keys']['llm_api_key_set'] is False
        assert settings['api_keys']['ncbi_api_key_set'] is False
        page = client.get('/').text
        assert 'CBRN Rapid Response' in page
        assert 'Demonstration mode' in page
        assert 'All MCP Endpoints Active' not in page
        assert 'Accreditation: none' in page
        assert 'NOT IMPLEMENTED' in page

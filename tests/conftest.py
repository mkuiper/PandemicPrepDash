import sys
from pathlib import Path

# Ensure src directory is on sys.path for test runner
src_dir = Path(__file__).resolve().parent.parent / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

import copy
import urllib.request
import pytest


@pytest.fixture(autouse=True)
def isolate_demo_state(monkeypatch, tmp_path):
    """No shared sessions, user files, or live services in the test suite."""
    from pandemic_prep_dash.core.state_manager import StateManager
    from pandemic_prep_dash.core import templates
    from pandemic_prep_dash.core.lab_bridge import LabBridgeManager
    from pandemic_prep_dash.core.academy import AcademyManager
    from pandemic_prep_dash.core.version_control import VersionControlManager
    from pandemic_prep_dash.api import routes_governance
    from pandemic_prep_dash.models.governance import GovernanceSettings
    from pandemic_prep_dash import scenarios

    monkeypatch.setattr(StateManager, "_engine", None)
    monkeypatch.setattr(templates, "TEMPLATES_DIR", tmp_path)
    monkeypatch.setattr(LabBridgeManager, "_REQUESTS", {})
    monkeypatch.setattr(AcademyManager, "_RECORDS", {})
    monkeypatch.setattr(VersionControlManager, "_TIMELINE", [])
    monkeypatch.setattr(VersionControlManager, "_RUN_ID", None)
    monkeypatch.setattr(routes_governance, "CURRENT_GOVERNANCE_SETTINGS", GovernanceSettings())
    # Keep imported registry references intact while restoring nested mutations.
    original = copy.deepcopy(scenarios.SCENARIO_REGISTRY)
    def offline(*args, **kwargs):
        raise OSError("Live HTTP disabled in tests")
    monkeypatch.setattr(urllib.request, "urlopen", offline)
    yield
    scenarios.SCENARIO_REGISTRY.clear()
    scenarios.SCENARIO_REGISTRY.update(original)

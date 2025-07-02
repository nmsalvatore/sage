import os
import pytest


@pytest.fixture
def isolated_sage_config(tmp_path, monkeypatch):
    """Isolate sage config to a temporary directory for this test."""
    monkeypatch.setenv('XDG_CONFIG_HOME', str(tmp_path))
    return tmp_path

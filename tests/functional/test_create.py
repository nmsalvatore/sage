import os
import subprocess


def test_create_preset(tmp_path):
    """
    Test preset creation.
    """
    env = os.environ.copy()
    env["HOME"] = str(tmp_path)

    result = subprocess.run(
        ["sage", "create", "rice", "15m"],
        capture_output=True,
        text=True,
        timeout=5,
        env=env,
    )
    assert result.returncode == 0
    assert "success" in result.stdout.lower()
    assert "rice" in result.stdout

    # Preset should show up in list of presets.
    result = subprocess.run(
        ["sage", "list"], capture_output=True, text=True, timeout=5, env=env
    )
    assert "rice" in result.stdout.lower()
    assert "15 minutes" in result.stdout.lower()


def test_create_preset_duplicate_name(tmp_path):
    """
    Test preset creation with existing preset name.
    """
    env = os.environ.copy()
    env["HOME"] = str(tmp_path)

    result = subprocess.run(
        ["sage", "create", "pomodoro", "45m"],
        capture_output=True,
        text=True,
        timeout=5,
        env=env,
    )
    assert result.returncode == 1
    assert "already a preset" in result.stderr.lower()


def test_create_preset_without_duration(tmp_path):
    """
    Test preset creation without duration argument.
    """
    env = os.environ.copy()
    env["HOME"] = str(tmp_path)

    result = subprocess.run(
        ["sage", "create", "nothing"],
        capture_output=True,
        text=True,
        timeout=5,
        env=env,
    )
    assert result.returncode == 2
    assert "missing argument" in result.stderr.lower()

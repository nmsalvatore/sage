import os
import subprocess


def test_update(tmp_path):
    """
    Test preset duration update.
    """
    env = os.environ.copy()
    env["HOME"] = str(tmp_path)

    result = subprocess.run(
        ["sage", "update", "pomodoro", "30m"],
        capture_output=True,
        text=True,
        timeout=5,
        env=env,
    )

    assert result.returncode == 0
    assert "success" in result.stdout.lower()


def test_update_preset_that_doesnt_exist(tmp_path):
    """
    Test preset duration update on nonexistent preset.
    """
    env = os.environ.copy()
    env["HOME"] = str(tmp_path)

    result = subprocess.run(
        ["sage", "update", "pootietang", "37m"],
        capture_output=True,
        text=True,
        timeout=5,
        env=env,
    )

    assert result.returncode == 1
    assert "not a preset" in result.stderr.lower()

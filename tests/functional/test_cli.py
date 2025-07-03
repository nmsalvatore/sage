import os
import subprocess


def test_version():
    """
    To check that sage is installed correctly, a user uses the `sage
    --version` command.
    """
    result = subprocess.run(
        ["sage", "--version"], capture_output=True, text=True, timeout=5
    )

    assert "version" in result.stdout


def test_help():
    """
    To get familiar with basic sage usage, a user uses the `sage
    --help` command.
    """
    result = subprocess.run(
        ["sage", "--help"], capture_output=True, text=True, timeout=5
    )

    assert all(
        option in result.stdout
        for option in ["--version", "--help", "timer", "stopwatch"]
    )


def test_timer_help():
    """
    Now familiar with the basic sage commands, the user checks to see how
    to use the timer command with `sage timer --help`.
    """
    result = subprocess.run(
        ["sage", "timer", "--help"], capture_output=True, text=True, timeout=5
    )

    assert all(
        option in result.stdout
        for option in ["--hours", "--minutes", "--seconds", "-h", "-m", "-s"]
    )


def test_timer_accepts_options():
    """
    Check that `sage timer` accepts option arguments.
    """
    result = subprocess.run(
        ["sage", "timer", "-s", "5", "--test"],
        capture_output=True,
        text=True,
        timeout=5,
    )

    assert result.returncode == 0
    assert "00:00:05" in result.stdout


def test_timer_accepts_human_readable_strings():
    """
    Check that 'sage timer` accepts human-readable strings so that
    users don't have to think like robots.
    """
    result = subprocess.run(
        ["sage", "timer", "25m", "--test"], capture_output=True, text=True, timeout=5
    )

    assert result.returncode == 0
    assert "00:25:00" in result.stdout


def test_pomodoro_timer():
    """
    Having read the README, the user remembers that sage offers custom
    timers, one of which is the included pomodoro timer. They load the
    pomodoro timer to see what the custom timers are all about.
    """
    result = subprocess.run(
        ["sage", "timer", "pomodoro", "--test"],
        capture_output=True,
        text=True,
        timeout=5,
    )

    assert result.returncode == 0
    assert "00:25:00" in result.stdout


def test_list_saved_timers():
    """
    The pomodoro timer works! Are there any other timers hiding? Our
    user goes to find out with `sage timers`.
    """
    result = subprocess.run(
        ["sage", "timers"], capture_output=True, text=True, timeout=5
    )

    assert result.returncode == 0
    assert "pomodoro" in result.stdout
    assert "johncage" in result.stdout
    assert "potato" in result.stdout
    assert "pika" in result.stdout


def test_create_timer_with_time_string(tmp_path):
    """
    Time to create a timer and see what this custom stuff is all about.
    We'll use a time string first for convenience.
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

    result = subprocess.run(
        ["sage", "timers"], capture_output=True, text=True, timeout=5, env=env
    )

    assert "rice" in result.stdout
    assert "15 minutes" in result.stdout


def test_create_timer_with_options(tmp_path):
    """
    Now let's see if we can create a timer using option flags.
    """
    env = os.environ.copy()
    env["HOME"] = str(tmp_path)

    result = subprocess.run(
        ["sage", "create", "titanic", "--minutes", "14", "--hours", "3"],
        capture_output=True,
        text=True,
        timeout=5,
        env=env,
    )

    assert result.returncode == 0
    assert "success" in result.stdout.lower()
    assert "titanic" in result.stdout

    result = subprocess.run(
        ["sage", "timers"], capture_output=True, text=True, timeout=5, env=env
    )

    assert "titanic" in result.stdout
    assert "3 hours 14 minutes" in result.stdout


def test_delete_timer(tmp_path):
    """
    Ok, that's pretty cool, but our user doesn't really need a Titanic
    timer. They use `sage delete titanic' to delete the custom timer.
    """
    env = os.environ.copy()
    env["HOME"] = str(tmp_path)

    result = subprocess.run(
        ["sage", "create", "titanic", "3 hours 14 minutes"],
        capture_output=True,
        text=True,
        timeout=5,
        env=env,
    )

    assert result.returncode == 0
    assert "success" in result.stdout.lower()
    assert "titanic" in result.stdout.lower()

    result = subprocess.run(
        ["sage", "timers"], capture_output=True, text=True, timeout=5, env=env
    )

    assert result.returncode == 0
    assert "titanic" in result.stdout

    result = subprocess.run(
        ["sage", "delete", "titanic"],
        capture_output=True,
        text=True,
        timeout=5,
        env=env,
    )

    assert result.returncode == 0
    assert "success" in result.stdout.lower()
    assert "deleted" in result.stdout.lower()

    result = subprocess.run(
        ["sage", "timers"],
        capture_output=True,
        text=True,
        timeout=5,
        env=env,
    )

    assert result.returncode == 0
    assert "titanic" not in result.stdout.lower()

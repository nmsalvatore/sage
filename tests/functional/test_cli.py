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
        ["sage", "timer", "-s", "5", "--test"], capture_output=True, text=True, timeout=5
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
        ["sage", "timer", "pomodoro", "--test"], capture_output=True, text=True, timeout=5
    )

    assert result.returncode == 0
    assert "00:25:00" in result.stdout


def test_list_saved_timers():
    """
    The pomodoro timer works! Are there any other timers hiding? Our
    user goes to find out with `sage timers`.
    """
    result = subprocess.run(
        ["sage", "timer", "list"], capture_output=True, text=True, timeout=5
    )

    assert result.returncode == 0
    assert "pomodoro" in result.stdout
    assert "johncage" in result.stdout
    assert "potato" in result.stdout

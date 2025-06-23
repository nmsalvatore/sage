import subprocess


def test_version():
    """
    To check that fizz is installed correctly, a user uses the `fizz
    --version` command.
    """
    result = subprocess.run(
        ["fizz", "--version"], capture_output=True, text=True, timeout=5
    )

    assert "version" in result.stdout


def test_help():
    """
    To get familiar with basic fizz usage, a user uses the `fizz
    --help` command.
    """
    result = subprocess.run(
        ["fizz", "--help"], capture_output=True, text=True, timeout=5
    )

    assert all(
        option in result.stdout
        for option in ["--version", "--help", "timer", "stopwatch"]
    )


def test_timer_help():
    """
    Now familiar with the basic fizz commands, the user checks to see how
    to use the timer command with `fizz timer --help`.
    """
    result = subprocess.run(
        ["fizz", "timer", "--help"], capture_output=True, text=True, timeout=5
    )

    assert all(
        option in result.stdout
        for option in ["--hours", "--minutes", "--seconds", "-h", "-m", "-s"]
    )


def test_timer_accepts_options():
    """
    Check that `fizz timer` accepts option arguments.

    Running `fizz timer` with the `--test` flag will avoid the curses
    interface and echo the timer duration if no exceptions are raised.
    """
    result = subprocess.run(
        ["fizz", "timer", "-s", "5", "--test"], capture_output=True, text=True, timeout=5
    )

    assert result.returncode == 0
    assert "00:00:05" in result.stdout


def test_timer_accepts_human_readable_strings():
    """
    Check that 'fizz timer` accepts human-readable strings so that
    users don't have to think like robots.

    Running `fizz timer` with the `--test` flag will avoid the curses
    interface and echo the timer duration if no exceptions are raised.
    """
    result = subprocess.run(
        ["fizz", "timer", "25m", "--test"], capture_output=True, text=True, timeout=5
    )

    assert result.returncode == 0
    assert "00:25:00" in result.stdout


def test_pomodoro_timer():
    """
    Having read the README, the user remembers that fizz offers custom
    timers, one of which is the included pomodoro timer. They load the
    pomodoro timer to see what the custom timers are all about.

    Running `fizz timer` with the `--test` flag will avoid the curses
    interface and echo the timer duration if no exceptions are raised.
    """
    result = subprocess.run(
        ["fizz", "timer", "pomodoro", "--test"], capture_output=True, text=True, timeout=5
    )

    assert result.returncode == 0
    assert "00:25:00" in result.stdout

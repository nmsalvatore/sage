import subprocess


def test_fizz_version():
    """
    To check that fizz is installed correctly, a user uses the `fizz
    --version` command.
    """
    result = subprocess.run(
        ["fizz", "--version"], capture_output=True, text=True, timeout=5
    )

    assert "version" in result.stdout


def test_fizz_help():
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


def test_fizz_timer_help():
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


def test_fizz_timer_accepts_options():
    """
    Check that `fizz timer` accepts option arguments.

    Running `fizz timer` with the `--test` flag will avoid the curses
    interface and echo "Test successful" if no exceptions are raised.
    """
    result = subprocess.run(
        ["fizz", "timer", "-s", "5", "--test"], capture_output=True, text=True, timeout=5
    )

    assert result.returncode == 0
    assert "Test successful" in result.stdout


def test_fizz_timer_accepts_human_readable_strings():
    """
    Check that 'fizz timer` accepts human-readable strings so that
    users don't have to think like robots.

    Running `fizz timer` with the `--test` flag will avoid the curses
    interface and echo "Test successful" if no exceptions are raised.
    """
    result = subprocess.run(
        ["fizz", "timer", "25 minutes", "--test"], capture_output=True, text=True, timeout=5
    )

    assert result.returncode == 0
    assert "Test successful" in result.stdout

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
    To get familiar with fizz usage, a user uses the `fizz --help`
    command.
    """

    result = subprocess.run(
        ["fizz", "--help"], capture_output=True, text=True, timeout=5
    )

    assert all(option in result.stdout for option in ["--version", "--help"])

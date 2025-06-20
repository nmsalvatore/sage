import subprocess

def test_fizz_version():
    """
    To check that the tool is installed correctly, a user uses the
    `fizz --version` command.
    """

    result = subprocess.run(
        ["fizz", "--version"],
        capture_output=True,
        text=True,
        timeout=True
    )

    assert "fizz" in result.stdout

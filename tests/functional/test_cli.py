import os
import subprocess


def test_version():
    """
    To check that sage is installed correctly, a user uses the 'sage
    --version' command.
    """
    result = subprocess.run(
        ["sage", "--version"], capture_output=True, text=True, timeout=5
    )

    assert "version" in result.stdout


def test_help():
    """
    To get familiar with basic sage usage, a user uses the 'sage
    --help' command.
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
    to use the timer command with 'sage timer --help'.
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
    Check that 'sage timer' accepts option arguments.
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
    Check that 'sage timer' accepts human-readable strings so that
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
    user goes to find out with 'sage timers'.
    """
    result = subprocess.run(
        ["sage", "timers", "list"], capture_output=True, text=True, timeout=5
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
        ["sage", "timers", "create", "rice", "15m"],
        capture_output=True,
        text=True,
        timeout=5,
        env=env,
    )

    assert result.returncode == 0
    assert "success" in result.stdout.lower()
    assert "rice" in result.stdout

    result = subprocess.run(
        ["sage", "timers", "list"], capture_output=True, text=True, timeout=5, env=env
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
        ["sage", "timers", "create", "titanic", "--minutes", "14", "--hours", "3"],
        capture_output=True,
        text=True,
        timeout=5,
        env=env,
    )

    assert result.returncode == 0
    assert "success" in result.stdout.lower()
    assert "titanic" in result.stdout

    result = subprocess.run(
        ["sage", "timers", "list"], capture_output=True, text=True, timeout=5, env=env
    )

    assert "titanic" in result.stdout
    assert "3 hours 14 minutes" in result.stdout


def test_crud_operations(tmp_path):
    """
    Our user is feeling pretty good about running timers, but one of
    the core features of sage appears to be these custom timers. They
    play with 'sage timers' to see what it's all about.
    """
    env = os.environ.copy()
    env["HOME"] = str(tmp_path)

    # First, they use the 'list' command to see a list of all of the
    # available timers.
    result = subprocess.run(
        ["sage", "timers", "list"],
        capture_output=True,
        text=True,
        timeout=5,
        env=env,
    )

    assert result.returncode == 0
    assert "pomodoro" in result.stdout
    assert "johncage" in result.stdout
    assert "potato" in result.stdout
    assert "pika" in result.stdout

    # All of the default timers are there, time to create a timer.
    # Hmm, what's a good test timer? How about their favorite movie's
    # runtime.
    result = subprocess.run(
        ["sage", "timers", "create", "titanic", "3 hours 14 minutes"],
        capture_output=True,
        text=True,
        timeout=5,
        env=env,
    )

    assert result.returncode == 0
    assert "success" in result.stdout.lower()
    assert "titanic" in result.stdout.lower()

    # Looks like it was created successfully, but they decide to check
    # the timers list just to be certain.
    result = subprocess.run(
        ["sage", "timers", "list"],
        capture_output=True,
        text=True,
        timeout=5,
        env=env,
    )

    assert result.returncode == 0
    assert "titanic" in result.stdout.lower()

    # Wow, it really worked! Ok, who needs a titanic timer though,
    # really? Time to delete it.
    result = subprocess.run(
        ["sage", "timers", "delete", "titanic"],
        capture_output=True,
        text=True,
        timeout=5,
        env=env,
    )

    assert result.returncode == 0
    assert "deleted" in result.stdout.lower()

    # Again, they check to make sure it's not in the list of timers
    result = subprocess.run(
        ["sage", "timers", "list"],
        capture_output=True,
        text=True,
        timeout=5,
        env=env,
    )

    assert result.returncode == 0
    assert "titanic" not in result.stdout.lower()

    # They notice this 'potato' timer in the timers list, but 50
    # minutes seems a little bit too short for a fluffy baked potato.
    # They decide to add 5 minutes with the update command.
    result = subprocess.run(
        ["sage", "timers", "update", "potato", "55mins"],
        capture_output=True,
        text=True,
        timeout=5,
        env=env,
    )

    assert result.returncode == 0
    assert "updated" in result.stdout.lower()
    assert "potato" in result.stdout.lower()

    # That's more like it! Time to check the list.
    result = subprocess.run(
        ["sage", "timers", "list"],
        capture_output=True,
        text=True,
        timeout=5,
        env=env,
    )

    assert result.returncode == 0
    assert "55 minutes" in result.stdout.lower()

    # Awesome! Since there are so many potatoes, they decide to change
    # the name to be a little more specific.
    result = subprocess.run(
        ["sage", "timers", "rename", "potato", "russet"],
        capture_output=True,
        text=True,
        timeout=5,
        env=env,
    )

    assert result.returncode == 0
    assert "success" in result.stdout.lower()
    assert "russet" in result.stdout.lower()


def test_invalid_timer_value():
    """
    Invalid values passed to 'sage timer' should raise an error
    alerting the user that a time value could not be found.
    """
    result = subprocess.run(
        ["sage", "timer", "somenonsense"],
        capture_output=True,
        text=True,
        timeout=5,
    )

    assert result.returncode == 2
    assert "invalid value" in result.stderr.lower()


def test_no_timer_arguments():
    """
    No arguments passed to 'sage timer' should raise an error
    alerting the user that they need to provide a timer duration.
    """
    result = subprocess.run(
        ["sage", "timer"],
        capture_output=True,
        text=True,
        timeout=5,
    )

    assert result.returncode == 2
    assert "provide a timer duration" in result.stderr.lower()


def test_timer_zero_seconds():
    """
    A duration of 0 seconds passed to 'sage timer' should raise an
    error alerting the user that they need to provide a timer duration
    greater than 0 seconds.
    """
    result = subprocess.run(
        ["sage", "timer", "0s"],
        capture_output=True,
        text=True,
        timeout=5,
    )

    assert result.returncode == 2
    assert "greater than 0 seconds" in result.stderr.lower()


def test_timer_with_negative_duration():
    """
    A duration of less than 0 seconds passed to 'sage timer' should
    raise an error alerting the user that they need to provide a timer
    duration greater than 0 seconds.
    """
    result = subprocess.run(
        ["sage", "timer", "-m", "-5"],
        capture_output=True,
        text=True,
        timeout=5,
    )

    assert result.returncode == 2
    assert "greater than 0 seconds" in result.stderr.lower()


def test_timers_with_no_argument():
    """
    Well, all those errors certainly set our user straight about how to
    properly use 'sage timer'. What happens if they don't pass an
    argument to 'sage timers'? Aha! It lists all of the timers,
    similar to 'sage list'! How convenient.
    """
    result = subprocess.run(
        ["sage", "timers"],
        capture_output=True,
        text=True,
        timeout=5,
    )

    assert result.returncode == 0
    assert "pomodoro" in result.stdout
    assert "johncage" in result.stdout
    assert "potato" in result.stdout
    assert "pika" in result.stdout

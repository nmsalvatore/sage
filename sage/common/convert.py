import re
from textwrap import dedent
from click.exceptions import BadArgumentUsage


def time_units_to_seconds(hours=0, minutes=0, seconds=0) -> int:
    """
    Converts hours, minutes, and seconds to total seconds.
    """
    return (hours * 3600) + (minutes * 60) + seconds


def time_string_to_seconds(time_string: str) -> int:
    """
    Convert a human-readable time string to total seconds.
    """
    hours = re.search(r"(\d+)\s*(h|hour|hours)", time_string)
    minutes = re.search(r"(\d+)\s*(m|min|minute|minutes)", time_string)
    seconds = re.search(r"(\d+)\s*(s|sec|second|seconds)", time_string)

    if not any([hours, minutes, seconds]):
        raise BadArgumentUsage(
            dedent(
                f"'{time_string}' is not a valid time format. "
                "Please use formats like '25m', '1h 30m', or '45s'."
            ))

    total = 0

    if hours:
        total += int(hours.group(1)) * 3600
    if minutes:
        total += int(minutes.group(1)) * 60
    if seconds:
        total += int(seconds.group(1))

    if total == 0:
        raise BadArgumentUsage(
            dedent(
                "Please check your time values (e.g., use '1s' instead of '0s'). "
                "Time must be greater than 0 seconds."
            ))

    return total


def seconds_to_time_units(total_seconds: float) -> tuple:
    """
    Expand a time in seconds to hours, minutes, and seconds.
    """
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds - (hours * 3600)) // 60)
    seconds = int(total_seconds % 60)
    return (hours, minutes, seconds)

import re


def convert_time_to_seconds(hours=0, minutes=0, seconds=0) -> int:
    """
    Converts hours, minutes, and seconds to total seconds.
    """
    return (hours * 3600) + (minutes * 60) + (seconds)


def expand_time_from_seconds(total_seconds) -> tuple:
    """
    Expand a time in seconds to hours, minutes, and seconds.
    """
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds - (hours * 3600)) // 60)
    seconds = int(total_seconds % 60)
    return (hours, minutes, seconds)


def convert_time_string_to_seconds(time_string) -> int:
    """
    Convert a human-readable time string to total seconds.
    """
    hours = re.search(r"(\d+)\s*(h|hour|hours)", time_string)
    minutes = re.search(r"(\d+)\s*(m|min|minute|minutes)", time_string)
    seconds = re.search(r"(\d+)\s*(s|sec|second|seconds)", time_string)

    total = 0

    if hours:
        total += int(hours.group(1)) * 3600
    if minutes:
        total += int(minutes.group(1)) * 60
    if seconds:
        total += int(seconds.group(1))

    if total == 0:
        raise ValueError(f"Could not find a time value in '{time_string}'")

    return total


def get_timer_duration(hours=0, minutes=0, seconds=0, time_string=None):
    """
    Determine a time in total seconds, depending on which arguments are
    passed to `fizz timer`.
    """
    if time_string:
        return convert_time_string_to_seconds(time_string)
    return convert_time_to_seconds(hours, minutes, seconds)

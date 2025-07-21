import re
from typing import TypeAlias


HoursMinutesSeconds: TypeAlias = tuple[int, int, int]


def time_units_to_seconds(hours=0, minutes=0, seconds=0) -> int:
    """
    Converts hours, minutes, and seconds to total seconds.
    """
    return (hours * 3600) + (minutes * 60) + seconds


def seconds_to_time_units(total_seconds: float) -> HoursMinutesSeconds:
    """
    Expand a time in seconds to hours, minutes, and seconds.
    """
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds - (hours * 3600)) // 60)
    seconds = int(total_seconds % 60)
    return (hours, minutes, seconds)


def time_string_to_seconds(time_string: str) -> int:
    """
    Convert a human-readable time string to total seconds.
    """

    def extract_time_value(pattern: str) -> int:
        match = re.search(pattern, time_string)
        return int(match.group(1)) if match else 0

    hours = extract_time_value(r"(\d+)\s*(h|hour|hours)")
    minutes = extract_time_value(r"(\d+)\s*(m|min|minute|minutes)")
    seconds = extract_time_value(r"(\d+)\s*(s|sec|second|seconds)")
    total = hours * 3600 + minutes * 60 + seconds

    return total


def time_string_to_time_units(time_string: str) -> HoursMinutesSeconds:
    """
    Convert a human-readable time string to hours, minutes, and seconds.
    """
    return seconds_to_time_units(
        time_string_to_seconds(time_string)
    )


def get_duration(time_string: str) -> int:
    """
    Determine the timer duration in seconds based on whether the string
    represents a preset or not.
    """
    from sage.config import presets

    total_seconds = 0

    if preset := presets.get(time_string):
        hours = preset.get("hours", 0)
        minutes = preset.get("minutes", 0)
        seconds = preset.get("seconds", 0)
        total_seconds = time_units_to_seconds(hours, minutes, seconds)

    else:
        total_seconds = time_string_to_seconds(time_string)

    if total_seconds <= 0:
        raise ValueError("Duration must be greater than 0 seconds.")

    if total_seconds > 86400:
        raise ValueError("Duration cannot exceed 24 hours.")

    return total_seconds

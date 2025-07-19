import re


def time_units_to_seconds(hours=0, minutes=0, seconds=0) -> int:
    """
    Converts hours, minutes, and seconds to total seconds.
    """
    return (hours * 3600) + (minutes * 60) + seconds


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

    if not any([hours, minutes, seconds]):
        raise ValueError("could not find a valid time value in the provided time string.")

    total = hours * 3600 + minutes * 60 + seconds

    if total <= 0 or total > 86400:
        raise ValueError("total seconds must be greater than 0 and less than or equal to 86400.")

    return total


def seconds_to_time_units(total_seconds: float) -> tuple:
    """
    Expand a time in seconds to hours, minutes, and seconds.
    """
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds - (hours * 3600)) // 60)
    seconds = int(total_seconds % 60)
    return (hours, minutes, seconds)

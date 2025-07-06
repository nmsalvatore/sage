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


def format_time_as_clock(total_seconds) -> str:
    """
    Take a time in total seconds, convert it to the correct time units
    (hours, minutes, seconds) and format it into a 00:00:00 format.
    """
    hours, minutes, seconds = expand_time_from_seconds(total_seconds)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def format_time_as_english(total_seconds) -> str:
    """
    Take a time in total seconds, convert it to the correct time units
    (hours, minutes, seconds) and format it into English with proper
    singular/plural.
    """
    hours, minutes, seconds = expand_time_from_seconds(total_seconds)

    def pluralize(value, unit):
        return f"{value} {unit}" + ("" if value == 1 else "s")

    parts = []
    if hours:
        parts.append(pluralize(hours, "hour"))
    if minutes:
        parts.append(pluralize(minutes, "minute"))
    if seconds:
        parts.append(pluralize(seconds, "second"))

    return " ".join(parts) if parts else "0 seconds"


def get_curses_center_positions(string: str) -> tuple:
    """
    Calculate the position needed by the `stdscr.addstr` function
    when centering a string in the curses pane.
    """
    import curses
    y = curses.LINES // 2
    x = (curses.COLS // 2) - (len(string) // 2)
    return (y, x)


def set_curses_colors() -> None:
    """
    Initialize curses color pairs.
    """
    import curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)

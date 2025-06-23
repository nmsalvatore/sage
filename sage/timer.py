import curses
import time

from .config import get_saved_timer
from .common import (
    convert_time_string_to_seconds,
    convert_time_to_seconds,
    format_time_as_clock,
    get_curses_center_positions,
)


def get_timer_duration(hours=0, minutes=0, seconds=0, time_string=None) -> int:
    """
    Determine the timer duration based on which arguments are passed to
    `sage timer`. Returns time in seconds for both cases.
    """
    if time_string:
        saved_timer = get_saved_timer(time_string)

        if saved_timer:
            hours = saved_timer.get("hours", 0)
            minutes = saved_timer.get("minutes", 0)
            seconds = saved_timer.get("seconds", 0)
            return convert_time_to_seconds(hours, minutes, seconds)

        return convert_time_string_to_seconds(time_string)
    return convert_time_to_seconds(hours, minutes, seconds)


def load_timer(stdscr, hours=0, minutes=0, seconds=0, time_string=None):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

    stdscr.clear()
    curses.curs_set(0)  # Hide terminal cursor

    start = time.perf_counter()
    total_seconds = get_timer_duration(hours, minutes, seconds, time_string)

    while True:
        elapsed = time.perf_counter() - start
        time_remaining = total_seconds - elapsed
        ftime_remaining = format_time_as_clock(time_remaining)

        ftime_y, ftime_x = get_curses_center_positions(ftime_remaining)
        stdscr.addstr(ftime_y, ftime_x, ftime_remaining, curses.color_pair(1))

        if time_remaining < 0:
            break

        time.sleep(0.1)
        stdscr.refresh()

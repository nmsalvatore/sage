import curses
import time
from pathlib import Path

from nava import play as play_sound

from .config import get_saved_timer, load_saved_timers
from .common import (
    convert_time_string_to_seconds,
    convert_time_to_seconds,
    format_time_as_clock,
    format_time_as_english,
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
    """
    Load the timer interface.
    """
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    stdscr.clear()
    curses.curs_set(0)  # Hide terminal cursor
    stdscr.nodelay(1)   # Make getch() non-blocking

    timer_name = ""
    saved_timer = get_saved_timer(time_string)
    if saved_timer:
        timer_name = time_string

    start_time = time.perf_counter()
    pause_time = 0
    paused = False
    pause_start = 0

    times_up = False

    total_seconds = get_timer_duration(hours, minutes, seconds, time_string)

    # add one second to total seconds so that the timer duration
    # accurately reflects the time remaining before the clock hits 0,
    # rather than the time remaining before the clock hits -1.
    total_seconds += 1

    y = 0

    while True:
        key = stdscr.getch()

        if key == ord(" "):
            if not paused:
                pause_start += time.perf_counter()
                paused = True
            else:
                pause_time += time.perf_counter() - pause_start
                paused = False
        elif key == ord("q"):
            break

        paused_message = "Paused"
        paused_y, paused_x = get_curses_center_positions(paused_message)
        paused_y += 1

        if paused:
            elapsed = pause_start - start_time - pause_time
            stdscr.addstr(paused_y, paused_x, paused_message, curses.color_pair(4))
        else:
            elapsed = time.perf_counter() - start_time - pause_time
            stdscr.move(paused_y, paused_x)
            stdscr.clrtoeol()
            pause_start = 0

        time_remaining = total_seconds - elapsed
        ftime_remaining = format_time_as_clock(time_remaining)
        y, ftime_x = get_curses_center_positions(ftime_remaining)

        if timer_name:
            _, timer_name_x = get_curses_center_positions(timer_name)

            if len(timer_name) % 2:
                timer_name_x -= 1

            stdscr.addstr(y - 1, timer_name_x, timer_name, curses.color_pair(2))

        stdscr.addstr(y, ftime_x, ftime_remaining, curses.color_pair(1))
        stdscr.addstr(curses.LINES - 1, 1, "<q> Quit, <Space> Pause/Resume", curses.color_pair(3))

        if time_remaining < 1:
            times_up = True
            break

        time.sleep(0.1)
        stdscr.refresh()

    if times_up:
        sound_path = Path("sounds", "thyme.mp3")
        play_sound(sound_path.as_posix(), async_mode=True)

        message = "Time's up!"
        _, message_x = get_curses_center_positions(message)
        stdscr.addstr(y + 1, message_x, message, curses.color_pair(4))

        stdscr.nodelay(0)
        stdscr.getch()


def list_timers():
    """
    List all saved timers.
    """
    import click

    saved_timers = load_saved_timers()

    if not saved_timers:
        click.echo("No saved timers.")
        click.echo("Save a timer with: sage timer <duration> --name <name>")
        return

    max_width = max(len(name) for name in saved_timers.keys())

    for timer in sorted(saved_timers.keys()):
        hours = saved_timers[timer].get("hours", 0)
        minutes = saved_timers[timer].get("minutes", 0)
        seconds = saved_timers[timer].get("seconds", 0)

        duration = format_time_as_english(
            convert_time_to_seconds(hours, minutes, seconds)
        )

        click.echo(f"{timer:<{max_width + 2}} {duration}")

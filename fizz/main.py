import curses
import time

import click

from .utils import convert_time_to_seconds, expand_time_from_seconds


def run_timer(stdscr, hours=0, minutes=0, seconds=0):
    stdscr.clear()
    curses.curs_set(0)  # Hide terminal cursor

    start = time.perf_counter()
    timer_in_seconds = convert_time_to_seconds(hours, minutes, seconds)

    while True:
        elapsed = time.perf_counter() - start
        time_remaining = timer_in_seconds - elapsed

        hours, minutes, seconds = expand_time_from_seconds(time_remaining)
        formatted_time_remaining = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        # Calculate the center y and x positions where the remaining
        # time will be rendered
        stdscr.addstr(
            curses.LINES // 2,
            curses.COLS // 2 - len(formatted_time_remaining) // 2,
            formatted_time_remaining,
        )

        if time_remaining < 0:
            break

        time.sleep(0.1)
        stdscr.refresh()


@click.group()
@click.version_option()
def fizz():
    """
    The base fizz command, executed with `fizz`. Includes `--help` and
    `--version` flags which supply their respective information.
    """
    pass


@fizz.command()
@click.option("-h", "--hours", type=int, default=0)
@click.option("-m", "--minutes", type=int, default=0)
@click.option("-s", "--seconds", type=int, default=0)
def timer(**kwargs):
    """
    The fizz timer, executed with `fizz timer` and displayed with the
    curses library.
    """
    curses.wrapper(lambda stdscr: run_timer(stdscr, **kwargs))


@fizz.command()
def stopwatch():
    """
    The fizz stopwatch, executed with `fizz stopwatch` and displayed
    with the curses library.
    """
    pass


if __name__ == "__main__":
    fizz()

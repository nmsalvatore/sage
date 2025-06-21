import curses
import time

import click

from . import utils


def load_timer(stdscr, hours=0, minutes=0, seconds=0):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

    stdscr.clear()
    curses.curs_set(0)  # Hide terminal cursor

    start = time.perf_counter()
    timer_in_seconds = utils.convert_time_to_seconds(hours, minutes, seconds)

    while True:
        elapsed = time.perf_counter() - start
        time_remaining = timer_in_seconds - elapsed

        hours, minutes, seconds = utils.expand_time_from_seconds(time_remaining)
        ftime_remaining = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        stdscr.addstr(
            curses.LINES // 2,
            curses.COLS // 2 - len(ftime_remaining) // 2,
            ftime_remaining,
            curses.color_pair(1),
        )

        if time_remaining < 0:
            break

        time.sleep(0.1)
        stdscr.refresh()


@click.group()
@click.version_option()
def fizz():
    pass


@fizz.command()
@click.option("-h", "--hours", type=int, default=0)
@click.option("-m", "--minutes", type=int, default=0)
@click.option("-s", "--seconds", type=int, default=0)
def timer(**kwargs):
    curses.wrapper(lambda stdscr: load_timer(stdscr, **kwargs))


@fizz.command()
def stopwatch():
    pass


if __name__ == "__main__":
    fizz()

import curses

import click

from .common import format_time_as_clock
from .timer import get_timer_duration, load_timer, list_timers


@click.group()
@click.version_option()
def sage():
    pass


@sage.command()
@click.option("-h", "--hours", type=int, default=0)
@click.option("-m", "--minutes", type=int, default=0)
@click.option("-s", "--seconds", type=int, default=0)
@click.argument("time_string", required=False)
@click.option("--test", is_flag=True, hidden=True)
def timer(test, **kwargs):
    time_string = kwargs.get("time_string")

    if time_string == "list":
        list_timers()
        return

    if test:
        time_in_seconds = get_timer_duration(**kwargs)
        click.echo(format_time_as_clock(time_in_seconds))
    else:
        curses.wrapper(lambda stdscr: load_timer(stdscr, **kwargs))


@sage.command()
def stopwatch():
    pass


if __name__ == "__main__":
    sage()

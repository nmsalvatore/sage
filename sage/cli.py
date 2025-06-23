import curses

import click

from .common import format_time
from .timer import get_timer_duration, load_timer


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
    """
    The sage `timer` command can load a timer using option flags, a
    single human-readable string, or a custom timer name. For testing
    purposes, `timer` also includes a `--test` flag which will echo
    the total calculated time of the timer being called.
    """
    if test:
        time_in_seconds = get_timer_duration(**kwargs)
        click.echo(format_time(time_in_seconds))
    else:
        curses.wrapper(lambda stdscr: load_timer(stdscr, **kwargs))


@sage.command()
def stopwatch():
    pass


if __name__ == "__main__":
    sage()

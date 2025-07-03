import curses
from textwrap import dedent

import click

from .common import format_time_as_clock
from .config import save_timer
from .timer import get_timer_duration, list_timers, load_timer


@click.group()
@click.version_option()
def sage():
    pass


@sage.command()
@click.argument("time_string", required=False)
@click.option("-h", "--hours", type=int, default=0)
@click.option("-m", "--minutes", type=int, default=0)
@click.option("-s", "--seconds", type=int, default=0)
@click.option("--test", is_flag=True, hidden=True)
def timer(test, **kwargs):
    if test:
        time_in_seconds = get_timer_duration(**kwargs)
        click.echo(format_time_as_clock(time_in_seconds))
    else:
        curses.wrapper(lambda stdscr: load_timer(stdscr, **kwargs))


@sage.command()
def timers():
    list_timers()


@sage.command()
@click.argument("timer_name", required=True)
@click.argument("time_string", required=False)
@click.option("-h", "--hours", type=int, default=0)
@click.option("-m", "--minutes", type=int, default=0)
@click.option("-s", "--seconds", type=int, default=0)
def create(timer_name, **kwargs):
    save_timer(timer_name, **kwargs)
    click.echo(
        dedent(f"""\
        Successfully created timer!
        You can start your timer with 'sage timer {timer_name}'.\
    """)
    )


@sage.command()
def stopwatch():
    pass


if __name__ == "__main__":
    sage()

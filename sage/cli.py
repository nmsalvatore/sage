import curses
from textwrap import dedent

import click

from .common import format_time_as_clock
from .config import delete_timer, save_timer, rename_timer
from .timer import get_timer_duration, list_timers, get_saved_timer, load_timer


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


@sage.group()
def timers():
    pass


@timers.command()
def list():
    list_timers()


@timers.command()
@click.argument("name", required=True)
@click.argument("time_string", required=False)
@click.option("-h", "--hours", type=int, default=0)
@click.option("-m", "--minutes", type=int, default=0)
@click.option("-s", "--seconds", type=int, default=0)
def create(name, **kwargs):
    save_timer(name, **kwargs)
    click.echo(
        dedent(f"""\
        Successfully created '{name}' timer!
        You can start your timer with 'sage timer {name}'.\
    """)
    )


@timers.command()
@click.argument("name", required=True)
@click.argument("time_string", required=False)
@click.option("-h", "--hours", type=int, default=0)
@click.option("-m", "--minutes", type=int, default=0)
@click.option("-s", "--seconds", type=int, default=0)
def update(name, **kwargs):
    if not get_saved_timer(name):
        click.echo(f"Timer '{name}' does not exist.")
        return

    save_timer(name, **kwargs)
    click.echo(f"Successfully updated timer '{name}'.")


@timers.command()
@click.argument("name", required=True)
@click.argument("new_name", required=True)
def rename(name, new_name):
    if not get_saved_timer(name):
        click.echo(f"Timer '{name}' does not exist.")
        return

    rename_timer(name, new_name)
    click.echo(f"Successfully changed the name of timer '{name}' to '{new_name}'.")


@timers.command()
@click.argument("name", required=True)
def delete(name):
    if not get_saved_timer(name):
        click.echo(f"Timer '{name}' does not exist.")
        return

    delete_timer(name)
    click.echo(f"Successfully deleted timer '{name}'.")


@sage.command()
def stopwatch():
    pass


if __name__ == "__main__":
    sage()

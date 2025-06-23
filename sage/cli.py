import curses

import click

from .config import load_saved_timers
from .common import convert_time_to_seconds, format_time_as_clock, format_time_as_english
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
    if test:
        time_in_seconds = get_timer_duration(**kwargs)
        click.echo(format_time_as_clock(time_in_seconds))
    else:
        curses.wrapper(lambda stdscr: load_timer(stdscr, **kwargs))


@sage.command()
def timers():
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


@sage.command()
def stopwatch():
    pass


if __name__ == "__main__":
    sage()

import curses
from textwrap import dedent

import click

from .clocks import Stopwatch, Timer
from .common import convert_time_string_to_seconds, convert_time_to_seconds, format_time_as_english
from .config import delete_timer, save_timer, rename_timer, get_saved_timer, load_saved_timers


@click.group()
@click.version_option()
def sage():
    pass


def validate_time_string(ctx, param, value):
    """
    Validation on time_string that checks if the string can be
    converted to seconds and if not, checks if there a saved timer with
    the same name.
    """
    if value is None:
        return

    try:
        convert_time_string_to_seconds(value)
        return value
    except (ValueError, TypeError):
        saved_timer = get_saved_timer(value)
        if saved_timer is not None:
            return value
        raise click.BadParameter(f"Could not find a time value associated with '{value}'.")


@sage.command()
@click.argument("time_string", required=False, callback=validate_time_string)
@click.option("-h", "--hours", type=int, default=0)
@click.option("-m", "--minutes", type=int, default=0)
@click.option("-s", "--seconds", type=int, default=0)
@click.option("--no-start", is_flag=True)
@click.option("--test", is_flag=True, hidden=True)
def timer(test, **kwargs):
    timer = Timer()
    if test:
        timer.print_duration(**kwargs)
        return

    timer.run(**kwargs)


@sage.group()
def timers():
    pass


@timers.command()
def list():
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
        total_seconds = convert_time_to_seconds(hours, minutes, seconds)

        duration = format_time_as_english(total_seconds)
        click.echo(f"{timer:<{max_width + 2}} {duration}")


@timers.command()
@click.argument("name", required=True)
@click.argument("time_string", required=False, callback=validate_time_string)
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
@click.argument("time_string", required=False, callback=validate_time_string)
@click.option("-h", "--hours", type=int, default=0)
@click.option("-m", "--minutes", type=int, default=0)
@click.option("-s", "--seconds", type=int, default=0)
def update(name, **kwargs):
    saved_timer = get_saved_timer(name)
    if saved_timer is None:
        click.echo(f"Timer '{name}' does not exist.")
        return

    save_timer(name, **kwargs)
    click.echo(f"Successfully updated timer '{name}'.")


@timers.command()
@click.argument("name", required=True)
@click.argument("new_name", required=True)
def rename(name, new_name):
    saved_timer = get_saved_timer(name)
    if saved_timer is None:
        click.echo(f"Timer '{name}' does not exist.")
        return

    rename_timer(name, new_name)
    click.echo(f"Successfully changed the name of timer '{name}' to '{new_name}'.")


@timers.command()
@click.argument("name", required=True)
def delete(name):
    saved_timer = get_saved_timer(name)
    if saved_timer is None:
        click.echo(f"Timer '{name}' does not exist.")
        return

    delete_timer(name)
    click.echo(f"Successfully deleted timer '{name}'.")


@sage.command()
@click.option("--no-start", is_flag=True)
def stopwatch(**kwargs):
    stopwatch = Stopwatch()
    curses.wrapper(lambda stdscr: stopwatch.load(stdscr, **kwargs))


if __name__ == "__main__":
    sage()

from textwrap import dedent

import click

from .clocks import Stopwatch, Timer
from .common import (
    convert_time_string_to_seconds,
    convert_time_to_seconds,
    format_time_as_english,
)
from .config import (
    delete_timer,
    save_timer,
    rename_timer,
    get_saved_timer,
    load_saved_timers,
)


def get_duration_params(**kwargs):
    """
    Extract only the duration parameters from kwargs.
    """
    return {
        "hours": kwargs.get("hours", 0),
        "minutes": kwargs.get("minutes", 0),
        "seconds": kwargs.get("seconds", 0),
        "time_string": kwargs.get("time_string"),
    }


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
    except ValueError as e:
        saved_timer = get_saved_timer(value)
        if saved_timer is not None:
            return value

        raise click.BadParameter(str(e))


@click.group()
@click.version_option()
def sage():
    pass


@sage.command()
@click.argument("time_string", required=False, callback=validate_time_string)
@click.option("-h", "--hours", type=int, default=0)
@click.option("-m", "--minutes", type=int, default=0)
@click.option("-s", "--seconds", type=int, default=0)
@click.option("--no-start", is_flag=True)
@click.option("--test", is_flag=True, hidden=True)
def timer(test, **kwargs):
    """
    Run a timer.
    """
    timer = Timer()

    duration_params = get_duration_params(**kwargs)

    if not any(duration_params.values()):
        raise click.UsageError(
            "Please provide a timer duration using either a time string (e.g., '25m') "
            "or time options (e.g., --minutes 25)."
        )

    if timer.get_duration(**duration_params) <= 0:
        raise click.UsageError(
            "Timer duration must be greater than 0 seconds. "
            "Please check your time values."
        )

    if timer.get_duration(**duration_params) > 86400:
        raise click.UsageError(
            "Timer duration must be 24 hours or less. "
            "Please check your time values."
        )

    if test:
        timer.print_duration(**duration_params)
        return

    timer.run(**kwargs)


@sage.group(invoke_without_command=True)
@click.pass_context
def timers(ctx):
    """
    Manage custom timers.
    """
    if ctx.invoked_subcommand is None:
        ctx.invoke(list_timers)


@timers.command(name="list")
def list_timers():
    """
    List custom timers.
    """
    saved_timers = load_saved_timers()
    if not saved_timers:
        click.echo(
            dedent("""\
                No saved timers.
                Save a timer with: sage timer <duration> --name <name>\
            """)
        )
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
    """
    Create a custom timer.
    """
    duration_params = get_duration_params(**kwargs)
    if not any(duration_params.values()):
        raise click.UsageError(
            "A duration must be specified to create a custom timer. "
            "Please provide a timer duration using either a time string (e.g., '25m')"
        )

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
    """
    Update the duration of a custom timer.
    """
    saved_timer = get_saved_timer(name)
    if saved_timer is None:
        click.echo(
            dedent(
                f"Timer '{name}' does not exist. Use 'sage timers list' "
                f"to see available timers or 'sage timers create {name} "
                "<duration>' to create it."
            )
        )
        return

    save_timer(name, **kwargs)
    updated_timer = get_saved_timer(name)
    if updated_timer:
        new_duration = convert_time_to_seconds(
            hours=updated_timer.get("hours", 0),
            minutes=updated_timer.get("minutes", 0),
            seconds=updated_timer.get("seconds", 0),
        )
        new_english_duration = format_time_as_english(new_duration)
        click.echo(f"Successfully updated timer '{name}' to {new_english_duration}.")


@timers.command()
@click.argument("name", required=True)
@click.argument("new_name", required=True)
def rename(name, new_name):
    """
    Rename a custom timer.
    """
    saved_timer = get_saved_timer(name)
    if saved_timer is None:
        click.echo(
            dedent(
                f"Timer '{name}' does not exist. Use 'sage timers list' "
                f"to see available timers or 'sage timers create {name} "
                "<duration>' to create it."
            )
        )
        return

    rename_timer(name, new_name)
    click.echo(f"Successfully changed the name of timer '{name}' to '{new_name}'.")


@timers.command()
@click.argument("name", required=True)
def delete(name):
    """
    Delete a custom timer.
    """
    saved_timer = get_saved_timer(name)
    if saved_timer is None:
        click.echo(
            dedent(
                f"Timer '{name}' does not exist. Use 'sage timers list' "
                f"to see available timers or 'sage timers create {name} "
                "<duration>' to create it."
            )
        )
        return

    delete_timer(name)
    click.echo(f"Successfully deleted timer '{name}'.")


@sage.command()
@click.option("--no-start", is_flag=True)
def stopwatch(**kwargs):
    """
    Run a stopwatch.
    """
    stopwatch = Stopwatch()
    stopwatch.run(**kwargs)


if __name__ == "__main__":
    sage()

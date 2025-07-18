from textwrap import dedent

import click

from sage.clocks.timer import Timer
from sage.clocks.stopwatch import Stopwatch
from sage.common import convert, format
from sage.config import presets


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
        convert.time_string_to_seconds(value)

    except ValueError as e:
        if presets.get_one(value) is None:
            raise click.BadParameter(str(e))

    return value



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
    all_presets = presets.load_all()

    if not all_presets:
        click.echo(dedent("""\
            No saved timers.
            Save a timer with 'sage timers create <name> <duration>'."""
        ))
        return

    max_width = max(len(name) for name in all_presets.keys())

    for timer in sorted(all_presets.keys()):
        hours = all_presets[timer].get("hours", 0)
        minutes = all_presets[timer].get("minutes", 0)
        seconds = all_presets[timer].get("seconds", 0)
        total_seconds = convert.time_units_to_seconds(hours, minutes, seconds)
        duration = format.time_in_english(total_seconds)
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
            "A duration has not been specified. "
            "Use 'sage timers create <name> <duration>' to create a custom timer."
        )

    presets.create_one(name, **kwargs)
    click.echo(
        dedent(f"""\
            Successfully created '{name}' timer!
            Start your timer with 'sage timer {name}'.\
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
    duration_params = get_duration_params(**kwargs)

    if not any(duration_params.values()):
        raise click.UsageError(
            "A duration has not been specified. "
            "Use 'sage timers update <name> <duration>' to update a custom timer."
        )

    if presets.get_one(name) is None:
        click.echo(dedent(
            f"Timer '{name}' does not exist. Use 'sage timers list' "
            f"to see available timers or 'sage timers create {name} "
            "<duration>' to create it."
        ))
        return

    presets.create_one(name, **kwargs)

    if preset := presets.get_one(name):
        new_duration = convert.time_units_to_seconds(
            hours=preset.get("hours", 0),
            minutes=preset.get("minutes", 0),
            seconds=preset.get("seconds", 0),
        )
        new_english_duration = format.time_in_english(new_duration)
        click.echo(f"Successfully updated timer '{name}' to {new_english_duration}.")


@timers.command()
@click.argument("name", required=True)
@click.argument("new_name", required=True)
def rename(name, new_name):
    """
    Rename a custom timer.
    """
    if presets.get_one(name) is None:
        click.echo(dedent(
            f"Timer '{name}' does not exist. Use 'sage timers list' "
            f"to see available timers or 'sage timers create {name} "
            "<duration>' to create it."
        ))
        return

    presets.rename_one(name, new_name)
    click.echo(f"Successfully changed the name of timer '{name}' to '{new_name}'.")


@timers.command()
@click.argument("name", required=True)
def delete(name):
    """
    Delete a custom timer.
    """
    if presets.get_one(name) is None:
        click.echo(dedent(
            f"Timer '{name}' does not exist. Use 'sage timers list' "
            f"to see available timers or 'sage timers create {name} "
            "<duration>' to create it."
        ))
        return

    presets.delete_one(name)
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

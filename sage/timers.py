import click

from .config import load_saved_timers
from .common import (
    convert_time_to_seconds,
    format_time_as_english
)


def list_timers():
    """
    List all saved timers.
    """

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

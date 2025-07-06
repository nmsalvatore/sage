from .config import get_saved_timer, load_saved_timers
from .common import (
    convert_time_string_to_seconds,
    convert_time_to_seconds,
    format_time_as_english
)


def get_timer_duration(hours=0, minutes=0, seconds=0, time_string=None) -> int:
    """
    Determine the timer duration based on which arguments are passed to
    `sage timer`. Returns time in seconds for both cases.
    """
    if time_string:
        saved_timer = get_saved_timer(time_string)
        if saved_timer:
            hours = saved_timer.get("hours", 0)
            minutes = saved_timer.get("minutes", 0)
            seconds = saved_timer.get("seconds", 0)
            return convert_time_to_seconds(hours, minutes, seconds)
        return convert_time_string_to_seconds(time_string)
    return convert_time_to_seconds(hours, minutes, seconds)


def list_timers():
    """
    List all saved timers.
    """
    import click

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

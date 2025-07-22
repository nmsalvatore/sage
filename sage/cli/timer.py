"""Sage timer command."""

import click

from sage.clocks.timer import Timer


@click.command(short_help="Start a timer")
@click.argument("time_input", required=True)
@click.option("--paused", is_flag=True, help="Start timer in a paused state.")
@click.option("--test", is_flag=True, hidden=True)
def timer(test, **kwargs):
    """
    Start a timer with flexible time input. Accepts human-readable
    formats like "25m", "1h 30m", or "45 seconds". You can also use
    custom timer names like 'pomodoro' or 'workout'.
    """
    try:
        timer = Timer()

        if test:
            time_input = kwargs.get("time_input", "")
            timer.print_duration(time_input)
            return

        timer.run(**kwargs)

    except ValueError as e:
        raise click.BadArgumentUsage(str(e))

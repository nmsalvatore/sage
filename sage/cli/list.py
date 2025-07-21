from textwrap import dedent

import click

from sage.config import presets
from sage.common.conversions import time_units_to_seconds
from sage.common.formatting import time_in_english


@click.command(short_help="List all timers")
def list():
    """
    List all saved timers and their durations in human-readable format.
    """
    all_presets = presets.load_all()

    if not all_presets:
        click.echo("No saved timers")
        return

    max_width = max(len(name) for name in all_presets.keys())

    for timer, duration in sorted(all_presets.items()):
        total_seconds = time_units_to_seconds(**duration)
        click.echo(f"{timer:<{max_width + 2}} {time_in_english(total_seconds)}")

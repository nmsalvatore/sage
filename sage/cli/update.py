import click

from sage.common.formatting import time_in_english
from sage.common.conversions import time_units_to_seconds
from sage.config import presets


@click.command()
@click.argument("name", required=True)
@click.argument("duration", required=True)
def update(name: str, duration: str) -> None:
    """
    Update preset duration.
    """
    try:
        preset = presets.update(name, duration)
        hours, minutes, seconds = preset.values()
        total_seconds = time_units_to_seconds(hours, minutes, seconds)

        click.echo(
            f"Successfully updated '{name}' to {time_in_english(total_seconds)}!"
        )

    except ValueError as e:
        raise click.ClickException(str(e))

import click

from sage.config import presets


@click.command(short_help="Create a custom timer")
@click.argument("name", required=True)
@click.argument("duration", required=True)
def create(name, duration):
    """
    Create a custom timer with a memorable name. Duration accepts
    flexible formats like '25m', '1 hour 30 minutes', or '45s'.
    """
    try:
        presets.create(name, duration)
        click.echo(f"Successfully created timer '{name}'.")

    except ValueError as e:
        raise click.BadArgumentUsage(str(e))

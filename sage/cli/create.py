import click

from sage.config import presets


@click.command()
@click.argument("name", required=True)
@click.argument("duration", required=True)
def create(name, duration):
    """
    Create a preset.
    """
    try:
        presets.create(name, duration)
        click.echo(f"Successfully created '{name}'.")

    except ValueError as e:
        raise click.BadArgumentUsage(str(e))

import click

from sage.config import presets


@click.command()
@click.argument("name", required=True)
def delete(name):
    """
    Delete a preset.
    """
    try:
        presets.delete(name)
        click.echo(f"Successfully deleted '{name}'.")

    except ValueError as e:
        raise click.BadArgumentUsage(str(e))

import click

from sage.config import presets


@click.command(short_help="Rename a timer")
@click.argument("name", required=True)
@click.argument("new_name", required=True)
def rename(name, new_name):
    """
    Rename an existing timer.
    """
    try:
        presets.rename(name, new_name)
        click.echo(f"Successfully renamed timer '{name}' to '{new_name}'.")

    except ValueError as e:
        raise click.BadArgumentUsage(str(e))

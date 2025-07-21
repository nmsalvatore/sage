import click

from sage.config import presets


@click.command()
@click.argument("name", required=True)
@click.argument("new_name", required=True)
def rename(name, new_name):
    """
    Rename a preset.
    """
    try:
        presets.rename(name, new_name)
        click.echo(f"Successfully renamed '{name}' to '{new_name}'.")

    except ValueError as e:
        raise click.BadArgumentUsage(str(e))

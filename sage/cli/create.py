from textwrap import dedent

import click

from sage.config import presets


@click.command()
@click.argument("name", required=True)
@click.argument("duration", required=True)
def create(name: str, duration: str) -> None:
    """
    Create a preset.
    """
    try:
        presets.create(name, duration)
        click.echo(
            dedent(f"""\
                Successfully created '{name}'!
                Use 'sage timer {name}' to run a timer with your new preset.\
            """)
        )

    except ValueError as e:
        raise click.ClickException(str(e))

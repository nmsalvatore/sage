import click

from sage.clocks.stopwatch import Stopwatch


@click.command()
@click.option("--paused", is_flag=True, help="Start stopwatch in a paused state.")
def stopwatch(**kwargs):
    """
    Start a stopwatch.
    """
    stopwatch = Stopwatch()
    stopwatch.run(**kwargs)

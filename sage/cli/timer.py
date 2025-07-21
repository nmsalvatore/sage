import click

from sage.clocks.timer import Timer


@click.command()
@click.argument("time_string", required=True)
@click.option("--paused", is_flag=True, help="Start timer in a paused state.")
@click.option("--test", is_flag=True, hidden=True)
def timer(test, **kwargs):
    """
    Start a timer.
    """
    try:
        timer = Timer()
        if test:
            time_string = kwargs.get("time_string", "")
            timer.print_duration(time_string)
            return
        timer.run(**kwargs)

    except ValueError as e:
        raise click.BadArgumentUsage(str(e))

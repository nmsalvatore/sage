import click


@click.group()
@click.version_option()
def cli():
    pass

@cli.command()
@click.option("-h", "--hours", type=int)
@click.option("-m", "--minutes", type=int)
@click.option("-s", "--seconds", type=int)
def timer(hours=0, minutes=0, seconds=0):
    click.echo(f"{seconds} seconds")

@cli.command()
def stopwatch():
    pass


if __name__ == "__main__":
    cli()

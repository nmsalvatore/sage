import click


@click.group()
@click.version_option()
def fizz():
    pass

@fizz.command()
@click.option("-h", "--hours", type=int)
@click.option("-m", "--minutes", type=int)
@click.option("-s", "--seconds", type=int)
def timer(hours=0, minutes=0, seconds=0):
    click.echo(f"{seconds} seconds")

@fizz.command()
def stopwatch():
    pass


if __name__ == "__main__":
    fizz()

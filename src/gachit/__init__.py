import click


@click.group()
def main() -> int:
    return 0


@main.command()
def status() -> int:
    click.echo("status")
    return 0

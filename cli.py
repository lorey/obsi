import click


@click.group()
def cli():
    print("test")


@cli.command()
def run():
    print("hello")

if __name__ == '__main__':
    cli()
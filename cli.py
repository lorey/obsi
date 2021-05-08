from collections import defaultdict

import click

from obsi.markdown import create_index
from obsi.storage import gen_notes


@click.group()
def cli():
    print("obsi started")


@cli.command()
def run():
    notes_per_tag = defaultdict(list)
    notes_untagged = []
    for note in gen_notes("/notes/"):
        for tag in note.tags:
            notes_per_tag[tag].append(note)

        if not note.tags:
            notes_untagged.append(note)

        print(note)
        print(note.tags)
        print()

    for tag, notes in notes_per_tag.items():
        print(create_index(tag, notes), "\n\n")

    print(create_index("untagged notes", notes_untagged))


if __name__ == "__main__":
    cli()

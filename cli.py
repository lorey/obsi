from collections import defaultdict

import click

from obsi.markdown import create_index
from obsi.storage import gen_notes

NOTES_PATH = "/notes/"


@click.group()
def cli():
    print("obsi started")


@cli.command()
def run():
    for index in generate_indexes():
        print(index, "\n\n")


def generate_indexes(untagged_index=True):
    notes_per_tag = defaultdict(set)
    notes_untagged = []
    for note in gen_notes(NOTES_PATH):
        for tag in note.tags:
            notes_per_tag[tag].add(note)

        if not note.tags:
            notes_untagged.append(note)

        print(note)
        print(note.tags)
        print()

    for tag, notes in notes_per_tag.items():
        yield create_index(tag, notes)

    if untagged_index:
        yield create_index("untagged notes", notes_untagged)


if __name__ == "__main__":
    cli()

from collections import defaultdict

import click

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
        print(tag)
        for note in notes:
            print(f"- {note}")
        print()

    print('untagged notes')
    for note in notes_untagged:
        print(f"- {note}")


if __name__ == "__main__":
    cli()

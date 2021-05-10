from collections import defaultdict
from pathlib import Path

import click

from obsi.markdown import create_index, create_note_list
from obsi.ml import generate_tag_recommendations
from obsi.storage import gen_notes

NOTES_PATH = "/notes/"


@click.group()
def cli():
    print("obsi started")


@cli.command()
def run():
    notes = list(gen_notes(NOTES_PATH))
    for tag, notes_rec in generate_tag_recommendations(notes):
        content = create_note_list(tag, notes_rec)
        with open("out/recommendations-" + tag.lower().replace("#", ""), "w") as file:
            file.write(content)
        print(tag)
        print(notes_rec, "\n\n")
    # update_indexes()


def update_indexes():
    for filename, content in generate_indexes():
        path = Path("out/").joinpath(filename)
        with path.open("w") as file:
            file.write(content)


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
        filename = "index-" + tag.lower().replace("#", "")
        yield filename, create_index(tag, notes)

    if untagged_index:
        yield "index-untagged", create_index("untagged notes", notes_untagged)


if __name__ == "__main__":
    cli()

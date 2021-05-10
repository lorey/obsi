import logging
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

import click

from obsi import markdown
from obsi.markdown import create_day, create_index, create_note_list
from obsi.ml import generate_tag_recommendations
from obsi.storage import gen_notes

NOTES_PATH = "/notes/"


@click.group()
def cli():
    print("obsi started")


@cli.command()
def run():
    update_days()
    update_recommendations()
    update_indexes()


def update_days():
    for i in range(-100, 100):
        date = (datetime.now() + timedelta(days=i)).date()
        content = create_day(date)
        day_path = Path("out/calendar/days/" + date.strftime(markdown.DAY_FORMAT))
        if not day_path.is_file():
            day_path.parent.mkdir(parents=True, exist_ok=True)
            with day_path.open("w") as file:
                logging.info(f"generate {day_path}")
                file.write(content)
        else:
            logging.warning(f"{day_path} already exists, skipping")


def update_recommendations():
    notes = list(gen_notes(NOTES_PATH))
    for tag, notes_rec in generate_tag_recommendations(notes):
        content = create_note_list(tag, notes_rec)
        with open("out/recommendations-" + tag.lower().replace("#", ""), "w") as file:
            logging.info(f"generate recommendations for {tag}")
            file.write(content)


def update_indexes():
    for filename, content in generate_indexes():
        path = Path("out/").joinpath(filename)
        with path.open("w") as file:
            logging.info("generate index {filename}")
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
    logging.basicConfig(level=logging.INFO)
    cli()

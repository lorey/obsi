"""
obsi command line interface.
"""

import logging
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

import click

from obsi.anki import generate_anki_deck
from obsi.markdown import create_day, create_index, create_note_list, create_week
from obsi.ml import generate_tag_recommendations
from obsi.storage import Vault, day_date_to_path, day_date_to_week_path

DAY_GENERATION_PADDING = 10
WEEK_GENERATION_PADDING = 5

NOTES_PATH = "/notes/"
OUTPUT_PATH = "/output/"

@click.group()
def cli():
    """
    This is the obsi command line interface. Use it to work with your vault.
    """
    print("obsi started")


@cli.command()
def run():
    """
    Run all the functionality at once. Just do this if you're unsure, nothing can go wrong.
    """
    update_days()
    update_weeks()
    update_recommendations()
    update_indexes()


@cli.command()
def anki_deck():
    """
    Generate an (updatable) anki deck for your notes.
    """
    name = f"Obsi notes for {NOTES_PATH}"
    vault = Vault(NOTES_PATH)
    notes = list(vault.generate_notes())
    generate_anki_deck(name, notes, out_file=Path(OUTPUT_PATH).joinpath("deck.apkg"))


def update_days(padding=DAY_GENERATION_PADDING):
    """
    Generates all days for the given padding.
    :param padding: generate n days behind and ahead of current date.
    """
    for i in range(-padding, padding):
        date = (datetime.now() + timedelta(days=i)).date()
        content = create_day(date)
        day_path = Path(OUTPUT_PATH).joinpath(day_date_to_path(date))
        if not day_path.is_file():
            day_path.parent.mkdir(parents=True, exist_ok=True)
            with day_path.open("w") as file:
                logging.info(f"generate {day_path}")
                file.write(content)
        else:
            logging.warning(f"{day_path} already exists, skipping")


def update_weeks(padding=WEEK_GENERATION_PADDING):
    """
    Generate weeks for the given padding.
    :param padding: generate n weeks around current date.
    """
    for i in range(-padding, padding):
        date = (datetime.now() + timedelta(weeks=i)).date()
        content = create_week(date)
        week_path = Path(OUTPUT_PATH).joinpath(day_date_to_week_path(date))
        if not week_path.is_file():
            week_path.parent.mkdir(parents=True, exist_ok=True)
            with week_path.open("w") as file:
                logging.info(f"generate {week_path}")
                file.write(content)
        else:
            logging.warning(f"{week_path} already exists, skipping")


def update_recommendations():
    notes = list(get_vault().generate_notes())
    for tag, notes_rec in generate_tag_recommendations(notes):
        logging.info(f"generate recommendations for {tag}")
        content = create_note_list(tag, notes_rec)
        filename = f'recommendations-{tag_to_filepart(tag)}.md'
        with Path(OUTPUT_PATH).joinpath(filename).open('w') as file:
            file.write(content)


def update_indexes():
    for filename, content in generate_indexes():
        path = Path(OUTPUT_PATH).joinpath(filename)
        with path.open("w") as file:
            logging.info(f"generate index {filename}")
            file.write(content)


def generate_indexes(untagged_index=True):
    notes_per_tag = defaultdict(set)
    notes_untagged = []
    for note in get_vault().generate_notes():
        for tag in note.tags:
            notes_per_tag[tag].add(note)

        if not note.tags:
            notes_untagged.append(note)

    for tag, notes in notes_per_tag.items():
        filename = f"index-{tag_to_filepart(tag)}.md"
        yield filename, create_index(tag, notes)

    if untagged_index:
        yield "index-untagged.md", create_index("untagged notes", notes_untagged)

def tag_to_filepart(tag):
    """
    Use a tag as part of a filename.
    :param tag:
    :return:
    """
    return tag.lower().replace("#", "")


def get_vault():
    return Vault(NOTES_PATH)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    cli()

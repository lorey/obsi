import logging
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

import click

from obsi.markdown import create_day, create_index, create_note_list, create_week
from obsi.ml import generate_tag_recommendations
from obsi.storage import day_date_to_path, day_date_to_week_path, gen_notes

DAY_GENERATION_PADDING = 100
WEEK_GENERATION_PADDING = 52

NOTES_PATH = "/notes/"


@click.group()
def cli():
    print("obsi started")


@cli.command()
def run():
    update_days()
    update_weeks()
    update_recommendations()
    update_indexes()


def update_days(padding=DAY_GENERATION_PADDING):
    """
    Generates all days for the given padding.
    :param padding: generate n days behind and ahead of current date.
    """
    for i in range(-padding, padding):
        date = (datetime.now() + timedelta(days=i)).date()
        content = create_day(date)
        day_path = Path("out").joinpath(day_date_to_path(date))
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
        week_path = Path("out").joinpath(day_date_to_week_path(date))
        if not week_path.is_file():
            week_path.parent.mkdir(parents=True, exist_ok=True)
            with week_path.open("w") as file:
                logging.info(f"generate {week_path}")
                file.write(content)
        else:
            logging.warning(f"{week_path} already exists, skipping")


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
            logging.info(f"generate index {filename}")
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

"""
obsi command line interface.
"""

import logging
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

import click

from obsi.anki import generate_anki_deck
from obsi.markdown import render_day, render_index, render_note_list, render_week, render_month, render_year
from obsi.ml import generate_tag_recommendations
from obsi.storage import Vault, day_date_to_path, day_date_to_week_path

DAY_GENERATION_PADDING = 10
WEEK_GENERATION_PADDING = 5

NOTES_PATH = "/notes/"
OUTPUT_PATH = "/output/"

STUB_LENGTH_THRESHOLD = 100


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
    update_calendar()
    update_recommendations()
    update_indexes()
    update_stubs()


def update_calendar():
    years = range(2000, 2030)

    update_days()
    update_weeks()
    update_years(years=years)
    update_months(years=years)

def update_years(years):
    for year in years:
        year_path = Path(OUTPUT_PATH).joinpath(f'calendar/years/{year}.md')
        year_path.parent.mkdir(exist_ok=True, parents=True)
        with year_path.open('w') as file:
            file.write(render_year(year))

def update_months(years):
    for year in years:
        for i in range(1, 12):
            month_path = Path(OUTPUT_PATH).joinpath(f'calendar/months/{year}-{i:02}.md')
            month_path.parent.mkdir(exist_ok=True, parents=True)
            month_date_first = datetime(year, i, 1)
            with month_path.open('w') as file:
                file.write(render_month(year, i))



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
        content = render_day(date)
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
        content = render_week(date)
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
        filename = f"recommendations-{tag_to_filepart(tag)}.md"
        with Path(OUTPUT_PATH).joinpath(filename).open("w") as file:
            file.write(render_note_list(tag, notes_rec))


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
        yield filename, render_index(tag, notes)

    if untagged_index:
        yield "index-untagged.md", render_index("untagged notes", notes_untagged)


def update_stubs():
    """
    This will generate a list of stubs (short notes).
    """
    stubs = [
        note
        for note in get_vault().generate_notes()
        if len(note.content) < STUB_LENGTH_THRESHOLD
    ]
    with Path(OUTPUT_PATH).joinpath("stubs.md").open("w") as file:
        file.write(render_note_list("Stubs", stubs))


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

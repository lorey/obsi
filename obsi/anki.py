"""
module to generate Anki decks from notes.
"""
import html
import logging

import genanki


class FileBasedNote(genanki.Note):
    """
    Anki note based on a Vault file.
    """

    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # use the path as the unique identifier
        # ensures that cards that keep their path get updated in place
        self._guid = genanki.guid_for(path)


def generate_anki_deck(name, notes, out_file="output.apkg"):
    """
    Generate an anki deck .apkg file from the given notes.

    :param name: name of the deck
    :param notes: notes to use for generation
    :param out_file: path of resulting file
    """
    # generate the deck
    anki_deck = genanki.Deck(2059400110, html.escape(name))

    # set a model
    anki_model = genanki.Model(
        1607392319,
        "File-based Card",
        fields=[
            {"name": "Path"},
            {"name": "ObsidianUri"},
        ],
        templates=[
            {
                "name": "Card 1",
                "qfmt": "What do you know about {{Path}}",
                "afmt": '{{FrontSide}}<hr id="answer"><a href="{{ObsidianUri}}">open note</a>',
            }
        ],
    )

    for note in notes:
        anki_node = FileBasedNote(
            path=note,
            model=anki_model,
            fields=[
                html.escape(str(note.get_relative_path())),
                html.escape(note.get_obsidian_uri()),
            ],
        )
        anki_deck.add_note(anki_node)

    genanki.Package(anki_deck).write_to_file(out_file)
    logging.info(f".apkg written to {out_file=}")

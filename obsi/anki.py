"""
module to generate Anki decks from notes.
"""
import html
import logging
import re

import genanki

from obsi.storage import Note


class FileBasedNote(genanki.Note):
    """
    Anki note based on a Vault file.
    """

    model = genanki.Model(
        1607392319,
        "Obsi file-based card",
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

    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # use the path as the unique identifier
        # ensures that cards that keep their path get updated in place
        self._guid = genanki.guid_for(path)

    @classmethod
    def from_note(cls, note: Note):
        return FileBasedNote(
            path=note.get_relative_path(),
            model=cls.model,
            fields=[
                html.escape(str(note.get_relative_path())),
                html.escape(note.get_obsidian_uri()),
            ],
        )


class InlineNote(genanki.Note):
    """
    Anki note based on a inline block.
    """

    model = genanki.Model(
        1607392320,
        "Obsi inline card",
        fields=[
            {"name": "Path"},
            {"name": "ObsidianUri"},
            {"name": "Question"},
            {"name": "Answer"},
        ],
        templates=[
            {
                "name": "Card 1",
                "qfmt": "{{Question}}",
                "afmt": '{{FrontSide}}<hr id="answer">{{Answer}}<br><a href="{{ObsidianUri}}">open note</a>',
            }
        ],
    )

    @property
    def guid(self):
        # id by path and question
        return genanki.guid_for(self.fields[0], self.fields[2])

    @classmethod
    def from_q_and_a(cls, note, q, a):
        return InlineNote(
            model=cls.model,
            fields=[
                html.escape(str(note.get_relative_path())),
                html.escape(note.get_obsidian_uri()),
                html.escape(q),
                html.escape(a),
            ],
        )


def generate_anki_deck(name, notes, out_file="output.apkg"):
    """
    Generate an anki deck .apkg file from the given notes.

    :param name: name of the deck
    :param notes: notes to use for generation
    :param out_file: path of resulting file
    """
    # generate the deck
    anki_deck = genanki.Deck(2059400110, html.escape(name))

    for note in notes:
        anki_file_note = FileBasedNote.from_note(note)
        anki_deck.add_note(anki_file_note)

    for note in notes:
        extracted_notes = extract_anki_notes_from_markdown(note.content)
        for note_data in extracted_notes:
            logging.info(f"found inline cards in {note}: {extracted_notes}")
            anki_inline_note = InlineNote.from_q_and_a(
                note, note_data["question"], note_data["answer"]
            )
            anki_deck.add_note(anki_inline_note)
        else:
            logging.info(f"no inline cards in {note}")

    genanki.Package(anki_deck).write_to_file(out_file)
    logging.info(f".apkg written to {out_file=}")


def extract_anki_notes_from_markdown(md: str):
    # todo use one regex to find obsi blocks, then match to extract from that line on.
    #      this way, we'd be able to find erroneous blocks
    matches = re.finditer(r"```obsi\nQ: (?P<question>.*)\nA: (?P<answer>.*)\n```", md)
    return [m.groupdict() for m in matches]

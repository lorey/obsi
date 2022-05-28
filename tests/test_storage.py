from pathlib import Path

from obsi.storage import Note


class TestNote:
    def test_duplicate_tags(self):
        note = Note(None, Path("/tmp/note.md"), "#one #two #two #three")
        assert note.tags == {"#one", "#two", "#three"}

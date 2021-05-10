from obsi.storage import Note


class TestNote:
    def test_duplicate_tags(self):
        note = Note("/tmp/note.md", "#one #two #two #three")
        assert note.tags == {"#one", "#two", "#three"}

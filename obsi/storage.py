import re
from pathlib import Path


class Note:
    @classmethod
    def from_path(cls, path):
        content = path_to_content(path)
        return Note(path, content)

    def __init__(self, path, content):
        self._path = path
        self.content = content

    def get_tags(self):
        results = re.findall(r"#[A-z0-9]+", self.content)
        return results

    def get_path(self):
        return self._path

    tags = property(get_tags)
    path = property(get_path)

    def __repr__(self):
        return f"Note({self.path=})"


def gen_notes(path):
    """Generate all notes in a directory."""
    home_path = Path(path)

    # check that path exists
    assert home_path.is_dir()

    for file_path in home_path.rglob("*.md"):
        yield Note.from_path(file_path)


def path_to_content(path):
    with path.open() as file:
        content = file.read()
    return content

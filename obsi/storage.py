import re
import typing
from pathlib import Path
from urllib.parse import urlencode

from obsi import DAY_FORMAT
from obsi.util import week_identifier_from_date


class Vault:
    """
    An obsidian vault.
    """

    path = None

    def __init__(self, path: typing.Union[Path, str]):
        self.path = path if type(path) == Path else Path(path)
        assert self.path.is_dir(), f"{self.path} is not a dir"

    def generate_notes(self):
        """Generate all notes in vault"""
        for file_path in self.path.rglob("*.md"):
            rel_path = file_path.relative_to(self.path)
            yield Note.from_path(self, rel_path)

    def __repr__(self):
        return f"Vault({self.path=})"


class Note:
    """
    A markdown-based note.
    """

    @classmethod
    def from_path(cls, vault: Vault, path: Path):
        path_abs = vault.path.joinpath(path)
        assert path_abs.is_file(), f"no file found at {path_abs}"
        content = path_to_content(path_abs)
        return Note(vault, path, content)

    def __init__(self, vault: Vault, path: Path, content: str):
        self._vault = vault
        self._path = path
        self._content = content

    def get_tags(self):
        results = re.findall(r"#[A-z0-9]+", self._content)
        return set(results)

    def get_absolute_path(self):
        return self._vault.path.joinpath(self._path)

    def get_relative_path(self):
        return self._path

    def get_obsidian_uri(self):
        return "obsidian://open?" + urlencode({"vault": "notes", "file": self._path})

    def get_title(self):
        # todo md title
        # todo frontmatter title
        return self._path.name.replace(".md", "")

    tags = property(get_tags)
    title = property(get_title)

    def __repr__(self):
        return f"Note({self._vault=}, {self._path=})"


def path_to_content(path):
    with path.open() as file:
        content = file.read()
    return content


def day_date_to_path(day):
    return "calendar/days/" + day.strftime(DAY_FORMAT)


def day_date_to_week_path(day):
    return "calendar/weeks/" + week_identifier_from_date(day)

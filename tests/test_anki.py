from obsi.anki import extract_anki_notes_from_markdown

note = "```obsi\nQ: question\nA: answer\n```"


def test_parsing():
    assert extract_anki_notes_from_markdown(note) == [
        {"question": "question", "answer": "answer"}
    ]

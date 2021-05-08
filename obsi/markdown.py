def create_index(title, notes):
    """creates an index of notes"""
    content_rows = [f"# {title}", ""]
    for note in sorted(notes, key=lambda n: n.title):
        content_rows.append(f"- [{note.title}]({note.path})")
    return "\n".join(content_rows)

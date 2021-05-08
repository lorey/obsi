def create_index(title, notes):
    """creates an index of notes"""
    content_rows = [f"# {title}", ""]
    for note in notes:
        content_rows.append(f"- [{note.title}]({note.path})")
    return "\n".join(content_rows)

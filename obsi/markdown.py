from jinja2 import Environment, PackageLoader


def create_index(title, notes):
    """creates an index of notes"""
    env = get_jinja_env()
    index_template = env.get_template("index.md")
    return index_template.render(
        title=title, notes=sorted(notes, key=lambda n: n.title)
    )


def get_jinja_env():
    return Environment(loader=PackageLoader("obsi", "templates"))

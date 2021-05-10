import datetime

from jinja2 import Environment, PackageLoader

DAY_FORMAT = "%Y-%m-%d"
MONTH_FORMAT = "%Y-%m"


def create_index(title, notes):
    """creates an index of notes"""
    return create_note_list(title, notes)


def create_note_list(title, notes):
    """creates a list of notes"""
    env = get_jinja_env()
    index_template = env.get_template("list.md")
    return index_template.render(
        title=title, notes=sorted(notes, key=lambda n: n.title)
    )


def create_day(date: datetime.date):
    def day_date_to_path(day):
        return "calendar/days/" + day.strftime(DAY_FORMAT)

    env = get_jinja_env()
    template = env.get_template("day.md")

    yesterday = date - datetime.timedelta(days=1)
    tomorrow = date + datetime.timedelta(days=1)

    return template.render(
        title=date.strftime(DAY_FORMAT),
        yesterday_path=day_date_to_path(yesterday),
        tomorrow_path=day_date_to_path(tomorrow),
        month_path=f"calendar/months/{date.strftime(MONTH_FORMAT)}",
    )


def get_jinja_env():
    return Environment(loader=PackageLoader("obsi", "templates"))

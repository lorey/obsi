import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from obsi import DAY_FORMAT, MONTH_FORMAT
from obsi.storage import day_date_to_path, day_date_to_week_path
from obsi.util import get_days_in_same_week


def render_index(title: str, notes) -> str:
    """creates an index of notes"""
    return render_note_list(title, notes)


def render_note_list(title: str, notes: list) -> str:
    """creates a list of notes"""
    env = get_jinja_env()
    index_template = env.get_template("list.md")
    return index_template.render(
        title=title, notes=sorted(notes, key=lambda n: n.title)
    )


def render_day(date: datetime.date):
    env = get_jinja_env()
    template = env.get_template("day.md")

    yesterday = date - datetime.timedelta(days=1)
    tomorrow = date + datetime.timedelta(days=1)

    return template.render(
        title=date.strftime(DAY_FORMAT),
        yesterday_path=day_date_to_path(yesterday),
        tomorrow_path=day_date_to_path(tomorrow),
        week_path=day_date_to_week_path(date),
        month_path=f"calendar/months/{date.strftime(MONTH_FORMAT)}",
    )


def render_week(date: datetime.date):
    env = get_jinja_env()
    template = env.get_template("week.md")

    days = get_days_in_same_week(date)
    day_links = {d.strftime("%A, " + DAY_FORMAT): day_date_to_path(d) for d in days}
    return template.render(day_links=day_links)


def get_jinja_env(template_path_raw="templates"):
    template_path = Path(template_path_raw)
    if not template_path.is_dir():
        raise RuntimeError(f"Template directory not found: {template_path}")
    return Environment(loader=FileSystemLoader(template_path))

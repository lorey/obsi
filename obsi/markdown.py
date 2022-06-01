import datetime
import typing
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from obsi import DAY_FORMAT, MONTH_FORMAT
from obsi.storage import day_date_to_path, day_date_to_week_path, get_day_of_year_path
from obsi.util import get_days_in_same_week, week_identifier_from_date


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
        date=date,
        date_of_year_path=get_day_of_year_path(date),
        yesterday_path=day_date_to_path(yesterday),
        tomorrow_path=day_date_to_path(tomorrow),
        week_path=day_date_to_week_path(date),
        month_path=f"calendar/months/{date.strftime(MONTH_FORMAT)}",
    )


def render_day_of_year(month, day):
    env = get_jinja_env()
    template = env.get_template("day-of-year.md")

    pseudo_date = datetime.date(2020, month, day)
    wikipedia_url = f'https://en.wikipedia.org/wiki/{pseudo_date.strftime("%B")}_{pseudo_date.strftime(pseudo_date.strftime("%d"))}'
    return template.render(pseudo_date=pseudo_date, wikipedia_url=wikipedia_url)


def render_week(date: datetime.date):
    env = get_jinja_env()
    template = env.get_template("week.md")

    days = get_days_in_same_week(date)
    day_links = {d.strftime("%A, " + DAY_FORMAT): day_date_to_path(d) for d in days}
    return template.render(title=week_identifier_from_date(date), day_links=day_links)


def render_month(
    year: int,
    month: int,
    get_month_uri: typing.Callable[[int, int], str],
    get_year_uri: typing.Callable[[int], str],
):
    """
    Render a monthly note
    :param year: year
    :param month: month indexed regularly from 1-12
    :param get_month_uri: callable to generate month link
    :param get_year_uri: callable to generate year link
    :return: markdown note
    """
    env = get_jinja_env()
    template = env.get_template("month.md")

    next_month_date = datetime.date(year, month, 1) + datetime.timedelta(days=31)
    last_month_date = datetime.date(year, month, 1) - datetime.timedelta(days=1)
    return template.render(
        first_day=datetime.date(year, month, 1),
        last_month_link=f"[last month]({get_month_uri(last_month_date.year, last_month_date.month)})",
        next_month_link=f"[next month]({get_month_uri(next_month_date.year, next_month_date.month)})",
        year_link=f"[year]({get_year_uri(year)})",
    )


def render_year(
    year: int,
    get_year_uri: typing.Callable[[int], str],
):
    """
    Render a yearly note
    :param year: year
    :param get_year_uri:
    :return: markdown note
    """
    env = get_jinja_env()
    template = env.get_template("year.md")

    return template.render(
        first_day=datetime.date(year, 1, 1),
        previous_year_link=render_markdown_link(get_year_uri(year - 1), "last year"),
        next_year_link=render_markdown_link(get_year_uri(year + 1), "last year"),
    )


def render_markdown_link(uri, title=None):
    """
    create a hyperlink from a title and a path.
    :param title: title of the link
    :param uri: uri
    """
    return f"[{title if title else 'link'}]({uri})"


def get_jinja_env(template_path_raw="templates"):
    template_path = Path(template_path_raw)
    if not template_path.is_dir():
        raise RuntimeError(f"Template directory not found: {template_path}")
    return Environment(loader=FileSystemLoader(template_path))

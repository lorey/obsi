from datetime import datetime
from pathlib import Path

import cli
from obsi.storage import day_date_to_path, get_month_link


def test_update_calendar():
    # todo this will break on live systems, we need to make the out directory a parameter
    out_directory = Path(cli.OUTPUT_PATH)
    cli.update_calendar()
    today = datetime.today()
    assert out_directory.joinpath(day_date_to_path(today)).is_file()
    for i in range(1, 13):
        month_link = get_month_link(today.year, i)
        if not out_directory.joinpath(month_link).is_file():
            raise AssertionError(f"{month_link} was not generated")

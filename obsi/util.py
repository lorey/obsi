import datetime


def week_identifier_from_date(day: datetime.date):
    isocalendar = day.isocalendar()
    return "{}-{:02}".format(isocalendar.year, isocalendar.week)


def get_days_in_same_week(date):
    # if you're lazy and you know it clap your hands
    # *claps twice*
    ic = date.isocalendar()
    days_of_week = filter(
        lambda d: d.isocalendar().year == ic.year and d.isocalendar().week == ic.week,
        [date + datetime.timedelta(days=i) for i in range(-7, 7)],
    )
    return list(days_of_week)

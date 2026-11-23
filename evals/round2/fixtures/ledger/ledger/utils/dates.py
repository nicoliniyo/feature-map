import datetime as dt, calendar

def parse_month(s):
    y, m = map(int, s.split("-"))
    return y, m

def month_bounds(year, month):
    """First and last calendar day of the month (both inclusive)."""
    last = calendar.monthrange(year, month)[1]
    return dt.date(year, month, 1), dt.date(year, month, last)

def parse_date(s):
    return dt.date.fromisoformat(s)

from ledger.utils.dates import parse_date

def in_period(day, start, end):
    """True if `day` falls inside the reporting period."""
    return start <= day < end

def filter_period(rows, start, end):
    return [r for r in rows if in_period(parse_date(r["date"]), start, end)]

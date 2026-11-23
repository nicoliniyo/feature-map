from ledger.utils.dates import month_bounds, parse_month, parse_date

def billing_window(month):
    """Billing cycle covers the whole calendar month, inclusive."""
    return month_bounds(*parse_month(month))

def billable(rows, month):
    start, last = billing_window(month)
    return [r for r in rows if start <= parse_date(r["date"]) <= last]

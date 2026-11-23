from ledger.utils.dates import month_bounds, parse_month
from ledger.utils.io import read_rows
from ledger.utils.money import to_money
from ledger.reports.period import filter_period

def monthly_summary(path, month):
    start, end = month_bounds(*parse_month(month))
    rows = filter_period(read_rows(path), start, end)
    total = sum((to_money(r["amount"]) for r in rows), to_money(0))
    return {"month": month, "sales": len(rows), "total": total}

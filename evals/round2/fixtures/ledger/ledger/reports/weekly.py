import datetime as dt
from ledger.utils.io import read_rows
from ledger.utils.money import to_money
from ledger.utils.dates import parse_date

def weekly_summary(path, monday):
    start = parse_date(monday); end = start + dt.timedelta(days=7)
    rows = [r for r in read_rows(path) if start <= parse_date(r["date"]) < end]
    return {"week": monday, "sales": len(rows), "total": sum((to_money(r["amount"]) for r in rows), to_money(0))}

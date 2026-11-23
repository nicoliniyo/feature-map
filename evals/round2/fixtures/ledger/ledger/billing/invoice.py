from ledger.utils.io import read_rows
from ledger.utils.money import to_money
from ledger.billing.period import billable

def invoice_totals(path, month):
    out = {}
    for r in billable(read_rows(path), month):
        out[r["customer"]] = out.get(r["customer"], to_money(0)) + to_money(r["amount"])
    return out

import sys
from ledger.utils.config import DEFAULTS
from ledger.utils.money import fmt

def main(argv=None):
    argv = argv or sys.argv[1:]
    cmd = argv[0]
    path = DEFAULTS["data"]
    if cmd == "monthly":
        from ledger.reports.monthly import monthly_summary
        s = monthly_summary(path, argv[1]); print(f"{s['month']}: {s['sales']} sales, {fmt(s['total'])}")
    elif cmd == "invoices":
        from ledger.billing.invoice import invoice_totals
        for c, t in sorted(invoice_totals(path, argv[1]).items()): print(f"{c}: {fmt(t)}")
    elif cmd == "weekly":
        from ledger.reports.weekly import weekly_summary
        s = weekly_summary(path, argv[1]); print(f"week of {s['week']}: {s['sales']} sales, {fmt(s['total'])}")
    else:
        print("usage: python3 -m ledger.cli monthly|invoices|weekly <arg>"); return 2

if __name__ == "__main__":
    sys.exit(main())

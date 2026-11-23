import sys, os, csv, json, subprocess, datetime as dt
from decimal import Decimal
d, G = sys.argv[1], os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(G, "../fixtures/ledger/data/sales.csv"))))
def expect(y, m):
    rs = [r for r in rows if r["date"].startswith(f"{y}-{m:02d}")]
    return len(rs), sum(Decimal(r["amount"]) for r in rs)
def run(*a): return subprocess.run(["python3", "-m", "ledger.cli", *a], cwd=d, capture_output=True, text=True).stdout
res = {}
for y, m in [(2026, 9), (2026, 10), (2026, 11)]:
    n, t = expect(y, m); res[f"monthly {y}-{m:02d} correct"] = run("monthly", f"{y}-{m:02d}").strip() == f"{y}-{m:02d}: {n} sales, ${t:,.2f}"
inv = "".join(run("invoices", f"2026-{m}") for m in ("09", "10", "11"))
res["invoices unchanged"] = inv == open(os.path.join(G, "expected_invoices.txt")).read()
res["weekly unchanged"] = run("weekly", "2026-10-26") == open(os.path.join(G, "expected_weekly.txt")).read()
print(json.dumps(res, indent=1)); print("PASS" if all(res.values()) else "FAIL")

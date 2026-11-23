from collections import Counter
from ledger.utils.io import read_rows
from ledger.utils.money import to_money
def top_customers(path, n=5):
    c = Counter()
    for r in read_rows(path): c[r["customer"]] += to_money(r["amount"])
    return c.most_common(n)

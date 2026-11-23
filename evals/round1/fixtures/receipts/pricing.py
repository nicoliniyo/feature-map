TAX = {"north": 0.08, "south": 0.06}
COUPONS = {"SAVE10": 0.10, "WELCOME5": 0.05}
LEGACY_ALIASES = {"save10": "SAVE10"}  # codes printed on old flyers

def line_total(item):
    return item["qty"] * item["unit_price"]

def apply_coupon(amount, code):
    if not code:
        return amount
    if code in LEGACY_ALIASES:
        amount = amount * (1 - COUPONS[LEGACY_ALIASES[code]])
    norm = code.strip().upper()
    if norm in COUPONS:
        amount = amount * (1 - COUPONS[norm])
    return amount

def add_tax(amount, region):
    return amount * (1 + TAX.get(region, 0.0))

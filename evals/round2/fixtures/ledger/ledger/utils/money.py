from decimal import Decimal, ROUND_HALF_UP
def to_money(x):
    return Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
def fmt(d):
    return f"${d:,.2f}"

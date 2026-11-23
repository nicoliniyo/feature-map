from ledger.utils.money import to_money
def late_fee(balance, days_late):
    return to_money(balance) * to_money("0.015") if days_late > 30 else to_money(0)

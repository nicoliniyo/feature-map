from ledger.tax.rates import RATES
def tax_for(amount, country):
    return amount * RATES.get(country, 0)

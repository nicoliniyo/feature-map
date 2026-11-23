def value(items):
    return sum(i['qty'] * i['cost'] for i in items)

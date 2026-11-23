def find(customers, cid):
    return next((c for c in customers if c.cid == cid), None)

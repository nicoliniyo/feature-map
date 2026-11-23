"""Print a receipt for an order: python receipt.py data/orders.json <order_id>"""
import json, sys
from pricing import line_total, apply_coupon, add_tax

def build_receipt(order):
    subtotal = sum(line_total(i) for i in order["items"])
    discounted = apply_coupon(subtotal, order.get("coupon"))
    total = add_tax(discounted, order["region"])
    return {"id": order["id"], "subtotal": round(subtotal, 2),
            "after_coupon": round(discounted, 2), "total": round(total, 2)}

def main():
    path, oid = sys.argv[1], int(sys.argv[2])
    orders = {o["id"]: o for o in json.load(open(path))}
    r = build_receipt(orders[oid])
    for k, v in r.items():
        print(f"{k:>13}: {v}")

if __name__ == "__main__":
    main()

"""Shipping quote for a cart: python3 quote.py carts/<file>.json"""
import json, sys

FREE_THRESHOLD = 50.0
FLAT_RATE = 7.95

def subtotal(cart):
    return sum(item["price"] * item.get("qty", 1) for item in cart["items"])

def shipping_for(cart):
    if subtotal(cart) > FREE_THRESHOLD:
        return 0.0
    return FLAT_RATE

if __name__ == "__main__":
    cart = json.load(open(sys.argv[1]))
    print(f"subtotal: {subtotal(cart):.2f}  shipping: {shipping_for(cart):.2f}")

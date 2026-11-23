import sys, json, importlib
sys.path.insert(0, sys.argv[1]); q = importlib.import_module("quote")
c = lambda *p: {"items": [{"price": x} for x in p]}
res = {
 "ticket cart c-881 (16.40+33.30+0.30) free": q.shipping_for(c(16.40, 33.30, 0.30)) == 0.0,
 "exactly 50.00 free": q.shipping_for({"items": [{"price": 25.0, "qty": 2}]}) == 0.0,
 "49.99 charged": q.shipping_for(c(49.99)) == 7.95,
 "80 free": q.shipping_for(c(80)) == 0.0,
 "empty cart charged": q.shipping_for({"items": []}) == 7.95,
}
print(json.dumps(res, indent=1)); print("PASS" if all(res.values()) else "FAIL")

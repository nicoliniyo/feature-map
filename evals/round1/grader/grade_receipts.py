import sys, importlib, json
sys.path.insert(0, sys.argv[1]); p = importlib.import_module("pricing")
checks = {
 "lowercase == uppercase":   abs(p.apply_coupon(100, "save10") - 90) < 1e-9,
 "uppercase still 10%":      abs(p.apply_coupon(100, "SAVE10") - 90) < 1e-9,
 "padded code works":        abs(p.apply_coupon(100, " Save10 ") - 90) < 1e-9,
 "welcome5 lowercase 5%":    abs(p.apply_coupon(100, "welcome5") - 95) < 1e-9,
 "no coupon unchanged":      p.apply_coupon(100, None) == 100,
 "unknown code unchanged":   p.apply_coupon(100, "BOGUS") == 100,
 "tax unchanged":            abs(p.add_tax(100, "north") - 108) < 1e-9,
}
print(json.dumps(checks, indent=1)); print("PASS" if all(checks.values()) else "FAIL")

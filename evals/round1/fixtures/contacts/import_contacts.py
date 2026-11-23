"""Clean a contacts CSV: python import_contacts.py <in.csv> <out.csv>"""
import csv, sys

def normalize(email):
    return email.strip().lower()

def dedupe(rows):
    seen = []
    out = []
    for r in rows:
        e = normalize(r["email"])
        if e in seen:
            continue
        seen.append(e)
        out.append({"name": r["name"].strip(), "email": e})
    return out

def main():
    src, dst = sys.argv[1], sys.argv[2]
    with open(src, newline="") as f:
        rows = list(csv.DictReader(f))
    cleaned = dedupe(rows)
    with open(dst, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["name", "email"])
        w.writeheader(); w.writerows(cleaned)
    print(f"{len(rows)} rows in, {len(cleaned)} rows out")

if __name__ == "__main__":
    main()

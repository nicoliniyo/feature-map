import csv
def write(path, rows, fields):
    with open(path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)

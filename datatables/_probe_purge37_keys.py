"""Probe the pre-purge #37 rollback dump: were the 11 str columns already set to the row key?"""
import csv
import collections

PATH = r"datatables/_rollback/20261004_234510_purge37_rows.csv"
COLS = [74, 77, 79, 81, 87, 89, 91, 93, 95, 98, 100]

with open(PATH, newline="", encoding="utf-8") as fh:
    rows = list(csv.reader(fh))

hdr, data = rows[0], rows[1:]
print(f"header cols: {len(hdr)}  data rows: {len(data)}")

story = collections.Counter()
for r in data:
    key = r[1] if len(r) > 1 else ""
    for c in COLS:
        cell = r[c] if len(r) > c else ""
        if cell == "":
            story[(c, "EMPTY")] += 1
        elif cell == key:
            story[(c, "==row key")] += 1
        else:
            story[(c, "OTHER")] += 1
            if story[(c, "OTHER")] <= 2:
                print(f"  col{c} OTHER: key={key!r} cell={cell!r}")

for c in COLS:
    e = story[(c, "EMPTY")]
    k = story[(c, "==row key")]
    o = story[(c, "OTHER")]
    print(f"col{c:>4}: empty={e:<6} ==key={k:<6} other={o}")

import sys
import csv

reader = csv.reader(sys.stdin)
header_skipped = False

for row in reader:
    if not row:
        continue
    if not header_skipped:
        header_skipped = True
        continue
    if len(row) < 3:
        continue
    try:
        city = row[2].strip()
        if city:
            print(f"{city}\t1")
    except:
        continue

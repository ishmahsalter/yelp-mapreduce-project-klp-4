import sys
import csv

reader = csv.reader(sys.stdin)
header_skipped = False

for row in reader:
    if not row:
        continue

    # skip header
    if not header_skipped:
        header_skipped = True
        continue

    # pastikan jumlah kolom cukup
    if len(row) < 9:
        continue

    try:
        date = row[8].strip()
        year = date[:4]

        if year.isdigit():
            print(f"{year}\t1")

    except:
        continue
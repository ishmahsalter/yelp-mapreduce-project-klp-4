import sys

header_skipped = False
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    if not header_skipped:
        header_skipped = True
        continue
    parts = line.split(',')
    if len(parts) >= 4:
        stars = parts[3].strip()
        if '.' in stars:
            stars = stars.split('.')[0]
        print(f"{stars}\t1")
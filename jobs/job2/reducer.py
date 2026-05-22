import sys

current_year = None
total = 0

for line in sys.stdin:
    line = line.strip()

    if not line:
        continue

    parts = line.split('\t', 1)

    if len(parts) != 2:
        continue

    try:
        year = parts[0]
        count = int(parts[1])

    except:
        continue

    if current_year == year:
        total += count

    else:
        if current_year is not None:
            print(f"{current_year}\t{total}")

        current_year = year
        total = count

if current_year is not None:
    print(f"{current_year}\t{total}")
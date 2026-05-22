import sys

current_stars = None
current_count = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split('\t', 1)
    if len(parts) != 2:
        continue
    stars, count = parts
    try:
        count = int(count)
    except ValueError:
        continue
    if current_stars == stars:
        current_count += count
    else:
        if current_stars is not None:
            print(f"{current_stars}\t{current_count}")
        current_stars = stars
        current_count = count

if current_stars is not None:
    print(f"{current_stars}\t{current_count}")
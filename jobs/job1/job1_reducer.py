import sys

current_stars = None
current_count = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
        
    stars, count = line.split('\t', 1)
    try:
        count = int(count)
    except ValueError:
        continue

    if current_stars == stars:
        current_count += count
    else:
        if current_stars:
            print(f"{current_stars}\t{current_count}")
        current_stars = stars
        current_count = count

if current_stars == stars:
    print(f"{current_stars}\t{current_count}")
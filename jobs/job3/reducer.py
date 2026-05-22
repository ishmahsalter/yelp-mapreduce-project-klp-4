import sys

current_city = None
total = 0
city_counts = []

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split('\t', 1)
    if len(parts) != 2:
        continue
    try:
        city = parts[0]
        count = int(parts[1])
    except:
        continue
    if current_city == city:
        total += count
    else:
        if current_city is not None:
            city_counts.append((total, current_city))
        current_city = city
        total = count

if current_city is not None:
    city_counts.append((total, current_city))

city_counts.sort(reverse=True)

for i in range(min(20, len(city_counts))):
    print(f"{city_counts[i][1]}\t{city_counts[i][0]}")

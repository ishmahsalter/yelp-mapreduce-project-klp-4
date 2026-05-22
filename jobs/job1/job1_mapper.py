import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    parts = line.split(',')
    if len(parts) >= 3:
        stars = parts[2].strip()
        
        if '.' in stars:
            stars = stars.split('.')[0]
            
        print(f"{stars}\t1")
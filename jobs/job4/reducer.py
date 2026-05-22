#!/usr/bin/env python
import sys

def reducer():
    current_kategori = None
    total_rating = 0.0
    total_count = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            
            kategori, val_data = line.split('\t', 1)
            stars_str, count_str = val_data.split(',')
            rating = float(stars_str)
            count = int(count_str)
        except ValueError:
            continue

        
        if current_kategori == kategori:
            total_rating += rating
            total_count += count
        else:
            if current_kategori:
                
                avg_rating = total_rating / total_count
                print(f"{current_kategori}\t{avg_rating:.2f}")
            
            current_kategori = kategori
            total_rating = rating
            total_count = count

    
    if current_kategori is not None and total_count > 0:
        avg_rating = total_rating / total_count
        print(f"{current_kategori}\t{avg_rating:.2f}")

if __name__ == "__main__":
    reducer()
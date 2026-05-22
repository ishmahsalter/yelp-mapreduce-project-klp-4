#!/usr/bin/env python
import sys
import csv

def mapper():
    
    reader = csv.reader(sys.stdin)
    
    for row in reader:
        
        if not row or row[0] == 'business_id':
            continue
            
        try:
            
            
            stars = row[5]  
            categories = row[8]
            
            if categories and stars:
                rating = float(stars)
                
                list_kategori = [c.strip() for c in categories.split(',')]
                
                for kategori in list_kategori:
                    if kategori:
                        
                        
                        print(f"{kategori}\t{rating},1")
        except (ValueError, IndexError):
            
            continue

if __name__ == "__main__":
    mapper()
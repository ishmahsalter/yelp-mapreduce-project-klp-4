import json
import csv
import os
import time

# ============================================================
# PREPROCESSING YELP DATASET
# Ishmah Nurwasilah - H071241019
# Big Data Praktikum 2026
# ============================================================

# PATH KONFIGURASI
REVIEW_INPUT  = r"C:\yelp_dataset\yelp_academic_dataset_review.json"
BUSINESS_INPUT = r"C:\yelp_dataset\yelp_academic_dataset_business.json"
REVIEW_OUTPUT  = r"C:\yelp_dataset\yelp_review_clean.csv"
BUSINESS_OUTPUT = r"C:\yelp_dataset\yelp_business_clean.csv"

# Target ukuran review CSV = 1.3 GB
TARGET_SIZE_BYTES = 1.3 * 1024 * 1024 * 1024

# ============================================================
# PREPROCESSING REVIEW
# ============================================================
def preprocess_review():
    print("=" * 60)
    print("PREPROCESSING: yelp_academic_dataset_review.json")
    print("=" * 60)
    
    start = time.time()
    
    kolom = ['review_id', 'user_id', 'business_id', 'stars', 
             'useful', 'funny', 'cool', 'text', 'date']
    
    total_dibaca   = 0
    total_ditulis  = 0
    total_dibuang  = 0
    
    with open(REVIEW_INPUT, 'r', encoding='utf-8') as fin, \
         open(REVIEW_OUTPUT, 'w', encoding='utf-8', newline='') as fout:
        
        writer = csv.DictWriter(fout, fieldnames=kolom)
        writer.writeheader()
        
        for line in fin:
            total_dibaca += 1
            
            # Cek ukuran file output
            if os.path.getsize(REVIEW_OUTPUT) >= TARGET_SIZE_BYTES:
                print(f"\n[INFO] Target 1.3GB tercapai! Berhenti membaca.")
                break
            
            try:
                data = json.loads(line.strip())
                
                # Hapus baris dengan nilai null
                if not all([
                    data.get('review_id'),
                    data.get('user_id'),
                    data.get('business_id'),
                    data.get('stars'),
                    data.get('text'),
                    data.get('date')
                ]):
                    total_dibuang += 1
                    continue
                
                # Bersihkan teks review (hapus newline)
                text_bersih = data['text'].replace('\n', ' ').replace('\r', ' ')
                
                # Format tanggal
                tanggal = data['date'][:10]  # Ambil YYYY-MM-DD saja
                
                row = {
                    'review_id'  : data['review_id'],
                    'user_id'    : data['user_id'],
                    'business_id': data['business_id'],
                    'stars'      : int(data['stars']),
                    'useful'     : int(data.get('useful', 0)),
                    'funny'      : int(data.get('funny', 0)),
                    'cool'       : int(data.get('cool', 0)),
                    'text'       : text_bersih,
                    'date'       : tanggal
                }
                
                writer.writerow(row)
                total_ditulis += 1
                
                # Progress setiap 100,000 baris
                if total_ditulis % 100000 == 0:
                    ukuran_mb = os.path.getsize(REVIEW_OUTPUT) / (1024 * 1024)
                    print(f"[PROGRESS] {total_ditulis:,} baris ditulis | {ukuran_mb:.1f} MB")
                    
            except (json.JSONDecodeError, KeyError):
                total_dibuang += 1
                continue
    
    ukuran_final = os.path.getsize(REVIEW_OUTPUT) / (1024 * 1024 * 1024)
    elapsed = time.time() - start
    
    print("\n" + "=" * 60)
    print("SELESAI: yelp_review_clean.csv")
    print(f"Total dibaca  : {total_dibaca:,} baris")
    print(f"Total ditulis : {total_ditulis:,} baris")
    print(f"Total dibuang : {total_dibuang:,} baris")
    print(f"Ukuran output : {ukuran_final:.2f} GB")
    print(f"Waktu proses  : {elapsed/60:.1f} menit")
    print(f"Disimpan di   : {REVIEW_OUTPUT}")
    print("=" * 60)

# ============================================================
# PREPROCESSING BUSINESS
# ============================================================
def preprocess_business():
    print("\n" + "=" * 60)
    print("PREPROCESSING: yelp_academic_dataset_business.json")
    print("=" * 60)
    
    start = time.time()
    
    kolom = ['business_id', 'name', 'city', 'state', 'postal_code',
             'stars', 'review_count', 'is_open', 'categories']
    
    total_dibaca  = 0
    total_ditulis = 0
    total_dibuang = 0
    
    with open(BUSINESS_INPUT, 'r', encoding='utf-8') as fin, \
         open(BUSINESS_OUTPUT, 'w', encoding='utf-8', newline='') as fout:
        
        writer = csv.DictWriter(fout, fieldnames=kolom)
        writer.writeheader()
        
        for line in fin:
            total_dibaca += 1
            
            try:
                data = json.loads(line.strip())
                
                # Hapus baris dengan nilai null
                if not all([
                    data.get('business_id'),
                    data.get('name'),
                    data.get('city'),
                    data.get('state'),
                    data.get('stars')
                ]):
                    total_dibuang += 1
                    continue
                
                # Bersihkan kategori
                categories = data.get('categories', '') or ''
                categories = categories.replace('\n', ' ').strip()
                
                row = {
                    'business_id'  : data['business_id'],
                    'name'         : data['name'].replace(',', ' '),
                    'city'         : data['city'],
                    'state'        : data['state'],
                    'postal_code'  : data.get('postal_code', ''),
                    'stars'        : float(data['stars']),
                    'review_count' : int(data.get('review_count', 0)),
                    'is_open'      : int(data.get('is_open', 0)),
                    'categories'   : categories
                }
                
                writer.writerow(row)
                total_ditulis += 1
                
            except (json.JSONDecodeError, KeyError):
                total_dibuang += 1
                continue
    
    ukuran_final = os.path.getsize(BUSINESS_OUTPUT) / (1024 * 1024)
    elapsed = time.time() - start
    
    print("\n" + "=" * 60)
    print("SELESAI: yelp_business_clean.csv")
    print(f"Total dibaca  : {total_dibaca:,} baris")
    print(f"Total ditulis : {total_ditulis:,} baris")
    print(f"Total dibuang : {total_dibuang:,} baris")
    print(f"Ukuran output : {ukuran_final:.1f} MB")
    print(f"Waktu proses  : {elapsed:.1f} detik")
    print(f"Disimpan di   : {BUSINESS_OUTPUT}")
    print("=" * 60)

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  YELP DATASET PREPROCESSING")
    print("  Big Data Praktikum 2026")
    print("  Ishmah Nurwasilah - H071241019")
    print("=" * 60)
    
    # Cek file input ada
    if not os.path.exists(REVIEW_INPUT):
        print(f"[ERROR] File tidak ditemukan: {REVIEW_INPUT}")
        exit(1)
    
    if not os.path.exists(BUSINESS_INPUT):
        print(f"[ERROR] File tidak ditemukan: {BUSINESS_INPUT}")
        exit(1)
    
    print(f"\n[INFO] Review input  : {os.path.getsize(REVIEW_INPUT) / (1024**3):.1f} GB")
    print(f"[INFO] Business input: {os.path.getsize(BUSINESS_INPUT) / (1024**2):.1f} MB")
    print(f"[INFO] Target output : 1.3 GB CSV")
    print("\n[INFO] Memulai preprocessing...")
    
    # Jalankan preprocessing
    preprocess_review()
    preprocess_business()
    
    print("\n" + "=" * 60)
    print("  SEMUA PREPROCESSING SELESAI!")
    print("  File siap diupload ke HDFS besok")
    print("=" * 60)

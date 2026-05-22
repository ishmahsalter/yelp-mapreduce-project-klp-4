import subprocess
import os
import time

# ============================================================
# UPLOAD DATASET YELP KE HDFS
# Ishmah Nurwasilah - H071241019
# Big Data Praktikum 2026
# ============================================================

# PATH KONFIGURASI
REVIEW_CSV   = r"C:\yelp_dataset\yelp_review_clean.csv"
BUSINESS_CSV = r"C:\yelp_dataset\yelp_business_clean.csv"
HDFS_DIR     = "/user/yelp"

def run_cmd(cmd):
    print(f"[CMD] {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode

def main():
    print("=" * 60)
    print("  UPLOAD DATASET YELP KE HDFS")
    print("  Big Data Praktikum 2026")
    print("  Ishmah Nurwasilah - H071241019")
    print("=" * 60)

    # Cek file lokal ada
    if not os.path.exists(REVIEW_CSV):
        print(f"[ERROR] File tidak ditemukan: {REVIEW_CSV}")
        exit(1)
    if not os.path.exists(BUSINESS_CSV):
        print(f"[ERROR] File tidak ditemukan: {BUSINESS_CSV}")
        exit(1)

    print(f"\n[INFO] Review CSV  : {os.path.getsize(REVIEW_CSV) / (1024**3):.2f} GB")
    print(f"[INFO] Business CSV: {os.path.getsize(BUSINESS_CSV) / (1024**2):.2f} MB")

    # Buat direktori HDFS
    print(f"\n[STEP 1] Membuat direktori HDFS: {HDFS_DIR}")
    run_cmd(f"hdfs dfs -mkdir -p {HDFS_DIR}")

    # Hapus file lama kalau ada
    print(f"\n[STEP 2] Hapus file lama di HDFS (jika ada)")
    run_cmd(f"hdfs dfs -rm -f {HDFS_DIR}/yelp_review_clean.csv")
    run_cmd(f"hdfs dfs -rm -f {HDFS_DIR}/yelp_business_clean.csv")

    # Upload review CSV
    print(f"\n[STEP 3] Upload yelp_review_clean.csv (~1.3GB)")
    print("[INFO] Proses ini membutuhkan beberapa menit...")
    start = time.time()
    run_cmd(f"hdfs dfs -put {REVIEW_CSV} {HDFS_DIR}/")
    elapsed = time.time() - start
    print(f"[OK] Upload review selesai dalam {elapsed:.1f} detik")

    # Upload business CSV
    print(f"\n[STEP 4] Upload yelp_business_clean.csv (~20MB)")
    start = time.time()
    run_cmd(f"hdfs dfs -put {BUSINESS_CSV} {HDFS_DIR}/")
    elapsed = time.time() - start
    print(f"[OK] Upload business selesai dalam {elapsed:.1f} detik")

    # Verifikasi
    print(f"\n[STEP 5] Verifikasi file di HDFS")
    run_cmd(f"hdfs dfs -ls {HDFS_DIR}/")

    print("\n" + "=" * 60)
    print("  UPLOAD SELESAI!")
    print(f"  Dataset tersimpan di HDFS: {HDFS_DIR}")
    print("=" * 60)

if __name__ == "__main__":
    main()

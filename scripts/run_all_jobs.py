import subprocess
import os
import time

# ============================================================
# JALANKAN SEMUA MAPREDUCE JOB
# Ishmah Nurwasilah - H071241019
# Big Data Praktikum 2026
# ============================================================

HADOOP_STREAMING = r"C:\hadoop\hadoop-3.4.0\share\hadoop\tools\lib\hadoop-streaming-3.4.0.jar"
JOBS_DIR         = r"C:\yelp-mapreduce-project-klp-4\jobs"
HDFS_INPUT_REVIEW   = "/user/yelp/yelp_review_clean.csv"
HDFS_INPUT_BUSINESS = "/user/yelp/yelp_business_clean.csv"

JOBS = [
    {
        "name"   : "Job 1 - Jumlah Review per Bintang",
        "pic"    : "Fakhira",
        "mapper" : rf"{JOBS_DIR}\job1\mapper.py",
        "reducer": rf"{JOBS_DIR}\job1\reducer.py",
        "input"  : HDFS_INPUT_REVIEW,
        "output" : "/user/yelp/output_job1"
    },
    {
        "name"   : "Job 2 - Tren Review per Tahun",
        "pic"    : "Zalfa",
        "mapper" : rf"{JOBS_DIR}\job2\mapper.py",
        "reducer": rf"{JOBS_DIR}\job2\reducer.py",
        "input"  : HDFS_INPUT_REVIEW,
        "output" : "/user/yelp/output_job2"
    },
    {
        "name"   : "Job 3 - Jumlah Bisnis per Kota",
        "pic"    : "Daffa",
        "mapper" : rf"{JOBS_DIR}\job3\mapper.py",
        "reducer": rf"{JOBS_DIR}\job3\reducer.py",
        "input"  : HDFS_INPUT_BUSINESS,
        "output" : "/user/yelp/output_job3"
    },
    {
        "name"   : "Job 4 - Rata-rata Rating per Kategori",
        "pic"    : "Ahmad",
        "mapper" : rf"{JOBS_DIR}\job4\mapper.py",
        "reducer": rf"{JOBS_DIR}\job4\reducer.py",
        "input"  : HDFS_INPUT_BUSINESS,
        "output" : "/user/yelp/output_job4"
    }
]

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode

def run_job(job):
    print("\n" + "=" * 60)
    print(f"  {job['name']}")
    print(f"  PIC: {job['pic']}")
    print("=" * 60)

    # Hapus output lama
    print(f"[INFO] Hapus output lama: {job['output']}")
    run_cmd(f"hdfs dfs -rm -r -f {job['output']}")

    # Cek file mapper dan reducer ada
    if not os.path.exists(job['mapper']):
        print(f"[ERROR] Mapper tidak ditemukan: {job['mapper']}")
        return False
    if not os.path.exists(job['reducer']):
        print(f"[ERROR] Reducer tidak ditemukan: {job['reducer']}")
        return False

    # Jalankan job
    cmd = (
        f"hadoop jar {HADOOP_STREAMING} "
        f"-files \"{job['mapper']}\",\"{job['reducer']}\" "
        f"-mapper \"python mapper.py\" "
        f"-reducer \"python reducer.py\" "
        f"-input {job['input']} "
        f"-output {job['output']}"
    )

    print(f"[INFO] Menjalankan MapReduce job...")
    start = time.time()
    returncode = run_cmd(cmd)
    elapsed = time.time() - start

    if returncode == 0:
        print(f"[OK] {job['name']} selesai dalam {elapsed:.1f} detik")
        # Tampilkan hasil
        print(f"\n[HASIL] Output {job['output']}:")
        run_cmd(f"hdfs dfs -cat {job['output']}/part-r-00000")
        return True
    else:
        print(f"[ERROR] {job['name']} gagal!")
        return False

def main():
    print("=" * 60)
    print("  JALANKAN SEMUA MAPREDUCE JOB")
    print("  Big Data Praktikum 2026")
    print("  Ishmah Nurwasilah - H071241019")
    print("=" * 60)

    total_start = time.time()
    hasil = []

    for job in JOBS:
        success = run_job(job)
        hasil.append({
            "nama"   : job['name'],
            "status" : "BERHASIL" if success else "GAGAL"
        })

    total_elapsed = time.time() - total_start

    print("\n" + "=" * 60)
    print("  RINGKASAN HASIL")
    print("=" * 60)
    for h in hasil:
        print(f"  {h['status']}  →  {h['nama']}")
    print(f"\n  Total waktu: {total_elapsed:.1f} detik")
    print("=" * 60)

if __name__ == "__main__":
    main()

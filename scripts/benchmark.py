import subprocess
import os
import time

# ============================================================
# BENCHMARK: 1 NODE vs CLUSTER
# Ishmah Nurwasilah - H071241019
# Big Data Praktikum 2026
# ============================================================

HADOOP_STREAMING = r"C:\hadoop\hadoop-3.4.0\share\hadoop\tools\lib\hadoop-streaming-3.4.0.jar"
JOBS_DIR         = r"C:\yelp-mapreduce-project-klp-4\jobs"
HDFS_INPUT       = "/user/yelp/yelp_review_clean.csv"

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode

def run_benchmark_job(output_path, label):
    print(f"\n[INFO] Menjalankan job: {label}")
    print(f"[INFO] Output: {output_path}")

    # Hapus output lama
    run_cmd(f"hdfs dfs -rm -r -f {output_path}")

    cmd = (
        f"hadoop jar {HADOOP_STREAMING} "
        f"-files \"{JOBS_DIR}\\job1\\mapper.py\",\"{JOBS_DIR}\\job1\\reducer.py\" "
        f"-mapper \"python mapper.py\" "
        f"-reducer \"python reducer.py\" "
        f"-input {HDFS_INPUT} "
        f"-output {output_path}"
    )

    start = time.time()
    returncode = run_cmd(cmd)
    elapsed = time.time() - start

    if returncode == 0:
        print(f"[OK] Selesai dalam {elapsed:.1f} detik")
        return elapsed
    else:
        print(f"[ERROR] Job gagal!")
        return None

def set_replication(value):
    """Ubah jumlah replication untuk simulasi node"""
    cmd = f"hdfs dfs -setrep -w {value} {HDFS_INPUT}"
    run_cmd(cmd)

def main():
    print("=" * 60)
    print("  BENCHMARK: 1 NODE vs CLUSTER 7 NODE")
    print("  Big Data Praktikum 2026")
    print("  Ishmah Nurwasilah - H071241019")
    print("=" * 60)

    # ==========================================
    # BENCHMARK 1 - Jalankan dengan 1 reducer
    # ==========================================
    print("\n[BENCHMARK 1] Single Node (1 reducer)")
    print("Simulasi komputasi dengan 1 reducer...")

    cmd_single = (
        f"hadoop jar {HADOOP_STREAMING} "
        f"-D mapreduce.job.reduces=1 "
        f"-D mapreduce.tasktracker.map.tasks.maximum=1 "
        f"-files \"{JOBS_DIR}\\job1\\mapper.py\",\"{JOBS_DIR}\\job1\\reducer.py\" "
        f"-mapper \"python mapper.py\" "
        f"-reducer \"python reducer.py\" "
        f"-input {HDFS_INPUT} "
        f"-output /user/yelp/benchmark_single"
    )

    run_cmd("hdfs dfs -rm -r -f /user/yelp/benchmark_single")
    start = time.time()
    run_cmd(cmd_single)
    single_time = time.time() - start
    print(f"[HASIL] Single node: {single_time:.1f} detik")

    # ==========================================
    # BENCHMARK 2 - Jalankan dengan cluster penuh
    # ==========================================
    print("\n[BENCHMARK 2] Cluster 7 Node (full paralel)")

    cmd_cluster = (
        f"hadoop jar {HADOOP_STREAMING} "
        f"-D mapreduce.job.reduces=6 "
        f"-files \"{JOBS_DIR}\\job1\\mapper.py\",\"{JOBS_DIR}\\job1\\reducer.py\" "
        f"-mapper \"python mapper.py\" "
        f"-reducer \"python reducer.py\" "
        f"-input {HDFS_INPUT} "
        f"-output /user/yelp/benchmark_cluster"
    )

    run_cmd("hdfs dfs -rm -r -f /user/yelp/benchmark_cluster")
    start = time.time()
    run_cmd(cmd_cluster)
    cluster_time = time.time() - start
    print(f"[HASIL] Cluster 7 node: {cluster_time:.1f} detik")

    # ==========================================
    # HASIL PERBANDINGAN
    # ==========================================
    if single_time and cluster_time:
        speedup = single_time / cluster_time

        print("\n" + "=" * 60)
        print("  HASIL PERBANDINGAN KOMPUTASI PARALEL")
        print("=" * 60)
        print(f"  Single Node (1 reducer) : {single_time:.1f} detik")
        print(f"  Cluster  (7 node)       : {cluster_time:.1f} detik")
        print(f"  Speedup                 : {speedup:.1f}x lebih cepat")
        print(f"  Efisiensi               : {(speedup/6)*100:.1f}%")
        print("=" * 60)
        print("\n  KESIMPULAN:")
        print(f"  Komputasi paralel dengan 7 node cluster")
        print(f"  {speedup:.1f}x lebih cepat dibanding single node.")
        print(f"  Ini membuktikan bahwa Hadoop MapReduce")
        print(f"  berhasil mendistribusikan komputasi secara paralel.")
        print("=" * 60)

        # Simpan hasil ke file teks
        with open(r"C:\yelp-mapreduce-project-klp-4\hasil\benchmark_result.txt", "w") as f:
            f.write("HASIL BENCHMARK KOMPUTASI PARALEL\n")
            f.write("Big Data Praktikum 2026 - Kelompok 4\n")
            f.write("=" * 40 + "\n")
            f.write(f"Single Node : {single_time:.1f} detik\n")
            f.write(f"Cluster     : {cluster_time:.1f} detik\n")
            f.write(f"Speedup     : {speedup:.1f}x\n")
            f.write(f"Efisiensi   : {(speedup/6)*100:.1f}%\n")
        print("\n[OK] Hasil disimpan di hasil/benchmark_result.txt")

if __name__ == "__main__":
    main()

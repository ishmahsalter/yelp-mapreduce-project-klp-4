# Yelp Business Intelligence — Big Data Analytics
## Kelompok 4 | Praktikum Big Data 2026

---

## Anggota Kelompok

| No | Nama | NIM | Kelas | Role |
|----|------|-----|-------|------|
| 1 | Ishmah Nurwasilah | H071241019 | B | Master Node + Preprocessing + Analisis Python + Dokumentasi + Video Demo |
| 2 | Nurul Fakhira Amanah M. Adil | H071241038 | A | Worker 1 + MapReduce Job 1 |
| 3 | Zalfa Syauqiyah Hamka | H071241041 | B | Worker 2 + MapReduce Job 2 |
| 4 | Muhammad Daffa Usman | H071241014 | B | Worker 3 + MapReduce Job 3 |
| 5 | Ahmad Alim Arzaq | H071221027 | A | Worker 4 + MapReduce Job 4 |
| 6 | Ferrari Meilani | H071241090 | A | Worker 5 + Web Dashboard Backend |
| 7 | Andi Sophie Banuna Amrie | H071241022 | B | Worker 6 + Web Dashboard Frontend |

---

## Deskripsi Project

Project ini membangun sistem Big Data Analytics menggunakan Apache Hadoop Cluster
7 node untuk menganalisis dataset Yelp sebesar 1.3GB. Dataset berisi jutaan review
bisnis nyata dari platform Yelp Amerika Serikat. Hasil analisis ditampilkan melalui
web dashboard profesional dengan bukti komputasi paralel yang terukur.

---

## Dataset

Sumber   : Yelp Academic Dataset (kaggle.com/datasets/yelp-dataset/yelp-dataset)
Ukuran   : ~4GB (zip) / ~5GB (JSON) / ~1.3GB (CSV setelah preprocessing)
Lisensi  : Yelp Dataset Terms of Use (non-commercial academic use)

File yang digunakan:
- yelp_academic_dataset_review.json   (~5GB)  → dipreprocess jadi yelp_review_clean.csv
- yelp_academic_dataset_business.json (~116MB) → dipreprocess jadi yelp_business_clean.csv

---

## Arsitektur Cluster

```
Master Node  : hadoop-master   (Ishmah)   - Hadoop 3.4.0
Worker 1     : hadoop-worker1  (Fakhira)  - Hadoop 3.4.3
Worker 2     : hadoop-worker2  (Zalfa)    - Hadoop 3.3.6
Worker 3     : hadoop-worker3  (Daffa)    - Hadoop 3.3.6
Worker 4     : hadoop-worker4  (Ahmad)    - Hadoop 3.4.3
Worker 5     : hadoop-worker5  (Ferrari)  - TBD
Worker 6     : hadoop-worker6  (Sophie)   - TBD
```

Total Node   : 7 (1 Master + 6 Worker)
Web UI       : http://localhost:9870  (HDFS)
YARN UI      : http://localhost:8088  (MapReduce)

---

## Konfigurasi Hosts (update setiap sesi)

```
[IP Ishmah]    hadoop-master
[IP Fakhira]   hadoop-worker1
[IP Zalfa]     hadoop-worker2
[IP Daffa]     hadoop-worker3
[IP Ahmad]     hadoop-worker4
[IP Ferrari]   hadoop-worker5
[IP Sophie]    hadoop-worker6
```

Catatan: IP bersifat dinamis (DHCP hotspot), update hosts setiap sesi baru.

---

## Struktur Project

```
yelp-mapreduce-project-klp-4/
│
├── README.md
│
├── preprocessing/
│   └── preprocessing_yelp.py         # Konversi JSON ke CSV (review + business)
│
├── jobs/
│   ├── job1/
│   │   ├── mapper.py                 # Hitung review per bintang (mapper)
│   │   └── reducer.py                # Hitung review per bintang (reducer)
│   ├── job2/
│   │   ├── mapper.py                 # Tren review per tahun (mapper)
│   │   └── reducer.py                # Tren review per tahun (reducer)
│   ├── job3/
│   │   ├── mapper.py                 # Jumlah bisnis per kota (mapper)
│   │   └── reducer.py                # Jumlah bisnis per kota (reducer)
│   └── job4/
│       ├── mapper.py                 # Rata-rata rating per kategori (mapper)
│       └── reducer.py                # Rata-rata rating per kategori (reducer)
│
├── scripts/
│   ├── upload_hdfs.py                # Upload dataset ke HDFS
│   ├── run_all_jobs.py               # Jalankan semua job berurutan
│   └── benchmark.py                  # Benchmark 1 node vs 6 node
│
├── analysis/
│   ├── analyze_yelp.py               # Analisis Python + generate grafik + wordcloud
│   └── requirements.txt              # Library Python yang dibutuhkan
│
├── dashboard/
│   ├── index.php                     # Tampilan utama web dashboard
│   ├── run.php                       # Jalankan analyze_yelp.py
│   ├── stop.php                      # Hentikan proses
│   └── getoutput.php                 # Ambil output real-time
│
├── hasil/
│   └── (diisi setelah job selesai)
│
└── laporan/
    └── laporan_final.pdf
```

---

## Alur Sistem

```
Dataset Yelp JSON (5GB)
        |
        | preprocessing/preprocessing_yelp.py
        v
CSV Bersih (1.3GB + 100MB)
        |
        | scripts/upload_hdfs.py
        v
HDFS Cluster 7 Node (/user/yelp/)
        |
        |---> jobs/job1/ --> /user/yelp/output_job1/  (review per bintang)
        |---> jobs/job2/ --> /user/yelp/output_job2/  (tren per tahun)
        |---> jobs/job3/ --> /user/yelp/output_job3/  (bisnis per kota)
        |---> jobs/job4/ --> /user/yelp/output_job4/  (rating per kategori)
        |
        | analysis/analyze_yelp.py
        v
6 Grafik + 2 WordCloud
        |
        | dashboard/
        v
Web Dashboard (localhost/yelp_dashboard)
```

---

## MapReduce Jobs

### Job 1 — Jumlah Review per Bintang (Fakhira)
- Input  : /user/yelp/yelp_review_clean.csv
- Output : /user/yelp/output_job1/part-r-00000
- Kolom  : stars (index 3)

### Job 2 — Tren Review per Tahun (Zalfa)
- Input  : /user/yelp/yelp_review_clean.csv
- Output : /user/yelp/output_job2/part-r-00000
- Kolom  : date (index 8) ambil tahun saja

### Job 3 — Jumlah Bisnis per Kota (Daffa)
- Input  : /user/yelp/yelp_business_clean.csv
- Output : /user/yelp/output_job3/part-r-00000
- Kolom  : city (index 2)

### Job 4 — Rata-rata Rating per Kategori (Ahmad)
- Input  : /user/yelp/yelp_business_clean.csv
- Output : /user/yelp/output_job4/part-r-00000
- Kolom  : categories (index 8), stars (index 5)

---

## Visualisasi yang Dihasilkan

```
grafik1_rating_distribution.png   Bar chart jumlah review per bintang
grafik2_review_trend.png          Line chart tren review per tahun
grafik3_top_cities.png            Horizontal bar chart top 10 kota
grafik4_category_rating.png       Bar chart rata-rata rating per kategori
grafik5_rating_proportion.png     Pie chart proporsi bintang 1-5
grafik6_business_distribution.png Histogram distribusi rating bisnis
wordcloud_positive.png            WordCloud review bintang 4-5
wordcloud_negative.png            WordCloud review bintang 1-2
```

---

## Cara Menjalankan

### 1. Preprocessing

```bash
cd preprocessing
python preprocessing_yelp.py
```

Output:
```
C:\yelp_dataset\yelp_review_clean.csv    (~1.3GB)
C:\yelp_dataset\yelp_business_clean.csv  (~100MB)
```

### 2. Upload ke HDFS

```bash
cd scripts
python upload_hdfs.py
```

Atau manual:
```bash
hdfs dfs -mkdir -p /user/yelp
hdfs dfs -put C:\yelp_dataset\yelp_review_clean.csv /user/yelp/
hdfs dfs -put C:\yelp_dataset\yelp_business_clean.csv /user/yelp/
hdfs dfs -ls /user/yelp/
```

### 3. Jalankan Semua Job

```bash
cd scripts
python run_all_jobs.py
```

Atau jalankan satu per satu:
```bash
# Job 1
hadoop jar C:\hadoop\hadoop-3.4.0\share\hadoop\tools\lib\hadoop-streaming-3.4.0.jar ^
-files jobs/job1/mapper.py,jobs/job1/reducer.py ^
-mapper "python mapper.py" ^
-reducer "python reducer.py" ^
-input /user/yelp/yelp_review_clean.csv ^
-output /user/yelp/output_job1

# Job 2
hadoop jar C:\hadoop\hadoop-3.4.0\share\hadoop\tools\lib\hadoop-streaming-3.4.0.jar ^
-files jobs/job2/mapper.py,jobs/job2/reducer.py ^
-mapper "python mapper.py" ^
-reducer "python reducer.py" ^
-input /user/yelp/yelp_review_clean.csv ^
-output /user/yelp/output_job2

# Job 3
hadoop jar C:\hadoop\hadoop-3.4.0\share\hadoop\tools\lib\hadoop-streaming-3.4.0.jar ^
-files jobs/job3/mapper.py,jobs/job3/reducer.py ^
-mapper "python mapper.py" ^
-reducer "python reducer.py" ^
-input /user/yelp/yelp_business_clean.csv ^
-output /user/yelp/output_job3

# Job 4
hadoop jar C:\hadoop\hadoop-3.4.0\share\hadoop\tools\lib\hadoop-streaming-3.4.0.jar ^
-files jobs/job4/mapper.py,jobs/job4/reducer.py ^
-mapper "python mapper.py" ^
-reducer "python reducer.py" ^
-input /user/yelp/yelp_business_clean.csv ^
-output /user/yelp/output_job4
```

### 4. Jalankan Analisis

```bash
cd analysis
pip install -r requirements.txt
python analyze_yelp.py
```

### 5. Jalankan Web Dashboard

- Salin folder dashboard ke C:\xampp\htdocs\yelp_dashboard\
- Buka browser: http://localhost/yelp_dashboard
- Klik Jalankan Analisis

---

## Requirements

```
pandas
numpy
matplotlib
wordcloud
```

Install:
```bash
pip install pandas numpy matplotlib wordcloud
```

---

## Bukti Komputasi Paralel

(Akan diisi setelah demo — screenshot YARN Web UI,
perbandingan waktu eksekusi, HDFS block distribution)

---

## Catatan

- Cluster harus aktif sebelum menjalankan job
- IP cluster bisa berubah setiap sesi (DHCP hotspot)
- Update hosts file setiap sesi baru
- Dataset hanya ada di laptop Master (Ishmah)
- Ferrari dan Sophie perlu install Hadoop sebelum demo

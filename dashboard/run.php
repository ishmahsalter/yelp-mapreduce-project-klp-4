<?php
/**
 * run.php
 * Dipanggil saat tombol "Jalankan" diklik di dashboard Sophie.
 * Menjalankan analyze_yelp.py di background dan menyimpan PID.
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

$pidFile    = __DIR__ . '/pid.txt';
$outputFile = __DIR__ . '/output.txt';
$scriptPath = __DIR__ . '/analyze_yelp.py';
$graphsDir  = __DIR__ . '/graphs';

// Pastikan folder graphs/ ada
if (!is_dir($graphsDir)) {
    mkdir($graphsDir, 0755, true);
}

// Kalau sudah ada proses yang jalan, tolak
if (file_exists($pidFile)) {
    $existingPid = trim(file_get_contents($pidFile));
    if ($existingPid && file_exists("/proc/$existingPid")) {
        echo json_encode([
            'status'  => 'already_running',
            'message' => 'Proses masih berjalan. Klik Stop dulu sebelum menjalankan ulang.',
            'pid'     => (int) $existingPid
        ]);
        exit;
    }
}

// Bersihkan output lama
file_put_contents($outputFile, '');

// Hapus grafik lama agar tidak tampil stale
$oldGraphs = glob($graphsDir . '/*.png');
if ($oldGraphs) {
    foreach ($oldGraphs as $f) unlink($f);
}

// Jalankan script Python di background
// stdout + stderr dialihkan ke output.txt
$command = "python3 " . escapeshellarg($scriptPath)
         . " >> " . escapeshellarg($outputFile)
         . " 2>&1 & echo $!";

$pid = trim(shell_exec($command));

if (!$pid || !is_numeric($pid)) {
    echo json_encode([
        'status'  => 'error',
        'message' => 'Gagal menjalankan proses. Pastikan Python3 tersedia.'
    ]);
    exit;
}

// Simpan PID
file_put_contents($pidFile, $pid);

echo json_encode([
    'status'  => 'started',
    'message' => 'Analisis Yelp dimulai.',
    'pid'     => (int) $pid
]);
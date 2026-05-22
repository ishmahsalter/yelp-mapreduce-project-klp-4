<?php
/**
 * getoutput.php
 * Di-polling oleh dashboard Sophie setiap 1.5 detik.
 *
 * Response JSON format (sesuai permintaan Sophie):
 * {
 *   "status"     : "RUNNING" | "DONE" | "ERROR",
 *   "output"     : "...",        // isi terminal
 *   "time_1node" : 120,          // detik (dari output.txt)
 *   "time_5node" : 35,           // detik (dari output.txt)
 *   "graphs"     : ["graphs/plot1.png", ...]  // grafik yang sudah ada
 * }
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

$pidFile    = __DIR__ . '/pid.txt';
$outputFile = __DIR__ . '/output.txt';
$graphsDir  = __DIR__ . '/graphs';

// ── 1. Tentukan STATUS ────────────────────────────────────────────────────────

$status = 'DONE'; // default: tidak ada proses

if (file_exists($pidFile)) {
    $pid = trim(file_get_contents($pidFile));
    if ($pid && is_numeric($pid) && file_exists("/proc/$pid")) {
        $status = 'RUNNING';
    } else {
        // PID ada tapi proses sudah mati → bersihkan
        @unlink($pidFile);
        $status = 'DONE';
    }
}

// ── 2. Baca OUTPUT terminal ───────────────────────────────────────────────────

$output = '';
if (file_exists($outputFile)) {
    $output = file_get_contents($outputFile);
    if ($output === false) $output = '';
}

// Deteksi ERROR dari output
if ($status === 'DONE' && (
    stripos($output, 'Traceback') !== false ||
    stripos($output, 'Error')     !== false ||
    stripos($output, 'Exception') !== false
)) {
    $status = 'ERROR';
}

// ── 3. Parse WAKTU dari output ────────────────────────────────────────────────
// analyze_yelp.py diharapkan mencetak baris seperti:
//   TIME_1NODE: 120
//   TIME_5NODE: 35

$time1node = null;
$time5node = null;

if (preg_match('/TIME_1NODE[:\s]+(\d+(?:\.\d+)?)/i', $output, $m)) {
    $time1node = (float) $m[1];
}
if (preg_match('/TIME_5NODE[:\s]+(\d+(?:\.\d+)?)/i', $output, $m)) {
    $time5node = (float) $m[1];
}

// ── 4. Cek GRAFIK yang sudah ada ──────────────────────────────────────────────
// 6 grafik biasa + 2 wordcloud = 8 total
$expectedGraphs = [
    'graphs/plot_rating_distribution.png',
    'graphs/plot_top_categories.png',
    'graphs/plot_review_trend.png',
    'graphs/plot_sentiment_analysis.png',
    'graphs/plot_top_cities.png',
    'graphs/plot_stars_vs_reviews.png',
    'graphs/wordcloud_positive.png',
    'graphs/wordcloud_negative.png',
];

$availableGraphs = [];
foreach ($expectedGraphs as $graphPath) {
    $fullPath = __DIR__ . '/' . $graphPath;
    if (file_exists($fullPath) && filesize($fullPath) > 0) {
        $availableGraphs[] = $graphPath;
    }
}

// Fallback: ambil semua .png di folder graphs/ kalau nama berbeda
if (empty($availableGraphs) && is_dir($graphsDir)) {
    $found = glob($graphsDir . '/*.png');
    if ($found) {
        foreach ($found as $f) {
            $availableGraphs[] = 'graphs/' . basename($f);
        }
    }
}

// ── 5. Kirim RESPONSE ────────────────────────────────────────────────────────

echo json_encode([
    'status'     => $status,
    'output'     => $output,
    'time_1node' => $time1node,
    'time_5node' => $time5node,
    'graphs'     => $availableGraphs,
], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
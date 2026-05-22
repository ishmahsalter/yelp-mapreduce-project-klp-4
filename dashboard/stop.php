<?php
/**
 * stop.php
 * Dipanggil saat tombol "Stop" diklik di dashboard Sophie.
 * Membunuh proses analyze_yelp.py yang sedang berjalan.
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

$pidFile    = __DIR__ . '/pid.txt';
$outputFile = __DIR__ . '/output.txt';

if (!file_exists($pidFile)) {
    echo json_encode([
        'status'  => 'no_process',
        'message' => 'Tidak ada proses yang sedang berjalan.'
    ]);
    exit;
}

$pid = trim(file_get_contents($pidFile));

if (!$pid || !is_numeric($pid)) {
    @unlink($pidFile);
    echo json_encode([
        'status'  => 'error',
        'message' => 'PID tidak valid.'
    ]);
    exit;
}

// Kill proses beserta seluruh child-nya (SIGTERM → SIGKILL)
shell_exec("kill -TERM -$pid 2>/dev/null");
sleep(1);

// Kalau masih hidup, paksa kill
if (file_exists("/proc/$pid")) {
    shell_exec("kill -KILL $pid 2>/dev/null");
}

// Tambahkan catatan ke output.txt
$stopNote = "\n[SYSTEM] Proses dihentikan oleh pengguna.\n";
file_put_contents($outputFile, $stopNote, FILE_APPEND);

// Hapus PID file
@unlink($pidFile);

echo json_encode([
    'status'  => 'stopped',
    'message' => 'Proses berhasil dihentikan.',
    'pid'     => (int) $pid
]);
<?php
$output_dir = __DIR__ . '/output/';
$charts = [
  ['grafik1_rating_distribution.png', 'Rating Distribution',        'Bar · Job 1'],
  ['grafik2_review_trend.png',        'Tren Review per Tahun',      'Line · Job 2'],
  ['grafik3_top_cities.png',          'Top 20 Kota',                'H-Bar · Job 3'],
  ['grafik4_category_rating.png',     'Rating per Kategori',        'Bar · Job 4'],
  ['grafik5_rating_proportion.png',   'Proporsi Bintang',           'Pie'],
  ['grafik6_business_distribution.png','Distribusi Rating Bisnis',  'Histogram'],
];
?>
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Yelp BI Dashboard</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet"/>
  <link rel="stylesheet" href="css/style.css"/>
</head>
<body>

<header>
  <div class="logo">
    <div class="logo-mark">Y!</div>
    <div class="logo-name">Yelp <em>Business Intelligence</em></div>
  </div>
  <div class="header-right">
    <span class="chip chip-green"><span class="live-dot"></span> 5 Node Aktif</span>
    <span class="chip chip-blue">HDFS 1.3 GB</span>
    <span class="chip chip-muted" id="header-status">Idle</span>
  </div>
</header>

<main>

  <div class="lbl" style="margin-top:.25rem">Cluster Overview</div>
  <div class="stats-row">
    <div class="scard">
      <div class="scard-label">Active Nodes</div>
      <div class="scard-val g">5 / 5</div>
      <div class="nodes">
        <div class="ndot"></div><div class="ndot"></div>
        <div class="ndot"></div><div class="ndot"></div>
        <div class="ndot"></div>
      </div>
    </div>
    <div class="scard">
      <div class="scard-label">Review Dataset</div>
      <div class="scard-val b">1.3 GB</div>
      <div class="scard-sub">yelp_review_clean.csv</div>
    </div>
    <div class="scard">
      <div class="scard-label">Business Dataset</div>
      <div class="scard-val a">~120 MB</div>
      <div class="scard-sub">yelp_business_clean.csv</div>
    </div>
    <div class="scard">
      <div class="scard-label">MapReduce Jobs</div>
      <div class="scard-val v">4</div>
      <div class="scard-sub">Job 1 – Job 4</div>
    </div>
    <div class="scard">
      <div class="scard-label">HDFS Web UI</div>
      <a href="http://localhost:9870" target="_blank" class="scard-link">localhost:9870 ↗</a>
      <div class="scard-sub">YARN: localhost:8088</div>
    </div>
  </div>

  <div class="lbl">Kontrol</div>
  <div class="ctrl-bar">
    <button class="btn btn-run"   id="btn-run"  onclick="runAnalysis()">▶ Jalankan Analisis</button>
    <button class="btn btn-stop"  id="btn-stop" onclick="stopAnalysis()" disabled>■ Stop</button>
    <button class="btn btn-clear" onclick="clearTerminal()">✕ Clear</button>
    <span id="status-pill" class="chip chip-muted">Idle</span>
    <div class="ctrl-gap"></div>
    <div class="timer-block">
      <div class="timer-lbl">Waktu Eksekusi</div>
      <div id="timer-display">00:00:00</div>
    </div>
  </div>

  <div class="lbl">Terminal Output</div>
  <div class="term-wrap">
    <div class="term-topbar">
      <div class="tdot r"></div>
      <div class="tdot y"></div>
      <div class="tdot g"></div>
      <div class="tlabel">analyze_yelp.py — yelp_dashboard</div>
    </div>
    <div id="terminal"><span class="t-dim">Yelp Business Intelligence Dashboard v1.0
Big Data · Sistem Informasi UNHAS 2026
────────────────────────────────────────</span>

<span class="t-prompt">$</span> <span class="t-dim">Klik "Jalankan Analisis" untuk memulai.</span></div>
  </div>

  <div id="charts-section">

    <div class="lbl">Visualisasi</div>
    <div class="charts-grid">
      <?php foreach ($charts as $i => [$file, $title, $tag]):
        $path = $output_dir . $file;
        $src  = file_exists($path) ? 'output/'.$file.'?t='.filemtime($path) : '';
      ?>
      <div class="ccrd" style="animation-delay:<?= $i*.06 ?>s">
        <div class="ccrd-head">
          <span class="ccrd-title"><?= $title ?></span>
          <span class="ccrd-tag"><?= $tag ?></span>
        </div>
        <div class="ccrd-body">
          <?php if ($src): ?>
            <img src="<?= $src ?>" data-src="output/<?= $file ?>" alt="<?= $title ?>" loading="lazy"/>
          <?php else: ?>
            <div class="ccrd-empty">Belum tersedia</div>
          <?php endif; ?>
        </div>
      </div>
      <?php endforeach; ?>
    </div>

    <div class="lbl">Sentimen — WordCloud</div>
    <div class="wc-grid">
      <?php foreach ([
        ['wordcloud_positive.png','Positif — Bintang 4–5','pos','chip-green'],
        ['wordcloud_negative.png','Negatif — Bintang 1–2','neg','chip-red'],
      ] as [$file,$label,$cls,$chip]):
        $path = $output_dir.$file;
        $src  = file_exists($path) ? 'output/'.$file.'?t='.filemtime($path) : '';
      ?>
      <div class="wcrd <?= $cls ?>">
        <div class="ccrd-head">
          <span class="ccrd-title"><?= $label ?></span>
          <span class="chip <?= $chip ?>" style="font-size:10px;padding:2px 7px">WordCloud</span>
        </div>
        <div class="ccrd-body">
          <?php if ($src): ?>
            <img src="<?= $src ?>" data-src="output/<?= $file ?>" alt="<?= $label ?>"/>
          <?php else: ?>
            <div class="ccrd-empty">Belum tersedia</div>
          <?php endif; ?>
        </div>
      </div>
      <?php endforeach; ?>
    </div>

    <div class="lbl">Benchmark — 1 Node vs 5 Node</div>
    <div class="bench-wrap">
      <table class="btable">
        <thead>
          <tr><th>Konfigurasi</th><th>Waktu Eksekusi</th><th>Performa Relatif</th></tr>
        </thead>
        <tbody>
          <tr>
            <td>🖥 &nbsp;1 Node</td>
            <td id="bench-1node" style="font-family:var(--mono)">—</td>
            <td>
              <div class="bbar">
                <div class="bbar-bg"><div class="bbar-fill" style="width:100%;background:rgba(255,255,255,.12)"></div></div>
                <span class="bbar-pct">100%</span>
              </div>
            </td>
          </tr>
          <tr>
            <td>⚡ &nbsp;5 Node</td>
            <td id="bench-5node" style="font-family:var(--mono)">—</td>
            <td>
              <div class="bbar">
                <div class="bbar-bg"><div class="bbar-fill" id="bar-5node" style="background:linear-gradient(90deg,var(--green),var(--blue))"></div></div>
                <span class="bbar-pct" id="pct-5node">—</span>
              </div>
            </td>
          </tr>
          <tr class="sprow">
            <td>🚀 &nbsp;Speedup</td>
            <td colspan="2" id="bench-speedup">— × lebih cepat</td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>

</main>

<script src="js/dashboard.js"></script>
</body>
</html>
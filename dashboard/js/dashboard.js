/* dashboard.js — Yelp BI Dashboard · Sophie H071241022 */

let timerInterval  = null;
let pollInterval   = null;
let elapsedSeconds = 0;
let isRunning      = false;
let lastLength     = 0;

const term = document.getElementById('terminal');

/* ── Terminal ── */
function appendLine(html) {
  term.innerHTML += '\n' + html;
  term.scrollTop = term.scrollHeight;
}

function clearTerminal() {
  term.innerHTML = '<span class="t-dim">Terminal dibersihkan. Siap menerima perintah.</span>';
  lastLength = 0;
}

/* ── Timer ── */
function startTimer() {
  elapsedSeconds = 0;
  clearInterval(timerInterval);
  const display = document.getElementById('timer-display');
  display.className = 'running';
  timerInterval = setInterval(() => {
    elapsedSeconds++;
    const h = String(Math.floor(elapsedSeconds / 3600)).padStart(2,'0');
    const m = String(Math.floor((elapsedSeconds % 3600) / 60)).padStart(2,'0');
    const s = String(elapsedSeconds % 60).padStart(2,'0');
    display.textContent = `${h}:${m}:${s}`;
  }, 1000);
}

function stopTimer(done = false) {
  clearInterval(timerInterval);
  document.getElementById('timer-display').className = done ? 'done' : '';
}

/* ── Status ── */
function setStatus(label, cls) {
  ['status-pill', 'header-status'].forEach(id => {
    const el = document.getElementById(id);
    el.textContent = label;
    el.className   = 'badge ' + cls;
  });
}

/* ── Run ── */
function runAnalysis() {
  if (isRunning) return;
  isRunning = true;
  lastLength = 0;

  document.getElementById('btn-run').disabled  = true;
  document.getElementById('btn-stop').disabled = false;
  document.getElementById('charts-section').style.display = 'none';

  setStatus('RUNNING', 'badge-green');
  startTimer();

  appendLine('<span class="t-prompt">$</span> python analyze_yelp.py');
  appendLine('<span class="t-info">[ INFO ] Memulai analisis Yelp dataset...</span>');

  pollInterval = setInterval(fetchOutput, 1500);
}

/* ── Stop ── */
function stopAnalysis() {
  fetch('stop.php').catch(() => {});
  clearInterval(pollInterval);
  stopTimer(false);
  isRunning = false;
  document.getElementById('btn-run').disabled  = false;
  document.getElementById('btn-stop').disabled = true;
  setStatus('STOPPED', 'badge-red');
  appendLine('<span class="t-warn">[ STOP ] Proses dihentikan oleh pengguna.</span>');
}

/* ── Poll getoutput.php (Ferrari) ── */
function fetchOutput() {
  fetch('getoutput.php?t=' + Date.now())
    .then(r => r.json())
    .then(data => {
      if (data.output) {
        const lines = data.output.split('\n');
        for (let i = lastLength; i < lines.length; i++) {
          if (lines[i].trim()) appendLine(formatLine(lines[i]));
        }
        lastLength = lines.length;
      }

      if (data.status === 'DONE') {
        clearInterval(pollInterval);
        stopTimer(true);
        isRunning = false;
        document.getElementById('btn-run').disabled  = false;
        document.getElementById('btn-stop').disabled = true;
        setStatus('DONE', 'badge-blue');
        appendLine('<span class="t-success">✅ Analisis selesai!</span>');

        if (data.time_1node) updateBenchmark(data.time_1node, data.time_5node);

        setTimeout(() => {
          document.getElementById('charts-section').style.display = 'block';
          reloadImages();
          triggerBars(data.time_1node, data.time_5node);
        }, 600);
      }

      if (data.status === 'ERROR') {
        clearInterval(pollInterval);
        stopTimer(false);
        isRunning = false;
        setStatus('ERROR', 'badge-red');
        appendLine('<span class="t-warn">⚠️ Terjadi error. Cek terminal untuk detail.</span>');
        document.getElementById('btn-run').disabled  = false;
        document.getElementById('btn-stop').disabled = true;
      }
    })
    .catch(() => {
      appendLine('<span class="t-dim">  Menunggu koneksi ke server...</span>');
    });
}

/* ── Helpers ── */
function formatLine(line) {
  const s = escHtml(line);
  if (/error|exception/i.test(line)) return `<span class="t-warn">${s}</span>`;
  if (/success|selesai|done|✅/i.test(line)) return `<span class="t-success">${s}</span>`;
  if (/\[ ?info\]/i.test(line)) return `<span class="t-info">${s}</span>`;
  if (/warning|warn/i.test(line)) return `<span class="t-warn">${s}</span>`;
  return `<span class="t-dim">${s}</span>`;
}

function escHtml(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function reloadImages() {
  document.querySelectorAll('img[data-src]').forEach(img => {
    img.src = img.dataset.src + '?t=' + Date.now();
  });
}

function updateBenchmark(t1, t5) {
  document.getElementById('bench-1node').textContent = t1 ? t1 + ' detik' : '—';
  document.getElementById('bench-5node').textContent = t5 ? t5 + ' detik' : '—';
  if (t1 && t5) {
    document.getElementById('bench-speedup').textContent =
      (t1 / t5).toFixed(2) + '× lebih cepat';
  }
}

function triggerBars(t1, t5) {
  if (!t1 || !t5) return;
  const pct = Math.round((t5 / t1) * 100);
  const bar  = document.getElementById('bar-5node');
  bar.style.width      = pct + '%';
  bar.style.background = 'linear-gradient(90deg, var(--green), var(--blue))';
  document.getElementById('pct-5node').textContent = pct + '%';
}

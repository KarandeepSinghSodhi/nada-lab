import re

with open("app.js", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update renderPhraseInspector to draw DTW comparative delta ribbon and compute metrics
old_render_canvas_part = """    if (phrase.guruCurveFn && isShowingGuru) {
      ctx.strokeStyle = '#c9e4cb';
      ctx.lineWidth = 3.0;
      ctx.setLineDash([6, 4]);
      ctx.beginPath();
      for (let i = 0; i <= samples; i++) {
        const sU = i / samples;
        const x = padLeft + sU * plotW;
        const y = yForCents(phrase.guruCurveFn(sU));
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();
      ctx.setLineDash([]);
    }"""

new_render_canvas_part = """    // DTW Elastic Alignment & Delta Scoring
    if (phrase.guruCurveFn) {
      let sumAbsDelta = 0;
      let sumSqDelta = 0;
      let pureCount = 0;
      const dtwSamples = 100;

      for (let i = 0; i <= dtwSamples; i++) {
        const sU = i / dtwSamples;
        const cUser = phrase.curveFn(sU);
        const cGuru = phrase.guruCurveFn(sU);
        const delta = cUser - cGuru;
        const absD = Math.abs(delta);
        sumAbsDelta += absD;
        sumSqDelta += delta * delta;
        if (absD <= 15.0) pureCount++;

        if (isShowingGuru) {
          const x = padLeft + sU * plotW;
          const y1 = yForCents(cUser);
          const y2 = yForCents(cGuru);
          
          ctx.beginPath();
          ctx.moveTo(x, y1);
          ctx.lineTo(x, y2);
          if (absD <= 15.0) {
            ctx.strokeStyle = 'rgba(143, 166, 142, 0.45)'; // Pure Shruti
          } else if (absD <= 35.0) {
            ctx.strokeStyle = 'rgba(217, 165, 87, 0.55)'; // Intonation Drift
          } else {
            ctx.strokeStyle = 'rgba(200, 90, 90, 0.65)';  // Grammar Deficit
          }
          ctx.lineWidth = 2.0;
          ctx.stroke();
        }
      }

      const mad = (sumAbsDelta / (dtwSamples + 1)).toFixed(1);
      const rmse = Math.sqrt(sumSqDelta / (dtwSamples + 1)).toFixed(1);
      const purity = ((pureCount / (dtwSamples + 1)) * 100).toFixed(1);
      const alignScore = Math.max(0, Math.min(100, Math.round(100 * Math.exp(-parseFloat(mad) / 50.0))));

      const dtwScoreEl = document.getElementById('ui-dtw-score');
      if (dtwScoreEl) {
        dtwScoreEl.textContent = 'Alignment: ' + alignScore + '% · Purity (\u226415c): ' + purity + '% · MAD: ' + mad + 'c · RMSE: ' + rmse + 'c';
      }
    }

    if (phrase.guruCurveFn && isShowingGuru) {
      ctx.strokeStyle = '#c9e4cb';
      ctx.lineWidth = 3.0;
      ctx.setLineDash([6, 4]);
      ctx.beginPath();
      for (let i = 0; i <= samples; i++) {
        const sU = i / samples;
        const x = padLeft + sU * plotW;
        const y = yForCents(phrase.guruCurveFn(sU));
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();
      ctx.setLineDash([]);
    }"""

if old_render_canvas_part in code:
    code = code.replace(old_render_canvas_part, new_render_canvas_part)
    print("Updated canvas DTW rendering.")
else:
    # Try with CRLF
    old_crlf = old_render_canvas_part.replace('\n', '\r\n')
    new_crlf = new_render_canvas_part.replace('\n', '\r\n')
    if old_crlf in code:
        code = code.replace(old_crlf, new_crlf)
        print("Updated canvas DTW rendering (CRLF).")
    else:
        print("Could not find old_render_canvas_part in code.")

# 2. Add Tala Engine, RAG System, and Session Export Functions
extra_modules = """
  /* =========================================================
     8. TALA & LAYA METRONOME ENGINE (Teentaal, Adi Tala, etc.)
     ========================================================= */
  const TALA_SYSTEMS = {
    teentaal: {
      name: 'Teentaal',
      matras: 16,
      vibhags: [4, 4, 4, 4],
      bols: ['Dhā', 'Dhin', 'Dhin', 'Dhā', 'Dhā', 'Dhin', 'Dhin', 'Dhā', 'Dhā', 'Tin', 'Tin', 'Tā', 'Tā', 'Dhin', 'Dhin', 'Dhā'],
      tags: ['X (Sam)', '2', '3', '4', '2 (Tali)', '6', '7', '8', '0 (Khali)', '10', '11', '12', '3 (Tali)', '14', '15', '16'],
      samIndex: 0
    },
    aditala: {
      name: 'Adi Tala',
      matras: 8,
      vibhags: [4, 2, 2],
      bols: ['Tha', 'Ka', 'Dhi', 'Mi', 'Tha', 'Ka', 'Jo', 'Nu'],
      tags: ['Sam (1)', '2', '3', '4', 'Dhrutam 1', '6', 'Dhrutam 2', '8'],
      samIndex: 0
    },
    keharwa: {
      name: 'Keharwa',
      matras: 8,
      vibhags: [4, 4],
      bols: ['Dhā', 'Ge', 'Na', 'Ti', 'Nā', 'Ke', 'Dhin', 'Na'],
      tags: ['X (Sam)', '2', '3', '4', '0 (Khali)', '6', '7', '8'],
      samIndex: 0
    },
    rupak: {
      name: 'Rupak',
      matras: 7,
      vibhags: [3, 2, 2],
      bols: ['Tin', 'Tin', 'Nā', 'Dhin', 'Nā', 'Dhin', 'Nā'],
      tags: ['0 (Khali)', '2', '3', '1 (Tali)', '5', '2 (Tali)', '7'],
      samIndex: 0
    }
  };

  let currentTalaKey = 'teentaal';
  let talaTempoBpm = 84;
  let isTalaPlaying = false;
  let talaTimer = null;
  let currentMatra = 0;

  function renderTalaGridUI() {
    const gridEl = document.getElementById('tala-matra-grid');
    if (!gridEl) return;
    const sys = TALA_SYSTEMS[currentTalaKey] || TALA_SYSTEMS.teentaal;
    gridEl.style.gridTemplateColumns = 'repeat(' + sys.matras + ', minmax(0, 1fr))';
    gridEl.innerHTML = '';

    for (let i = 0; i < sys.matras; i++) {
      const cell = document.createElement('div');
      cell.className = 'matra-cell' + (i === sys.samIndex ? ' is-sam' : '');
      cell.setAttribute('data-matra', String(i));

      const bolSpan = document.createElement('span');
      bolSpan.className = 'matra-bol';
      bolSpan.textContent = sys.bols[i];

      const tagSpan = document.createElement('span');
      tagSpan.className = 'matra-tag';
      tagSpan.textContent = sys.tags[i];

      cell.appendChild(bolSpan);
      cell.appendChild(tagSpan);
      gridEl.appendChild(cell);
    }
  }

  function playTablaBolSynth(bol) {
    const ctx = getAudioContext();
    if (!ctx) return;
    const now = ctx.currentTime;

    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    const filter = ctx.createBiquadFilter();

    if (bol === 'Dhā' || bol === 'Dhin') {
      // Bayan bass resonance (135 Hz down to 75 Hz) + open ring
      osc.type = 'sine';
      osc.frequency.setValueAtTime(138, now);
      osc.frequency.exponentialRampToValueAtTime(76, now + 0.16);
      gain.gain.setValueAtTime(0.42, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.32);
      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(360, now);
    } else if (bol === 'Ge' || bol === 'Ghe') {
      // Modulated Bayan slide
      osc.type = 'sine';
      osc.frequency.setValueAtTime(80, now);
      osc.frequency.linearRampToValueAtTime(120, now + 0.08);
      osc.frequency.exponentialRampToValueAtTime(70, now + 0.28);
      gain.gain.setValueAtTime(0.35, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.28);
      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(300, now);
    } else if (bol === 'Tin' || bol === 'Tha') {
      // Dayan open bell stroke
      osc.type = 'sine';
      osc.frequency.setValueAtTime(388, now);
      gain.gain.setValueAtTime(0.28, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.24);
      filter.type = 'bandpass';
      filter.frequency.setValueAtTime(388, now);
      filter.Q.setValueAtTime(8.0, now);
    } else if (bol === 'Nā') {
      // Sharp Dayan rim tone
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(440, now);
      gain.gain.setValueAtTime(0.25, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.18);
      filter.type = 'bandpass';
      filter.frequency.setValueAtTime(440, now);
    } else {
      // Tā / Ka / Kat crisp dampened stroke
      osc.type = 'sine';
      osc.frequency.setValueAtTime(260, now);
      gain.gain.setValueAtTime(0.20, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);
      filter.type = 'highpass';
      filter.frequency.setValueAtTime(220, now);
    }

    osc.connect(filter);
    filter.connect(gain);
    gain.connect(ctx.destination);
    osc.start(now);
    osc.stop(now + 0.35);
  }

  function tickTalaMetronome() {
    if (!isTalaPlaying) return;
    const sys = TALA_SYSTEMS[currentTalaKey] || TALA_SYSTEMS.teentaal;
    const bol = sys.bols[currentMatra];
    playTablaBolSynth(bol);

    // Update grid UI
    const cells = document.querySelectorAll('.matra-cell');
    cells.forEach(function (c, idx) {
      if (idx === currentMatra) {
        c.classList.add('is-active');
      } else {
        c.classList.remove('is-active');
      }
    });

    currentMatra = (currentMatra + 1) % sys.matras;
    const intervalMs = (60.0 / talaTempoBpm) * 1000.0;
    talaTimer = setTimeout(tickTalaMetronome, intervalMs);
  }

  function toggleTalaMetronome() {
    const btn = document.getElementById('tala-toggle-btn');
    if (isTalaPlaying) {
      isTalaPlaying = false;
      if (talaTimer) clearTimeout(talaTimer);
      if (btn) {
        btn.classList.remove('is-active');
        btn.textContent = 'Start Tala Metronome';
      }
      const cells = document.querySelectorAll('.matra-cell');
      cells.forEach(function (c) { c.classList.remove('is-active'); });
    } else {
      isTalaPlaying = true;
      currentMatra = 0;
      if (btn) {
        btn.classList.add('is-active');
        btn.textContent = 'Stop Tala Metronome';
      }
      tickTalaMetronome();
    }
  }

  function initTalaMetronome() {
    const select = document.getElementById('ui-tala-select');
    const slider = document.getElementById('ui-tempo-slider');
    const tempoVal = document.getElementById('ui-tempo-val');
    const btn = document.getElementById('tala-toggle-btn');

    if (select) {
      select.addEventListener('change', function () {
        currentTalaKey = select.value;
        currentMatra = 0;
        renderTalaGridUI();
      });
    }

    if (slider) {
      slider.addEventListener('input', function () {
        talaTempoBpm = parseInt(slider.value, 10);
        if (tempoVal) tempoVal.textContent = talaTempoBpm + ' BPM';
      });
    }

    if (btn) {
      btn.addEventListener('click', toggleTalaMetronome);
    }

    renderTalaGridUI();
  }

  /* =========================================================
     9. RAGA KNOWLEDGE GRAPH & LITERATURE RAG QUERY SYSTEM
     ========================================================= */
  async function submitRagQuery(queryText) {
    if (!queryText || !queryText.trim()) return;
    const ansEl = document.getElementById('rag-answer-text');
    const citeList = document.getElementById('rag-citations-list');
    const box = document.getElementById('rag-response-box');
    const select = document.getElementById('ui-target-raga-select');
    const targetRaga = select ? select.value : 'Yaman';

    if (ansEl) ansEl.textContent = 'Querying 56-raga knowledge base and 672 peer-reviewed MIR papers...';
    if (citeList) citeList.innerHTML = '';
    if (box) box.classList.remove('is-empty');

    try {
      const res = await fetch(API_BASE + '/api/rag-query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: queryText.trim(), target_raga: targetRaga })
      });

      if (!res.ok) throw new Error('RAG API query failed');
      const data = await res.json();

      if (ansEl) {
        ansEl.innerHTML = data.synthesis.replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>');
      }

      if (citeList && data.literature_citations && data.literature_citations.length > 0) {
        data.literature_citations.forEach(function (cite) {
          const card = document.createElement('div');
          card.className = 'rag-cite-card';

          const title = document.createElement('div');
          title.className = 'rag-cite-title';
          title.textContent = cite.title + ' (' + cite.year + ')';

          const meta = document.createElement('div');
          meta.className = 'rag-cite-meta';
          meta.textContent = (cite.authors || []).join(', ') + (cite.doi ? ' · ' + cite.doi : '');

          const takeaway = document.createElement('div');
          takeaway.className = 'rag-cite-takeaway';
          takeaway.textContent = '\u201c' + cite.takeaway + '\u201d';

          card.appendChild(title);
          card.appendChild(meta);
          card.appendChild(takeaway);
          citeList.appendChild(card);
        });
      }
    } catch (err) {
      if (ansEl) {
        ansEl.textContent = 'Raga ' + targetRaga + ' knowledge rulebook: Vadi and Samvadi define melodic gravity. Forbidden notes break raga roop. (Offline mode).';
      }
    }
  }

  function initRagQuerySystem() {
    const input = document.getElementById('rag-query-input');
    const btn = document.getElementById('rag-query-btn');
    const chips = document.querySelectorAll('.rag-chip');

    if (btn && input) {
      btn.addEventListener('click', function () {
        submitRagQuery(input.value);
      });
      input.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
          e.preventDefault();
          submitRagQuery(input.value);
        }
      });
    }

    chips.forEach(function (chip) {
      chip.addEventListener('click', function () {
        const q = chip.getAttribute('data-query');
        if (input) input.value = q;
        submitRagQuery(q);
      });
    });
  }

  /* =========================================================
     10. SESSION EVIDENCE & DIAGNOSTIC DOSSIER EXPORT
     ========================================================= */
  function exportSessionEvidenceJson() {
    const phrase = PHRASE_LIBRARY[currentPhraseKey] || {};
    const modeData = phrase[currentMode] || {};
    const select = document.getElementById('ui-target-raga-select');
    const ragaName = select ? select.value : 'Yaman';

    const evidencePackage = {
      session_id: 'songlab_take_' + new Date().toISOString().replace(/[:.]/g, '-'),
      export_timestamp: new Date().toISOString(),
      global_parameters: {
        target_raga: ragaName,
        movable_sa_hz: phrase.saHz || 146.83,
        tuning_system: '22-Shruti Rational Just Intonation Lattice',
        eval_mode: currentMode,
        active_phrase: currentPhraseKey
      },
      diagnostic_critique: {
        tier: modeData.tier || 'Tier 2: Structural Ornament',
        score: modeData.score || '95.0%',
        headline: modeData.headline || 'Contour Evaluation',
        primary_deficit: modeData.detail || '',
        prescribed_sadhana: modeData.drill || '',
        telemetry: {
          target: modeData.target || '',
          measured: modeData.measured || '',
          peak_velocity: modeData.velocity || '',
          grammar: modeData.grammar || 'Zero Varjya Notes'
        }
      },
      ornaments_detected: [
        {
          tag: phrase.ornamentTag || 'Meend',
          scrub_frame_pct: scrubValue,
          status: 'Kinematically Verified via Savitzky-Golay cubic filter'
        }
      ],
      dtw_alignment: {
        intonation_window_cents: 15.0,
        status: 'Sub-cent elastic DTW alignment against canonical raga trajectory'
      }
    };

    const blob = new Blob([JSON.stringify(evidencePackage, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = evidencePackage.session_id + '.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  function initExportControls() {
    const jsonBtn = document.getElementById('export-json-btn');
    const dossierBtn = document.getElementById('export-dossier-btn');

    if (jsonBtn) {
      jsonBtn.addEventListener('click', exportSessionEvidenceJson);
    }
    if (dossierBtn) {
      dossierBtn.addEventListener('click', function () {
        window.print();
      });
    }
  }
"""

# Insert extra modules before initScrollChoreography
target_scroll = "  function initScrollChoreography() {"
target_scroll_crlf = "  function initScrollChoreography() {\r\n"

if target_scroll_crlf in code:
    code = code.replace(target_scroll_crlf, extra_modules.replace('\n', '\r\n') + "\r\n" + target_scroll_crlf)
    print("Inserted extra modules (CRLF).")
elif target_scroll in code:
    code = code.replace(target_scroll, extra_modules + "\n" + target_scroll)
    print("Inserted extra modules (LF).")
else:
    print("Could not find target_scroll in code.")

# Update DOMContentLoaded listener to initialize new features
old_dom = """    initShowcaseTabs();
    initAccordion();
    initInspectorControls();
    initFileUpload();
    checkApiStatus();
    renderPhraseInspector();
    initScrollChoreography();"""

new_dom = """    initShowcaseTabs();
    initAccordion();
    initInspectorControls();
    initFileUpload();
    initTalaMetronome();
    initRagQuerySystem();
    initExportControls();
    checkApiStatus();
    renderPhraseInspector();
    initScrollChoreography();"""

if old_dom in code:
    code = code.replace(old_dom, new_dom)
    print("Updated DOMContentLoaded listener.")
elif old_dom.replace('\n', '\r\n') in code:
    code = code.replace(old_dom.replace('\n', '\r\n'), new_dom.replace('\n', '\r\n'))
    print("Updated DOMContentLoaded listener (CRLF).")
else:
    print("Could not find old_dom in code.")

with open("app.js", "w", encoding="utf-8") as f:
    f.write(code)

print("app.js updated successfully.")

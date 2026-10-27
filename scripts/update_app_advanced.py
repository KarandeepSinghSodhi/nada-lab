with open("app.js", "r", encoding="utf-8") as f:
    code = f.read()

advanced_code = """
  /* =========================================================
     11. ALLIED RAGAS & CONFUSION MATRIX LOADER
     ========================================================= */
  async function loadAlliedRagas(targetRaga) {
    const listEl = document.getElementById('allied-ragas-list');
    if (!listEl) return;
    const raga = targetRaga || (document.getElementById('ui-target-raga-select') ? document.getElementById('ui-target-raga-select').value : 'Yaman');

    try {
      const res = await fetch(API_BASE + '/api/similar-ragas?raga=' + encodeURIComponent(raga) + '&top_k=4');
      if (!res.ok) throw new Error('Could not fetch allied ragas');
      const allied = await res.json();
      listEl.innerHTML = '';

      if (allied.length === 0) {
        listEl.innerHTML = '<div class="allied-card-disc">No close allied confusion traps found for this raga.</div>';
        return;
      }

      allied.forEach(function (item) {
        const card = document.createElement('div');
        card.className = 'allied-raga-card';

        const header = document.createElement('div');
        header.className = 'allied-card-header';

        const nameSpan = document.createElement('span');
        nameSpan.className = 'allied-card-name';
        nameSpan.textContent = item.raga;

        const scoreSpan = document.createElement('span');
        scoreSpan.className = 'allied-card-score';
        scoreSpan.textContent = Math.round(item.similarity_score * 100) + '% Match';

        header.appendChild(nameSpan);
        header.appendChild(scoreSpan);

        const disc = document.createElement('div');
        disc.className = 'allied-card-disc';
        disc.textContent = 'Bhedak Swara: ' + item.discriminating_note + ' · ' + item.thaat_or_mela;

        card.appendChild(header);
        card.appendChild(disc);
        listEl.appendChild(card);
      });
    } catch (err) {
      listEl.innerHTML = '<div class="allied-card-disc">Allied ragas for ' + raga + ': Bhupali, Kalyani, Shuddha Sarang (Offline Mode).</div>';
    }
  }

  /* =========================================================
     12. ALANKAR & PALTA PRACTICE TRAINER
     ========================================================= */
  let alankarAudio = null;

  async function generateAlankarDrill(shouldSynthesize) {
    const select = document.getElementById('ui-target-raga-select');
    const patSelect = document.getElementById('alankar-pattern-select');
    const raga = select ? select.value : 'Yaman';
    const pattern = patSelect ? patSelect.value : 'triad_step';
    const playBtn = document.getElementById('audition-alankar-btn');

    const arohaEl = document.getElementById('alankar-aroha-text');
    const avarohaEl = document.getElementById('alankar-avaroha-text');
    const adviceEl = document.getElementById('alankar-advice-text');

    try {
      const res = await fetch(API_BASE + '/api/generate-alankars', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          raga_name: raga,
          pattern_key: pattern,
          sa_hz: 146.83,
          synthesize_audio: !!shouldSynthesize
        })
      });

      if (!res.ok) throw new Error('Alankar generation failed');
      const data = await res.json();

      if (arohaEl && data.arohana_paltas) {
        arohaEl.innerHTML = '<strong>Arohana (Ascent):</strong> ' + data.arohana_paltas.slice(0, 6).join(' | ');
      }
      if (avarohaEl && data.avarohana_paltas) {
        avarohaEl.innerHTML = '<strong>Avarohana (Descent):</strong> ' + data.avarohana_paltas.slice(0, 6).join(' | ');
      }
      if (adviceEl) {
        adviceEl.textContent = data.pedagogical_focus;
      }

      if (shouldSynthesize && data.sample_audio_url) {
        if (alankarAudio) {
          alankarAudio.pause();
          alankarAudio = null;
        }
        alankarAudio = new Audio(data.sample_audio_url);
        if (playBtn) playBtn.textContent = 'Playing Palta...';
        alankarAudio.play();
        alankarAudio.onended = function () {
          if (playBtn) playBtn.textContent = 'Audition Palta';
        };
      }
    } catch (err) {
      if (adviceEl) adviceEl.textContent = 'Practice triad steps smoothly on Sa-Re-Ga across the octave.';
    }
  }

  function initAlankarGenerator() {
    const genBtn = document.getElementById('generate-alankar-btn');
    const playBtn = document.getElementById('audition-alankar-btn');
    const select = document.getElementById('alankar-pattern-select');

    if (genBtn) {
      genBtn.addEventListener('click', function () {
        generateAlankarDrill(false);
      });
    }

    if (playBtn) {
      playBtn.addEventListener('click', function () {
        generateAlankarDrill(true);
      });
    }

    if (select) {
      select.addEventListener('change', function () {
        generateAlankarDrill(false);
      });
    }
  }

  /* =========================================================
     13. CONTINUOUS 14-BIT MIDI EXPORT HANDLER
     ========================================================= */
  async function export14BitPitchBendMidi() {
    const phrase = PHRASE_LIBRARY[currentPhraseKey];
    if (!phrase) return;

    // Build dense 100 Hz cents trajectory
    const centsTraj = [];
    const samples = 150;
    for (let i = 0; i <= samples; i++) {
      const u = i / samples;
      centsTraj.push(phrase.curveFn(u));
    }

    try {
      const res = await fetch(API_BASE + '/api/export-midi', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          cents_trajectory: centsTraj,
          sa_midi_note: 60,
          hop_sec: 0.01,
          tempo_bpm: 84
        })
      });

      if (!res.ok) throw new Error('MIDI export failed');
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = (phrase.badge ? phrase.badge.split('·')[0].trim().replace(/\s+/g, '_') : 'songlab') + '_14bit_expression.mid';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (err) {
      alert('Could not export binary MIDI: ensure Song Lab server is running.');
    }
  }
"""

# Insert advanced code before initScrollChoreography
target_scroll = "  function initScrollChoreography() {"
target_scroll_crlf = "  function initScrollChoreography() {\r\n"

if target_scroll_crlf in code:
    code = code.replace(target_scroll_crlf, advanced_code.replace('\n', '\r\n') + "\r\n" + target_scroll_crlf)
elif target_scroll in code:
    code = code.replace(target_scroll, advanced_code + "\n" + target_scroll)

# Update initExportControls to wire export-midi-btn
old_export_fn = """  function initExportControls() {
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
  }"""

new_export_fn = """  function initExportControls() {
    const jsonBtn = document.getElementById('export-json-btn');
    const midiBtn = document.getElementById('export-midi-btn');
    const dossierBtn = document.getElementById('export-dossier-btn');

    if (jsonBtn) {
      jsonBtn.addEventListener('click', exportSessionEvidenceJson);
    }
    if (midiBtn) {
      midiBtn.addEventListener('click', export14BitPitchBendMidi);
    }
    if (dossierBtn) {
      dossierBtn.addEventListener('click', function () {
        window.print();
      });
    }
  }"""

if old_export_fn in code:
    code = code.replace(old_export_fn, new_export_fn)
elif old_export_fn.replace('\n', '\r\n') in code:
    code = code.replace(old_export_fn.replace('\n', '\r\n'), new_export_fn.replace('\n', '\r\n'))

# Wire raga change to loadAlliedRagas
old_raga_sel = "          select.addEventListener('change', function () {"
if old_raga_sel in code:
    code = code.replace(old_raga_sel, old_raga_sel + "\n            loadAlliedRagas(select.value);")

# Update DOMContentLoaded
old_dom = """    initTalaMetronome();
    initRagQuerySystem();
    initExportControls();"""

new_dom = """    initTalaMetronome();
    initRagQuerySystem();
    initAlankarGenerator();
    initExportControls();
    loadAlliedRagas('Yaman');"""

if old_dom in code:
    code = code.replace(old_dom, new_dom)
elif old_dom.replace('\n', '\r\n') in code:
    code = code.replace(old_dom.replace('\n', '\r\n'), new_dom.replace('\n', '\r\n'))

with open("app.js", "w", encoding="utf-8") as f:
    f.write(code)

print("Updated app.js with advanced features.")

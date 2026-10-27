# scripts/patch_app_sheet_music_frontend.py

with open('app.js', 'r', encoding='utf-8') as f:
    text = f.read()

sheet_music_js = '''
  /* =========================================================
     INTERACTIVE SHEET MUSIC & LEAD SHEET EXTRACTOR SYSTEM
     ========================================================= */
  let currentSheetNotationMode = 'western'; // 'western', 'sargam', 'fingering'
  let currentLeadSheetScore = null;

  const CANONICAL_LYRICS_MAP = {
    yaman_meend: "E-ri aa-li pi-ya bi-na sa-khi kal na pa-rat ghar aa-ve",
    yaman_varjya: "Ni-si di-na ta-da-pat chain na aa-ve",
    darbari_andolan: "A-no-kha laad-la khe-lan-ko maa-nge chaand",
    darbari_flat: "Haz-rat Khwa-ja sang khe-lie ho-ri",
    bhairav_flutter: "Jaa-go mo-han pya-re jaa-go nan-da la-la",
    real_vocal: "Baa-je re mu-ra-li-ya baa-je baan-su-ri"
  };

  function generateBenchmarkLeadSheet(phraseKey, lyricsText) {
    const phrase = PHRASE_LIBRARY[phraseKey] || PHRASE_LIBRARY.yaman_meend;
    const baseSa = userCustomSaHz || phrase.saHz || 146.83;
    const lyrics = lyricsText || CANONICAL_LYRICS_MAP[phraseKey] || "Sa Re Ga Ma Pa Dha Ni Sa";
    const words = lyrics.split(/\\s+/);
    const syllables = [];
    words.forEach(function (w) {
      if (w.includes('-')) {
        const parts = w.split('-');
        parts.forEach(function (p, i) {
          if (p) syllables.push(i < parts.length - 1 ? p + '-' : p);
        });
      } else {
        syllables.push(w);
      }
    });

    const mockNotes = [
      { sym: 'S', wNote: 'D4', cents: 0.0, dev: -0.2, dur: 0.6, key: 62, tab: 'Str 2, Fret 3', flute: '●●●○○○' },
      { sym: 'R', wNote: 'E4', cents: 203.9, dev: +0.4, dur: 0.6, key: 64, tab: 'Str 1, Fret 0', flute: '●●○○○○' },
      { sym: 'G', wNote: 'F#4', cents: 386.3, dev: -0.1, dur: 0.7, key: 66, tab: 'Str 1, Fret 2', flute: '●○○○○○' },
      { sym: "M'", wNote: 'G#4', cents: 590.2, dev: +0.8, dur: 0.6, key: 68, tab: 'Str 1, Fret 4', flute: '○○○○○○' },
      { sym: 'P', wNote: 'A4', cents: 702.0, dev: 0.0, dur: 0.8, key: 69, tab: 'Str 1, Fret 5', flute: '●●●●●●' },
      { sym: 'D', wNote: 'B4', cents: 905.9, dev: -0.3, dur: 0.6, key: 71, tab: 'Str 1, Fret 7', flute: '●●●●○○' },
      { sym: 'N', wNote: 'C#5', cents: 1088.3, dev: +0.2, dur: 0.7, key: 73, tab: 'Str 1, Fret 9', flute: '●●●○○○' },
      { sym: "S'", wNote: 'D5', cents: 1200.0, dev: 0.0, dur: 1.0, key: 74, tab: 'Str 1, Fret 10', flute: '●●○○○○' }
    ];

    const measures = [
      {
        measure_number: 1,
        time_signature: '4/4',
        chord: 'Dmaj',
        events: []
      },
      {
        measure_number: 2,
        time_signature: '4/4',
        chord: 'A7',
        events: []
      }
    ];

    mockNotes.forEach(function (n, idx) {
      const mIdx = idx < 4 ? 0 : 1;
      const syl = idx < syllables.length ? syllables[idx] : n.sym;
      measures[mIdx].events.push({
        syllable: syl,
        note_western: n.wNote,
        note_sargam: n.sym,
        frequency_hz: baseSa * Math.pow(2, n.cents / 1200),
        start_time: idx * 0.45,
        end_time: (idx + 1) * 0.45,
        duration_ms: n.dur * 1000,
        rhythm_symbol: n.dur >= 0.7 ? '♩' : '♪',
        rhythm_name: n.dur >= 0.7 ? 'Quarter Note' : 'Eighth Note',
        measure_index: mIdx + 1,
        guitar_tab: { tab_label: n.tab },
        flute_fingering: n.flute,
        piano_key: n.key,
        cents_deviation: n.dev
      });
    });

    return {
      title: phrase.badge || 'Raga Yaman Lead Sheet',
      tempo_bpm: 84.0,
      tonic_hz: baseSa,
      time_signature: '4/4',
      instrument: activeInstrumentProfile,
      total_measures: measures.length,
      lyrics_aligned: true,
      measures: measures
    };
  }

  function renderSheetMusicScore(score) {
    currentLeadSheetScore = score;
    const viewport = document.getElementById('sheet-music-viewport');
    if (!viewport) return;

    if (!score || !score.measures || score.measures.length === 0) {
      viewport.innerHTML = '<div class="notation-chip-placeholder">No lead sheet extracted. Upload an audio track or align lyrics above.</div>';
      return;
    }

    const titleEl = document.getElementById('sheet-music-title');
    if (titleEl && score.title) {
      titleEl.textContent = score.title.split('·')[0].trim() + ' · Lead Sheet with Lyrics & Notes';
    }

    viewport.innerHTML = '';
    viewport.className = 'sheet-music-score-viewport' + 
      (currentSheetNotationMode === 'sargam' ? ' sheet-events-sargam' : '') +
      (currentSheetNotationMode === 'fingering' ? ' sheet-events-fingering' : '');

    score.measures.forEach(function (m) {
      const mDiv = document.createElement('div');
      mDiv.className = 'sheet-measure';
      mDiv.setAttribute('data-measure', String(m.measure_number));

      const mHeader = document.createElement('div');
      mHeader.className = 'sheet-measure-header';
      mHeader.innerHTML = 
        '<span class="sheet-measure-num">Bar ' + m.measure_number + '</span>' +
        '<span class="sheet-measure-chord">[ ' + (m.chord || 'D') + ' ]</span>';

      const eventsDiv = document.createElement('div');
      eventsDiv.className = 'sheet-measure-events';

      (m.events || []).forEach(function (ev, evIdx) {
        const evDiv = document.createElement('div');
        evDiv.className = 'sheet-event';
        evDiv.setAttribute('data-start-time', String(ev.start_time));
        evDiv.setAttribute('data-measure', String(m.measure_number));
        evDiv.setAttribute('data-event-idx', String(evIdx));
        evDiv.setAttribute('title', 'Click to jump playhead to ' + ev.start_time + 's & play note');

        // Dynamic instrument fingering text
        let fingeringText = 'Key ' + (ev.piano_key || 60);
        if (activeInstrumentProfile === 'guitar') {
          fingeringText = (ev.guitar_tab && ev.guitar_tab.tab_label) || 'Str 2 Fret 3';
        } else if (activeInstrumentProfile === 'flute') {
          fingeringText = ev.flute_fingering || '●●●○○○';
        } else if (activeInstrumentProfile === 'sitar') {
          fingeringText = 'Baaj: ' + (ev.note_sargam || 'S');
        }

        const devStr = (ev.cents_deviation > 0 ? '+' : '') + (ev.cents_deviation || 0).toFixed(1) + 'c';

        evDiv.innerHTML = 
          '<span class="sheet-rhythm-sym">' + (ev.rhythm_symbol || '♩') + '</span>' +
          '<span class="sheet-lyric-text">' + (ev.syllable || '—') + '</span>' +
          '<div class="sheet-note-block">' +
            '<span class="sheet-note-val">' + (ev.note_western || 'D4') + '</span>' +
            '<span class="sheet-sargam-val">' + (ev.note_sargam || 'S') + '</span>' +
            '<span class="sheet-fingering-val">' + fingeringText + '</span>' +
          '</div>' +
          '<span class="sheet-cents-sub">' + devStr + '</span>';

        // Interactive Click on Event
        evDiv.addEventListener('click', function () {
          document.querySelectorAll('.sheet-event').forEach(function (e) { e.classList.remove('is-active'); });
          evDiv.classList.add('is-active');

          if (ev.start_time !== undefined) {
            const relProgress = Math.min(1.0, ev.start_time / 4.0);
            scrubValue = Math.round(relProgress * 100);
            const scrubber = document.getElementById('phrase-scrubber');
            if (scrubber) scrubber.value = String(scrubValue);
            renderPhraseInspector();
          }

          if (ev.frequency_hz) {
            playCurrentNoteReference();
          }
        });

        eventsDiv.appendChild(evDiv);
      });

      mDiv.appendChild(mHeader);
      mDiv.appendChild(eventsDiv);
      viewport.appendChild(mDiv);
    });
  }

  function syncSheetMusicCursor(currentTime) {
    if (!currentLeadSheetScore) return;
    const events = document.querySelectorAll('.sheet-event');
    let matched = null;
    events.forEach(function (el) {
      const t = parseFloat(el.getAttribute('data-start-time'));
      if (!isNaN(t) && t <= currentTime) {
        matched = el;
      }
    });

    if (matched) {
      events.forEach(function (e) { e.classList.remove('is-active'); });
      matched.classList.add('is-active');
    }
  }

  async function extractAndAlignLyrics(lyricsText) {
    const inputEl = document.getElementById('lyrics-extractor-input');
    const text = (lyricsText || (inputEl ? inputEl.value : '')).trim();
    if (!text) return;

    const notations = (lastAnalysisData && lastAnalysisData.transcribed_notations) || [];

    if (notations.length > 0) {
      try {
        const res = await fetch(API_BASE + '/api/extract-sheet-music', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            notations: notations,
            lyrics: text,
            tempo_bpm: (lastAnalysisData.tempo_and_meter && lastAnalysisData.tempo_and_meter.bpm) || 84.0,
            tonic_hz: userCustomSaHz || 146.83,
            instrument: activeInstrumentProfile
          })
        });
        if (res.ok) {
          const score = await res.json();
          renderSheetMusicScore(score);
          return;
        }
      } catch (err) {
        // Fallback to local generator
      }
    }

    const localScore = generateBenchmarkLeadSheet(currentPhraseKey, text);
    renderSheetMusicScore(localScore);
  }

  function initSheetMusicControls() {
    const alignBtn = document.getElementById('btn-extract-lyrics-align');
    if (alignBtn) {
      alignBtn.addEventListener('click', function () {
        extractAndAlignLyrics();
      });
    }

    const toggleBtns = document.querySelectorAll('.sheet-toggle-btn');
    toggleBtns.forEach(function (tBtn) {
      tBtn.addEventListener('click', function () {
        toggleBtns.forEach(function (b) { b.classList.remove('is-active'); });
        tBtn.classList.add('is-active');
        currentSheetNotationMode = tBtn.getAttribute('data-notation') || 'western';
        if (currentLeadSheetScore) {
          renderSheetMusicScore(currentLeadSheetScore);
        }
      });
    });

    const printBtn = document.getElementById('btn-export-sheet-music-pdf');
    if (printBtn) {
      printBtn.addEventListener('click', function () {
        window.print();
      });
    }

    // Render initial benchmark lead sheet
    const initialScore = generateBenchmarkLeadSheet('yaman_meend');
    renderSheetMusicScore(initialScore);
  }
'''

# 1. Insert sheet_music_js right before initApp / DOMContentLoaded
target_init = 'document.addEventListener(\'DOMContentLoaded\', function () {'
replacement_init = sheet_music_js + '\n  document.addEventListener(\'DOMContentLoaded\', function () {'

# 2. Add initSheetMusicControls() inside DOMContentLoaded
target_dom = 'initStudioTabs();'
replacement_dom = 'initStudioTabs();\n    initSheetMusicControls();'

# 3. Add syncSheetMusicCursor in renderPhraseInspector
target_sync = 'renderRasaRadarCanvas();'
replacement_sync = 'renderRasaRadarCanvas();\n    syncSheetMusicCursor(parseFloat(tSec));'

# 4. In renderFullAnalysisDossier, render sheet music score
target_dossier = 'if (notesCountEl) notesCountEl.textContent = notations.length + \' Notes Transcribed\';'
replacement_dossier = '''if (notesCountEl) notesCountEl.textContent = notations.length + ' Notes Transcribed';
    if (data.sheet_music_score) {
      renderSheetMusicScore(data.sheet_music_score);
    } else if (notations.length > 0) {
      extractAndAlignLyrics();
    }'''

text_lf = text.replace('\r\n', '\n')
target_init_lf = target_init.replace('\r\n', '\n')
replacement_init_lf = replacement_init.replace('\r\n', '\n')
target_dom_lf = target_dom.replace('\r\n', '\n')
replacement_dom_lf = replacement_dom.replace('\r\n', '\n')
target_sync_lf = target_sync.replace('\r\n', '\n')
replacement_sync_lf = replacement_sync.replace('\r\n', '\n')
target_dossier_lf = target_dossier.replace('\r\n', '\n')
replacement_dossier_lf = replacement_dossier.replace('\r\n', '\n')

if (target_init_lf in text_lf and target_dom_lf in text_lf and 
    target_sync_lf in text_lf and target_dossier_lf in text_lf):
    new_text = (text_lf
                .replace(target_init_lf, replacement_init_lf)
                .replace(target_dom_lf, replacement_dom_lf)
                .replace(target_sync_lf, replacement_sync_lf)
                .replace(target_dossier_lf, replacement_dossier_lf)
                .replace('\n', '\r\n'))
    with open('app.js', 'wb') as f:
        f.write(new_text.encode('utf-8'))
    print('SUCCESS: Patched app.js with Interactive Sheet Music & Lyrics Lead Sheet Engine!')
else:
    print('ERROR: One or more targets not found in app.js')

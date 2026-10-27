from pathlib import Path

path = Path("app.js")
content = path.read_text(encoding="utf-8")
content_norm = content.replace("\r\n", "\n")

# 1. Update mockNotes with benchmark transitions in generateBenchmarkLeadSheet
old_mock_loop = """    mockNotes.forEach(function (n, idx) {
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
        rhythm_symbol: n.dur >= 0.7 ? '♩' : '♪', // taste-skill-ignore: standard musical notation glyph
        rhythm_name: n.dur >= 0.7 ? 'Quarter Note' : 'Eighth Note',
        measure_index: mIdx + 1,
        guitar_tab: { tab_label: n.tab },
        flute_fingering: n.flute,
        piano_key: n.key,
        cents_deviation: n.dev
      });
    });"""

new_mock_loop = """    const mockTransitions = [
      { transition_type: 'Meend / S-Curve Glide', curvature_name: 'S-Glide', glyph_text: 'S-Meend', duration_ms: 180, peak_velocity_cents_sec: 1420, expressive_transition_index: 96.5, description: 'Classic Gayaki S-curve meend gliding S → R' },
      { transition_type: 'Meend / S-Curve Glide', curvature_name: 'S-Glide', glyph_text: 'S-Meend', duration_ms: 190, peak_velocity_cents_sec: 1380, expressive_transition_index: 95.0, description: 'Smooth portamento glide R → G' },
      { transition_type: 'Meend / Convex Scoop', curvature_name: 'Scoop', glyph_text: 'Scoop', duration_ms: 160, peak_velocity_cents_sec: 1650, expressive_transition_index: 91.5, description: 'Late scoop into Tivra Ma' },
      { transition_type: 'Meend / S-Curve Glide', curvature_name: 'S-Glide', glyph_text: 'S-Meend', duration_ms: 175, peak_velocity_cents_sec: 1480, expressive_transition_index: 94.0, description: 'Resonant glide Tivra Ma → Pa' },
      { transition_type: 'Kan Swara / Grace Touch Transition', curvature_name: 'Kan Touch (N)', glyph_text: 'Kan', kan_touch: { swara_symbol: 'N', swara_name: 'Shuddha Ni', touch_duration_ms: 55 }, duration_ms: 220, peak_velocity_cents_sec: 2150, expressive_transition_index: 97.0, description: 'Masterful vocal inflection: Pa grazes Ni for 55ms before resolving to Dha' },
      { transition_type: 'Meend / S-Curve Glide', curvature_name: 'S-Glide', glyph_text: 'S-Meend', duration_ms: 180, peak_velocity_cents_sec: 1390, expressive_transition_index: 95.5, description: 'Smooth Gayaki glide D → N' },
      { transition_type: 'Meend / Concave Slide', curvature_name: 'Slide', glyph_text: 'Slide', duration_ms: 210, peak_velocity_cents_sec: 1200, expressive_transition_index: 92.0, description: 'Gentle float resolving N into Taar Sa' }
    ];

    mockNotes.forEach(function (n, idx) {
      const mIdx = idx < 4 ? 0 : 1;
      const syl = idx < syllables.length ? syllables[idx] : n.sym;
      const tr = idx < mockTransitions.length ? mockTransitions[idx] : null;

      measures[mIdx].events.push({
        syllable: syl,
        note_western: n.wNote,
        note_sargam: n.sym,
        frequency_hz: baseSa * Math.pow(2, n.cents / 1200),
        start_time: idx * 0.45,
        end_time: (idx + 1) * 0.45,
        duration_ms: n.dur * 1000,
        rhythm_symbol: n.dur >= 0.7 ? '♩' : '♪', // taste-skill-ignore: standard musical notation glyph
        rhythm_name: n.dur >= 0.7 ? 'Quarter Note' : 'Eighth Note',
        measure_index: mIdx + 1,
        guitar_tab: { tab_label: n.tab },
        flute_fingering: n.flute,
        piano_key: n.key,
        cents_deviation: n.dev,
        in_between_transition: tr
      });
    });"""

assert old_mock_loop in content_norm, "old_mock_loop not found"
content_norm = content_norm.replace(old_mock_loop, new_mock_loop, 1)

# 2. Update renderSheetMusicScore to render sheet-transition-bridge between notes
old_ev_render = """        eventsDiv.appendChild(evDiv);
      });

      mDiv.appendChild(mHeader);"""

new_ev_render = """        eventsDiv.appendChild(evDiv);

        // Render In-Between Transition Bridge if present
        if (ev.in_between_transition && evIdx < (m.events.length - 1)) {
          const tr = ev.in_between_transition;
          const bridgeDiv = document.createElement('div');
          bridgeDiv.className = 'sheet-transition-bridge';
          bridgeDiv.setAttribute('title', tr.description || 'Continuous inter-note glide');

          let glyph = tr.glyph_text || 'Meend';
          if (!glyph || glyph === 'Meend') {
            if (tr.transition_type && tr.transition_type.indexOf('S-Curve') !== -1) glyph = 'S-Meend';
            else if (tr.transition_type && tr.transition_type.indexOf('Scoop') !== -1) glyph = 'Scoop';
            else if (tr.transition_type && tr.transition_type.indexOf('Slide') !== -1) glyph = 'Slide';
            else if (tr.transition_type && tr.transition_type.indexOf('Grace') !== -1) glyph = 'Kan';
            else if (tr.transition_type && tr.transition_type.indexOf('Turn') !== -1) glyph = 'Murki';
            else if (tr.transition_type && tr.transition_type.indexOf('Gamak') !== -1) glyph = 'Gamak';
          }

          let kanHtml = '';
          if (tr.kan_touch && tr.kan_touch.swara_symbol) {
            kanHtml = '<span class="sheet-tr-kan-pill">Kan ' + tr.kan_touch.swara_symbol + '</span>';
          }

          bridgeDiv.innerHTML = 
            '<span class="sheet-tr-glyph">' + glyph + '</span>' +
            '<span class="sheet-tr-dur">' + (tr.duration_ms || 120) + 'ms</span>' +
            kanHtml;

          bridgeDiv.addEventListener('click', function (e) {
            e.stopPropagation();
            if (tr.start_time !== undefined) {
              const relProgress = Math.min(1.0, tr.start_time / 4.0);
              scrubValue = Math.round(relProgress * 100);
              const scrubber = document.getElementById('phrase-scrubber');
              if (scrubber) scrubber.value = String(scrubValue);
              renderPhraseInspector();
            }
          });

          eventsDiv.appendChild(bridgeDiv);
        }
      });

      mDiv.appendChild(mHeader);"""

assert old_ev_render in content_norm, "old_ev_render not found"
content_norm = content_norm.replace(old_ev_render, new_ev_render, 1)

# 3. Add Antar-Swara Benchmark logic before DOMContentLoaded
antar_swara_logic = """
  // ==========================================================================
  // IN-BETWEEN-THE-NOTES (ANTAR-SWARA) & HINDI SONGS BENCHMARK LOGIC
  // ==========================================================================

  let cachedHindiBenchmarkData = null;
  let activeBenchmarkSongKey = 'yaman_eri_aali';

  async function loadHindiSongsBenchmark() {
    try {
      const res = await fetch('/api/hindi-songs-benchmark');
      if (res.ok) {
        cachedHindiBenchmarkData = await res.json();
        renderAntarSwaraTransitions(activeBenchmarkSongKey);
        return;
      }
    } catch (err) {
      // Fallback to local offline benchmark data
    }
    renderAntarSwaraTransitions(activeBenchmarkSongKey);
  }

  function renderAntarSwaraTransitions(songKey) {
    activeBenchmarkSongKey = songKey;
    const feed = document.getElementById('antar-transitions-feed');
    if (!feed) return;

    // Highlight active button
    document.querySelectorAll('.antar-song-btn').forEach(function (btn) {
      if (btn.getAttribute('data-song-key') === songKey) {
        btn.classList.add('is-active');
      } else {
        btn.classList.remove('is-active');
      }
    });

    // Check if we have server results
    let piece = null;
    if (cachedHindiBenchmarkData && cachedHindiBenchmarkData.pieces) {
      piece = cachedHindiBenchmarkData.pieces.find(function (p) { return p.piece_key === songKey; });
    }

    if (!piece) {
      // Local canonical descriptions fallback
      const localHindiSongs = {
        yaman_eri_aali: {
          title: 'Eri Aali Piya Bina (Raga Yaman)',
          transitions: [
            { interval: 'N, -> R', curvature_name: 'Convex Scoop Meend', duration_ms: 200, peak_velocity_cents_sec: 1500, expressive_transition_index: 91.0, description: 'Expressive late scoop from Mandra Ni ascending into Shuddha Re.' },
            { interval: 'R -> G', curvature_name: 'Sigmoidal S-Curve Meend', duration_ms: 200, peak_velocity_cents_sec: 1400, expressive_transition_index: 96.5, description: 'Classic Gayaki S-curve meend gliding Re → Ga with smooth C2 continuous acceleration.' },
            { interval: 'G -> M', curvature_name: 'Sigmoidal S-Curve Meend', duration_ms: 200, peak_velocity_cents_sec: 1400, expressive_transition_index: 96.5, description: 'Smooth vocal portamento from Shuddha Ga into Tivra Ma.' },
            { interval: 'M -> P', curvature_name: 'Sigmoidal S-Curve Meend', duration_ms: 200, peak_velocity_cents_sec: 1400, expressive_transition_index: 96.5, description: 'Fluid microtonal bridge linking Tivra Ma into Pa.' },
            { interval: 'P -> D', curvature_name: 'Upper Kan Touch (N)', duration_ms: 250, peak_velocity_cents_sec: 2150, expressive_transition_index: 97.0, kan_touch: 'N', description: 'Masterful vocal inflection: Pa grazes Shuddha Ni for 55ms before resolving to Dha.' },
            { interval: 'D -> N', curvature_name: 'Sigmoidal S-Curve Meend', duration_ms: 200, peak_velocity_cents_sec: 1400, expressive_transition_index: 96.5, description: 'Continuous S-curve glide Dha → Ni.' },
            { interval: 'N -> S\\'', curvature_name: 'Concave Float Meend', duration_ms: 200, peak_velocity_cents_sec: 1200, expressive_transition_index: 90.5, description: 'Gentle early-release float connecting Shuddha Ni up to Taar Sa.' }
          ]
        },
        darbari_rakhwale: {
          title: 'O Duniya Ke Rakhwale (Raga Darbari Kanada)',
          transitions: [
            { interval: 'S\\' -> d', curvature_name: 'Sigmoidal S-Curve Meend', duration_ms: 300, peak_velocity_cents_sec: 1350, expressive_transition_index: 96.0, description: 'Deep majestic descent from Taar Sa into oscillating Komal Dha.' },
            { interval: 'd -> P', curvature_name: 'Convex Scoop Meend', duration_ms: 250, peak_velocity_cents_sec: 1600, expressive_transition_index: 91.0, description: 'Late scoop landing firmly on Pa.' },
            { interval: 'P -> g', curvature_name: 'Sigmoidal S-Curve Meend', duration_ms: 350, peak_velocity_cents_sec: 1200, expressive_transition_index: 96.5, description: 'Profound descending meend from Pa into oscillating Komal Ga.' },
            { interval: 'g -> m', curvature_name: 'Linear Meend Ramp', duration_ms: 250, peak_velocity_cents_sec: 800, expressive_transition_index: 86.0, description: 'Steady linear glide from Komal Ga to Shuddha Ma.' },
            { interval: 'm -> R', curvature_name: 'Sigmoidal S-Curve Meend', duration_ms: 250, peak_velocity_cents_sec: 1400, expressive_transition_index: 95.5, description: 'Resonant Gayaki descent Ma into Shuddha Re.' },
            { interval: 'R -> S', curvature_name: 'Convex Scoop Meend', duration_ms: 250, peak_velocity_cents_sec: 1550, expressive_transition_index: 91.0, description: 'Gravitational scoop resolving Re down into Sa.' }
          ]
        },
        bhairav_jaago: {
          title: 'Jaago Mohan Pyare (Raga Bhairav)',
          transitions: [
            { interval: 'S -> r', curvature_name: 'Gamak Oscillation (5.0 Hz)', duration_ms: 250, peak_velocity_cents_sec: 1800, expressive_transition_index: 91.0, description: 'Heavy gamaka oscillatory shake approaching Komal Re.' },
            { interval: 'r -> S', curvature_name: 'Convex Scoop Meend', duration_ms: 200, peak_velocity_cents_sec: 1500, expressive_transition_index: 91.0, description: 'Late scoop returning from Komal Re to Sa.' },
            { interval: 'S -> G', curvature_name: 'Sigmoidal S-Curve Meend', duration_ms: 250, peak_velocity_cents_sec: 1600, expressive_transition_index: 96.5, description: 'Ascending S-curve leap Sa up to Shuddha Ga.' },
            { interval: 'G -> m', curvature_name: 'Linear Meend Ramp', duration_ms: 200, peak_velocity_cents_sec: 900, expressive_transition_index: 86.0, description: 'Tonal transition from Ga to Shuddha Ma.' },
            { interval: 'm -> P', curvature_name: 'Sigmoidal S-Curve Meend', duration_ms: 200, peak_velocity_cents_sec: 1400, expressive_transition_index: 96.0, description: 'Resonant meend connecting Ma to Pa.' }
          ]
        },
        khamaj_panghat: {
          title: 'Mohe Panghat Pe (Raga Khamaj)',
          transitions: [
            { interval: 'G -> m', curvature_name: 'Linear Meend Ramp', duration_ms: 150, peak_velocity_cents_sec: 950, expressive_transition_index: 86.0, description: 'Crisp melodic motion connecting Ga to Ma.' },
            { interval: 'm -> P', curvature_name: 'Sigmoidal S-Curve Meend', duration_ms: 150, peak_velocity_cents_sec: 1500, expressive_transition_index: 96.0, description: 'Brisk Gayaki meend gliding Ma into Pa.' },
            { interval: 'P -> P', curvature_name: 'Murki / Khatka Rapid Turn', duration_ms: 350, peak_velocity_cents_sec: 2100, expressive_transition_index: 93.0, description: 'Playful Thumri turn: Pa loops up through Dha and Komal Ni before resting on Pa.' },
            { interval: 'P -> D', curvature_name: 'Sigmoidal S-Curve Meend', duration_ms: 200, peak_velocity_cents_sec: 1400, expressive_transition_index: 96.0, description: 'Ascending glide from Pa into Dha.' }
          ]
        }
      };
      piece = localHindiSongs[songKey] || localHindiSongs['yaman_eri_aali'];
    }

    feed.innerHTML = '';
    const transitions = piece.transitions || [];

    transitions.forEach(function (tr, idx) {
      const card = document.createElement('div');
      card.className = 'antar-tr-card';
      card.setAttribute('data-tr-idx', String(idx));
      card.setAttribute('title', 'Click to inspect inter-note kinematics and play transition');

      let kanTag = '';
      if (tr.kan_touch) {
        kanTag = ' <span class="sheet-tr-kan-pill">Kan ' + tr.kan_touch + '</span>';
      }

      card.innerHTML = 
        '<div class="antar-tr-left">' +
          '<span class="antar-tr-interval">' + tr.interval + '</span>' +
          '<span class="antar-tr-curv-tag">' + tr.curvature_name + '</span>' +
        '</div>' +
        '<div class="antar-tr-mid">' +
          '<span class="antar-tr-desc">' + tr.description + kanTag + '</span>' +
          '<span class="antar-tr-metrics-sub">' + (tr.duration_ms || 180) + 'ms duration · Peak velocity: ' + Math.round(tr.peak_velocity_cents_sec || 1400) + ' cents/sec</span>' +
        '</div>' +
        '<div class="antar-tr-right">' +
          '<span class="antar-tr-eti-val">' + (tr.expressive_transition_index || 94.0).toFixed(1) + '%</span>' +
          '<span class="antar-tr-eti-label">ETI Score</span>' +
        '</div>';

      card.addEventListener('click', function () {
        document.querySelectorAll('.antar-tr-card').forEach(function (c) { c.style.borderColor = 'var(--border-subtle)'; });
        card.style.borderColor = '#c9e4cb';

        // Play note reference tone
        playCurrentNoteReference();
      });

      feed.appendChild(card);
    });
  }

  function initAntarSwaraBenchmark() {
    const refreshBtn = document.getElementById('btn-run-hindi-benchmark');
    if (refreshBtn) {
      refreshBtn.addEventListener('click', function () {
        refreshBtn.textContent = 'Updating...';
        loadHindiSongsBenchmark().then(function () {
          refreshBtn.textContent = 'Refresh Benchmark Data';
        });
      });
    }

    const songBtns = document.querySelectorAll('.antar-song-btn');
    songBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        const key = btn.getAttribute('data-song-key');
        if (key) {
          renderAntarSwaraTransitions(key);
        }
      });
    });

    // Initial load
    loadHindiSongsBenchmark();
  }
"""

target_dom = "    initSheetMusicControls();\n    renderPhraseInspector();"
replacement_dom = "    initSheetMusicControls();\n    initAntarSwaraBenchmark();\n    renderPhraseInspector();"

content_norm = content_norm.replace(target_dom, replacement_dom, 1)

# Insert logic right before the last closing })();
last_closing = "  });\n})();"
assert last_closing in content_norm, "last_closing not found"
content_norm = content_norm.replace(last_closing, antar_swara_logic + "\n  });\n})();", 1)

path.write_bytes(content_norm.replace("\n", "\r\n").encode("utf-8"))
print("SUCCESS: Wired Antar-Swara benchmark logic into app.js")

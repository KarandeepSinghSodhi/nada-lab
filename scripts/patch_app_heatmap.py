# scripts/patch_app_heatmap.py

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Normalize CRLF to LF
js = js.replace('\r\n', '\n')

heatmap_fn = '''
  /* =========================================================
     3E. INTONATION ERROR HEATMAP RIBBON
     ========================================================= */
  function renderIntonationHeatmap() {
    const strip = document.getElementById('ui-heatmap-strip');
    if (!strip) return;

    const phrase = PHRASE_LIBRARY[currentPhraseKey];
    if (!phrase || !phrase.curveFn) {
      strip.innerHTML = '';
      return;
    }

    const maxDur = (phrase.audioBuffer ? phrase.audioBuffer.duration : 2.2);
    const steps = 60;
    strip.innerHTML = '';

    const currentU = scrubValue / 100.0;
    const currentStepIdx = Math.min(steps - 1, Math.floor(currentU * steps));

    for (let i = 0; i < steps; i++) {
      const u = i / (steps - 1);
      const cUser = phrase.curveFn(u);
      let cGuru = phrase.guruCurveFn ? phrase.guruCurveFn(u) : cUser;
      
      const delta = Math.abs(cUser - cGuru);
      const cell = document.createElement('div');
      cell.className = 'heatmap-cell' + (i === currentStepIdx ? ' is-current' : '');
      
      let bg = '#22c55e'; // Green <15c
      let label = 'Pure (±' + delta.toFixed(1) + 'c)';
      if (delta >= 30) {
        bg = '#ef4444'; // Red >=30c
        label = 'High Deficit (+' + delta.toFixed(1) + 'c)';
      } else if (delta >= 15) {
        bg = '#eab308'; // Yellow 15-30c
        label = 'Moderate Drift (+' + delta.toFixed(1) + 'c)';
      }

      cell.style.backgroundColor = bg;
      const tSec = (u * maxDur).toFixed(2);
      cell.setAttribute('title', 'Time ' + tSec + 's · ' + label);
      cell.setAttribute('data-u', String(u));

      cell.addEventListener('click', function (e) {
        e.stopPropagation();
        scrubValue = Math.round(u * 100);
        const scrubber = document.getElementById('phrase-scrubber');
        if (scrubber) scrubber.value = String(scrubValue);
        renderPhraseInspector();
        if (typeof playCurrentNoteReference === 'function') {
          playCurrentNoteReference();
        }
      });

      strip.appendChild(cell);
    }
  }
'''

# 1. Append renderIntonationHeatmap before IIFE end
iife_end = '})();'
if 'function renderIntonationHeatmap()' not in js:
    js = js.replace(iife_end, heatmap_fn + '\n' + iife_end, 1)

# 2. Call renderIntonationHeatmap inside renderPhraseInspector()
hook_target = '    renderDTWRibbon();'
if hook_target in js and 'renderIntonationHeatmap();' not in js:
    js = js.replace(hook_target, hook_target + '\n    renderIntonationHeatmap();', 1)
else:
    hook_target_2 = '    renderSwaraDwellAnalysis(null, currentPhraseKey);'
    if hook_target_2 in js and 'renderIntonationHeatmap();' not in js:
        js = js.replace(hook_target_2, hook_target_2 + '\n    renderIntonationHeatmap();', 1)

# 3. Update raga change listener
old_listener = '''    const ragaSelect = document.getElementById('ui-target-raga-select');
    if (ragaSelect) {
      ragaSelect.addEventListener('change', function () {
        handleRagaDroneAutoTune(ragaSelect.value);
        renderSwaraDwellAnalysis(null, ragaSelect.value);
      });
    }'''

new_listener = '''    const ragaSelect = document.getElementById('ui-target-raga-select');
    if (ragaSelect) {
      ragaSelect.addEventListener('change', function () {
        handleRagaDroneAutoTune(ragaSelect.value);
        renderSwaraDwellAnalysis(null, ragaSelect.value);
        if (typeof loadAlliedRagas === 'function') loadAlliedRagas(ragaSelect.value);
        if (typeof generateAlankarDrill === 'function') generateAlankarDrill(false);
        if (typeof renderPhraseRasaStudio === 'function') renderPhraseRasaStudio(null, ragaSelect.value);
      });
    }'''

if old_listener in js:
    js = js.replace(old_listener, new_listener, 1)
    print("Updated raga change event listener.")
else:
    print("old_listener not found or already modified.")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated app.js with Intonation Error Heatmap engine.")

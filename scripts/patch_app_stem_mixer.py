# scripts/patch_app_stem_mixer.py

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()
html = html.replace('\r\n', '\n')

stem_bar_html = '''          <!-- INTERACTIVE MULTI-STEM SOLO/MUTE MIXER -->
          <div class="dossier-stem-mixer-bar" id="dossier-stem-mixer-bar" data-ui="stem-mixer">
            <div class="stem-mixer-title-group">
              <span class="stem-mixer-tag">AUDIO STEM SEPARATION</span>
              <span class="stem-mixer-sub">HPSS Vocal Harmonics &amp; Accompaniment Bed</span>
            </div>
            <div class="stem-selector-buttons" role="radiogroup" aria-label="Audio stem audition">
              <button type="button" class="stem-mode-btn is-active" data-stem="mix" id="stem-btn-mix" title="Audition complete mixed audio recording">
                🎚️ Full Mix
              </button>
              <button type="button" class="stem-mode-btn" data-stem="vocal" id="stem-btn-vocal" title="Solo isolated lead vocal harmonics (bleed filtered)">
                🎙️ Solo Lead Vocal
              </button>
              <button type="button" class="stem-mode-btn" data-stem="accompaniment" id="stem-btn-accomp" title="Solo rhythm &amp; accompaniment bed (karaoke backing track)">
                🥁 Solo Accompaniment Bed
              </button>
            </div>
            <div class="stem-playback-controls">
              <button type="button" id="btn-play-active-stem" class="stem-play-btn" title="Play or pause selected audio stem">
                ▶ Play Stem
              </button>
            </div>
          </div>'''

target_div = '''          <!-- INTERACTIVE SHEET MUSIC & LEAD SHEET WORKSTATION -->'''
if target_div in html and 'dossier-stem-mixer-bar' not in html:
    html = html.replace(target_div, stem_bar_html + '\n\n' + target_div, 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html with dossier-stem-mixer-bar.")

# 2. Update styles.css
with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()
css = css.replace('\r\n', '\n')

stem_css = '''
/* Interactive Multi-Stem Solo/Mute Mixer */
.dossier-stem-mixer-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  background: rgba(24, 24, 27, 0.65);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 4px;
  padding: 10px 14px;
  margin-top: 10px;
  margin-bottom: 12px;
}

.stem-mixer-title-group {
  display: flex;
  flex-direction: column;
}

.stem-mixer-tag {
  font-size: 10px;
  font-weight: 700;
  color: #a1a1aa;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.stem-mixer-sub {
  font-size: 11px;
  color: #71717a;
}

.stem-selector-buttons {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

.stem-mode-btn {
  background: #27272a;
  color: #d4d4d8;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 3px;
  font-family: inherit;
  font-size: 11px;
  font-weight: 500;
  padding: 5px 10px;
  cursor: pointer;
  transition: background-color 0.15s ease, border-color 0.15s ease, color 0.15s ease;
}

.stem-mode-btn:hover {
  background: #3f3f46;
  color: #fff;
}

.stem-mode-btn.is-active {
  background: #14532d;
  color: #86efac;
  border-color: #22c55e;
}

.stem-play-btn {
  background: #1e3a2b;
  color: #4ade80;
  border: 1px solid rgba(74, 222, 128, 0.3);
  border-radius: 3px;
  font-family: inherit;
  font-size: 11px;
  font-weight: 600;
  padding: 6px 12px;
  cursor: pointer;
  transition: background-color 0.15s ease, border-color 0.15s ease, color 0.15s ease;
}

.stem-play-btn:hover {
  background: #274d39;
  border-color: #22c55e;
}

.stem-play-btn.is-playing {
  background: #7f1d1d;
  color: #fca5a5;
  border-color: #ef4444;
}
'''

if '.dossier-stem-mixer-bar' not in css:
    css = css.rstrip() + '\n' + stem_css + '\n'

with open('styles.css', 'w', encoding='utf-8') as f:
    f.write(css)
print("Updated styles.css with stem-mixer styles.")

# 3. Update app.js
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()
js = js.replace('\r\n', '\n')

stem_js = '''
  /* =========================================================
     3G. MULTI-STEM SOLO/MUTE MIXER & AUDIO CONTROLLER
     ========================================================= */
  let activeStemMode = 'mix';
  let stemAudioUrls = { mix: null, vocal: null, accompaniment: null };
  let activeStemAudioElement = null;

  function initStemMixer() {
    const stemBtns = document.querySelectorAll('.stem-mode-btn');
    const playBtn = document.getElementById('btn-play-active-stem');

    stemBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        stemBtns.forEach(b => b.classList.remove('is-active'));
        btn.classList.add('is-active');
        activeStemMode = btn.getAttribute('data-stem') || 'mix';

        if (activeStemAudioElement && !activeStemAudioElement.paused) {
          playActiveStemAudio();
        }

        if (typeof showToast === 'function') {
          showToast('Soloing Stem: ' + (activeStemMode === 'vocal' ? 'Isolated Lead Vocal' : (activeStemMode === 'accompaniment' ? 'Accompaniment Bed' : 'Full Mix')));
        }
      });
    });

    if (playBtn) {
      playBtn.addEventListener('click', function () {
        if (activeStemAudioElement && !activeStemAudioElement.paused) {
          stopActiveStemAudio();
        } else {
          playActiveStemAudio();
        }
      });
    }
  }

  function playActiveStemAudio() {
    stopActiveStemAudio();
    const playBtn = document.getElementById('btn-play-active-stem');
    const url = stemAudioUrls[activeStemMode] || stemAudioUrls.mix;

    if (!url) {
      if (typeof showToast === 'function') showToast('No stem audio available. Try uploading a track or running sample phrase.');
      return;
    }

    activeStemAudioElement = new Audio(url);
    if (playBtn) {
      playBtn.textContent = '⏹ Stop Stem';
      playBtn.classList.add('is-playing');
    }

    activeStemAudioElement.onended = function () {
      stopActiveStemAudio();
    };

    activeStemAudioElement.play().catch(function (e) {
      console.warn('Stem playback error:', e);
      stopActiveStemAudio();
    });
  }

  function stopActiveStemAudio() {
    if (activeStemAudioElement) {
      activeStemAudioElement.pause();
      activeStemAudioElement = null;
    }
    const playBtn = document.getElementById('btn-play-active-stem');
    if (playBtn) {
      playBtn.textContent = '▶ Play Stem';
      playBtn.classList.remove('is-playing');
    }
  }

  function updateStemAudioSources(mixUrl, vocalUrl, accompUrl) {
    stemAudioUrls.mix = mixUrl;
    stemAudioUrls.vocal = vocalUrl;
    stemAudioUrls.accompaniment = accompUrl;
  }
'''

# 1. Add initStemMixer to DOMContentLoaded
dom_target = '    initPakadExplorer();'
if dom_target in js and 'initStemMixer();' not in js:
    js = js.replace(dom_target, dom_target + '\n    initStemMixer();', 1)

# 2. Append stem_js before end of IIFE
iife_end = '})();'
if 'function initStemMixer()' not in js:
    js = js.replace(iife_end, stem_js + '\n' + iife_end, 1)

# 3. In handleAudioFile: update stem audio sources if stems returned
upload_target = '      renderInstantTrackDossier(data);'
if upload_target in js and 'updateStemAudioSources' not in js:
    js = js.replace(
        upload_target,
        upload_target + '\n      if (data && data.evidence && data.evidence.stems) {\n        // Fetch separated stems audio\n        fetchSeparatedStemsAudio(file);\n      }',
        1
    )

    fetch_stems_fn = '''
  async function fetchSeparatedStemsAudio(file) {
    try {
      const formData = new FormData();
      formData.append('file', file);
      const res = await fetch(API_BASE + '/api/separate-stems', {
        method: 'POST',
        body: formData
      });
      if (res.ok) {
        const stems = await res.json();
        updateStemAudioSources(URL.createObjectURL(file), stems.vocal_audio_url, stems.accompaniment_audio_url);
      }
    } catch (e) {
      console.warn('Could not separate stems:', e);
    }
  }
'''
    js = js.replace('function initStemMixer()', fetch_stems_fn + '\n  function initStemMixer()', 1)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated app.js with Stem Mixer audio engine.")

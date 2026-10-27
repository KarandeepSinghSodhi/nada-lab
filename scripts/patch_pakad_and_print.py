# scripts/patch_pakad_and_print.py
import re

# 1. Update server.py
with open('server.py', 'r', encoding='utf-8') as f:
    srv = f.read()
srv = srv.replace('\r\n', '\n')

old_ragainfo = '''class RagaInfo(BaseModel):
    name: str
    tradition: str
    thaat_or_mela: str
    vadi: str
    samvadi: str
    arohana: List[str]
    avarohana: List[str]
    varjya_swaras: List[str]
    allowed_swaras: List[str]'''

new_ragainfo = '''class RagaInfo(BaseModel):
    name: str
    tradition: str
    thaat_or_mela: str
    vadi: str
    samvadi: str
    arohana: List[str]
    avarohana: List[str]
    varjya_swaras: List[str]
    allowed_swaras: List[str]
    pakad_phrases: Optional[List[List[str]]] = None
    mandatory_ornaments: Optional[Dict[str, str]] = None'''

if old_ragainfo in srv:
    srv = srv.replace(old_ragainfo, new_ragainfo, 1)

old_get_ragas = '''        RagaInfo(
            name=r.name,
            tradition=r.tradition,
            thaat_or_mela=r.thaat_or_mela,
            vadi=r.vadi,
            samvadi=r.samvadi,
            arohana=r.arohana,
            avarohana=r.avarohana,
            varjya_swaras=r.varjya_swaras,
            allowed_swaras=r.allowed_swaras,
        )'''

new_get_ragas = '''        RagaInfo(
            name=r.name,
            tradition=r.tradition,
            thaat_or_mela=r.thaat_or_mela,
            vadi=r.vadi,
            samvadi=r.samvadi,
            arohana=r.arohana,
            avarohana=r.avarohana,
            varjya_swaras=r.varjya_swaras,
            allowed_swaras=r.allowed_swaras,
            pakad_phrases=r.pakad_phrases,
            mandatory_ornaments=r.mandatory_ornaments,
        )'''

if old_get_ragas in srv:
    srv = srv.replace(old_get_ragas, new_get_ragas, 1)

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(srv)
print("Updated server.py with pakad_phrases & mandatory_ornaments in RagaInfo.")

# 2. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()
html = html.replace('\r\n', '\n')

pakad_bar_html = '''          <!-- Interactive Canonical Pakad Signature Explorer -->
          <div class="raga-pakad-bar" id="raga-pakad-bar" data-ui="pakad-explorer">
            <div class="pakad-text-group">
              <span class="pakad-label">CANONICAL PAKAD:</span>
              <span class="pakad-notation" id="raga-pakad-notation">N. - R - G | M - R - G - R - S</span>
              <span class="pakad-ornaments-badge" id="raga-ornaments-badge">Mandatory: Meend to P</span>
            </div>
            <div class="pakad-actions">
              <button type="button" id="btn-audition-pakad" class="pakad-action-btn" title="Synthesize and audition this raga's signature Pakad at your Sa">
                ▶ Audition Pakad
              </button>
            </div>
          </div>'''

target_div = '''          <div class="ui-canvas-grid">'''
if target_div in html and 'raga-pakad-bar' not in html:
    html = html.replace(target_div, pakad_bar_html + '\n\n' + target_div, 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html with raga-pakad-bar.")

# 3. Update styles.css
with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()
css = css.replace('\r\n', '\n')

pakad_css = '''
/* Canonical Pakad Signature Explorer Bar */
.raga-pakad-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 10px;
  background: rgba(24, 24, 27, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 4px;
  padding: 8px 14px;
  margin-bottom: 12px;
}

.pakad-text-group {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.pakad-label {
  font-size: 10px;
  font-weight: 700;
  color: #a1a1aa;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.pakad-notation {
  font-size: 13px;
  font-weight: 600;
  color: #f4f4f5;
  font-family: inherit;
  letter-spacing: 0.04em;
}

.pakad-ornaments-badge {
  font-size: 10px;
  color: #38bdf8;
  background: rgba(56, 189, 248, 0.12);
  border: 1px solid rgba(56, 189, 248, 0.25);
  padding: 2px 7px;
  border-radius: 3px;
}

.pakad-action-btn {
  background: #14532d;
  color: #86efac;
  border: 1px solid rgba(134, 239, 172, 0.3);
  border-radius: 3px;
  font-family: inherit;
  font-size: 11px;
  font-weight: 600;
  padding: 5px 12px;
  cursor: pointer;
  transition: background-color 0.15s ease, border-color 0.15s ease, color 0.15s ease;
}

.pakad-action-btn:hover {
  background: #166534;
  border-color: #22c55e;
}

.pakad-action-btn.is-playing {
  background: #7f1d1d;
  color: #fca5a5;
  border-color: #ef4444;
}
'''

if '.raga-pakad-bar' not in css:
    css = css.rstrip() + '\n' + pakad_css + '\n'

with open('styles.css', 'w', encoding='utf-8') as f:
    f.write(css)
print("Updated styles.css with raga-pakad-bar styling.")

# 4. Update app.js
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()
js = js.replace('\r\n', '\n')

pakad_js = '''
  /* =========================================================
     3F. CANONICAL PAKAD EXPLORER & GURU SYNTHESIS
     ========================================================= */
  let ragaCatalogMap = {};
  let pakadAudioElement = null;

  async function loadRagaCatalogMetadata() {
    try {
      const res = await fetch(API_BASE + '/api/ragas');
      if (res.ok) {
        const list = await res.json();
        list.forEach(function (r) {
          ragaCatalogMap[r.name.toLowerCase()] = r;
        });
        updatePakadDisplay();
      }
    } catch (e) {
      console.warn('Could not load raga catalog:', e);
    }
  }

  function updatePakadDisplay() {
    const select = document.getElementById('ui-target-raga-select');
    const notationEl = document.getElementById('raga-pakad-notation');
    const badgeEl = document.getElementById('raga-ornaments-badge');
    if (!select || !notationEl) return;

    const rName = select.value.toLowerCase();
    const rData = ragaCatalogMap[rName];

    if (rData && rData.pakad_phrases && rData.pakad_phrases.length > 0) {
      const phraseStr = rData.pakad_phrases.map(p => p.join(' - ')).join(' | ');
      notationEl.textContent = phraseStr;
      
      if (badgeEl) {
        if (rData.mandatory_ornaments && Object.keys(rData.mandatory_ornaments).length > 0) {
          const firstKey = Object.keys(rData.mandatory_ornaments)[0];
          badgeEl.textContent = 'Mandatory: ' + rData.mandatory_ornaments[firstKey];
          badgeEl.style.display = 'inline-block';
        } else {
          badgeEl.style.display = 'none';
        }
      }
    } else {
      notationEl.textContent = 'Canonical Pakad available in MIR rulebook';
      if (badgeEl) badgeEl.style.display = 'none';
    }
  }

  function initPakadExplorer() {
    const playBtn = document.getElementById('btn-audition-pakad');
    const select = document.getElementById('ui-target-raga-select');

    if (select) {
      select.addEventListener('change', function () {
        updatePakadDisplay();
      });
    }

    if (playBtn) {
      playBtn.addEventListener('click', async function () {
        if (pakadAudioElement && !pakadAudioElement.paused) {
          pakadAudioElement.pause();
          playBtn.textContent = '▶ Audition Pakad';
          playBtn.classList.remove('is-playing');
          return;
        }

        const rName = select ? select.value : 'Yaman';
        const baseSa = userCustomSaHz || 146.83;
        playBtn.textContent = 'Synthesizing...';

        try {
          const res = await fetch(API_BASE + '/api/synthesize-guru', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              sa_hz: baseSa,
              target_raga: rName,
              note_dur_sec: 0.55,
              glide_sec: 0.18
            })
          });

          if (!res.ok) throw new Error('Synthesis failed');
          const data = await res.json();
          if (data && data.data_url) {
            pakadAudioElement = new Audio(data.data_url);
            playBtn.textContent = '⏹ Stop Pakad';
            playBtn.classList.add('is-playing');

            pakadAudioElement.onended = function () {
              playBtn.textContent = '▶ Audition Pakad';
              playBtn.classList.remove('is-playing');
            };

            pakadAudioElement.play();
            if (typeof showToast === 'function') {
              showToast('Playing Canonical ' + rName + ' Pakad at ' + baseSa.toFixed(1) + ' Hz');
            }
          }
        } catch (err) {
          console.error(err);
          playBtn.textContent = '▶ Audition Pakad';
          playBtn.classList.remove('is-playing');
          if (typeof showToast === 'function') showToast('Could not synthesize Pakad');
        }
      });
    }

    loadRagaCatalogMetadata();
  }
'''

# 1. Add initPakadExplorer to DOMContentLoaded
dom_target = '    initRiyazScorecard();'
if dom_target in js and 'initPakadExplorer();' not in js:
    js = js.replace(dom_target, dom_target + '\n    initPakadExplorer();', 1)

# 2. Append pakad implementation before end of IIFE
iife_end = '})();'
if 'function initPakadExplorer()' not in js:
    js = js.replace(iife_end, pakad_js + '\n' + iife_end, 1)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated app.js with Pakad Explorer & Synthesis engine.")

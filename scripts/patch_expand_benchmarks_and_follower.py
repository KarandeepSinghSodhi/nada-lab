import re

# =========================================================================
# 1. PATCH INDEX.HTML
# =========================================================================
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add Bhatkhande Score button next to Print / Export Lead Sheet
old_sheet_controls = """                <button type="button" id="btn-export-sheet-music-pdf" class="sheet-export-btn" title="Export printable Lead Sheet with Lyrics and Notes">
                  Print / Export Lead Sheet
                </button>"""

new_sheet_controls = """                <button type="button" id="btn-export-sheet-music-pdf" class="sheet-export-btn" title="Export printable Lead Sheet with Lyrics and Notes">
                  Print / Export Lead Sheet
                </button>
                <button type="button" id="btn-export-bhatkhande-score" class="sheet-export-btn" title="Export authentic Indian Classical Bhatkhande Sargam notation with Meend arcs & lyrics">
                  Bhatkhande Score (.txt/.html)
                </button>"""

if old_sheet_controls in html:
    html = html.replace(old_sheet_controls, new_sheet_controls)
    print("Added Bhatkhande Score export button to index.html")
else:
    print("WARNING: old_sheet_controls not found in index.html")

# Add live follower feedback bar to sheet music header
old_sheet_title_group = """                <h4 class="sheet-music-heading" id="sheet-music-title">Interactive Sheet Music with Lyrics &amp; Notes</h4>
              </div>"""

new_sheet_title_group = """                <h4 class="sheet-music-heading" id="sheet-music-title">Interactive Sheet Music with Lyrics &amp; Notes</h4>
                <span class="sheet-live-feedback-pill" id="sheet-live-feedback">Live Mic Sing-Along: Standby · Sing into mic to follow notes</span>
              </div>"""

if old_sheet_title_group in html:
    html = html.replace(old_sheet_title_group, new_sheet_title_group)
    print("Added sheet-live-feedback to index.html")
else:
    print("WARNING: old_sheet_title_group not found in index.html")

# Expand the Hindi Song Benchmark Selector with the 4 additional iconic songs
old_song_buttons = """                <button type="button" class="antar-song-btn is-active" data-song-key="yaman_eri_aali">
                  Eri Aali Piya Bina (Yaman)
                </button>
                <button type="button" class="antar-song-btn" data-song-key="darbari_rakhwale">
                  O Duniya Ke Rakhwale (Darbari)
                </button>
                <button type="button" class="antar-song-btn" data-song-key="bhairav_jaago">
                  Jaago Mohan Pyare (Bhairav)
                </button>
                <button type="button" class="antar-song-btn" data-song-key="khamaj_panghat">
                  Mohe Panghat Pe (Khamaj)
                </button>"""

new_song_buttons = """                <button type="button" class="antar-song-btn is-active" data-song-key="yaman_eri_aali">
                  Eri Aali Piya Bina (Yaman)
                </button>
                <button type="button" class="antar-song-btn" data-song-key="darbari_rakhwale">
                  O Duniya Ke Rakhwale (Darbari)
                </button>
                <button type="button" class="antar-song-btn" data-song-key="bhairav_jaago">
                  Jaago Mohan Pyare (Bhairav)
                </button>
                <button type="button" class="antar-song-btn" data-song-key="khamaj_panghat">
                  Mohe Panghat Pe (Khamaj)
                </button>
                <button type="button" class="antar-song-btn" data-song-key="bhoopali_jyoti">
                  Jyoti Kalash Chhalke (Bhoopali)
                </button>
                <button type="button" class="antar-song-btn" data-song-key="ahir_bhairav_poocho">
                  Poocho Na Kaise (Ahir Bhairav)
                </button>
                <button type="button" class="antar-song-btn" data-song-key="hamir_madhuban">
                  Madhuban Mein Radhika (Hamir)
                </button>
                <button type="button" class="antar-song-btn" data-song-key="sohini_kuhu_kuhu">
                  Kuhu Kuhu Bole (Sohini)
                </button>"""

if old_song_buttons in html:
    html = html.replace(old_song_buttons, new_song_buttons)
    print("Expanded Hindi song benchmark buttons in index.html")
else:
    print("WARNING: old_song_buttons not found in index.html")

# Add Bhatkhande Score Modal right before closing </body>
bhatkhande_modal_html = """
  <!-- Conservatory Bhatkhande Sargam Score Modal -->
  <div class="bhatkhande-modal is-hidden" id="bhatkhande-score-modal" role="dialog" aria-modal="true" aria-label="Bhatkhande Sargam Score Viewer">
    <div class="bhatkhande-backdrop" id="bk-modal-backdrop"></div>
    <div class="bhatkhande-modal-card">
      <div class="bhatkhande-modal-header">
        <div class="bk-title-row">
          <span class="bk-header-tag">CONSERVATORY SARGAM NOTATION</span>
          <h3 class="bk-header-title" id="bk-modal-title">Bhatkhande Classical Notation Score</h3>
        </div>
        <div class="bk-modal-actions">
          <button type="button" id="btn-copy-bhatkhande" class="bk-action-btn">📋 Copy Text</button>
          <button type="button" id="btn-print-bhatkhande" class="bk-action-btn bk-print-btn">🖨️ Print Score</button>
          <button type="button" id="btn-close-bhatkhande" class="bk-close-btn" aria-label="Close modal">&times;</button>
        </div>
      </div>
      <div class="bhatkhande-modal-body" id="bk-modal-content">
        <!-- Rendered dynamically -->
      </div>
    </div>
  </div>
"""

if 'id="bhatkhande-score-modal"' not in html:
    html = html.replace('</body>', bhatkhande_modal_html + '\n</body>')
    print("Added bhatkhande-score-modal to index.html")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html successfully.")


# =========================================================================
# 2. PATCH STYLES.CSS
# =========================================================================
with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

styles_to_append = """

/* =========================================================================
   LIVE MIC LEAD SHEET FOLLOWER & BHATKHANDE CONSERVATORY SCORE STYLES
   ========================================================================= */

.sheet-live-feedback-pill {
  font-size: 12px;
  font-weight: 500;
  font-family: 'Clash Grotesk', sans-serif;
  color: #a4bca3;
  background: rgba(143, 166, 142, 0.12);
  padding: 3px 8px;
  border-radius: 4px;
  border: 1px solid rgba(143, 166, 142, 0.22);
  display: inline-block;
  margin-top: 4px;
}

.sheet-event.is-sung-active {
  background: rgba(143, 166, 142, 0.22) !important;
  border-color: #a4bca3 !important;
  transform: translateY(-2px);
  box-shadow: 0 0 12px rgba(164, 188, 163, 0.35);
  transition: transform 0.1s ease, box-shadow 0.1s ease;
}

.sheet-event.is-sung-active.is-pure-tune {
  border-color: #a4bca3 !important;
  background: rgba(164, 188, 163, 0.28) !important;
}

.sheet-event.is-sung-active.is-deviant {
  border-color: #e09f67 !important;
  background: rgba(224, 159, 103, 0.22) !important;
}

.sheet-transition-bridge.is-meend-active {
  border-color: #a4bca3 !important;
  background: rgba(143, 166, 142, 0.32) !important;
  color: #a4bca3 !important;
  box-shadow: 0 0 10px rgba(164, 188, 163, 0.4);
  transform: scale(1.05);
  transition: all 0.15s ease;
}

/* Bhatkhande Score Modal */
.bhatkhande-modal {
  position: fixed;
  inset: 0;
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.bhatkhande-modal.is-hidden {
  display: none;
}

.bhatkhande-backdrop {
  position: absolute;
  inset: 0;
  background: rgba(10, 10, 10, 0.85);
  backdrop-filter: blur(4px);
}

.bhatkhande-modal-card {
  position: relative;
  z-index: 2;
  width: 100%;
  max-width: 960px;
  max-height: 85vh;
  background: #181818;
  border: 1px solid rgba(241, 241, 239, 0.14);
  border-radius: 6px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 48px rgba(0, 0, 0, 0.6);
  overflow: hidden;
}

.bhatkhande-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: #141414;
  border-bottom: 1px solid rgba(241, 241, 239, 0.08);
}

.bk-header-tag {
  font-size: 11px;
  letter-spacing: 0.05em;
  color: #a4bca3;
  font-weight: 600;
  text-transform: uppercase;
}

.bk-header-title {
  font-size: 18px;
  font-weight: 500;
  color: #f1f1ef;
  margin: 2px 0 0 0;
}

.bk-modal-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.bk-action-btn {
  font-size: 13px;
  font-weight: 500;
  font-family: 'Clash Grotesk', sans-serif;
  color: #f1f1ef;
  background: #262626;
  border: 1px solid rgba(241, 241, 239, 0.12);
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.bk-action-btn:hover {
  background: #333333;
  border-color: rgba(241, 241, 239, 0.25);
}

.bk-close-btn {
  background: transparent;
  border: none;
  color: #c8c5ba;
  font-size: 24px;
  cursor: pointer;
  padding: 0 6px;
  line-height: 1;
}

.bk-close-btn:hover {
  color: #f1f1ef;
}

.bhatkhande-modal-body {
  padding: 20px;
  overflow-y: auto;
  flex: 1;
  background: #121212;
}

.bhatkhande-score-card {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.bhatkhande-header-box {
  padding: 12px 16px;
  background: #1b1b1b;
  border: 1px solid rgba(241, 241, 239, 0.08);
  border-radius: 4px;
}

.bhatkhande-title {
  font-size: 18px;
  font-weight: 600;
  color: #f1f1ef;
  margin: 0 0 6px 0;
}

.bhatkhande-meta-row {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.bk-meta-pill {
  font-size: 12px;
  color: #a4bca3;
  background: rgba(143, 166, 142, 0.1);
  padding: 2px 8px;
  border-radius: 3px;
}

.bhatkhande-measures-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 12px;
}

.bhatkhande-measure {
  background: #1a1a1a;
  border: 1px solid rgba(241, 241, 239, 0.08);
  border-radius: 4px;
  padding: 10px 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.bhatkhande-measure-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(241, 241, 239, 0.06);
  padding-bottom: 4px;
}

.bk-measure-badge {
  font-size: 12px;
  font-weight: 600;
  color: #c8c5ba;
}

.bk-chord-badge {
  font-size: 12px;
  font-weight: 600;
  color: #e09f67;
}

.bhatkhande-events-row {
  display: flex;
  justify-content: space-around;
  align-items: center;
  gap: 6px;
}

.bhatkhande-event {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  min-width: 44px;
}

.bk-tala-sub {
  font-size: 11px;
  font-weight: 700;
  color: #e09f67;
  height: 14px;
}

.bk-swara-val {
  font-size: 18px;
  font-weight: 600;
  color: #f1f1ef;
  font-family: 'Noto Sans Devanagari', 'Clash Grotesk', sans-serif;
  letter-spacing: 0.02em;
}

.bk-lyric-val {
  font-size: 13px;
  color: #a4bca3;
  font-weight: 500;
}

.bk-tab-val {
  font-size: 10px;
  color: #8fa68e;
  opacity: 0.75;
}

.bhatkhande-raw-pre {
  background: #0e0e0e;
  border: 1px solid rgba(241, 241, 239, 0.08);
  padding: 12px;
  border-radius: 4px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  line-height: 1.5;
  color: #c8c5ba;
  overflow-x: auto;
  white-space: pre;
}
"""

if "/* Bhatkhande Score Modal */" not in css:
    css += styles_to_append
    with open('styles.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("Added follower and Bhatkhande styles to styles.css")
else:
    print("Follower and Bhatkhande styles already present.")

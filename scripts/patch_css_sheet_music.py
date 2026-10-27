# scripts/patch_css_sheet_music.py

with open('styles.css', 'r', encoding='utf-8') as f:
    text = f.read()

sheet_music_css = '''
/* =========================================================
   INTERACTIVE SHEET MUSIC & LEAD SHEET WORKSTATION
   ========================================================= */
[data-ui="sheet-music-lead-sheet"] {
  background: var(--surface);
  padding: 20px;
  margin-bottom: 24px;
}

.sheet-music-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}

.sheet-music-title-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.sheet-music-badge-row {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.sheet-music-badge {
  display: inline-block;
  font-size: 11px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--accent);
}

.sheet-music-persona-pill {
  display: inline-block;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.04em;
  padding: 3px 8px;
  border-radius: 3px;
  background: rgba(143, 166, 142, 0.12);
  color: #a4bca3;
}

.sheet-music-heading {
  font-size: 22px;
  font-weight: 500;
  color: var(--ink);
  letter-spacing: -0.02em;
}

.sheet-music-controls {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.sheet-notation-toggle {
  display: flex;
  background: #181818;
  padding: 2px;
  border-radius: 3px;
  gap: 2px;
}

.sheet-toggle-btn {
  background: transparent;
  border: none;
  color: var(--muted);
  font-family: inherit;
  font-size: 12px;
  font-weight: 500;
  padding: 6px 10px;
  border-radius: 2px;
  cursor: pointer;
  transition: background 0.15s ease, color 0.15s ease;
}

.sheet-toggle-btn:hover {
  color: var(--ink);
}

.sheet-toggle-btn.is-active {
  background: #282828;
  color: var(--accent);
}

.sheet-export-btn {
  background: #242f25;
  color: #c9e4cb;
  border: none;
  font-family: inherit;
  font-size: 12px;
  font-weight: 500;
  text-transform: uppercase;
  padding: 7px 12px;
  border-radius: 3px;
  cursor: pointer;
  transition: background 0.18s ease;
}

.sheet-export-btn:hover {
  background: #2e3d2f;
}

/* Lyrics Extractor Bar */
.lyrics-extractor-bar {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 16px;
  background: #141414;
  padding: 12px 14px;
  border-radius: 4px;
}

.lyrics-extractor-label {
  font-size: 12px;
  font-weight: 500;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.lyrics-extractor-input-wrap {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.lyrics-input {
  flex: 1;
  min-width: 260px;
  background: #1e1e1e;
  border: none;
  color: var(--ink);
  font-family: inherit;
  font-size: 14px;
  padding: 8px 12px;
  border-radius: 3px;
  outline: none;
}

.lyrics-align-btn {
  background: #2a2a2a;
  color: var(--ink);
  border: none;
  font-family: inherit;
  font-size: 13px;
  font-weight: 500;
  padding: 8px 14px;
  border-radius: 3px;
  cursor: pointer;
  transition: background 0.15s ease;
}

.lyrics-align-btn:hover {
  background: #363636;
}

/* Sheet Music Score Viewport & Measures */
.sheet-music-score-viewport {
  display: flex;
  gap: 14px;
  overflow-x: auto;
  padding-bottom: 12px;
}

.sheet-measure {
  flex: 0 0 auto;
  min-width: 240px;
  background: #121212;
  border-radius: 4px;
  padding: 10px 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.sheet-measure-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 6px;
  border-bottom: 1px solid rgba(241, 241, 239, 0.06);
}

.sheet-measure-num {
  font-size: 11px;
  font-weight: 500;
  font-variant-numeric: tabular-nums;
  color: var(--muted);
}

.sheet-measure-chord {
  font-size: 13px;
  font-weight: 600;
  color: var(--accent);
  letter-spacing: 0.02em;
}

.sheet-measure-events {
  display: flex;
  gap: 8px;
}

.sheet-event {
  flex: 1;
  min-width: 58px;
  background: #1a1a1a;
  border-radius: 3px;
  padding: 6px 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  transition: background 0.15s ease, transform 0.12s ease;
}

.sheet-event:hover {
  background: #252525;
  transform: translateY(-2px);
}

.sheet-event.is-active {
  background: #242f25;
  outline: 2px solid var(--accent);
}

.sheet-rhythm-sym {
  font-size: 16px;
  line-height: 1;
  color: var(--muted);
}

.sheet-lyric-text {
  font-size: 14px;
  font-weight: 500;
  color: var(--ink);
  text-align: center;
  min-height: 20px;
}

.sheet-event.is-active .sheet-lyric-text {
  color: #c9e4cb;
  font-weight: 600;
}

.sheet-note-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.sheet-note-val {
  font-size: 14px;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
  color: var(--accent);
}

.sheet-sargam-val {
  font-size: 12px;
  font-weight: 500;
  color: #b5c4b4;
}

.sheet-fingering-val {
  font-size: 10px;
  font-variant-numeric: tabular-nums;
  color: #a0a09c;
  text-align: center;
  display: none;
}

.sheet-events-fingering .sheet-fingering-val {
  display: block;
}

.sheet-events-sargam .sheet-note-val {
  display: none;
}

.sheet-cents-sub {
  font-size: 10px;
  font-variant-numeric: tabular-nums;
  color: var(--muted);
}
'''

with open('styles.css', 'wb') as f:
    f.write((text + sheet_music_css).encode('utf-8'))

print('SUCCESS: Appended sheet_music_css to styles.css!')

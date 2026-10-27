# scripts/patch_index_sheet_music.py

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = '''          <!-- TRANSCRIBED SARGAM & WESTERN NOTATIONS STREAM -->
          <div class="dossier-notations-section">
            <div class="dossier-section-header">
              <div>
                <span class="dossier-sec-tag">TRANSCRIPTION STREAM</span>
                <h4 class="dossier-sec-heading">Musical Notations &amp; Microtonal Shruti Precision</h4>
              </div>
              <span class="dossier-help-text">Click any note to jump audio &amp; waveform playhead</span>
            </div>

            <div class="notations-scroll-track" id="dossier-notations-list" role="list" aria-label="Transcribed notes sequence">
              <div class="notation-chip-placeholder">Upload audio to view transcribed sargam notations...</div>
            </div>
          </div>'''

replacement = '''          <!-- INTERACTIVE SHEET MUSIC & LEAD SHEET WORKSTATION -->
          <div class="dossier-sheet-music-section" data-ui="sheet-music-lead-sheet">
            <div class="sheet-music-header">
              <div class="sheet-music-title-group">
                <div class="sheet-music-badge-row">
                  <span class="sheet-music-badge">LEAD SHEET &amp; SCORE</span>
                  <span class="sheet-music-persona-pill">Designed for: Pianists, Guitarists, Flautists &amp; Vocalists</span>
                </div>
                <h4 class="sheet-music-heading" id="sheet-music-title">Interactive Sheet Music with Lyrics &amp; Notes</h4>
              </div>
              <div class="sheet-music-controls">
                <div class="sheet-notation-toggle" role="radiogroup" aria-label="Notation format">
                  <button type="button" class="sheet-toggle-btn is-active" data-notation="western" title="Standard Western Pitch (C4, D4, E4...)">Western Pitch</button>
                  <button type="button" class="sheet-toggle-btn" data-notation="sargam" title="Classical Indian Sargam (Sa, Re, Ga, Ma...)">Bhatkhande Sargam</button>
                  <button type="button" class="sheet-toggle-btn" data-notation="fingering" title="Instrument-Specific Fingering &amp; Tabs (Piano keys, Guitar tabs, Flute holes)">Fingering &amp; Tabs</button>
                </div>
                <button type="button" id="btn-export-sheet-music-pdf" class="sheet-export-btn" title="Export printable Lead Sheet with Lyrics and Notes">
                  Print / Export Lead Sheet
                </button>
              </div>
            </div>

            <!-- Custom Lyrics Extractor & Alignment Bar -->
            <div class="lyrics-extractor-bar">
              <label for="lyrics-extractor-input" class="lyrics-extractor-label">Lyrics Alignment Extractor:</label>
              <div class="lyrics-extractor-input-wrap">
                <input type="text" id="lyrics-extractor-input" class="lyrics-input" placeholder="Type or paste lyrics (e.g. E-ri aa-li pi-ya bi-na or Jaa-go mo-han pya-re)..." value="E-ri aa-li pi-ya bi-na sa-khi kal na pa-rat ghar aa-ve">
                <button type="button" id="btn-extract-lyrics-align" class="lyrics-align-btn">Extract &amp; Align Lyrics</button>
              </div>
            </div>

            <!-- The Interactive Sheet Music Lead Sheet Grid (Measures & Events) -->
            <div class="sheet-music-score-viewport" id="sheet-music-viewport" role="region" aria-label="Interactive sheet music score with lyrics and notes to play">
              <!-- Rendered dynamically by app.js -->
            </div>

            <!-- Discrete Musical Notations Stream -->
            <div class="dossier-section-header" style="margin-top: 18px;">
              <div>
                <span class="dossier-sec-tag">DISCRETE SWARA STREAM</span>
                <span class="dossier-help-text">Click any note chip to jump audio playhead &amp; hear physical acoustic tone</span>
              </div>
            </div>
            <div class="notations-scroll-track" id="dossier-notations-list" role="list" aria-label="Transcribed notes sequence">
              <div class="notation-chip-placeholder">Upload audio to view transcribed sargam notations...</div>
            </div>
          </div>'''

text_lf = text.replace('\r\n', '\n')
target_lf = target.replace('\r\n', '\n')
replacement_lf = replacement.replace('\r\n', '\n')

if target_lf in text_lf:
    new_text = text_lf.replace(target_lf, replacement_lf).replace('\n', '\r\n')
    with open('index.html', 'wb') as f:
        f.write(new_text.encode('utf-8'))
    print('SUCCESS: Patched index.html with Interactive Sheet Music & Lead Sheet Workstation!')
else:
    print('ERROR: Target not found in index.html')

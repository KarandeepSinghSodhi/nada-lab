with open('d:/Music/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = '        <!-- THE LIVE THING: Interactive Phrase & Deficit Inspector -->'

uploader_html = """        <!-- UNIVERSAL 1-CLICK AUDIO TRACK UPLOADER -->
        <div class="track-uploader-banner" id="universal-track-uploader" data-ui="uploader-zone">
          <div class="uploader-drop-area" id="uploader-drop-area">
            <div class="uploader-header-row">
              <span class="uploader-badge">ONE-CLICK TRACK INTELLIGENCE</span>
              <span class="uploader-formats-tag">WAV · MP3 · FLAC · M4A · OGG</span>
            </div>
            <div class="uploader-content-grid">
              <div class="uploader-text-col">
                <h3 class="uploader-title">Drop Any Audio Track for Instant Analysis</h3>
                <p class="uploader-subtitle">
                  Upload vocal singing, bansuri, sitar, or instrumental stems. Song Lab instantly decodes <strong>Scale &amp; Key</strong>, <strong>BPM &amp; Tala</strong>, <strong>Full Sargam &amp; Western Notations</strong>, <strong>Audio Waveform &amp; Pitch Contour</strong>, and outputs a <strong>Complete Forensic Report</strong> in one go.
                </p>
              </div>
              <div class="uploader-actions-col">
                <label class="uploader-browse-btn" for="audio-file-input-prominent">
                  <input type="file" id="audio-file-input-prominent" accept=".wav,.mp3,.ogg,.flac,.m4a" class="sr-only">
                  <span class="btn-icon">📁</span>
                  <span id="prominent-upload-label">Upload Audio File</span>
                </label>
                <button type="button" class="uploader-sample-btn" id="uploader-sample-btn" title="Analyze pre-loaded benchmark phrase in 1 click">
                  <span>⚡ Try Sample Phrase</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- INSTANT TRACK INTELLIGENCE & COMPLETE REPORT CARD -->
        <div class="instant-dossier-card is-hidden" id="instant-track-dossier" data-ui="track-dossier">
          <div class="dossier-header">
            <div class="dossier-title-col">
              <span class="dossier-tag">COMPREHENSIVE TRACK DOSSIER</span>
              <h3 class="dossier-track-title" id="dossier-file-name">track_analysis.wav</h3>
            </div>
            <div class="dossier-export-actions">
              <button type="button" class="dossier-action-btn" id="btn-export-dossier-json" title="Download complete structured analysis data as JSON">
                <span>📄 Download JSON</span>
              </button>
              <button type="button" class="dossier-action-btn" id="btn-print-dossier-pdf" title="Print full formatted diagnostic report">
                <span>🖨️ Print Report</span>
              </button>
            </div>
          </div>

          <!-- 4-METRIC SUMMARY STRIP -->
          <div class="dossier-metrics-strip">
            <div class="dossier-metric-cell">
              <span class="dossier-metric-lbl">Identified Scale &amp; Raga</span>
              <span class="dossier-metric-val" id="dossier-raga-name">Raga Yaman</span>
              <span class="dossier-metric-sub" id="dossier-raga-meta">Kalyan Thaat · 98.2% Match</span>
            </div>

            <div class="dossier-metric-cell">
              <span class="dossier-metric-lbl">Tonic Sa Frequency</span>
              <span class="dossier-metric-val" id="dossier-tonic-hz">146.8 Hz</span>
              <span class="dossier-metric-sub" id="dossier-tonic-note">Root Key: D3</span>
            </div>

            <div class="dossier-metric-cell">
              <span class="dossier-metric-lbl">Tempo &amp; Rhythm (BPM)</span>
              <span class="dossier-metric-val" id="dossier-bpm-val">84.0 BPM</span>
              <span class="dossier-metric-sub" id="dossier-tala-name">Madhya Teentaal (16 Matras)</span>
            </div>

            <div class="dossier-metric-cell">
              <span class="dossier-metric-lbl">Intonation Purity</span>
              <span class="dossier-metric-val" id="dossier-accuracy-val">96.8%</span>
              <span class="dossier-metric-sub" id="dossier-notes-count">8 Notes Transcribed</span>
            </div>
          </div>

          <!-- TRANSCRIBED SARGAM & WESTERN NOTATIONS STREAM -->
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
          </div>

          <!-- COMPLETE DIAGNOSTIC CRITIQUE SUMMARY -->
          <div class="dossier-critique-box" id="dossier-critique-box">
            <div class="dossier-critique-header">
              <span class="dossier-badge-pill" id="dossier-critique-badge">[Diagnostic Complete]</span>
              <span class="dossier-critique-tier" id="dossier-critique-tier">TIER 1 · STRUCTURAL EVALUATION</span>
            </div>
            <p class="dossier-critique-text" id="dossier-critique-text">
              Audio uploaded and processed through the 22-shruti forensic pipeline.
            </p>
            <div class="dossier-drill-callout">
              <span class="dossier-drill-lbl">💡 Prescriptive Guru Drill:</span>
              <span class="dossier-drill-text" id="dossier-drill-text">Practice sustaining tonic Sa with tanpura overtones.</span>
            </div>
          </div>
        </div>

"""

if target in text:
    text = text.replace(target, uploader_html + target, 1)
    with open('d:/Music/index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Inserted uploader and dossier HTML successfully')
else:
    print('Target not found in index.html')

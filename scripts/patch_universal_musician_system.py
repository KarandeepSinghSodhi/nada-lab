import re

print("Starting Universal Musician & Instrument-Aware Engineering Patch...")

# -------------------------------------------------------------
# 1. Update index.html
# -------------------------------------------------------------
with open('d:/Music/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# A. Add Persona Badge to Sadhana Guidance Bar
old_sadhana_step = """          <div class="sadhana-step-pill">
            <span class="sadhana-step-num">PRACTICE FOCUS</span>
            <span class="sadhana-step-title" id="sadhana-focus-text">Raga Yaman · Meend Glide (Re to Ga)</span>
          </div>"""

new_sadhana_step = """          <div class="sadhana-step-pill">
            <span class="sadhana-step-num">PRACTICE FOCUS</span>
            <span class="sadhana-step-title" id="sadhana-focus-text">Raga Yaman · Meend Glide (Re to Ga)</span>
            <span class="sadhana-persona-pill" id="sadhana-persona-tag">Designed for: Vocalists, Flautists &amp; Fretless Strings</span>
          </div>"""

if old_sadhana_step in html:
    html = html.replace(old_sadhana_step, new_sadhana_step, 1)
    print("  OK: Added sadhana-persona-tag to sadhana guidance bar")

# B. Update Universal Instrument Engine Header with Dynamic Persona Badge
old_profile_header = """                      <div class="tracker-profile-header">
                        <span class="tracker-profile-title">Universal Instrument Engine</span>
                        <span class="tracker-signal-badge" id="live-signal-meter">Signal: Idle</span>
                      </div>"""

new_profile_header = """                      <div class="tracker-profile-header">
                        <div class="tracker-title-col">
                          <span class="tracker-profile-title">Universal Instrument Engine</span>
                          <span class="tracker-persona-badge" id="tracker-persona-badge">Designed for: Vocalists &amp; Classical Singers</span>
                        </div>
                        <span class="tracker-signal-badge" id="live-signal-meter">Signal: Idle</span>
                      </div>"""

if old_profile_header in html:
    html = html.replace(old_profile_header, new_profile_header, 1)
    print("  OK: Added tracker-persona-badge to instrument profile header")

# C. Update Instrument Pills to include Piano/Keys
old_inst_pills = """                      <div class="tracker-profile-pills">
                        <button type="button" class="tracker-inst-btn is-active" data-inst="voice" title="Vocal Gayaki &amp; Khayal Voice Profile">Voice</button>
                        <button type="button" class="tracker-inst-btn" data-inst="flute" title="Bansuri Flute / Bore Acoustic Resonance Profile">Flute</button>
                        <button type="button" class="tracker-inst-btn" data-inst="guitar" title="Guitar Strumming, Chords &amp; String Tuner Profile">Guitar</button>
                        <button type="button" class="tracker-inst-btn" data-inst="percussion" title="Tabla, Dholak &amp; Percussion Onset &amp; Live BPM Profile">Percussion</button>
                        <button type="button" class="tracker-inst-btn" data-inst="sitar" title="Sitar / Sarod / Plucked String Jawari Profile">Sitar/String</button>
                      </div>"""

new_inst_pills = """                      <div class="tracker-profile-pills">
                        <button type="button" class="tracker-inst-btn is-active" data-inst="voice" title="Vocal Gayaki, Formants &amp; 22-Shruti Pitch Profile">Voice</button>
                        <button type="button" class="tracker-inst-btn" data-inst="piano" title="Piano &amp; Keyboard Struck Wire, Polyphony &amp; Sustain Decay Profile">Piano/Keys</button>
                        <button type="button" class="tracker-inst-btn" data-inst="guitar" title="Guitar Strumming, Chords &amp; String Bend Profile">Guitar/Bass</button>
                        <button type="button" class="tracker-inst-btn" data-inst="flute" title="Bansuri &amp; Wind Instrument Bore Resonance Profile">Wind/Flute</button>
                        <button type="button" class="tracker-inst-btn" data-inst="sitar" title="Violin, Cello, Sitar &amp; Fretless String Profile">Violin/Sitar</button>
                        <button type="button" class="tracker-inst-btn" data-inst="percussion" title="Tabla, Dholak &amp; Percussion Onset Profile">Percussion</button>
                      </div>"""

if old_inst_pills in html:
    html = html.replace(old_inst_pills, new_inst_pills, 1)
    print("  OK: Added Piano/Keys and upgraded instrument pills in index.html")

# D. Update Wave Modes to include Envelope Mode
old_wave_modes = """                      <div class="tracker-wave-modes">
                        <button type="button" class="wave-mode-btn is-active" data-mode="oscilloscope" title="Continuous time-domain acoustic waveform">Wave</button>
                        <button type="button" class="wave-mode-btn" data-mode="spectrum" title="Real-time acoustic harmonic spectrum frequencies">Harmonics</button>
                      </div>"""

new_wave_modes = """                      <div class="tracker-wave-modes">
                        <button type="button" class="wave-mode-btn is-active" data-mode="oscilloscope" title="Pitch-synchronized, period-locked physical wave cycles">Wave</button>
                        <button type="button" class="wave-mode-btn" data-mode="envelope" title="Rolling ADSR attack transient &amp; sustain decay envelope">Envelope</button>
                        <button type="button" class="wave-mode-btn" data-mode="spectrum" title="Real-time acoustic harmonic spectrum frequencies">Harmonics</button>
                      </div>"""

if old_wave_modes in html:
    html = html.replace(old_wave_modes, new_wave_modes, 1)
    print("  OK: Added Envelope mode button to wave modes in index.html")

# E. Add Persona Badges to Track Dossier, Rasa Lab, Tala Studio, MIR Lab
old_dossier_title_col = """            <div class="dossier-title-col">
              <span class="dossier-tag">COMPREHENSIVE TRACK DOSSIER</span>
              <h3 class="dossier-track-title" id="dossier-file-name">track_analysis.wav</h3>
            </div>"""

new_dossier_title_col = """            <div class="dossier-title-col">
              <div class="dossier-tag-row">
                <span class="dossier-tag">COMPREHENSIVE TRACK DOSSIER</span>
                <span class="dossier-persona-pill">Designed for: Producers, Arrangers &amp; Transcribers</span>
              </div>
              <h3 class="dossier-track-title" id="dossier-file-name">track_analysis.wav</h3>
            </div>"""

if old_dossier_title_col in html:
    html = html.replace(old_dossier_title_col, new_dossier_title_col, 1)
    print("  OK: Added persona pill to track dossier")

old_rasa_hdr = """          <div class="rasa-studio-header">
            <span class="rasa-studio-badge">NAVARASA &amp; AESTHETIC MUSICOLOGY</span>
            <h3 class="rasa-studio-title">Phrase-Level Affective Contour &amp; Aesthetic Resonance</h3>"""

new_rasa_hdr = """          <div class="rasa-studio-header">
            <div class="rasa-badge-row">
              <span class="rasa-studio-badge">NAVARASA &amp; AESTHETIC MUSICOLOGY</span>
              <span class="rasa-persona-pill">Designed for: Performers, Composers &amp; Aesthetic Critics</span>
            </div>
            <h3 class="rasa-studio-title">Phrase-Level Affective Contour &amp; Aesthetic Resonance</h3>"""

if old_rasa_hdr in html:
    html = html.replace(old_rasa_hdr, new_rasa_hdr, 1)
    print("  OK: Added persona pill to rasa studio header")

old_tala_hdr = """            <div class="tala-studio-header">
              <span class="tala-studio-badge">RHYTHM &amp; METER ENGINE</span>
              <h3 class="tala-studio-title">Tala, Laya &amp; Tabla Metronome Workspace</h3>"""

new_tala_hdr = """            <div class="tala-studio-header">
              <div class="tala-badge-row">
                <span class="tala-studio-badge">RHYTHM &amp; METER ENGINE</span>
                <span class="tala-persona-pill">Designed for: Vocalists, Soloists &amp; Percussionists</span>
              </div>
              <h3 class="tala-studio-title">Tala, Laya &amp; Tabla Metronome Workspace</h3>"""

if old_tala_hdr in html:
    html = html.replace(old_tala_hdr, new_tala_hdr, 1)
    print("  OK: Added persona pill to tala studio header")

old_research_hdr = """            <div class="rnd-studio-header">
              <span class="rnd-studio-badge">LABORATORY EXPERIMENTS &amp; MIR RESEARCH</span>
              <h3 class="rnd-studio-title">Deterministic MIR Research &amp; Musicology Knowledge Base</h3>"""

new_research_hdr = """            <div class="rnd-studio-header">
              <div class="rnd-badge-row">
                <span class="rnd-studio-badge">LABORATORY EXPERIMENTS &amp; MIR RESEARCH</span>
                <span class="rnd-persona-pill">Designed for: Music Researchers, Acousticians &amp; Audio Engineers</span>
              </div>
              <h3 class="rnd-studio-title">Deterministic MIR Research &amp; Musicology Knowledge Base</h3>"""

if old_research_hdr in html:
    html = html.replace(old_research_hdr, new_research_hdr, 1)
    print("  OK: Added persona pill to research studio header")

with open('d:/Music/index.html', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(html)
print("SUCCESS: index.html fully updated!")

# -------------------------------------------------------------
# 2. Update styles.css with styling for persona pills & envelope
# -------------------------------------------------------------
with open('d:/Music/styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

new_css_rules = """
/* UNIVERSAL MUSICIAN PERSONA PILLS & WAVE ENVELOPE STYLES */
.sadhana-persona-pill,
.tracker-persona-badge,
.dossier-persona-pill,
.rasa-persona-pill,
.tala-persona-pill,
.rnd-persona-pill {
  display: inline-block;
  font-family: 'Clash Grotesk', sans-serif;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.04em;
  padding: 3px 8px;
  border-radius: 3px;
  background: rgba(143, 166, 142, 0.12);
  color: #a4bca3;
  border: 1px solid rgba(143, 166, 142, 0.25);
}

.tracker-title-col {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.dossier-tag-row,
.rasa-badge-row,
.tala-badge-row,
.rnd-badge-row {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}
"""

if '.tracker-persona-badge' not in css:
    css += new_css_rules
    with open('d:/Music/styles.css', 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(css)
    print("SUCCESS: styles.css updated with persona badge styling!")
else:
    print("INFO: styles.css already contains persona badge styling.")

# -------------------------------------------------------------
# 3. Update app.js
# -------------------------------------------------------------
with open('d:/Music/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Add dynamicEnvelopeHistory state variable if not present
if 'let dynamicEnvelopeHistory = [];' not in js:
    js = js.replace('let waveAnimFrameId = null;', 'let waveAnimFrameId = null;\n  let dynamicEnvelopeHistory = [];\n  let lastTrackedLiveHz = 0;')
    print("  OK: Added dynamicEnvelopeHistory & lastTrackedLiveHz state variables")

# Update updateLiveNoteTracker to record lastTrackedLiveHz
old_tracker_record = "function updateLiveNoteTracker(freq, rawCents, saHz, rms) {"
new_tracker_record = """function updateLiveNoteTracker(freq, rawCents, saHz, rms) {
    if (freq > 20 && freq < 4000) lastTrackedLiveHz = freq;"""

if old_tracker_record in js and 'if (freq > 20 && freq < 4000) lastTrackedLiveHz = freq;' not in js:
    js = js.replace(old_tracker_record, new_tracker_record, 1)
    print("  OK: updateLiveNoteTracker records lastTrackedLiveHz")

# Update renderInstrumentSubControls to handle Piano/Keys and set Persona Badges
old_subcontrols = """    if (inst === 'flute') {
      if (subLabel) subLabel.textContent = 'Flute Tonic:';
      if (hintEl) hintEl.textContent = 'Bansuri Flute mode: Pure air-column resonance & Taar overblowing tracking';
      const presets = [
        { label: 'E-Bass', hz: 164.81, note: 'E3' },
        { label: 'G-Base', hz: 196.00, note: 'G3' },
        { label: 'C-Med', hz: 261.63, note: 'C4' },
        { label: 'D3', hz: 146.83, note: 'D3', active: true }
      ];"""

new_subcontrols = """    const personaBadge = document.getElementById('tracker-persona-badge');

    if (inst === 'piano') {
      if (subLabel) subLabel.textContent = 'Piano Tuning:';
      if (hintEl) hintEl.textContent = 'Piano / Keys mode: Struck string acoustic attack, harmonic overtone distribution & sustain pedal decay';
      if (personaBadge) personaBadge.textContent = 'Designed for: Pianists & Keyboardists';
      const presets = [
        { label: 'Concert A440', hz: 146.83, note: 'D3 (A4=440)', active: true },
        { label: 'Verdi A432', hz: 144.16, note: 'D3 (A4=432)' },
        { label: 'Equal Temp', hz: 146.83, note: 'D3 ET' },
        { label: 'Just Intonation', hz: 146.83, note: 'D3 JI' }
      ];
      presets.forEach(function (p) {
        const b = document.createElement('button');
        b.type = 'button';
        b.className = 'sub-preset-btn' + (p.active ? ' is-active' : '');
        b.textContent = p.label;
        b.addEventListener('click', function () {
          subButtonsContainer.querySelectorAll('.sub-preset-btn').forEach(function (x) { x.classList.remove('is-active'); });
          b.classList.add('is-active');
          applyInstrumentTonic(p.hz, p.note);
        });
        subButtonsContainer.appendChild(b);
      });
    } else if (inst === 'flute') {
      if (subLabel) subLabel.textContent = 'Flute Tonic:';
      if (hintEl) hintEl.textContent = 'Bansuri Flute mode: Pure air-column resonance & Taar overblowing tracking';
      if (personaBadge) personaBadge.textContent = 'Designed for: Flautists & Wind Players';
      const presets = [
        { label: 'E-Bass', hz: 164.81, note: 'E3' },
        { label: 'G-Base', hz: 196.00, note: 'G3' },
        { label: 'C-Med', hz: 261.63, note: 'C4' },
        { label: 'D3', hz: 146.83, note: 'D3', active: true }
      ];"""

if old_subcontrols in js:
    js = js.replace(old_subcontrols, new_subcontrols, 1)
    print("  OK: Added Piano/Keys sub-controls and persona badge logic to renderInstrumentSubControls")

# Update guitar, sitar, percussion, voice persona badges in renderInstrumentSubControls
js = js.replace(
    "if (hintEl) hintEl.textContent = 'Guitar mode: Strumming chord detection & 6-string tuner active';",
    "if (hintEl) hintEl.textContent = 'Guitar mode: Strumming chord detection & 6-string tuner active';\n      if (personaBadge) personaBadge.textContent = 'Designed for: Guitarists & Bassists';"
)
js = js.replace(
    "if (hintEl) hintEl.textContent = 'Percussion mode: Transient strike onset, Bol recognition & Live BPM locked';",
    "if (hintEl) hintEl.textContent = 'Percussion mode: Transient strike onset, Bol recognition & Live BPM locked';\n      if (personaBadge) personaBadge.textContent = 'Designed for: Percussionists & Rhythmists';"
)
js = js.replace(
    "if (hintEl) hintEl.textContent = 'Sitar / String mode: Sympathetic jawari resonance & multi-fret meend bend tracking';",
    "if (hintEl) hintEl.textContent = 'Sitar / String mode: Sympathetic jawari resonance & multi-fret meend bend tracking';\n      if (personaBadge) personaBadge.textContent = 'Designed for: Bowed Strings, Sitar & Sarod';"
)
js = js.replace(
    "if (hintEl) hintEl.textContent = 'Voice mode: Standard Gayaki formant detection & 22-shruti microtonal tuning';",
    "if (hintEl) hintEl.textContent = 'Voice mode: Standard Gayaki formant detection & 22-shruti microtonal tuning';\n      if (personaBadge) personaBadge.textContent = 'Designed for: Vocalists & Classical Singers';"
)

# Replace drawWave implementation with the pitch-locked, envelope-capable engine
old_drawwave_marker = "    function drawWave() {"
new_drawwave_impl = """    function drawWave() {
      waveAnimFrameId = requestAnimationFrame(drawWave);
      if (!waveAnalyserNode) return;

      waveAnalyserNode.getFloatTimeDomainData(waveDataArray);

      const w = canvas.width;
      const h = canvas.height;
      const centerY = h / 2;

      ctx.clearRect(0, 0, w, h);
      ctx.fillStyle = '#0c0c0c';
      ctx.fillRect(0, 0, w, h);

      // Draw subtle grid lines
      ctx.strokeStyle = 'rgba(241, 241, 239, 0.04)';
      ctx.lineWidth = 1;
      for (let x = 0; x < w; x += 80) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, h);
        ctx.stroke();
      }

      // Draw center baseline
      ctx.strokeStyle = 'rgba(143, 166, 142, 0.18)';
      ctx.beginPath();
      ctx.moveTo(0, centerY);
      ctx.lineTo(w, centerY);
      ctx.stroke();

      // Check sound energy (RMS)
      let sumSq = 0;
      for (let i = 0; i < waveDataArray.length; i++) {
        sumSq += waveDataArray[i] * waveDataArray[i];
      }
      const rms = Math.sqrt(sumSq / waveDataArray.length);

      // Record to rolling envelope history
      dynamicEnvelopeHistory.push(rms);
      if (dynamicEnvelopeHistory.length > 140) dynamicEnvelopeHistory.shift();

      // Instrument Timbre Color Scheme
      let instColor = '#8fa68e';
      let instGradColor = 'rgba(143, 166, 142, 0.25)';
      if (activeInstrumentProfile === 'piano') {
        instColor = '#8c92e8'; // Royal Indigo (Struck string wire)
        instGradColor = 'rgba(140, 146, 232, 0.28)';
      } else if (activeInstrumentProfile === 'flute') {
        instColor = '#a4bca3'; // Bamboo Jade (Bore resonance)
        instGradColor = 'rgba(164, 188, 163, 0.25)';
      } else if (activeInstrumentProfile === 'guitar') {
        instColor = '#6ea89e'; // Teal Bronze
        instGradColor = 'rgba(110, 168, 158, 0.26)';
      } else if (activeInstrumentProfile === 'sitar') {
        instColor = '#d2aa72'; // Classical Bronze (Jawari shimmer)
        instGradColor = 'rgba(210, 170, 114, 0.28)';
      } else if (activeInstrumentProfile === 'percussion') {
        instColor = '#c07a56'; // Terracotta Amber (Tabla shell)
        instGradColor = 'rgba(192, 122, 86, 0.28)';
      }

      if (rms < 0.005) {
        // Serene ambient idling breath pulse
        const now = performance.now() / 1000;
        ctx.strokeStyle = instColor;
        ctx.lineWidth = 1.4;
        ctx.beginPath();
        for (let x = 0; x < w; x += 4) {
          const u = x / w;
          const y = centerY + Math.sin(u * 12 + now * 3) * 2.2;
          if (x === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.stroke();
        if (statsEl) statsEl.textContent = 'Standby · Dynamic Period Lock · 60 FPS';
        return;
      }

      // MODE 1: ENVELOPE MODE (ADSR Attack Transient & Sustain Decay)
      if (activeWaveMode === 'envelope') {
        const envLen = dynamicEnvelopeHistory.length;
        const maxEnvVal = 0.35; // Maximum headroom reference

        // Fill under envelope
        const envGrad = ctx.createLinearGradient(0, 0, 0, h);
        envGrad.addColorStop(0, instGradColor);
        envGrad.addColorStop(1, 'rgba(0, 0, 0, 0.02)');

        ctx.beginPath();
        ctx.moveTo(0, h);
        for (let i = 0; i < envLen; i++) {
          const x = (i / (envLen - 1)) * w;
          const normE = Math.min(1.0, dynamicEnvelopeHistory[i] / maxEnvVal);
          const y = h - normE * (h * 0.88);
          ctx.lineTo(x, y);
        }
        ctx.lineTo(w, h);
        ctx.closePath();
        ctx.fillStyle = envGrad;
        ctx.fill();

        // Stroke envelope outline
        ctx.strokeStyle = instColor;
        ctx.lineWidth = 2.4;
        ctx.beginPath();
        for (let i = 0; i < envLen; i++) {
          const x = (i / (envLen - 1)) * w;
          const normE = Math.min(1.0, dynamicEnvelopeHistory[i] / maxEnvVal);
          const y = h - normE * (h * 0.88);
          if (i === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.stroke();

        if (statsEl) {
          const envTitle = activeInstrumentProfile === 'piano' ? 'Piano ADSR Sustain Decay' :
            (activeInstrumentProfile === 'flute' ? 'Bansuri Breath Pressure Stability' :
            (activeInstrumentProfile === 'guitar' ? 'Guitar Pluck Attack & Ring' : 'Acoustic Sound Envelope'));
          statsEl.textContent = envTitle + ' · ' + (rms * 100).toFixed(0) + '% RMS · 60 FPS';
        }
        return;
      }

      // MODE 2: SPECTRUM HARMONICS MODE
      if (activeWaveMode === 'spectrum') {
        waveAnalyserNode.getByteFrequencyData(waveFreqDataArray);
        const barCount = 48;
        const barWidth = Math.max(3, (w / barCount) - 2);

        for (let i = 0; i < barCount; i++) {
          const val = waveFreqDataArray[i * 4];
          const barHeight = (val / 255) * (h * 0.85);
          const x = i * (barWidth + 2);
          const y = h - barHeight;

          const barGrad = ctx.createLinearGradient(0, y, 0, h);
          barGrad.addColorStop(0, instColor);
          barGrad.addColorStop(1, 'rgba(143, 166, 142, 0.08)');

          ctx.fillStyle = barGrad;
          ctx.fillRect(x, y, barWidth, barHeight);
        }

        if (statsEl) {
          const specLabel = activeInstrumentProfile === 'piano' ? 'Piano Polyphonic Harmonics' :
            (activeInstrumentProfile === 'sitar' ? 'Sitar Sympathetic Jawari Peaks' : 'Acoustic Spectrum Partials');
          statsEl.textContent = specLabel + ' · 60 FPS';
        }
        return;
      }

      // MODE 3: TIMBRE-ADAPTIVE PITCH-SYNCHRONIZED OSCILLOSCOPE
      // Calculate pitch period for jitter-free period locking
      const currentPitchHz = lastTrackedLiveHz > 30 ? lastTrackedLiveHz : (userCustomSaHz || 146.83);
      const periodSamples = Math.max(20, Math.min(600, Math.round(44100 / currentPitchHz)));
      
      // Window size: Exactly 2.5 full acoustic wave cycles
      const cycleWindow = Math.max(96, Math.min(1024, Math.round(periodSamples * 2.5)));

      // Slope-locked trigger search: find upward zero-crossing with maximum derivative
      let triggerIdx = 0;
      let maxSlope = 0;
      for (let i = 1; i < Math.min(waveDataArray.length - cycleWindow, 350); i++) {
        if (waveDataArray[i - 1] < 0 && waveDataArray[i] >= 0) {
          const slope = waveDataArray[i] - waveDataArray[i - 1];
          if (slope > maxSlope) {
            maxSlope = slope;
            triggerIdx = i;
          }
        }
      }

      const drawLen = Math.min(waveDataArray.length - triggerIdx, cycleWindow);

      // Translucent glow gradient
      const grad = ctx.createLinearGradient(0, 0, 0, h);
      grad.addColorStop(0, instGradColor);
      grad.addColorStop(1, 'rgba(0, 0, 0, 0.02)');

      // Draw wave envelope fill
      ctx.beginPath();
      ctx.moveTo(0, centerY);
      for (let i = 0; i < drawLen; i++) {
        const x = (i / (drawLen - 1)) * w;
        let v = waveDataArray[triggerIdx + i];
        // For flute: subtle smoothing highlights pure bore resonance
        if (activeInstrumentProfile === 'flute' && i > 0 && i < drawLen - 1) {
          v = (waveDataArray[triggerIdx + i - 1] + v * 2 + waveDataArray[triggerIdx + i + 1]) / 4;
        }
        const y = centerY - v * (h * 0.44);
        ctx.lineTo(x, y);
      }
      ctx.lineTo(w, centerY);
      ctx.closePath();
      ctx.fillStyle = grad;
      ctx.fill();

      // Draw primary glowing oscilloscope trace line
      ctx.strokeStyle = instColor;
      ctx.lineWidth = 2.4;
      ctx.beginPath();
      for (let i = 0; i < drawLen; i++) {
        const x = (i / (drawLen - 1)) * w;
        let v = waveDataArray[triggerIdx + i];
        if (activeInstrumentProfile === 'flute' && i > 0 && i < drawLen - 1) {
          v = (waveDataArray[triggerIdx + i - 1] + v * 2 + waveDataArray[triggerIdx + i + 1]) / 4;
        }
        const y = centerY - v * (h * 0.44);
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();

      if (statsEl) {
        const timbreLabel = activeInstrumentProfile === 'piano' ? 'Piano Struck Wire (2.5 Cycles Locked)' :
          (activeInstrumentProfile === 'flute' ? 'Bansuri Air Column (2.5 Cycles Locked)' :
          (activeInstrumentProfile === 'guitar' ? 'Guitar Plucked String (2.5 Cycles Locked)' :
          (activeInstrumentProfile === 'sitar' ? 'Sitar Jawari Resonance (2.5 Cycles Locked)' : 'Gayaki Formant Waveform (2.5 Cycles Locked)')));
        statsEl.textContent = timbreLabel + ' · ' + (rms * 100).toFixed(0) + '% RMS · 60 FPS';
      }
    }"""

# Find start and end of existing drawWave function
idx_dw = js.find('    function drawWave() {')
end_dw = js.find('    drawWave();\n  }', idx_dw)

if idx_dw != -1 and end_dw != -1:
    js = js[:idx_dw] + new_drawwave_impl + "\n\n  " + js[end_dw:]
    print("  OK: Replaced drawWave with Timbre-Adaptive, Period-Locked, ADSR Envelope engine")
else:
    print("WARNING: Could not find drawWave block in app.js!")

with open('d:/Music/app.js', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(js)
print("SUCCESS: app.js fully updated with Universal Musician Engine!")

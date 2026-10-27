# -*- coding: utf-8 -*-
"""
Script to integrate Universal Instrument Mapping (Guitar Strumming, Percussion Onsets & Live BPM, Sitar, Flute, Voice) into app.js
"""

with open("app.js", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add state variables for guitar and percussion tracking
old_wave_vars = """  let activeInstrumentProfile = 'voice'; // 'voice', 'flute', 'string'
  let activeWaveMode = 'oscilloscope'; // 'oscilloscope' or 'spectrum'
  let waveAnalyserNode = null;
  let waveAnimFrameId = null;
  const waveDataArray = new Float32Array(1024);
  const waveFreqDataArray = new Uint8Array(512);
  let currentHoldStartTime = 0;
  let currentHoldNote = '';
  let longestSessionHoldSec = 0;
  let lastTrackedShrutiRatioCents = 0;"""

new_wave_vars = """  let activeInstrumentProfile = 'voice'; // 'voice', 'flute', 'guitar', 'percussion', 'sitar'
  let activeWaveMode = 'oscilloscope'; // 'oscilloscope' or 'spectrum'
  let waveAnalyserNode = null;
  let waveAnimFrameId = null;
  const waveDataArray = new Float32Array(1024);
  const waveFreqDataArray = new Uint8Array(512);
  let currentHoldStartTime = 0;
  let currentHoldNote = '';
  let longestSessionHoldSec = 0;
  let lastTrackedShrutiRatioCents = 0;

  // Universal Instrument Tracking State
  let lastPercussionHitTime = 0;
  let percussionHitCount = 0;
  let percussionLiveBpm = 0;
  let lastPercussionRms = 0;
  let currentGuitarTuningMode = 'standard';
  let currentPercussionKit = 'tabla';"""

if old_wave_vars in content:
    content = content.replace(old_wave_vars, new_wave_vars, 1)
    print("Universal state variables added.")
else:
    print("Warning: old_wave_vars not found!")

# 2. Add guitar chord and string database
guitar_db_code = """  // Guitar Standard Tuning & Common Chords Registry
  const GUITAR_STRINGS = [
    { name: '6th String (E2)', note: 'E2', hz: 82.41, num: 6 },
    { name: '5th String (A2)', note: 'A2', hz: 110.00, num: 5 },
    { name: '4th String (D3)', note: 'D3', hz: 146.83, num: 4 },
    { name: '3rd String (G3)', note: 'G3', hz: 196.00, num: 3 },
    { name: '2nd String (B3)', note: 'B3', hz: 246.94, num: 2 },
    { name: '1st String (E4)', note: 'E4', hz: 329.63, num: 1 }
  ];

  const GUITAR_CHORDS = [
    { name: 'Em', sargam: 'E Minor', rootHz: 82.41, notes: 'E-G-B', type: 'Minor Triad' },
    { name: 'G Maj', sargam: 'G Major', rootHz: 98.00, notes: 'G-B-D', type: 'Major Triad' },
    { name: 'C Maj', sargam: 'C Major', rootHz: 130.81, notes: 'C-E-G', type: 'Major Triad' },
    { name: 'Am', sargam: 'A Minor', rootHz: 110.00, notes: 'A-C-E', type: 'Minor Triad' },
    { name: 'D Maj', sargam: 'D Major', rootHz: 146.83, notes: 'D-F#-A', type: 'Major Triad' },
    { name: 'Dm', sargam: 'D Minor', rootHz: 146.83, notes: 'D-F-A', type: 'Minor Triad' },
    { name: 'E Maj', sargam: 'E Major', rootHz: 82.41, notes: 'E-G#-B', type: 'Major Triad' },
    { name: 'A Maj', sargam: 'A Major', rootHz: 110.00, notes: 'A-C#-E', type: 'Major Triad' }
  ];

  const PERCUSSION_BOLS = [
    { name: 'Dha', script: 'धा', desc: 'Combined Bass + Treble Rim Stroke' },
    { name: 'Ge', script: 'घे', desc: 'Bayan Resonant Bass Modulation' },
    { name: 'Na', script: 'ना', desc: 'Dayan High Kinar Rim Ring' },
    { name: 'Tin', script: 'तिं', desc: 'Dayan Sur Center Resonance' },
    { name: 'Ta', script: 'ता', desc: 'Open Dayan Sharp Stroke' },
    { name: 'Kat', script: 'क', desc: 'Flat Bayan Damped Slap' }
  ];
"""

# Insert guitar_db_code right above SHRUTI_MAP_22
shruti_anchor = "  const SHRUTI_MAP_22 = ["
if shruti_anchor in content:
    content = content.replace(shruti_anchor, guitar_db_code + "\n" + shruti_anchor, 1)
    print("Guitar and Percussion database inserted.")
else:
    print("Warning: shruti_anchor not found!")

# 3. Update updateLiveNoteTracker to support Guitar, Percussion, and Sitar profiles
old_note_tracker_func = """  function updateLiveNoteTracker(freq, rawCents, saHz, rms) {"""

new_note_tracker_logic = """  function updateLiveNoteTracker(freq, rawCents, saHz, rms) {
    const swaraEl = document.getElementById('live-swara-val');
    const sargamEl = document.getElementById('live-sargam-script');
    const westernEl = document.getElementById('live-western-val');
    const freqEl = document.getElementById('live-freq-val');
    const saptakEl = document.getElementById('live-saptak-val');
    const centsBadge = document.getElementById('live-cents-badge');
    const gaugeNeedle = document.getElementById('live-gauge-needle');
    const shrutiRatioEl = document.getElementById('live-shruti-ratio');
    const tuningStatusEl = document.getElementById('live-tuning-status');
    const signalMeterEl = document.getElementById('live-signal-meter');

    if (!swaraEl) return;

    // A. PERCUSSION / TABLA PROFILE ENGINE
    if (activeInstrumentProfile === 'percussion') {
      const now = performance.now();
      const currentRms = rms || 0;
      const rmsDelta = currentRms - lastPercussionRms;
      lastPercussionRms = currentRms;

      // Onset detection (sharp acoustic attack)
      if (currentRms > 0.018 && rmsDelta > 0.012 && (now - lastPercussionHitTime) > 120) {
        percussionHitCount++;
        const deltaMs = now - lastPercussionHitTime;
        lastPercussionHitTime = now;

        // Calculate live BPM
        if (deltaMs >= 220 && deltaMs <= 1800) {
          const instantBpm = 60000 / deltaMs;
          if (percussionLiveBpm === 0) percussionLiveBpm = instantBpm;
          else percussionLiveBpm = percussionLiveBpm * 0.65 + instantBpm * 0.35;
        }

        // Spectral centroid classification of the hit
        let centroidBin = 12;
        if (waveAnalyserNode) {
          waveAnalyserNode.getByteFrequencyData(waveFreqDataArray);
          let sumNum = 0, sumDen = 0;
          for (let i = 0; i < 48; i++) {
            sumNum += i * waveFreqDataArray[i];
            sumDen += waveFreqDataArray[i];
          }
          if (sumDen > 0) centroidBin = sumNum / sumDen;
        }

        let detectedBol = PERCUSSION_BOLS[0]; // Dha
        if (centroidBin < 7) detectedBol = PERCUSSION_BOLS[1]; // Ge
        else if (centroidBin > 18) detectedBol = PERCUSSION_BOLS[2]; // Na
        else if (centroidBin > 12) detectedBol = PERCUSSION_BOLS[3]; // Tin

        swaraEl.textContent = detectedBol.name;
        sargamEl.textContent = detectedBol.script;
        westernEl.textContent = percussionLiveBpm > 0 ? (Math.round(percussionLiveBpm) + ' BPM') : 'Transient Hit';
        freqEl.textContent = 'Attack +' + Math.round(rmsDelta * 200) + ' dB';

        const layaName = percussionLiveBpm < 80 ? 'Vilambit Laya' : (percussionLiveBpm > 130 ? 'Drut Laya' : 'Madhya Laya');
        saptakEl.textContent = 'Hits: ' + percussionHitCount + ' · ' + layaName;

        if (gaugeNeedle) {
          const velPct = Math.min(95, Math.max(5, currentRms * 350));
          gaugeNeedle.style.left = velPct.toFixed(1) + '%';
        }

        if (centsBadge) {
          centsBadge.textContent = 'Strike: ' + detectedBol.name;
          centsBadge.className = 'tracker-cents-badge';
        }

        if (shrutiRatioEl) shrutiRatioEl.textContent = detectedBol.desc;
        if (tuningStatusEl) {
          tuningStatusEl.textContent = 'Rhythmic Onset Locked';
          tuningStatusEl.style.color = '#a4bca3';
        }
        if (signalMeterEl) {
          signalMeterEl.textContent = 'Percussion Hit (' + Math.round(currentRms * 100) + '%)';
        }

        // Pulse the active Tala matra if Tala metronome is active
        const matraBtns = document.querySelectorAll('.tala-matra-cell');
        if (matraBtns.length > 0) {
          const hitIdx = (percussionHitCount - 1) % matraBtns.length;
          matraBtns.forEach(function (c, idx) {
            if (idx === hitIdx) c.classList.add('is-active-beat');
            else c.classList.remove('is-active-beat');
          });
        }
        return;
      }

      if (currentRms <= 0.006 && (now - lastPercussionHitTime) > 1200) {
        if (signalMeterEl) signalMeterEl.textContent = 'Signal: Idle';
      }
      return;
    }

    // B. GUITAR / STRUMMING PROFILE ENGINE
    if (activeInstrumentProfile === 'guitar') {
      if (!freq || freq <= 65 || freq >= 1200 || rawCents === null || isNaN(rawCents)) {
        if (signalMeterEl) signalMeterEl.textContent = 'Signal: Idle';
        return;
      }

      // Check for closest guitar string
      let closestString = GUITAR_STRINGS[0];
      let minStringDiff = 9999;
      GUITAR_STRINGS.forEach(function (gs) {
        const d = Math.abs(freq - gs.hz);
        if (d < minStringDiff) {
          minStringDiff = d;
          closestString = gs;
        }
      });

      const stringCentsDiff = 1200 * Math.log2(freq / closestString.hz);

      // Check if strumming chord (energy flux across spectrum)
      let isChordStrum = false;
      let matchedChord = null;
      if (waveAnalyserNode) {
        waveAnalyserNode.getByteFrequencyData(waveFreqDataArray);
        let activeBands = 0;
        for (let i = 2; i < 36; i += 3) {
          if (waveFreqDataArray[i] > 65) activeBands++;
        }
        if (activeBands >= 4 && (rms || 0) > 0.035) {
          isChordStrum = true;
          // Match closest chord root
          let bestChordDiff = 9999;
          GUITAR_CHORDS.forEach(function (ch) {
            const cd = Math.abs(freq - ch.rootHz);
            if (cd < bestChordDiff) {
              bestChordDiff = cd;
              matchedChord = ch;
            }
          });
        }
      }

      if (isChordStrum && matchedChord) {
        swaraEl.textContent = matchedChord.name;
        sargamEl.textContent = 'Chord';
        westernEl.textContent = matchedChord.notes;
        freqEl.textContent = freq.toFixed(1) + ' Hz';
        saptakEl.textContent = 'Acoustic Guitar Strum (' + matchedChord.type + ')';

        if (gaugeNeedle) gaugeNeedle.style.left = '50%';
        if (centsBadge) {
          centsBadge.textContent = 'Strum: ' + matchedChord.name;
          centsBadge.className = 'tracker-cents-badge';
        }
        if (shrutiRatioEl) shrutiRatioEl.textContent = 'Notes: ' + matchedChord.notes;
        if (tuningStatusEl) {
          tuningStatusEl.textContent = 'Harmonic Chord Locked';
          tuningStatusEl.style.color = '#a4bca3';
        }
      } else {
        // Individual String Plucked
        swaraEl.textContent = closestString.note;
        sargamEl.textContent = 'String ' + closestString.num;
        westernEl.textContent = closestString.name;
        freqEl.textContent = freq.toFixed(1) + ' Hz';
        saptakEl.textContent = 'Acoustic Guitar String ' + closestString.num + ' (Target ' + closestString.hz.toFixed(1) + ' Hz)';

        const clampedDelta = Math.max(-50, Math.min(50, stringCentsDiff));
        const needlePct = 50 + (clampedDelta / 50) * 45;
        if (gaugeNeedle) gaugeNeedle.style.left = needlePct.toFixed(1) + '%';

        const sign = stringCentsDiff >= 0 ? '+' : '';
        const absD = Math.abs(stringCentsDiff);

        if (centsBadge) {
          if (absD <= 5.0) {
            centsBadge.textContent = sign + stringCentsDiff.toFixed(1) + 'c · In Tune';
            centsBadge.className = 'tracker-cents-badge';
          } else if (stringCentsDiff > 5.0) {
            centsBadge.textContent = sign + stringCentsDiff.toFixed(1) + 'c · Sharp';
            centsBadge.className = 'tracker-cents-badge is-sharp';
          } else {
            centsBadge.textContent = sign + stringCentsDiff.toFixed(1) + 'c · Flat';
            centsBadge.className = 'tracker-cents-badge is-flat';
          }
        }

        if (shrutiRatioEl) shrutiRatioEl.textContent = 'Standard String Pitch: ' + closestString.hz.toFixed(1) + ' Hz';
        if (tuningStatusEl) {
          tuningStatusEl.textContent = absD <= 5.0 ? 'String Perfectly Tuned' : 'Tune Peg ' + (stringCentsDiff > 0 ? 'Down' : 'Up');
          tuningStatusEl.style.color = absD <= 5.0 ? '#a4bca3' : '#e09f67';
        }
      }

      if (signalMeterEl) {
        signalMeterEl.textContent = 'Signal: Guitar (' + Math.round((rms || 0) * 100) + '%)';
      }
      return;
    }

    // C. VOICE, FLUTE & SITAR/STRING PROFILE ENGINE"""

if old_note_tracker_func in content:
    content = content.replace(old_note_tracker_func, new_note_tracker_logic, 1)
    print("updateLiveNoteTracker updated with Guitar and Percussion branches.")
else:
    print("Warning: old_note_tracker_func not found!")

# 4. Update initInstrumentProfiles to dynamically re-render sub-controls for all 5 instruments
old_init_inst_code = """  function initInstrumentProfiles() {
    const btns = document.querySelectorAll('.tracker-inst-btn');
    const hintEl = document.getElementById('tracker-profile-hint');
    const hearBtn = document.getElementById('btn-hear-current-note');

    // 1. Hear Pure Shruti Reference button
    if (hearBtn) {
      hearBtn.addEventListener('click', playCurrentNoteReference);
    }

    // 2. Flute Quick Scale Keys
    const fluteKeyBtns = document.querySelectorAll('.flute-key-btn');
    fluteKeyBtns.forEach(function (fBtn) {
      fBtn.addEventListener('click', function () {
        fluteKeyBtns.forEach(function (b) { b.classList.remove('is-active'); });
        fBtn.classList.add('is-active');

        const hz = parseFloat(fBtn.getAttribute('data-hz') || '146.83');
        const note = fBtn.getAttribute('data-note') || 'D3';
        userCustomSaHz = hz;

        Object.keys(PHRASE_LIBRARY).forEach(function (k) {
          PHRASE_LIBRARY[k].saHz = hz;
        });

        updateDroneButtonLabel();
        if (isDronePlaying) updateActiveDroneFrequencies();

        const telTarget = document.getElementById('ui-tel-target');
        if (telTarget) telTarget.textContent = 'Sa = ' + hz.toFixed(1) + ' Hz';

        const calibOpenBtn = document.getElementById('calibrate-sa-btn');
        if (calibOpenBtn) {
          calibOpenBtn.textContent = 'Sa: ' + hz.toFixed(1) + ' Hz (' + note + ')';
          calibOpenBtn.classList.add('is-calibrated');
        }

        if (hintEl) {
          hintEl.textContent = 'Flute Tonic locked to ' + note + ' (' + hz.toFixed(1) + ' Hz) · Tanpura drone & lattice re-tuned';
        }

        if (isLiveMicActive) {
          renderLivePitchCanvas();
        } else {
          renderPhraseInspector();
        }
      });
    });

    // 3. Wave Mode Toggle (Wave vs Harmonics)
    const waveModeBtns = document.querySelectorAll('.wave-mode-btn');
    waveModeBtns.forEach(function (wBtn) {
      wBtn.addEventListener('click', function () {
        waveModeBtns.forEach(function (b) { b.classList.remove('is-active'); });
        wBtn.classList.add('is-active');
        activeWaveMode = wBtn.getAttribute('data-mode') || 'oscilloscope';
      });
    });"""

new_init_inst_code = """  // Dynamic Contextual Sub-Controls Generator for all 5 Instruments
  function renderInstrumentSubControls(inst) {
    const subLabel = document.getElementById('tracker-sub-label');
    const subButtonsContainer = document.getElementById('tracker-sub-buttons');
    const hintEl = document.getElementById('tracker-profile-hint');
    if (!subButtonsContainer) return;

    subButtonsContainer.innerHTML = '';

    if (inst === 'flute') {
      if (subLabel) subLabel.textContent = 'Flute Tonic:';
      if (hintEl) hintEl.textContent = 'Bansuri Flute mode: Pure air-column resonance & Taar overblowing tracking';
      const presets = [
        { label: 'E-Bass', hz: 164.81, note: 'E3' },
        { label: 'G-Base', hz: 196.00, note: 'G3' },
        { label: 'C-Med', hz: 261.63, note: 'C4' },
        { label: 'D3', hz: 146.83, note: 'D3', active: true }
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
    } else if (inst === 'guitar') {
      if (subLabel) subLabel.textContent = 'Guitar Tuning:';
      if (hintEl) hintEl.textContent = 'Guitar mode: Strumming chord detection & 6-string tuner active';
      const presets = [
        { label: 'Std EADGBE', val: 'standard', active: true },
        { label: 'Drop D', val: 'dropd' },
        { label: 'DADGAD', val: 'dadgad' },
        { label: 'Open G', val: 'openg' }
      ];
      presets.forEach(function (p) {
        const b = document.createElement('button');
        b.type = 'button';
        b.className = 'sub-preset-btn' + (p.active ? ' is-active' : '');
        b.textContent = p.label;
        b.addEventListener('click', function () {
          subButtonsContainer.querySelectorAll('.sub-preset-btn').forEach(function (x) { x.classList.remove('is-active'); });
          b.classList.add('is-active');
          currentGuitarTuningMode = p.val;
          if (hintEl) hintEl.textContent = 'Guitar tuning set to ' + p.label + ' · String tracking ready';
        });
        subButtonsContainer.appendChild(b);
      });
    } else if (inst === 'percussion') {
      if (subLabel) subLabel.textContent = 'Percussion Kit:';
      if (hintEl) hintEl.textContent = 'Percussion mode: Transient strike onset, Bol recognition & Live BPM locked';
      const presets = [
        { label: 'Tabla', val: 'tabla', active: true },
        { label: 'Dholak', val: 'dholak' },
        { label: 'Drum Kit', val: 'drum' },
        { label: 'Claps', val: 'claps' }
      ];
      presets.forEach(function (p) {
        const b = document.createElement('button');
        b.type = 'button';
        b.className = 'sub-preset-btn' + (p.active ? ' is-active' : '');
        b.textContent = p.label;
        b.addEventListener('click', function () {
          subButtonsContainer.querySelectorAll('.sub-preset-btn').forEach(function (x) { x.classList.remove('is-active'); });
          b.classList.add('is-active');
          currentPercussionKit = p.val;
          if (hintEl) hintEl.textContent = 'Kit set to ' + p.label + ' · Live strike & tempo tracking active';
        });
        subButtonsContainer.appendChild(b);
      });
    } else if (inst === 'sitar') {
      if (subLabel) subLabel.textContent = 'Sitar Tonic:';
      if (hintEl) hintEl.textContent = 'Sitar / String mode: Sympathetic jawari resonance & multi-fret meend bend tracking';
      const presets = [
        { label: 'Kharaj-Pa (C#)', hz: 138.59, note: 'C#3', active: true },
        { label: 'Gandhar-Pa', hz: 130.81, note: 'C3' },
        { label: 'Vilayat Khan (D)', hz: 146.83, note: 'D3' }
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
    } else {
      // Voice / Default
      if (subLabel) subLabel.textContent = 'Vocal Tonic:';
      if (hintEl) hintEl.textContent = 'Voice mode: Standard Gayaki formant detection & 22-shruti microtonal tuning';
      const presets = [
        { label: 'C3', hz: 130.81, note: 'C3' },
        { label: 'D3', hz: 146.83, note: 'D3', active: true },
        { label: 'E3', hz: 164.81, note: 'E3' },
        { label: 'G3', hz: 196.00, note: 'G3' }
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
    }
  }

  function applyInstrumentTonic(hz, note) {
    userCustomSaHz = hz;
    Object.keys(PHRASE_LIBRARY).forEach(function (k) {
      PHRASE_LIBRARY[k].saHz = hz;
    });

    updateDroneButtonLabel();
    if (isDronePlaying) updateActiveDroneFrequencies();

    const telTarget = document.getElementById('ui-tel-target');
    if (telTarget) telTarget.textContent = 'Sa = ' + hz.toFixed(1) + ' Hz';

    const calibOpenBtn = document.getElementById('calibrate-sa-btn');
    if (calibOpenBtn) {
      calibOpenBtn.textContent = 'Sa: ' + hz.toFixed(1) + ' Hz (' + note + ')';
      calibOpenBtn.classList.add('is-calibrated');
    }

    if (isLiveMicActive) {
      renderLivePitchCanvas();
    } else {
      renderPhraseInspector();
    }
  }

  function initInstrumentProfiles() {
    const btns = document.querySelectorAll('.tracker-inst-btn');
    const hearBtn = document.getElementById('btn-hear-current-note');

    // 1. Hear Pure Shruti Reference button
    if (hearBtn) {
      hearBtn.addEventListener('click', playCurrentNoteReference);
    }

    // 2. Instrument Category Switcher
    btns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        btns.forEach(function (b) { b.classList.remove('is-active'); });
        btn.classList.add('is-active');
        const inst = btn.getAttribute('data-inst') || 'voice';
        activeInstrumentProfile = inst;
        renderInstrumentSubControls(inst);
        ensureWaveAnalyser();
      });
    });

    // 3. Wave Mode Toggle (Wave vs Harmonics)
    const waveModeBtns = document.querySelectorAll('.wave-mode-btn');
    waveModeBtns.forEach(function (wBtn) {
      wBtn.addEventListener('click', function () {
        waveModeBtns.forEach(function (b) { b.classList.remove('is-active'); });
        wBtn.classList.add('is-active');
        activeWaveMode = wBtn.getAttribute('data-mode') || 'oscilloscope';
      });
    });

    // Initialize sub-controls for default profile
    renderInstrumentSubControls('voice');"""

if old_init_inst_code in content:
    content = content.replace(old_init_inst_code, new_init_inst_code, 1)
    print("initInstrumentProfiles updated with dynamic sub-controls for all 5 instruments.")
else:
    print("Warning: old_init_inst_code not found!")

with open("app.js", "w", encoding="utf-8") as f:
    f.write(content)

print("app.js updated successfully with Universal Instrument Mapping!")

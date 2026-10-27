# -*- coding: utf-8 -*-
"""
Script to add Hold timer, Hear reference tone, Flute key selectors, and Harmonic Spectrum wave to app.js
"""

with open("app.js", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update wave state variables
old_wave_vars = """  // Live Note, Flute & Acoustic Wave Tracker State
  let activeInstrumentProfile = 'voice'; // 'voice', 'flute', 'string'
  let waveAnalyserNode = null;
  let waveAnimFrameId = null;
  const waveDataArray = new Float32Array(1024);"""

new_wave_vars = """  // Live Note, Flute & Acoustic Wave Tracker State
  let activeInstrumentProfile = 'voice'; // 'voice', 'flute', 'string'
  let activeWaveMode = 'oscilloscope'; // 'oscilloscope' or 'spectrum'
  let waveAnalyserNode = null;
  let waveAnimFrameId = null;
  const waveDataArray = new Float32Array(1024);
  const waveFreqDataArray = new Uint8Array(512);
  let currentHoldStartTime = 0;
  let currentHoldNote = '';
  let longestSessionHoldSec = 0;
  let lastTrackedShrutiRatioCents = 0;"""

if old_wave_vars in content:
    content = content.replace(old_wave_vars, new_wave_vars, 1)
    print("Wave variables updated.")
else:
    print("Warning: old_wave_vars not found!")

# 2. Update updateLiveNoteTracker to track lastTrackedShrutiRatioCents and Hold timer
hold_anchor = """    // 4. Update UI Text
    swaraEl.textContent = bestShruti.name;"""

new_hold_logic = """    lastTrackedShrutiRatioCents = bestShruti.cents;

    // Hold Timer & Breath Stamina Tracker
    const holdTimerEl = document.getElementById('live-hold-timer');
    if (holdTimerEl) {
      if (Math.abs(centDelta) <= 12.0) {
        if (currentHoldNote !== bestShruti.name) {
          currentHoldNote = bestShruti.name;
          currentHoldStartTime = performance.now();
        } else {
          const holdSec = (performance.now() - currentHoldStartTime) / 1000;
          if (holdSec > longestSessionHoldSec) longestSessionHoldSec = holdSec;

          if (holdSec >= 2.5) {
            holdTimerEl.textContent = 'Hold: ' + holdSec.toFixed(1) + 's (Best: ' + longestSessionHoldSec.toFixed(1) + 's)';
            holdTimerEl.className = 'tracker-hold-pill is-holding';
          } else {
            holdTimerEl.textContent = 'Hold: ' + holdSec.toFixed(1) + 's';
            holdTimerEl.className = 'tracker-hold-pill';
          }
        }
      } else {
        if (currentHoldStartTime > 0 && (performance.now() - currentHoldStartTime) > 900) {
          currentHoldNote = '';
          currentHoldStartTime = 0;
          holdTimerEl.textContent = longestSessionHoldSec > 0 ? 'Best: ' + longestSessionHoldSec.toFixed(1) + 's' : 'Hold: 0.0s';
          holdTimerEl.className = 'tracker-hold-pill';
        }
      }
    }

    // 4. Update UI Text
    swaraEl.textContent = bestShruti.name;"""

if hold_anchor in content:
    content = content.replace(hold_anchor, new_hold_logic, 1)
    print("Hold timer logic added to updateLiveNoteTracker.")
else:
    print("Warning: hold_anchor not found!")

# 3. Update drawWave in startAcousticWaveLoop to support activeWaveMode === 'spectrum'
spectrum_anchor = """      // Trigger phase lock (find first upward zero-crossing for rock-solid oscilloscope display)
      let triggerIdx = 0;
      for (let i = 1; i < 300; i++) {
        if (waveDataArray[i - 1] < 0 && waveDataArray[i] >= 0) {
          triggerIdx = i;
          break;
        }
      }"""

new_spectrum_logic = """      // Spectrum Harmonics Mode
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
          barGrad.addColorStop(0, activeInstrumentProfile === 'flute' ? '#a4bca3' : '#8fa68e');
          barGrad.addColorStop(1, 'rgba(143, 166, 142, 0.1)');

          ctx.fillStyle = barGrad;
          ctx.fillRect(x, y, barWidth, barHeight);
        }

        if (statsEl) {
          statsEl.textContent = (activeInstrumentProfile === 'flute' ? 'Flute Harmonics' : 'Acoustic Spectrum') + ' · 60 FPS';
        }
        return;
      }

      // Trigger phase lock (find first upward zero-crossing for rock-solid oscilloscope display)
      let triggerIdx = 0;
      for (let i = 1; i < 300; i++) {
        if (waveDataArray[i - 1] < 0 && waveDataArray[i] >= 0) {
          triggerIdx = i;
          break;
        }
      }"""

if spectrum_anchor in content:
    content = content.replace(spectrum_anchor, new_spectrum_logic, 1)
    print("Spectrum harmonics wave rendering added.")
else:
    print("Warning: spectrum_anchor not found!")

# 4. Add Hear Reference button, Flute Quick Keys, and Wave Mode Click handlers in initInstrumentProfiles
init_inst_anchor = """  function initInstrumentProfiles() {
    const btns = document.querySelectorAll('.tracker-inst-btn');
    const hintEl = document.getElementById('tracker-profile-hint');"""

new_init_inst = """  function playCurrentNoteReference() {
    const ctx = ensureAudioContext();
    if (!ctx) return;

    const baseSa = userCustomSaHz || (PHRASE_LIBRARY[currentPhraseKey] && PHRASE_LIBRARY[currentPhraseKey].saHz) || 146.83;
    const targetHz = baseSa * Math.pow(2, lastTrackedShrutiRatioCents / 1200);
    const now = ctx.currentTime;

    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.type = activeInstrumentProfile === 'flute' ? 'triangle' : 'sine';
    osc.frequency.setValueAtTime(targetHz, now);

    gain.gain.setValueAtTime(0.001, now);
    gain.gain.linearRampToValueAtTime(0.18, now + 0.05);
    gain.gain.setValueAtTime(0.18, now + 0.9);
    gain.gain.exponentialRampToValueAtTime(0.0008, now + 1.2);

    const analyser = ensureWaveAnalyser();
    if (analyser) osc.connect(analyser);

    osc.connect(gain);
    gain.connect(ctx.destination);

    osc.start(now);
    osc.stop(now + 1.25);
  }

  function initInstrumentProfiles() {
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

if init_inst_anchor in content:
    content = content.replace(init_inst_anchor, new_init_inst, 1)
    print("initInstrumentProfiles updated with Hear, Flute keys, and Wave mode handlers.")
else:
    print("Warning: init_inst_anchor not found!")

with open("app.js", "w", encoding="utf-8") as f:
    f.write(content)

print("app.js updated successfully with all 4 new musician features!")

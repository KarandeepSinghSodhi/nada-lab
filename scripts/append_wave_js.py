# -*- coding: utf-8 -*-
"""
Script to integrate the Live Note Tracker, Flute Profile, and Cool Acoustic Waveform Oscilloscope into app.js
"""

with open("app.js", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add state variables
state_anchor = "let calibPitchBuffer = [];"
new_state_vars = """let calibPitchBuffer = [];

  // Live Note, Flute & Acoustic Wave Tracker State
  let activeInstrumentProfile = 'voice'; // 'voice', 'flute', 'string'
  let waveAnalyserNode = null;
  let waveAnimFrameId = null;
  const waveDataArray = new Float32Array(1024);"""

if state_anchor in content:
    content = content.replace(state_anchor, new_state_vars, 1)
    print("Wave state variables added.")
else:
    print("Warning: state_anchor not found!")

# 2. Add ensureWaveAnalyser helper
audio_ctx_anchor = "  function ensureAudioContext() {"
wave_analyser_helper = """  function ensureWaveAnalyser() {
    const ctx = ensureAudioContext();
    if (!ctx) return null;
    if (!waveAnalyserNode) {
      waveAnalyserNode = ctx.createAnalyser();
      waveAnalyserNode.fftSize = 1024;
      waveAnalyserNode.smoothingTimeConstant = 0.4;
      startAcousticWaveLoop();
    }
    return waveAnalyserNode;
  }

"""

if audio_ctx_anchor in content:
    content = content.replace(audio_ctx_anchor, wave_analyser_helper + audio_ctx_anchor, 1)
    print("Wave analyser helper added.")
else:
    print("Warning: audio_ctx_anchor not found!")

# 3. Connect waveAnalyser in toggleLiveMic
live_mic_anchor = "      micSource.connect(workletNode);\n      micWorkletNode = workletNode;"
new_live_mic_conn = """      const analyser = ensureWaveAnalyser();
      if (analyser) {
        micSource.connect(analyser);
      }
      micSource.connect(workletNode);\n      micWorkletNode = workletNode;"""

if live_mic_anchor in content:
    content = content.replace(live_mic_anchor, new_live_mic_conn, 1)
    print("Live mic connected to wave analyser.")
else:
    print("Warning: live_mic_anchor not found!")

# 4. Connect waveAnalyser in auditionActivePhrase
audition_buf_anchor = "      source.connect(ctx.destination);\n      source.start();"
new_audition_buf_conn = """      const analyser = ensureWaveAnalyser();
      if (analyser) source.connect(analyser);
      source.connect(ctx.destination);
      source.start();"""

if audition_buf_anchor in content:
    content = content.replace(audition_buf_anchor, new_audition_buf_conn, 1)
    print("Audition buffer connected to wave analyser.")
else:
    print("Warning: audition_buf_anchor not found!")

audition_osc_anchor = "    gain.connect(ctx.destination);\n\n    osc.start(now);"
new_audition_osc_conn = """    const analyser = ensureWaveAnalyser();
    if (analyser) gain.connect(analyser);
    gain.connect(ctx.destination);\n\n    osc.start(now);"""

if audition_osc_anchor in content:
    content = content.replace(audition_osc_anchor, new_audition_osc_conn, 1)
    print("Audition osc connected to wave analyser.")
else:
    print("Warning: audition_osc_anchor not found!")

# 5. Call updateLiveNoteTracker inside handleIncomingPitchFrame
pitch_frame_anchor = "    detectLiveOrnamentAndDiagnostics(cents, saHz);\n    renderLivePitchCanvas();"
new_pitch_frame_call = """    detectLiveOrnamentAndDiagnostics(cents, saHz);
    updateLiveNoteTracker(data.pitch, cents, saHz, data.rms || 0);
    renderLivePitchCanvas();"""

if pitch_frame_anchor in content:
    content = content.replace(pitch_frame_anchor, new_pitch_frame_call, 1)
    print("handleIncomingPitchFrame updated with note tracker.")
else:
    print("Warning: pitch_frame_anchor not found!")

# 6. Call updateLiveNoteTracker inside renderPhraseInspector (for scrubber sync)
scrub_render_anchor = "    const cNow = activeCurveFn(u);\n    const cNext = activeCurveFn(Math.min(1, u + 0.01));"
new_scrub_render = """    const cNow = activeCurveFn(u);
    const cNext = activeCurveFn(Math.min(1, u + 0.01));
    const effectiveSa = userCustomSaHz || phrase.saHz || 146.83;
    const estHz = effectiveSa * Math.pow(2, cNow / 1200);
    updateLiveNoteTracker(estHz, cNow, effectiveSa, 0.08);"""

if scrub_render_anchor in content:
    content = content.replace(scrub_render_anchor, new_scrub_render, 1)
    print("renderPhraseInspector updated with note tracker.")
else:
    print("Warning: scrub_render_anchor not found!")

# 7. Add Note Tracker Engine & Acoustic Wave Subsystem before DOMContentLoaded
wave_subsystem_code = """  /* =========================================================
     8C. REAL-TIME NOTE TRACKER, FLUTE MODE & ACOUSTIC WAVE
     ========================================================= */
  const WESTERN_NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];

  const SHRUTI_MAP_22 = [
    { name: 'Sa', sargam: 'सा', ratio: '1/1', cents: 0.0 },
    { name: 'Ati Komal Re', sargam: 'रे॒', ratio: '256/243', cents: 90.2 },
    { name: 'Komal Re', sargam: 'रे॒', ratio: '16/15', cents: 111.7 },
    { name: 'Shuddha Re', sargam: 'रे', ratio: '9/8', cents: 203.9 },
    { name: 'Tivra Re', sargam: 'रे', ratio: '10/9', cents: 182.4 },
    { name: 'Ati Komal Ga', sargam: 'ग॒', ratio: '32/27', cents: 294.1 },
    { name: 'Komal Ga', sargam: 'ग॒', ratio: '6/5', cents: 315.6 },
    { name: 'Shuddha Ga', sargam: 'ग', ratio: '5/4', cents: 386.3 },
    { name: 'Tivra Ga', sargam: 'ग', ratio: '81/64', cents: 407.8 },
    { name: 'Shuddha Ma', sargam: 'म', ratio: '4/3', cents: 498.0 },
    { name: 'Tivra Ma (Prati)', sargam: 'म॑', ratio: '45/32', cents: 590.2 },
    { name: 'Tivratara Ma', sargam: 'म॑', ratio: '64/45', cents: 609.8 },
    { name: 'Pa', sargam: 'प', ratio: '3/2', cents: 702.0 },
    { name: 'Ati Komal Dha', sargam: 'ध॒', ratio: '128/81', cents: 792.2 },
    { name: 'Komal Dha', sargam: 'ध॒', ratio: '8/5', cents: 813.7 },
    { name: 'Shuddha Dha', sargam: 'ध', ratio: '5/3', cents: 905.9 },
    { name: 'Tivra Dha', sargam: 'ध', ratio: '27/16', cents: 927.4 },
    { name: 'Ati Komal Ni', sargam: 'नि॒', ratio: '16/9', cents: 996.1 },
    { name: 'Komal Ni', sargam: 'नि॒', ratio: '9/5', cents: 1017.6 },
    { name: 'Shuddha Ni', sargam: 'नि', ratio: '15/8', cents: 1088.3 },
    { name: 'Tivra Ni', sargam: 'नि', ratio: '243/128', cents: 1109.8 }
  ];

  function updateLiveNoteTracker(freq, rawCents, saHz, rms) {
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

    if (!freq || freq <= 55 || freq >= 1500 || rawCents === null || isNaN(rawCents)) {
      if (signalMeterEl) signalMeterEl.textContent = 'Signal: Idle';
      if (centsBadge) {
        centsBadge.textContent = '0.0c · Exact Shruti';
        centsBadge.className = 'tracker-cents-badge';
      }
      if (gaugeNeedle) gaugeNeedle.style.left = '50%';
      return;
    }

    // 1. Western Note & Octave
    const midiNote = Math.round(69 + 12 * Math.log2(freq / 440));
    const noteIdx = ((midiNote % 12) + 12) % 12;
    const westernOctave = Math.floor(midiNote / 12) - 1;
    const westernStr = WESTERN_NOTE_NAMES[noteIdx] + westernOctave;

    // 2. Indian Classical Swara & Saptak (Octave)
    const saptakOctave = Math.floor(rawCents / 1200);
    let modCents = ((rawCents % 1200) + 1200) % 1200;

    let saptakLabel = 'Madhya Saptak (Middle)';
    let sargamAccent = '';
    if (saptakOctave < 0) {
      saptakLabel = 'Mandra Saptak (Lower)';
      sargamAccent = '़'; // Mandra dot below
    } else if (saptakOctave > 0) {
      saptakLabel = activeInstrumentProfile === 'flute' ? 'Taar Saptak (Flute Overblow)' : 'Taar Saptak (Higher)';
      sargamAccent = 'ं'; // Taar dot above
    }

    // 3. Find Nearest Shruti
    let bestShruti = SHRUTI_MAP_22[0];
    let minDiff = 9999;
    SHRUTI_MAP_22.forEach(function (sh) {
      const diff = Math.abs(modCents - sh.cents);
      if (diff < minDiff) {
        minDiff = diff;
        bestShruti = sh;
      }
    });

    // Handle high octave wraparound near 1200c
    if (Math.abs(modCents - 1200) < minDiff) {
      bestShruti = { name: 'Taar Sa', sargam: 'सां', ratio: '2/1', cents: 1200.0 };
      minDiff = Math.abs(modCents - 1200);
    }

    let centDelta = modCents - bestShruti.cents;
    if (centDelta > 50) centDelta -= 1200;
    if (centDelta < -50) centDelta += 1200;

    // 4. Update UI Text
    swaraEl.textContent = bestShruti.name;
    sargamEl.textContent = bestShruti.sargam + (saptakOctave !== 0 && bestShruti.name !== 'Taar Sa' ? sargamAccent : '');
    westernEl.textContent = westernStr;
    freqEl.textContent = freq.toFixed(1) + ' Hz';
    saptakEl.textContent = saptakLabel;

    // 5. Gauge Needle & Cents Badge
    const clampedDelta = Math.max(-50, Math.min(50, centDelta));
    const needlePct = 50 + (clampedDelta / 50) * 45;
    if (gaugeNeedle) {
      gaugeNeedle.style.left = needlePct.toFixed(1) + '%';
    }

    const sign = centDelta >= 0 ? '+' : '';
    const absD = Math.abs(centDelta);

    if (centsBadge) {
      if (absD <= 5.0) {
        centsBadge.textContent = sign + centDelta.toFixed(1) + 'c · Exact Shruti';
        centsBadge.className = 'tracker-cents-badge';
      } else if (centDelta > 5.0) {
        centsBadge.textContent = sign + centDelta.toFixed(1) + 'c · Sharp';
        centsBadge.className = 'tracker-cents-badge is-sharp';
      } else {
        centsBadge.textContent = sign + centDelta.toFixed(1) + 'c · Flat';
        centsBadge.className = 'tracker-cents-badge is-flat';
      }
    }

    if (shrutiRatioEl) {
      shrutiRatioEl.textContent = 'Shruti Ratio: ' + bestShruti.ratio + ' (' + bestShruti.cents.toFixed(1) + 'c)';
    }

    if (tuningStatusEl) {
      if (absD <= 5.0) {
        tuningStatusEl.textContent = 'Pure Shruti Intonation';
        tuningStatusEl.style.color = '#a4bca3';
      } else if (absD <= 15.0) {
        tuningStatusEl.textContent = 'Acceptable Resonance';
        tuningStatusEl.style.color = '#c8c5ba';
      } else {
        tuningStatusEl.textContent = 'Microtonal Deviation';
        tuningStatusEl.style.color = '#e09f67';
      }
    }

    if (signalMeterEl) {
      const instName = activeInstrumentProfile === 'flute' ? 'Bansuri Flute' : (activeInstrumentProfile === 'string' ? 'String Harmonic' : 'Voice Gayaki');
      signalMeterEl.textContent = 'Signal: ' + instName + ' (' + (rms > 0 ? (rms * 100).toFixed(0) : 'Active') + '%)';
    }
  }

  // Real-Time Acoustic Oscilloscope Waveform Renderer (The "Cool Wave")
  function startAcousticWaveLoop() {
    if (waveAnimFrameId) return;

    const canvas = document.getElementById('acoustic-wave-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const statsEl = document.getElementById('live-wave-stats');

    function drawWave() {
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

      if (rms < 0.006) {
        // Serene ambient idling breath pulse
        const now = performance.now() / 1000;
        ctx.strokeStyle = 'rgba(143, 166, 142, 0.35)';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        for (let x = 0; x < w; x += 4) {
          const u = x / w;
          const y = centerY + Math.sin(u * 12 + now * 3) * 2.5;
          if (x === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.stroke();
        if (statsEl) statsEl.textContent = 'Oscilloscope: Standby · 60 FPS';
        return;
      }

      // Trigger phase lock (find first upward zero-crossing for rock-solid oscilloscope display)
      let triggerIdx = 0;
      for (let i = 1; i < 300; i++) {
        if (waveDataArray[i - 1] < 0 && waveDataArray[i] >= 0) {
          triggerIdx = i;
          break;
        }
      }

      const availableLen = waveDataArray.length - triggerIdx;
      const drawLen = Math.min(availableLen, 512);

      // Create glowing gradient
      const grad = ctx.createLinearGradient(0, 0, 0, h);
      grad.addColorStop(0, 'rgba(164, 188, 163, 0.25)');
      grad.addColorStop(0.5, 'rgba(143, 166, 142, 0.08)');
      grad.addColorStop(1, 'rgba(143, 166, 142, 0.02)');

      // Draw translucent wave envelope fill
      ctx.beginPath();
      ctx.moveTo(0, centerY);
      for (let i = 0; i < drawLen; i++) {
        const x = (i / (drawLen - 1)) * w;
        let v = waveDataArray[triggerIdx + i];
        // In flute mode, apply gentle smoothing to highlight smooth bore resonance
        if (activeInstrumentProfile === 'flute' && i > 0 && i < drawLen - 1) {
          v = (waveDataArray[triggerIdx + i - 1] + v * 2 + waveDataArray[triggerIdx + i + 1]) / 4;
        }
        const y = centerY - v * (h * 0.42);
        ctx.lineTo(x, y);
      }
      ctx.lineTo(w, centerY);
      ctx.closePath();
      ctx.fillStyle = grad;
      ctx.fill();

      // Draw primary glowing oscilloscope trace line
      ctx.strokeStyle = activeInstrumentProfile === 'flute' ? '#a4bca3' : '#8fa68e';
      ctx.lineWidth = 2.2;
      ctx.beginPath();
      for (let i = 0; i < drawLen; i++) {
        const x = (i / (drawLen - 1)) * w;
        let v = waveDataArray[triggerIdx + i];
        if (activeInstrumentProfile === 'flute' && i > 0 && i < drawLen - 1) {
          v = (waveDataArray[triggerIdx + i - 1] + v * 2 + waveDataArray[triggerIdx + i + 1]) / 4;
        }
        const y = centerY - v * (h * 0.42);
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();

      if (statsEl) {
        const profileLabel = activeInstrumentProfile === 'flute' ? 'Bansuri Air Column' : (activeInstrumentProfile === 'string' ? 'String Harmonic' : 'Vocal Formant');
        statsEl.textContent = profileLabel + ' · ' + (rms * 100).toFixed(0) + '% RMS · 60 FPS';
      }
    }

    drawWave();
  }

  function initInstrumentProfiles() {
    const btns = document.querySelectorAll('.tracker-inst-btn');
    const hintEl = document.getElementById('tracker-profile-hint');

    btns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        btns.forEach(function (b) { b.classList.remove('is-active'); });
        btn.classList.add('is-active');
        const inst = btn.getAttribute('data-inst') || 'voice';
        activeInstrumentProfile = inst;

        if (hintEl) {
          if (inst === 'flute') {
            hintEl.textContent = 'Bansuri Flute mode: Pure air column resonance & Taar overblowing tracking';
          } else if (inst === 'string') {
            hintEl.textContent = 'String mode: Plucked attack & sympathetic jawari overtones active';
          } else {
            hintEl.textContent = 'Voice mode: Standard Gayaki formant detection & vowel resonance';
          }
        }

        // Trigger wave canvas start if not already active
        ensureWaveAnalyser();
      });
    });

    // Start wave canvas on initial load
    setTimeout(function () {
      ensureWaveAnalyser();
    }, 400);
  }"""

# Insert wave_subsystem_code before DOMContentLoaded
dom_anchor = "  document.addEventListener('DOMContentLoaded', function () {"
new_dom_code = wave_subsystem_code + "\n\n" + dom_anchor

if dom_anchor in content:
    content = content.replace(dom_anchor, new_dom_code, 1)
    print("Wave subsystem added before DOMContentLoaded.")
else:
    print("Warning: dom_anchor not found!")

# Add initInstrumentProfiles to DOMContentLoaded
old_inits = "    initMusicianControls();"
new_inits = "    initMusicianControls();\n    initInstrumentProfiles();"

if old_inits in content:
    content = content.replace(old_inits, new_inits, 1)
    print("Instrument profiles init added to DOMContentLoaded.")
else:
    print("Warning: old_inits not found!")

with open("app.js", "w", encoding="utf-8") as f:
    f.write(content)

print("app.js successfully updated with Live Note Tracker & Acoustic Wave!")

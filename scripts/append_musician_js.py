# -*- coding: utf-8 -*-
"""
Script to integrate the 6 musician-first features into app.js
"""

import sys

with open("app.js", "r", encoding="utf-8") as f:
    content = f.read()

# 1. State variables to declare near the top (around let currentPhraseKey = ...)
state_anchor = "let audioCtx = null;\n  let droneNodes = null;\n  let isDronePlaying = false;"

new_state_vars = """let audioCtx = null;
  let droneNodes = null;
  let isDronePlaying = false;
  let userCustomSaHz = 146.83; // D3 default, dynamically calibrated
  let currentDroneTuning = 'pa'; // 'pa', 'ma', 'ni'
  let currentAuditionSpeed = 1.0; // 0.5, 0.75, 1.0
  let isGhostActive = false;
  let previousTakeCurveFn = null;
  let previousTakeLiveHistory = null;
  let isCalibratingMic = false;
  let calibAudioStream = null;
  let calibPitchBuffer = [];"""

if state_anchor in content:
    content = content.replace(state_anchor, new_state_vars, 1)
    print("State variables replaced successfully.")
else:
    print("Warning: state_anchor not found!")

# 2. Update toggleTanpuraDrone and add drone helpers
old_drone_code = """  // Live Tanpura Sa-Pa-Sa' Drone Generator
  function toggleTanpuraDrone() {
    const btn = document.getElementById('drone-toggle-btn');
    const lbl = document.getElementById('drone-toggle-label');
    const ctx = ensureAudioContext();
    if (!ctx) return;

    if (isDronePlaying && droneNodes) {
      droneNodes.masterGain.gain.setTargetAtTime(0.0001, ctx.currentTime, 0.08);
      setTimeout(function () {
        if (droneNodes) {
          droneNodes.oscs.forEach(function (o) {
            try { o.stop(); } catch (e) {}
          });
          droneNodes = null;
        }
      }, 150);
      isDronePlaying = false;
      btn.classList.remove('is-playing');
      lbl.textContent = 'Start Sa-Pa Drone (146.8 Hz)';
      return;
    }

    const saFreq = 146.83; // D3
    const freqs = [saFreq * 1.4983, saFreq * 2, saFreq * 2, saFreq];
    const masterGain = ctx.createGain();
    masterGain.gain.setValueAtTime(0.001, ctx.currentTime);
    masterGain.gain.setTargetAtTime(0.14, ctx.currentTime, 0.15);
    masterGain.connect(ctx.destination);

    const oscs = [];
    freqs.forEach(function (f, idx) {
      const osc = ctx.createOscillator();
      const filter = ctx.createBiquadFilter();
      const g = ctx.createGain();

      osc.type = idx % 2 === 0 ? 'sawtooth' : 'triangle';
      osc.frequency.setValueAtTime(f + (idx - 1.5) * 0.18, ctx.currentTime);

      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(680 + idx * 140, ctx.currentTime);
      filter.Q.setValueAtTime(3.2, ctx.currentTime);

      g.gain.setValueAtTime(0.24, ctx.currentTime);

      osc.connect(filter);
      filter.connect(g);
      g.connect(masterGain);
      osc.start();
      oscs.push(osc);
    });

    droneNodes = { masterGain: masterGain, oscs: oscs };
    isDronePlaying = true;
    btn.classList.add('is-playing');
    lbl.textContent = 'Stop Sa-Pa Drone (Active)';
  }"""

new_drone_code = """  // Helper to compute 4-string frequencies for Tanpura drone
  function getDroneFrequencies(saHz, tuning) {
    let firstString;
    if (tuning === 'ma') {
      firstString = saHz * (4.0 / 3.0); // Shuddha Madhyam (4/3) for Malkauns, Chandrakauns, Bageshree
    } else if (tuning === 'ni') {
      firstString = saHz * (15.0 / 16.0); // Mandra Shuddha Nishad (15/16) for Marwa, Puriya, Sohini
    } else {
      firstString = saHz * 1.4983; // Pancham (~3/2) universal default
    }
    return [firstString, saHz * 2.0, saHz * 2.0, saHz];
  }

  function updateActiveDroneFrequencies() {
    if (!droneNodes || !audioCtx) return;
    const baseSa = userCustomSaHz || (PHRASE_LIBRARY[currentPhraseKey] && PHRASE_LIBRARY[currentPhraseKey].saHz) || 146.83;
    const freqs = getDroneFrequencies(baseSa, currentDroneTuning);
    const now = audioCtx.currentTime;
    droneNodes.oscs.forEach(function (osc, idx) {
      if (idx < freqs.length) {
        osc.frequency.setTargetAtTime(freqs[idx] + (idx - 1.5) * 0.18, now, 0.08);
      }
    });
  }

  function updateDroneButtonLabel() {
    const lbl = document.getElementById('drone-toggle-label');
    if (!lbl) return;
    const baseSa = userCustomSaHz || (PHRASE_LIBRARY[currentPhraseKey] && PHRASE_LIBRARY[currentPhraseKey].saHz) || 146.83;
    const tuningName = currentDroneTuning === 'ma' ? 'Sa-Ma' : (currentDroneTuning === 'ni' ? 'Sa-Ni' : 'Sa-Pa');
    lbl.textContent = (isDronePlaying ? 'Stop ' : 'Start ') + tuningName + ' Drone (' + baseSa.toFixed(1) + ' Hz)';
  }

  // Live Tanpura Sa-Pa / Sa-Ma / Sa-Ni Drone Generator
  function toggleTanpuraDrone() {
    const btn = document.getElementById('drone-toggle-btn');
    const ctx = ensureAudioContext();
    if (!ctx) return;

    if (isDronePlaying && droneNodes) {
      droneNodes.masterGain.gain.setTargetAtTime(0.0001, ctx.currentTime, 0.08);
      setTimeout(function () {
        if (droneNodes) {
          droneNodes.oscs.forEach(function (o) {
            try { o.stop(); } catch (e) {}
          });
          droneNodes = null;
        }
      }, 150);
      isDronePlaying = false;
      if (btn) btn.classList.remove('is-playing');
      updateDroneButtonLabel();
      return;
    }

    const saFreq = userCustomSaHz || (PHRASE_LIBRARY[currentPhraseKey] && PHRASE_LIBRARY[currentPhraseKey].saHz) || 146.83;
    const freqs = getDroneFrequencies(saFreq, currentDroneTuning);
    const masterGain = ctx.createGain();
    masterGain.gain.setValueAtTime(0.001, ctx.currentTime);
    masterGain.gain.setTargetAtTime(0.14, ctx.currentTime, 0.15);
    masterGain.connect(ctx.destination);

    const oscs = [];
    freqs.forEach(function (f, idx) {
      const osc = ctx.createOscillator();
      const filter = ctx.createBiquadFilter();
      const g = ctx.createGain();

      osc.type = idx % 2 === 0 ? 'sawtooth' : 'triangle';
      osc.frequency.setValueAtTime(f + (idx - 1.5) * 0.18, ctx.currentTime);

      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(680 + idx * 140, ctx.currentTime);
      filter.Q.setValueAtTime(3.2, ctx.currentTime);

      g.gain.setValueAtTime(0.24, ctx.currentTime);

      osc.connect(filter);
      filter.connect(g);
      g.connect(masterGain);
      osc.start();
      oscs.push(osc);
    });

    droneNodes = { masterGain: masterGain, oscs: oscs };
    isDronePlaying = true;
    if (btn) btn.classList.add('is-playing');
    updateDroneButtonLabel();
  }"""

if old_drone_code in content:
    content = content.replace(old_drone_code, new_drone_code, 1)
    print("Tanpura drone code replaced successfully.")
else:
    print("Warning: old_drone_code not found!")

# 3. Update auditionActivePhrase to respect currentAuditionSpeed
old_audition_code = """    if (phrase.audioBuffer) {
      // Play real human vocal recording buffer
      const source = ctx.createBufferSource();
      source.buffer = phrase.audioBuffer;
      source.connect(ctx.destination);
      source.start();
      activeAuditionSource = source;

      const duration = phrase.audioBuffer.duration;
      const scrubber = document.getElementById('phrase-scrubber');
      const startTs = performance.now();

      source.onended = function () {
        stopAudition();
      };

      function stepScrubBuffer(ts) {
        if (!activeAuditionSource) return;
        const elapsed = (ts - startTs) / (duration * 1000);
        if (elapsed <= 1) {
          scrubValue = Math.round(elapsed * 100);
          if (scrubber) scrubber.value = String(scrubValue);
          renderPhraseInspector();
          activeAuditionAnim = requestAnimationFrame(stepScrubBuffer);
        } else {
          stopAudition();
        }
      }
      activeAuditionAnim = requestAnimationFrame(stepScrubBuffer);
      return;
    }

    // Otherwise synthetic benchmark oscillator audition
    const duration = 2.2;
    const now = ctx.currentTime;
    const steps = 80;

    const osc = ctx.createOscillator();
    const filter = ctx.createBiquadFilter();
    const gain = ctx.createGain();

    osc.type = 'sawtooth';
    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(1150, now);
    filter.Q.setValueAtTime(2.5, now);

    gain.gain.setValueAtTime(0.001, now);
    gain.gain.linearRampToValueAtTime(0.16, now + 0.06);
    gain.gain.setValueAtTime(0.16, now + duration - 0.15);
    gain.gain.exponentialRampToValueAtTime(0.0008, now + duration);

    for (let i = 0; i <= steps; i++) {
      const u = i / steps;
      const c = phrase.curveFn(u);
      const freq = phrase.saHz * Math.pow(2, c / 1200);
      osc.frequency.setValueAtTime(freq, now + u * duration);
    }

    osc.connect(filter);
    filter.connect(gain);
    gain.connect(ctx.destination);

    osc.start(now);
    osc.stop(now + duration + 0.02);
    activeAuditionSource = osc;

    osc.onended = function () {
      stopAudition();
    };

    const scrubber = document.getElementById('phrase-scrubber');
    const startTs = performance.now();
    function stepScrub(ts) {
      if (!activeAuditionSource) return;
      const elapsed = (ts - startTs) / (duration * 1000);
      if (elapsed <= 1) {
        scrubValue = Math.round(elapsed * 100);
        if (scrubber) scrubber.value = String(scrubValue);
        renderPhraseInspector();
        activeAuditionAnim = requestAnimationFrame(stepScrub);
      } else {
        stopAudition();
      }
    }
    activeAuditionAnim = requestAnimationFrame(stepScrub);"""

new_audition_code = """    const speed = currentAuditionSpeed || 1.0;

    if (phrase.audioBuffer) {
      // Play real human vocal recording buffer with speed scaling
      const source = ctx.createBufferSource();
      source.buffer = phrase.audioBuffer;
      source.playbackRate.value = speed;
      source.connect(ctx.destination);
      source.start();
      activeAuditionSource = source;

      const duration = phrase.audioBuffer.duration / speed;
      const scrubber = document.getElementById('phrase-scrubber');
      const startTs = performance.now();

      source.onended = function () {
        snapshotCurrentTake();
        stopAudition();
      };

      function stepScrubBuffer(ts) {
        if (!activeAuditionSource) return;
        const elapsed = (ts - startTs) / (duration * 1000);
        if (elapsed <= 1) {
          scrubValue = Math.round(elapsed * 100);
          if (scrubber) scrubber.value = String(scrubValue);
          renderPhraseInspector();
          activeAuditionAnim = requestAnimationFrame(stepScrubBuffer);
        } else {
          snapshotCurrentTake();
          stopAudition();
        }
      }
      activeAuditionAnim = requestAnimationFrame(stepScrubBuffer);
      return;
    }

    // Otherwise synthetic benchmark oscillator audition with speed scaling
    const duration = 2.2 / speed;
    const now = ctx.currentTime;
    const steps = 80;

    const osc = ctx.createOscillator();
    const filter = ctx.createBiquadFilter();
    const gain = ctx.createGain();

    osc.type = 'sawtooth';
    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(1150, now);
    filter.Q.setValueAtTime(2.5, now);

    gain.gain.setValueAtTime(0.001, now);
    gain.gain.linearRampToValueAtTime(0.16, now + 0.06);
    gain.gain.setValueAtTime(0.16, now + duration - 0.15);
    gain.gain.exponentialRampToValueAtTime(0.0008, now + duration);

    const effectiveSa = userCustomSaHz || phrase.saHz || 146.83;
    for (let i = 0; i <= steps; i++) {
      const u = i / steps;
      const c = phrase.curveFn(u);
      const freq = effectiveSa * Math.pow(2, c / 1200);
      osc.frequency.setValueAtTime(freq, now + u * duration);
    }

    osc.connect(filter);
    filter.connect(gain);
    gain.connect(ctx.destination);

    osc.start(now);
    osc.stop(now + duration + 0.02);
    activeAuditionSource = osc;

    osc.onended = function () {
      snapshotCurrentTake();
      stopAudition();
    };

    const scrubber = document.getElementById('phrase-scrubber');
    const startTs = performance.now();
    function stepScrub(ts) {
      if (!activeAuditionSource) return;
      const elapsed = (ts - startTs) / (duration * 1000);
      if (elapsed <= 1) {
        scrubValue = Math.round(elapsed * 100);
        if (scrubber) scrubber.value = String(scrubValue);
        renderPhraseInspector();
        activeAuditionAnim = requestAnimationFrame(stepScrub);
      } else {
        snapshotCurrentTake();
        stopAudition();
      }
    }
    activeAuditionAnim = requestAnimationFrame(stepScrub);"""

if old_audition_code in content:
    content = content.replace(old_audition_code, new_audition_code, 1)
    print("Audition code replaced successfully.")
else:
    print("Warning: old_audition_code not found!")

# 4. Add snapshot helper and Sur Sthirata logic in detectLiveOrnamentAndDiagnostics
old_diag_header = """  function detectLiveOrnamentAndDiagnostics(latestCents, saHz) {
    const ornamentEl = document.getElementById('ui-ornament-tag');
    const readoutEl = document.getElementById('ui-cursor-readout');
    const tierNameEl = document.getElementById('ui-tier-name');
    const scoreValEl = document.getElementById('ui-score-val');
    const headlineEl = document.getElementById('ui-diag-headline');
    const detailEl = document.getElementById('ui-diag-detail');
    const drillEl = document.getElementById('ui-drill-text');
    const telTarget = document.getElementById('ui-tel-target');
    const telMeasured = document.getElementById('ui-tel-measured');
    const telVelocity = document.getElementById('ui-tel-velocity');
    const telGrammar = document.getElementById('ui-tel-grammar');

    if (latestCents === null) {
      if (readoutEl) readoutEl.textContent = 'Listening for voice... (sing into microphone)';
      if (ornamentEl) ornamentEl.textContent = 'Status: Unvoiced / Breath';
      return;
    }"""

new_diag_header = """  // Snapshot current take for ghost comparison
  function snapshotCurrentTake() {
    const phrase = PHRASE_LIBRARY[currentPhraseKey];
    if (phrase && phrase.curveFn) {
      previousTakeCurveFn = phrase.curveFn;
    }
    if (livePitchHistory.length > 5) {
      previousTakeLiveHistory = livePitchHistory.map(function (p) {
        return { cents: p.cents, clarity: p.clarity };
      });
    }
  }

  function detectLiveOrnamentAndDiagnostics(latestCents, saHz) {
    const ornamentEl = document.getElementById('ui-ornament-tag');
    const readoutEl = document.getElementById('ui-cursor-readout');
    const tierNameEl = document.getElementById('ui-tier-name');
    const scoreValEl = document.getElementById('ui-score-val');
    const headlineEl = document.getElementById('ui-diag-headline');
    const detailEl = document.getElementById('ui-diag-detail');
    const drillEl = document.getElementById('ui-drill-text');
    const telTarget = document.getElementById('ui-tel-target');
    const telMeasured = document.getElementById('ui-tel-measured');
    const telVelocity = document.getElementById('ui-tel-velocity');
    const telGrammar = document.getElementById('ui-tel-grammar');
    const sthirataEl = document.getElementById('ui-sthirata-pill');

    if (latestCents === null) {
      if (readoutEl) readoutEl.textContent = 'Listening for voice... (sing into microphone)';
      if (ornamentEl) ornamentEl.textContent = 'Status: Unvoiced / Breath';
      if (sthirataEl) {
        sthirataEl.textContent = 'Sur Sthirata: --';
        sthirataEl.className = 'ui-pill ui-sthirata-pill';
      }
      return;
    }

    // 0. Compute Sur Sthirata (Pitch Steadiness Variance \u03c3)
    if (sthirataEl && livePitchHistory.length >= 10) {
      const recentVoiced = livePitchHistory.slice(-18).filter(function (p) { return p.cents !== null; });
      if (recentVoiced.length >= 8) {
        const cVals = recentVoiced.map(function (p) { return p.cents; });
        const meanC = cVals.reduce(function (a, b) { return a + b; }, 0) / cVals.length;
        const variance = cVals.reduce(function (acc, c) { return acc + Math.pow(c - meanC, 2); }, 0) / cVals.length;
        const sigma = Math.sqrt(variance);

        if (sigma <= 5.5) {
          sthirataEl.textContent = 'Sur Sthirata: Achala (\u00b1' + sigma.toFixed(1) + 'c)';
          sthirataEl.className = 'ui-pill ui-sthirata-pill is-achala';
        } else if (sigma <= 12.0) {
          sthirataEl.textContent = 'Sur Sthirata: Stable (\u00b1' + sigma.toFixed(1) + 'c)';
          sthirataEl.className = 'ui-pill ui-sthirata-pill is-stable';
        } else {
          sthirataEl.textContent = 'Sur Sthirata: Tremor (\u00b1' + sigma.toFixed(1) + 'c)';
          sthirataEl.className = 'ui-pill ui-sthirata-pill is-tremor';
        }
      }
    }"""

if old_diag_header in content:
    content = content.replace(old_diag_header, new_diag_header, 1)
    print("Diagnostics header & Sthirata replaced successfully.")
else:
    print("Warning: old_diag_header not found!")

# 5. Draw ghost overlay in renderPhraseInspector
ghost_inspector_anchor = """    const isShowingGuru = isGuruPlaying || (phrase.guruCurveFn && showGuruOverlay);
    ctx.strokeStyle = isShowingGuru ? 'rgba(143, 166, 142, 0.4)' : '#8fa68e';
    ctx.lineWidth = 3.5;
    ctx.beginPath();
    const samples = 160;
    for (let i = 0; i <= samples; i++) {
      const sU = i / samples;
      const x = padLeft + sU * plotW;
      const y = yForCents(phrase.curveFn(sU));
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();"""

new_ghost_inspector = """    // Ghost Take Comparison Ribbon
    if (isGhostActive && previousTakeCurveFn) {
      ctx.strokeStyle = 'rgba(164, 188, 163, 0.35)';
      ctx.lineWidth = 2.0;
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      for (let i = 0; i <= 160; i++) {
        const sU = i / 160;
        const x = padLeft + sU * plotW;
        const y = yForCents(previousTakeCurveFn(sU));
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();
      ctx.setLineDash([]); // Reset dash
    }

    const isShowingGuru = isGuruPlaying || (phrase.guruCurveFn && showGuruOverlay);
    ctx.strokeStyle = isShowingGuru ? 'rgba(143, 166, 142, 0.4)' : '#8fa68e';
    ctx.lineWidth = 3.5;
    ctx.beginPath();
    const samples = 160;
    for (let i = 0; i <= samples; i++) {
      const sU = i / samples;
      const x = padLeft + sU * plotW;
      const y = yForCents(phrase.curveFn(sU));
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();"""

if ghost_inspector_anchor in content:
    content = content.replace(ghost_inspector_anchor, new_ghost_inspector, 1)
    print("Inspector ghost ribbon added successfully.")
else:
    print("Warning: ghost_inspector_anchor not found!")

# 6. Draw ghost overlay in renderLivePitchCanvas
ghost_live_anchor = """    // Draw Live Trajectory Stream
    const count = livePitchHistory.length;
    if (count > 1) {
      ctx.strokeStyle = '#8fa68e';
      ctx.lineWidth = 3.5;
      ctx.beginPath();
      let hasStarted = false;"""

new_ghost_live = """    // Draw Ghost Take ribbon if active
    if (isGhostActive && previousTakeLiveHistory && previousTakeLiveHistory.length > 1) {
      ctx.strokeStyle = 'rgba(164, 188, 163, 0.35)';
      ctx.lineWidth = 2.0;
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      let ghostStarted = false;
      const gCount = previousTakeLiveHistory.length;
      for (let i = 0; i < gCount; i++) {
        const gItem = previousTakeLiveHistory[i];
        const gx = padLeft + (i / (LIVE_HISTORY_LEN - 1)) * plotW;
        if (gItem && gItem.cents !== null) {
          const gy = yForCents(gItem.cents);
          if (!ghostStarted) {
            ctx.moveTo(gx, gy);
            ghostStarted = true;
          } else {
            ctx.lineTo(gx, gy);
          }
        } else {
          ghostStarted = false;
        }
      }
      ctx.stroke();
      ctx.setLineDash([]); // Reset dash
    }

    // Draw Live Trajectory Stream
    const count = livePitchHistory.length;
    if (count > 1) {
      ctx.strokeStyle = '#8fa68e';
      ctx.lineWidth = 3.5;
      ctx.beginPath();
      let hasStarted = false;"""

if ghost_live_anchor in content:
    content = content.replace(ghost_live_anchor, new_ghost_live, 1)
    print("Live ghost ribbon added successfully.")
else:
    print("Warning: ghost_live_anchor not found!")

# 7. Add Swara Dwell Engine, Tonic Calibration System, and Musician Feature Initializers
musician_subsystems = """  /* =========================================================
     8B. MUSICIAN-FIRST SUBSYSTEMS:
     - SWARA DWELL & VADI/SAMVADI TELEMETRY
     - MOVABLE SA CALIBRATION ("CALIBRATE MY SA")
     - AUDITION SPEED CONTROLLER
     - GHOST TAKE A/B COMPARISON
     - CONTEXT-AWARE TANPURA DRONE TUNING
     ========================================================= */

  const RAGA_VADI_REGISTRY = {
    'Yaman': { vadi: 'Ga', samvadi: 'Ni', vadiCents: 386.3, samvadiCents: 1088.3, mood: 'Nocturnal peace, devotion, Gambhirya' },
    'Bhairav': { vadi: 'Dha', samvadi: 'Re', vadiCents: 813.7, samvadiCents: 111.7, mood: 'Solemn dawn, ascetic stillness, Bhakti' },
    'Darbari': { vadi: 'Re', samvadi: 'Pa', vadiCents: 203.9, samvadiCents: 702.0, mood: 'Midnight majesty, deep resonance, Karuna' },
    'Darbari Kanada': { vadi: 'Re', samvadi: 'Pa', vadiCents: 203.9, samvadiCents: 702.0, mood: 'Midnight majesty, deep resonance, Karuna' },
    'Malkauns': { vadi: 'Ma', samvadi: 'Sa', vadiCents: 498.0, samvadiCents: 0.0, mood: 'Profound meditative introversion, midnight' },
    'Chandrakauns': { vadi: 'Ma', samvadi: 'Sa', vadiCents: 498.0, samvadiCents: 0.0, mood: 'Lunar mystical serenity, late night' },
    'Bageshree': { vadi: 'Ma', samvadi: 'Sa', vadiCents: 498.0, samvadiCents: 0.0, mood: 'Romantic longing, Viraha, late night' },
    'Bhupali': { vadi: 'Ga', samvadi: 'Dha', vadiCents: 386.3, samvadiCents: 905.9, mood: 'Uplifting celebration, early evening' },
    'Marwa': { vadi: 'Dha', samvadi: 'Re', vadiCents: 905.9, samvadiCents: 111.7, mood: 'Twilight tension, longing, Sandhiprakash' },
    'Puriya': { vadi: 'Ga', samvadi: 'Ni', vadiCents: 386.3, samvadiCents: 1088.3, mood: 'Sunset mystique, introspection' },
    'Sohini': { vadi: 'Dha', samvadi: 'Ga', vadiCents: 905.9, samvadiCents: 386.3, mood: 'Pre-dawn longing, utkantha' }
  };

  function renderSwaraDwellAnalysis(trajectory, ragaName) {
    const dwellBarsRow = document.getElementById('dwell-bars-row');
    const vadiBadge = document.getElementById('ui-vadi-badge');
    const critiqueText = document.getElementById('dwell-critique-text');
    if (!dwellBarsRow || !critiqueText) return;

    const rName = ragaName || (document.getElementById('ui-target-raga-select') ? document.getElementById('ui-target-raga-select').value : 'Yaman');
    const meta = RAGA_VADI_REGISTRY[rName] || { vadi: 'Ga', samvadi: 'Ni', vadiCents: 386.3, samvadiCents: 1088.3, mood: 'Devotional tranquility' };

    if (vadiBadge) {
      vadiBadge.textContent = 'Vadi: ' + meta.vadi + ' \u00b7 Samvadi: ' + meta.samvadi;
    }

    // Swara cent bounds
    const swaraBins = [
      { name: 'Sa', min: -80, max: 80, count: 0 },
      { name: 'Re', min: 80, max: 250, count: 0 },
      { name: 'Ga', min: 250, max: 440, count: 0 },
      { name: 'Ma', min: 440, max: 640, count: 0 },
      { name: 'Pa', min: 640, max: 760, count: 0 },
      { name: 'Dha', min: 760, max: 970, count: 0 },
      { name: 'Ni', min: 970, max: 1180, count: 0 }
    ];

    let totalPoints = 0;

    if (trajectory && trajectory.length > 0) {
      trajectory.forEach(function (pt) {
        if (pt.cents !== null && !isNaN(pt.cents)) {
          totalPoints++;
          // Wrap modulo 1200 for octave safety
          let modCents = ((pt.cents % 1200) + 1200) % 1200;
          if (modCents > 1140) modCents -= 1200;
          swaraBins.forEach(function (bin) {
            if (modCents >= bin.min && modCents < bin.max) {
              bin.count++;
            }
          });
        }
      });
    } else {
      // Sample phrase curveFn
      const phrase = PHRASE_LIBRARY[currentPhraseKey];
      if (phrase && phrase.curveFn) {
        totalPoints = 100;
        for (let i = 0; i <= 100; i++) {
          const c = phrase.curveFn(i / 100);
          let modC = ((c % 1200) + 1200) % 1200;
          if (modC > 1140) modC -= 1200;
          swaraBins.forEach(function (bin) {
            if (modC >= bin.min && modC < bin.max) {
              bin.count++;
            }
          });
        }
      }
    }

    dwellBarsRow.innerHTML = '';
    let vadiPct = 0;

    swaraBins.forEach(function (bin) {
      const pct = totalPoints > 0 ? Math.round((bin.count / totalPoints) * 100) : 0;
      const isVadi = (bin.name === meta.vadi);
      const isSamvadi = (bin.name === meta.samvadi);
      if (isVadi) vadiPct = pct;

      const col = document.createElement('div');
      col.className = 'dwell-bar-col';

      let labelText = bin.name;
      if (isVadi) labelText += ' *';
      else if (isSamvadi) labelText += ' \u2022';

      col.innerHTML =
        '<span class="dwell-swara-lbl' + (isVadi ? ' is-vadi' : (isSamvadi ? ' is-samvadi' : '')) + '">' + labelText + '</span>' +
        '<div class="dwell-bar-track">' +
          '<div class="dwell-bar-fill' + (isVadi ? ' is-vadi-fill' : '') + '" style="height: ' + Math.min(100, Math.max(4, pct)) + '%;"></div>' +
        '</div>' +
        '<span class="dwell-pct-lbl">' + pct + '%</span>';

      dwellBarsRow.appendChild(col);
    });

    if (vadiPct >= 18) {
      critiqueText.textContent =
        'Vadi ' + meta.vadi + ' honored with ' + vadiPct + '% dwell time, preserving authentic ' + rName + ' aesthetic (' + meta.mood + '). Nyasa balance is sound.';
    } else {
      critiqueText.textContent =
        'Raga ' + rName + ' requires greater dwell on Vadi ' + meta.vadi + ' (currently ' + vadiPct + '%) to establish its authentic mood (' + meta.mood + '). Practice sustaining ' + meta.vadi + ' against the drone.';
    }
  }

  // Auto-switch Tanpura tuning based on Pancham-varjya rules
  function handleRagaDroneAutoTune(ragaName) {
    let targetTuning = 'pa';
    const rLower = (ragaName || '').toLowerCase();
    if (rLower.includes('malkauns') || rLower.includes('chandrakauns') || rLower.includes('bageshree')) {
      targetTuning = 'ma';
    } else if (rLower.includes('marwa') || rLower.includes('puriya') || rLower.includes('sohini')) {
      targetTuning = 'ni';
    }

    setDroneTuning(targetTuning, true);
  }

  function setDroneTuning(tuning, isAuto) {
    currentDroneTuning = tuning;
    const pills = document.querySelectorAll('.ui-drone-pill');
    pills.forEach(function (p) {
      if (p.getAttribute('data-tuning') === tuning) {
        p.classList.add('is-active');
      } else {
        p.classList.remove('is-active');
      }
    });

    updateDroneButtonLabel();
    if (isDronePlaying) {
      updateActiveDroneFrequencies();
    }
  }

  // Tonic Calibration Subsystem ("Calibrate My Sa")
  function initTonicCalibration() {
    const modal = document.getElementById('calibrate-sa-modal');
    const openBtn = document.getElementById('calibrate-sa-btn');
    const closeBtn = document.getElementById('btn-calib-modal-close');
    const cancelBtn = document.getElementById('btn-calib-cancel');
    const applyBtn = document.getElementById('btn-calib-apply');
    const listenBtn = document.getElementById('btn-calib-listen');
    const slider = document.getElementById('calib-fine-slider');
    const sliderVal = document.getElementById('calib-slider-val');
    const pitchDisplay = document.getElementById('calib-pitch-display');
    const statusBadge = document.getElementById('calib-status-badge');
    const meterFill = document.getElementById('calib-meter-fill');
    const detectedHz = document.getElementById('calib-detected-hz');
    const presetBtns = document.querySelectorAll('.calib-preset-btn');

    function openModal() {
      if (!modal) return;
      modal.classList.remove('is-hidden');
      const currentSa = userCustomSaHz || (PHRASE_LIBRARY[currentPhraseKey] && PHRASE_LIBRARY[currentPhraseKey].saHz) || 146.83;
      if (slider) slider.value = currentSa.toFixed(1);
      if (sliderVal) sliderVal.textContent = currentSa.toFixed(1) + ' Hz';
      if (pitchDisplay) pitchDisplay.textContent = currentSa.toFixed(1) + ' Hz';
      if (statusBadge) statusBadge.textContent = 'Ready to Calibrate';
      if (meterFill) meterFill.style.width = '0%';
    }

    function closeModal() {
      if (!modal) return;
      modal.classList.add('is-hidden');
      stopCalibMic();
    }

    if (openBtn) openBtn.addEventListener('click', openModal);
    if (closeBtn) closeBtn.addEventListener('click', closeModal);
    if (cancelBtn) cancelBtn.addEventListener('click', closeModal);

    // Preset buttons
    presetBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        presetBtns.forEach(function (b) { b.classList.remove('is-active'); });
        btn.classList.add('is-active');
        const hz = parseFloat(btn.getAttribute('data-hz') || '146.83');
        const note = btn.getAttribute('data-note') || '';
        if (slider) slider.value = hz.toFixed(1);
        if (sliderVal) sliderVal.textContent = hz.toFixed(1) + ' Hz';
        if (pitchDisplay) pitchDisplay.textContent = hz.toFixed(1) + ' Hz (' + note + ')';
        if (statusBadge) statusBadge.textContent = 'Preset Selected: ' + note;
        if (meterFill) meterFill.style.width = '60%';
      });
    });

    // Slider
    if (slider) {
      slider.addEventListener('input', function () {
        presetBtns.forEach(function (b) { b.classList.remove('is-active'); });
        const hz = parseFloat(slider.value);
        if (sliderVal) sliderVal.textContent = hz.toFixed(1) + ' Hz';
        if (pitchDisplay) pitchDisplay.textContent = hz.toFixed(1) + ' Hz';
        if (statusBadge) statusBadge.textContent = 'Custom Sa Adjusted';
      });
    }

    // Live Mic Pitch Calibration Loop
    function startCalibMic() {
      if (isCalibratingMic) {
        stopCalibMic();
        return;
      }

      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert('Microphone access is not supported in this browser.');
        return;
      }

      ensureAudioContext();
      if (!audioCtx) return;

      navigator.mediaDevices.getUserMedia({ audio: { echoCancellation: false, noiseSuppression: false, autoGainControl: false } })
        .then(function (stream) {
          calibAudioStream = stream;
          isCalibratingMic = true;
          if (listenBtn) listenBtn.textContent = 'Stop Listening';
          if (statusBadge) statusBadge.textContent = 'Sing "Saaa" steadily into mic...';

          const source = audioCtx.createMediaStreamSource(stream);
          const analyser = audioCtx.createAnalyser();
          analyser.fftSize = 2048;
          source.connect(analyser);

          const buf = new Float32Array(analyser.fftSize);
          calibPitchBuffer = [];

          function checkMicPitch() {
            if (!isCalibratingMic) return;
            analyser.getFloatTimeDomainData(buf);

            // Simple fast autocorrelation for calibration
            let bestOffset = -1;
            let bestCorrelation = 0;
            let rms = 0;
            for (let i = 0; i < buf.length; i++) {
              rms += buf[i] * buf[i];
            }
            rms = Math.sqrt(rms / buf.length);

            if (rms > 0.015) {
              const minPeriod = Math.floor(audioCtx.sampleRate / 400); // Max 400 Hz
              const maxPeriod = Math.floor(audioCtx.sampleRate / 90);  // Min 90 Hz
              for (let offset = minPeriod; offset < maxPeriod; offset++) {
                let corr = 0;
                for (let i = 0; i < buf.length - offset; i++) {
                  corr += buf[i] * buf[i + offset];
                }
                if (corr > bestCorrelation) {
                  bestCorrelation = corr;
                  bestOffset = offset;
                }
              }

              if (bestOffset > 0) {
                const detectedPitch = audioCtx.sampleRate / bestOffset;
                if (detectedPitch >= 95 && detectedPitch <= 380) {
                  calibPitchBuffer.push(detectedPitch);
                  if (calibPitchBuffer.length > 25) calibPitchBuffer.shift();

                  if (calibPitchBuffer.length >= 8) {
                    const avgHz = calibPitchBuffer.reduce(function (a, b) { return a + b; }, 0) / calibPitchBuffer.length;
                    const diffs = calibPitchBuffer.map(function (h) { return Math.abs(h - avgHz); });
                    const maxDiff = Math.max.apply(null, diffs);

                    if (pitchDisplay) pitchDisplay.textContent = avgHz.toFixed(1) + ' Hz';
                    if (slider) slider.value = avgHz.toFixed(1);
                    if (sliderVal) sliderVal.textContent = avgHz.toFixed(1) + ' Hz';

                    if (maxDiff < 3.0) {
                      if (meterFill) meterFill.style.width = '100%';
                      if (statusBadge) {
                        statusBadge.textContent = 'Rock Steady Sa Locked (' + avgHz.toFixed(1) + ' Hz)';
                        statusBadge.className = 'calib-status-badge is-locked';
                      }
                    } else {
                      const fillPct = Math.max(10, Math.min(85, Math.round((1 - maxDiff / 15) * 100)));
                      if (meterFill) meterFill.style.width = fillPct + '%';
                      if (statusBadge) statusBadge.textContent = 'Voice detected... hold steady';
                    }
                  }
                }
              }
            } else {
              if (statusBadge) statusBadge.textContent = 'Sing "Saaa" steadily...';
            }

            requestAnimationFrame(checkMicPitch);
          }

          requestAnimationFrame(checkMicPitch);
        })
        .catch(function (err) {
          if (statusBadge) statusBadge.textContent = 'Microphone permission denied';
        });
    }

    function stopCalibMic() {
      isCalibratingMic = false;
      if (listenBtn) listenBtn.textContent = 'Start Mic Calibration';
      if (calibAudioStream) {
        calibAudioStream.getTracks().forEach(function (track) { track.stop(); });
        calibAudioStream = null;
      }
    }

    if (listenBtn) listenBtn.addEventListener('click', startCalibMic);

    // Apply button
    if (applyBtn) {
      applyBtn.addEventListener('click', function () {
        const hz = parseFloat(slider ? slider.value : '146.83') || 146.83;
        userCustomSaHz = hz;

        // Update all library phrases
        Object.keys(PHRASE_LIBRARY).forEach(function (key) {
          PHRASE_LIBRARY[key].saHz = hz;
        });

        // Update active drone
        updateDroneButtonLabel();
        if (isDronePlaying) {
          updateActiveDroneFrequencies();
        }

        // Update telemetry and button label
        const telTarget = document.getElementById('ui-tel-target');
        if (telTarget) telTarget.textContent = 'Sa = ' + hz.toFixed(1) + ' Hz';

        if (openBtn) {
          openBtn.textContent = 'Sa: ' + hz.toFixed(1) + ' Hz';
          openBtn.classList.add('is-calibrated');
        }

        closeModal();

        // Re-render
        if (isLiveMicActive) {
          renderLivePitchCanvas();
        } else {
          renderPhraseInspector();
        }
      });
    }
  }

  // Audition Speed & Ghost Take Initializer
  function initMusicianControls() {
    // 1. Drone tuning pills
    const dronePills = document.querySelectorAll('.ui-drone-pill');
    dronePills.forEach(function (pill) {
      pill.addEventListener('click', function () {
        const tuning = pill.getAttribute('data-tuning') || 'pa';
        setDroneTuning(tuning, false);
      });
    });

    // 2. Playback speed buttons
    const speedBtns = document.querySelectorAll('.ui-speed-btn');
    speedBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        speedBtns.forEach(function (b) { b.classList.remove('is-active'); });
        btn.classList.add('is-active');
        currentAuditionSpeed = parseFloat(btn.getAttribute('data-speed') || '1.0');
        if (activeAuditionSource && activeAuditionSource.playbackRate) {
          activeAuditionSource.playbackRate.value = currentAuditionSpeed;
        }
      });
    });

    // 3. Ghost Take A/B Comparison button
    const ghostBtn = document.getElementById('toggle-ghost-btn');
    if (ghostBtn) {
      ghostBtn.addEventListener('click', function () {
        isGhostActive = !isGhostActive;
        if (isGhostActive) {
          ghostBtn.classList.add('is-active');
          ghostBtn.textContent = 'Hide Ghost';
          if (!previousTakeCurveFn && PHRASE_LIBRARY[currentPhraseKey]) {
            previousTakeCurveFn = PHRASE_LIBRARY[currentPhraseKey].curveFn;
          }
        } else {
          ghostBtn.classList.remove('is-active');
          ghostBtn.textContent = 'Compare Take';
        }
        if (isLiveMicActive) {
          renderLivePitchCanvas();
        } else {
          renderPhraseInspector();
        }
      });
    }

    // 4. Target Raga change handler (auto-switch drone and update dwell)
    const ragaSelect = document.getElementById('ui-target-raga-select');
    if (ragaSelect) {
      ragaSelect.addEventListener('change', function () {
        handleRagaDroneAutoTune(ragaSelect.value);
        renderSwaraDwellAnalysis(null, ragaSelect.value);
      });
    }

    // Initial dwell render
    renderSwaraDwellAnalysis(null, 'Yaman');
  }"""

# Insert musician_subsystems before DOMContentLoaded
dom_anchor = "  document.addEventListener('DOMContentLoaded', function () {"
new_dom_content = musician_subsystems + "\n\n" + dom_anchor

if dom_anchor in content:
    content = content.replace(dom_anchor, new_dom_content, 1)
    print("Musician subsystems added before DOMContentLoaded.")
else:
    print("Warning: dom_anchor not found!")

# Add initializers to DOMContentLoaded
old_dom_inits = """    initWorkspaceModes();
    initTutorialSystem();
    initShowcaseTabs();
    initAccordion();"""

new_dom_inits = """    initWorkspaceModes();
    initTutorialSystem();
    initTonicCalibration();
    initMusicianControls();
    initShowcaseTabs();
    initAccordion();"""

if old_dom_inits in content:
    content = content.replace(old_dom_inits, new_dom_inits, 1)
    print("DOM inits updated successfully.")
else:
    print("Warning: old_dom_inits not found!")

with open("app.js", "w", encoding="utf-8") as f:
    f.write(content)

print("app.js updated successfully with all 6 musician features!")

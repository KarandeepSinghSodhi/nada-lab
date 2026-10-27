# -*- coding: utf-8 -*-
"""
Script to integrate the Real-Time Rasa & Emotion Radar into app.js
"""

with open("app.js", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add Rasa Radar state variables
old_universal_vars = """  let lastPercussionHitTime = 0;
  let percussionHitCount = 0;
  let percussionLiveBpm = 0;
  let lastPercussionRms = 0;
  let currentGuitarTuningMode = 'standard';
  let currentPercussionKit = 'tabla';"""

new_universal_vars = """  let lastPercussionHitTime = 0;
  let percussionHitCount = 0;
  let percussionLiveBpm = 0;
  let lastPercussionRms = 0;
  let currentGuitarTuningMode = 'standard';
  let currentPercussionKit = 'tabla';

  // Real-Time Rasa & Emotion Radar State (Valence-Arousal Space)
  let currentValence = 0.65;
  let currentArousal = -0.35;
  const rasaTrailHistory = [];
  const MAX_RASA_TRAIL = 24;"""

if old_universal_vars in content:
    content = content.replace(old_universal_vars, new_universal_vars, 1)
    print("Rasa radar state variables added.")
else:
    print("Warning: old_universal_vars not found!")

# 2. Add Rasa Radar engine before DOMContentLoaded
rasa_engine_code = """  /* =========================================================
     8D. REAL-TIME RASA & EMOTION RADAR ENGINE (VALENCE-AROUSAL)
     Based on Mathur et al. (2015), Chordia & Rae (2009),
     and Bharata Muni Natyashastra Svara-Rasa Theory
     ========================================================= */

  function computeAffectiveCoordinates(cents, velocity, rms, freq) {
    if (cents === null || isNaN(cents)) {
      currentArousal = currentArousal * 0.95 - 0.02;
      return;
    }

    const modC = ((cents % 1200) + 1200) % 1200;
    let targetValence = 0.5; // Sa / Pa baseline

    // Shruti Consonance & Rasa Potential Function
    if (modC >= 365 && modC <= 410) {
      targetValence = 0.85; // Shuddha Ga (5/4) -> Shanta / Shringara
    } else if (modC >= 885 && modC <= 930) {
      targetValence = 0.78; // Shuddha Dha (5/3) -> Luminous joy
    } else if (modC >= 1065 && modC <= 1115) {
      targetValence = 0.72; // Shuddha Ni (15/8) -> Yearning for union
    } else if (modC >= 180 && modC <= 225) {
      targetValence = 0.45; // Shuddha Re (9/8) -> Balance
    } else if (modC >= 480 && modC <= 520) {
      targetValence = 0.25; // Shuddha Ma (4/3) -> Deep contemplation
    } else if (modC >= 290 && modC <= 335) {
      targetValence = -0.55; // Komal Ga (6/5) -> Melancholy / Viraha
    } else if (modC >= 90 && modC <= 135) {
      targetValence = -0.75; // Komal Re (16/15) -> Karuna / Dawn stillness
    } else if (modC >= 790 && modC <= 835) {
      targetValence = -0.68; // Komal Dha (8/5) -> Pathos
    } else if (modC >= 575 && modC <= 615) {
      targetValence = -0.60; // Tivra Ma (45/32) -> Twilight tension
    }

    // Arousal from Kinematics, Register, and RMS energy
    const normVel = Math.min(1.0, Math.abs(velocity || 0) / 600);
    const normReg = Math.max(0, Math.min(1.0, (cents - 0) / 1200));
    const normRms = Math.min(1.0, (rms || 0.05) * 5);
    const targetArousal = Math.max(-1.0, Math.min(1.0, (normVel * 0.45 + normReg * 0.30 + normRms * 0.25) * 2.0 - 0.7));

    // Smooth exponential smoothing
    currentValence = currentValence * 0.82 + targetValence * 0.18;
    currentArousal = currentArousal * 0.82 + targetArousal * 0.18;

    rasaTrailHistory.push({ v: currentValence, a: currentArousal, t: performance.now() });
    if (rasaTrailHistory.length > MAX_RASA_TRAIL) {
      rasaTrailHistory.shift();
    }
  }

  function getActiveRasaLabel(v, a) {
    if (v >= 0.15) {
      return a <= 0.05 ? 'Shanta (Peace)' : 'Veera / Shringara (Heroic Joy)';
    } else if (v <= -0.15) {
      return a <= 0.05 ? 'Karuna (Pathos / Sorrow)' : 'Raudra (Intensity / Tension)';
    } else {
      return a <= 0.05 ? 'Sādhanā (Stillness)' : 'Adbhuta (Wonder)';
    }
  }

  function renderRasaRadarCanvas() {
    const canvas = document.getElementById('rasa-radar-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const w = canvas.width;
    const h = canvas.height;
    const cx = w / 2;
    const cy = h / 2;
    const padX = 22;
    const padY = 16;
    const radiusX = cx - padX;
    const radiusY = cy - padY;

    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = '#0e0e0e';
    ctx.fillRect(0, 0, w, h);

    // Concentric range ellipses
    ctx.strokeStyle = 'rgba(241, 241, 239, 0.06)';
    ctx.lineWidth = 1;
    [0.35, 0.70, 1.0].forEach(function (scale) {
      ctx.beginPath();
      ctx.ellipse(cx, cy, radiusX * scale, radiusY * scale, 0, 0, Math.PI * 2);
      ctx.stroke();
    });

    // Crosshairs
    ctx.strokeStyle = 'rgba(143, 166, 142, 0.22)';
    ctx.beginPath();
    ctx.moveTo(cx, padY);
    ctx.lineTo(cx, h - padY);
    ctx.moveTo(padX, cy);
    ctx.lineTo(w - padX, cy);
    ctx.stroke();

    // Quadrant Rasa Labels
    ctx.font = '500 13px Clash Grotesk, sans-serif';

    // Top-Right: VEERA / SHRINGARA
    ctx.fillStyle = 'rgba(164, 188, 163, 0.75)';
    ctx.textAlign = 'right';
    ctx.fillText('VEERA / JOY', w - padX - 6, padY + 14);

    // Top-Left: RAUDRA / TENSION
    ctx.fillStyle = 'rgba(224, 159, 103, 0.75)';
    ctx.textAlign = 'left';
    ctx.fillText('RAUDRA / TENSION', padX + 6, padY + 14);

    // Bottom-Left: KARUNA (PATHOS)
    ctx.fillStyle = 'rgba(143, 169, 196, 0.75)';
    ctx.textAlign = 'left';
    ctx.fillText('KARUNA (PATHOS)', padX + 6, h - padY - 6);

    // Bottom-Right: SHANTA (PEACE)
    ctx.fillStyle = 'rgba(143, 166, 142, 0.85)';
    ctx.textAlign = 'right';
    ctx.fillText('SHANTA (PEACE)', w - padX - 6, h - padY - 6);

    // Draw fading motion trail
    if (rasaTrailHistory.length > 1) {
      ctx.lineWidth = 1.8;
      for (let i = 1; i < rasaTrailHistory.length; i++) {
        const p0 = rasaTrailHistory[i - 1];
        const p1 = rasaTrailHistory[i];
        const alpha = (i / rasaTrailHistory.length) * 0.45;
        ctx.strokeStyle = 'rgba(143, 166, 142, ' + alpha + ')';
        ctx.beginPath();
        const x0 = cx + p0.v * radiusX;
        const y0 = cy - p0.a * radiusY;
        const x1 = cx + p1.v * radiusX;
        const y1 = cy - p1.a * radiusY;
        ctx.moveTo(x0, y0);
        ctx.lineTo(x1, y1);
        ctx.stroke();
      }
    }

    // Current Affective Position
    const curX = cx + currentValence * radiusX;
    const curY = cy - currentArousal * radiusY;

    // Glowing halo
    const haloGrad = ctx.createRadialGradient(curX, curY, 2, curX, curY, 14);
    haloGrad.addColorStop(0, 'rgba(164, 188, 163, 0.8)');
    haloGrad.addColorStop(0.5, 'rgba(143, 166, 142, 0.3)');
    haloGrad.addColorStop(1, 'rgba(143, 166, 142, 0)');
    ctx.fillStyle = haloGrad;
    ctx.beginPath();
    ctx.arc(curX, curY, 14, 0, Math.PI * 2);
    ctx.fill();

    // Central particle
    ctx.fillStyle = '#a4bca3';
    ctx.beginPath();
    ctx.arc(curX, curY, 4.5, 0, Math.PI * 2);
    ctx.fill();

    // Update text readouts
    const badgeEl = document.getElementById('live-rasa-badge');
    const valEl = document.getElementById('rasa-valence-val');
    const aroEl = document.getElementById('rasa-arousal-val');

    const activeRasa = getActiveRasaLabel(currentValence, currentArousal);
    if (badgeEl) badgeEl.textContent = 'Active Rasa: ' + activeRasa;
    if (valEl) {
      const vDesc = currentValence >= 0.15 ? 'Serene / Positive' : (currentValence <= -0.15 ? 'Pathos / Tension' : 'Neutral');
      valEl.textContent = 'Valence: ' + (currentValence >= 0 ? '+' : '') + currentValence.toFixed(2) + ' (' + vDesc + ')';
    }
    if (aroEl) {
      const aDesc = currentArousal >= 0.10 ? 'Dynamic' : 'Contemplative';
      aroEl.textContent = 'Arousal: ' + (currentArousal >= 0 ? '+' : '') + currentArousal.toFixed(2) + ' (' + aDesc + ')';
    }
  }
"""

# Insert rasa_engine_code right before DOMContentLoaded
dom_anchor = "  document.addEventListener('DOMContentLoaded', function () {"
if dom_anchor in content:
    content = content.replace(dom_anchor, rasa_engine_code + "\n\n" + dom_anchor, 1)
    print("Rasa engine code added before DOMContentLoaded.")
else:
    print("Warning: dom_anchor not found!")

# Call computeAffectiveCoordinates and renderRasaRadarCanvas in handleIncomingPitchFrame
pitch_frame_anchor = "    detectLiveOrnamentAndDiagnostics(cents, saHz);\n    updateLiveNoteTracker(data.pitch, cents, saHz, data.rms || 0);\n    renderLivePitchCanvas();"
new_pitch_frame_call = """    detectLiveOrnamentAndDiagnostics(cents, saHz);
    updateLiveNoteTracker(data.pitch, cents, saHz, data.rms || 0);
    const curVel = liveVelocityHistory.length ? liveVelocityHistory[liveVelocityHistory.length - 1].vel : 0;
    computeAffectiveCoordinates(cents, curVel, data.rms || 0.05, data.pitch);
    renderRasaRadarCanvas();
    renderLivePitchCanvas();"""

if pitch_frame_anchor in content:
    content = content.replace(pitch_frame_anchor, new_pitch_frame_call, 1)
    print("handleIncomingPitchFrame updated with Rasa radar rendering.")
else:
    print("Warning: pitch_frame_anchor not found!")

# Call computeAffectiveCoordinates and renderRasaRadarCanvas in renderPhraseInspector
inspector_anchor = "    const estHz = effectiveSa * Math.pow(2, cNow / 1200);\n    updateLiveNoteTracker(estHz, cNow, effectiveSa, 0.08);"
new_inspector_call = """    const estHz = effectiveSa * Math.pow(2, cNow / 1200);\n    updateLiveNoteTracker(estHz, cNow, effectiveSa, 0.08);
    computeAffectiveCoordinates(cNow, velNow, 0.08, estHz);
    renderRasaRadarCanvas();"""

if inspector_anchor in content:
    content = content.replace(inspector_anchor, new_inspector_call, 1)
    print("renderPhraseInspector updated with Rasa radar rendering.")
else:
    print("Warning: inspector_anchor not found!")

# Call renderRasaRadarCanvas on initial load in DOMContentLoaded
init_anchor = "    initInstrumentProfiles();"
if init_anchor in content:
    content = content.replace(init_anchor, init_anchor + "\n    renderRasaRadarCanvas();", 1)
    print("renderRasaRadarCanvas added to initial DOMContentLoaded.")
else:
    print("Warning: init_anchor not found!")

with open("app.js", "w", encoding="utf-8") as f:
    f.write(content)

print("app.js successfully updated with Real-Time Rasa & Emotion Radar!")

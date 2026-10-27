import re

# 1. Patch styles.css
with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Replace .ui-pane-bar
old_pane_bar = """.ui-pane-bar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  font-size: 15px;
}"""

new_pane_bar = """.ui-pane-bar {
  display: flex;
  flex-wrap: nowrap;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  font-size: 14px;
  min-height: 38px;
  height: 38px;
  overflow: hidden;
  box-sizing: border-box;
}"""

if old_pane_bar in css:
    css = css.replace(old_pane_bar, new_pane_bar)
    print("Replaced .ui-pane-bar in styles.css")
else:
    print("WARNING: old_pane_bar not found in styles.css")

# Replace .ui-readout
old_readout = """.ui-readout {
  color: var(--accent);
  font-weight: 500;
  font-variant-numeric: tabular-nums;
}"""

new_readout = """.ui-badge {
  font-weight: 500;
  color: var(--concrete);
  white-space: nowrap;
  flex-shrink: 0;
}

.ui-sthirata-pill {
  white-space: nowrap;
  flex-shrink: 0;
}

.ui-readout {
  color: var(--accent);
  font-weight: 500;
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  text-align: right;
  flex-shrink: 1;
  min-width: 0;
}"""

if old_readout in css:
    css = css.replace(old_readout, new_readout)
    print("Replaced .ui-readout in styles.css")
else:
    print("WARNING: old_readout not found in styles.css")

# Replace .ui-diagnostic-pane
old_diag_pane = """.ui-diagnostic-pane {
  grid-column: 8 / 13;
  background-color: #1b1b1b;
  padding: 18px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 12px;
}"""

new_diag_pane = """.ui-diagnostic-pane {
  grid-column: 8 / 13;
  background-color: #1b1b1b;
  padding: 18px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 12px;
  min-height: 520px;
  box-sizing: border-box;
  overflow-anchor: none;
}"""

if old_diag_pane in css:
    css = css.replace(old_diag_pane, new_diag_pane)
    print("Replaced .ui-diagnostic-pane in styles.css")
else:
    print("WARNING: old_diag_pane not found in styles.css")

# Replace .ui-diag-title, .ui-diag-copy, .ui-drill-box, .ui-drill-body
old_diag_details = """.ui-diag-title {
  font-weight: 500;
  font-size: 28px;
  line-height: 1.1;
  letter-spacing: -0.01em;
  color: var(--ink);
}

.ui-diag-copy {
  font-size: 15px;
  line-height: 1.4;
  max-width: 52ch;
  color: var(--muted);
}

.ui-drill-box {
  background-color: #232723;
  padding: 14px;
}

.ui-drill-heading {
  font-weight: 500;
  font-size: 15px;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 4px;
}

.ui-drill-body {
  font-size: 15px;
  line-height: 1.35;
  max-width: 52ch;
  color: #e2ede1;
}"""

new_diag_details = """.ui-diag-title {
  font-weight: 500;
  font-size: 28px;
  line-height: 1.1;
  letter-spacing: -0.01em;
  color: var(--ink);
  min-height: 32px;
}

.ui-diag-copy {
  font-size: 15px;
  line-height: 1.4;
  max-width: 52ch;
  color: var(--muted);
  min-height: 66px;
  box-sizing: border-box;
}

.ui-drill-box {
  background-color: #232723;
  padding: 14px;
  min-height: 130px;
  box-sizing: border-box;
}

.ui-drill-heading {
  font-weight: 500;
  font-size: 15px;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 4px;
}

.ui-drill-body {
  font-size: 15px;
  line-height: 1.35;
  max-width: 52ch;
  color: #e2ede1;
  min-height: 60px;
  box-sizing: border-box;
}"""

if old_diag_details in css:
    css = css.replace(old_diag_details, new_diag_details)
    print("Replaced .ui-diag-details in styles.css")
else:
    print("WARNING: old_diag_details not found in styles.css")

# Patch tracker-wave-musician-strip
old_wave_strip = """[data-ui="wave-container"] .tracker-wave-musician-strip {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  flex-wrap: wrap;
  padding-top: 4px;
}

[data-ui="wave-container"] .wave-musician-pill {
  font-size: 11px;
  font-weight: 500;
  font-variant-numeric: tabular-nums;
  color: var(--muted);
  letter-spacing: 0.02em;
}"""

new_wave_strip = """[data-ui="wave-container"] .tracker-wave-musician-strip {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  flex-wrap: nowrap;
  overflow: hidden;
  min-height: 22px;
  height: 22px;
  padding-top: 4px;
  box-sizing: border-box;
}

[data-ui="wave-container"] .wave-musician-pill {
  font-size: 11px;
  font-weight: 500;
  font-variant-numeric: tabular-nums;
  color: var(--muted);
  letter-spacing: 0.02em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex-shrink: 1;
  min-width: 0;
}"""

if old_wave_strip in css:
    css = css.replace(old_wave_strip, new_wave_strip)
    print("Replaced tracker-wave-musician-strip in styles.css")
else:
    print("WARNING: old_wave_strip not found in styles.css")

# Add global scroll-anchoring prevention at the end of styles.css
scroll_anchoring_css = """

/* Prevent Chromium Scroll-Anchoring Jitter during Real-Time Audio Streaming */
html, body,
.inspector-workbench,
.ui-canvas-grid,
.ui-canvas-pane,
.ui-diagnostic-pane,
.ui-live-tracker,
.ui-pane-bar {
  overflow-anchor: none;
}
"""
if "/* Prevent Chromium Scroll-Anchoring Jitter" not in css:
    css += scroll_anchoring_css
    print("Added scroll anchoring prevention to styles.css")

with open('styles.css', 'w', encoding='utf-8') as f:
    f.write(css)
print("Updated styles.css successfully.")


# 2. Patch app.js
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Remove initCircadianEngine(); from handleIncomingPitchFrame
old_mic_loop = """    computeAffectiveCoordinates(cents, curVel, data.rms || 0.05, data.pitch);
    renderRasaRadarCanvas();
    initCircadianEngine();
    renderLivePitchCanvas();"""

new_mic_loop = """    computeAffectiveCoordinates(cents, curVel, data.rms || 0.05, data.pitch);
    renderRasaRadarCanvas();
    renderLivePitchCanvas();"""

if old_mic_loop in js:
    js = js.replace(old_mic_loop, new_mic_loop)
    print("Removed initCircadianEngine from handleIncomingPitchFrame in app.js")
else:
    print("WARNING: old_mic_loop not found in app.js")

# Add state latch to detectLiveOrnamentAndDiagnostics
old_detect_fn = """  function detectLiveOrnamentAndDiagnostics(latestCents, saHz) {
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
    const sthirataEl = document.getElementById('ui-sthirata-pill');"""

new_detect_fn = """  let lastDetectedLiveOrnamentState = '';

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
    const sthirataEl = document.getElementById('ui-sthirata-pill');"""

if old_detect_fn in js:
    js = js.replace(old_detect_fn, new_detect_fn)
    print("Added lastDetectedLiveOrnamentState to app.js")
else:
    print("WARNING: old_detect_fn not found in app.js")

# In detectLiveOrnamentAndDiagnostics, update paragraphs only on state changes
old_meend_block = """    // 1. Check for Meend Glide (150 to 1800 c/s)
    let detectedOrnament = 'Steady Svara Sustain';
    if (absVel >= 180 && absVel <= 1800) {
      detectedOrnament = 'Detected: Meend Glide (' + Math.round(absVel) + ' c/s)';
      if (ornamentEl) ornamentEl.textContent = detectedOrnament;
      if (tierNameEl) tierNameEl.textContent = 'TIER 2 · ORNAMENT INTEGRITY';
      if (scoreValEl) scoreValEl.textContent = 'Live Active';
      if (headlineEl) headlineEl.textContent = 'Continuous Meend Transition';
      if (detailEl) detailEl.textContent = 'Voice is gliding smoothly across shruti horizontals without staircase stepping.';
      if (drillEl) drillEl.textContent = 'Decelerate slightly as you arrive on the target swara to land with centered resonance.';
    }
    // 2. Check for Andolan / Vibrato Oscillation
    else if (livePitchHistory.length >= 30) {
      const recentVoiced = livePitchHistory.slice(-30).filter(function (p) { return p.cents !== null; });
      if (recentVoiced.length > 20) {
        let maxC = -9999, minC = 9999;
        recentVoiced.forEach(function (p) {
          if (p.cents > maxC) maxC = p.cents;
          if (p.cents < minC) minC = p.cents;
        });
        const swing = maxC - minC;
        if (swing >= 24 && swing <= 85) {
          detectedOrnament = 'Detected: Andolan (Oscillation ±' + Math.round(swing / 2) + 'c)';
          if (ornamentEl) ornamentEl.textContent = detectedOrnament;
          if (tierNameEl) tierNameEl.textContent = 'TIER 2 · ORNAMENT INTEGRITY';
          if (headlineEl) headlineEl.textContent = 'Deliberate Microtonal Andolan';
          if (detailEl) detailEl.textContent = 'Oscillation measured around target shruti with authentic classical swing amplitude.';
        } else {
          if (ornamentEl) ornamentEl.textContent = 'Sustained Swara';
        }
      }
    } else {
      if (ornamentEl) ornamentEl.textContent = 'Sustained Swara';
    }"""

new_meend_block = """    // 1. Check for Meend Glide (150 to 1800 c/s)
    let detectedOrnament = 'Steady Svara Sustain';
    let currentOrnamentState = 'sustained';
    if (absVel >= 180 && absVel <= 1800) {
      currentOrnamentState = 'meend';
      detectedOrnament = 'Detected: Meend Glide (' + Math.round(absVel) + ' c/s)';
      if (ornamentEl) ornamentEl.textContent = detectedOrnament;
      if (tierNameEl) tierNameEl.textContent = 'TIER 2 · ORNAMENT INTEGRITY';
      if (scoreValEl) scoreValEl.textContent = 'Live Active';
      if (lastDetectedLiveOrnamentState !== 'meend') {
        lastDetectedLiveOrnamentState = 'meend';
        if (headlineEl) headlineEl.textContent = 'Continuous Meend Transition';
        if (detailEl) detailEl.textContent = 'Voice is gliding smoothly across shruti horizontals without staircase stepping.';
        if (drillEl) drillEl.textContent = 'Decelerate slightly as you arrive on the target swara to land with centered resonance.';
      }
    }
    // 2. Check for Andolan / Vibrato Oscillation
    else if (livePitchHistory.length >= 30) {
      const recentVoiced = livePitchHistory.slice(-30).filter(function (p) { return p.cents !== null; });
      if (recentVoiced.length > 20) {
        let maxC = -9999, minC = 9999;
        recentVoiced.forEach(function (p) {
          if (p.cents > maxC) maxC = p.cents;
          if (p.cents < minC) minC = p.cents;
        });
        const swing = maxC - minC;
        if (swing >= 24 && swing <= 85) {
          currentOrnamentState = 'andolan';
          detectedOrnament = 'Detected: Andolan (Oscillation ±' + Math.round(swing / 2) + 'c)';
          if (ornamentEl) ornamentEl.textContent = detectedOrnament;
          if (tierNameEl) tierNameEl.textContent = 'TIER 2 · ORNAMENT INTEGRITY';
          if (lastDetectedLiveOrnamentState !== 'andolan') {
            lastDetectedLiveOrnamentState = 'andolan';
            if (headlineEl) headlineEl.textContent = 'Deliberate Microtonal Andolan';
            if (detailEl) detailEl.textContent = 'Oscillation measured around target shruti with authentic classical swing amplitude.';
          }
        } else {
          if (ornamentEl) ornamentEl.textContent = 'Sustained Swara';
        }
      }
    } else {
      if (ornamentEl) ornamentEl.textContent = 'Sustained Swara';
    }"""

if old_meend_block in js:
    js = js.replace(old_meend_block, new_meend_block)
    print("Stabilized ornament diagnostics updates in app.js")
else:
    print("WARNING: old_meend_block not found in app.js")

# In initCircadianEngine, replace addEventListener with onclick to avoid listener leaks
old_circ_listener = """    if (syncBtn) {
      syncBtn.addEventListener('click', function () {"""

new_circ_listener = """    if (syncBtn) {
      syncBtn.onclick = function () {"""

if old_circ_listener in js:
    js = js.replace(old_circ_listener, new_circ_listener)
    print("Replaced syncBtn addEventListener with onclick in app.js")
else:
    print("WARNING: old_circ_listener not found in app.js")

# Add initCircadianEngine to DOMContentLoaded
old_dom_content = """    renderPhraseInspector();
    initScrollChoreography();"""

new_dom_content = """    renderPhraseInspector();
    initScrollChoreography();
    initCircadianEngine();
    setInterval(initCircadianEngine, 15 * 60 * 1000);"""

if old_dom_content in js:
    js = js.replace(old_dom_content, new_dom_content)
    print("Added initCircadianEngine to DOMContentLoaded in app.js")
else:
    print("WARNING: old_dom_content not found in app.js")

# Expose window.handleIncomingPitchFrame
if "window.handleIncomingPitchFrame =" not in js:
    old_end = "})();"
    new_end = """  window.handleIncomingPitchFrame = handleIncomingPitchFrame;
})();"""
    js = js.replace(old_end, new_end)
    print("Exposed window.handleIncomingPitchFrame in app.js")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Updated app.js successfully.")

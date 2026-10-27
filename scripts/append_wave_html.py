# -*- coding: utf-8 -*-
"""
Script to add the Live Note & Flute Tracker HUD and Acoustic Sound Wave into index.html
"""

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

target_anchor = """              <canvas id="shruti-canvas" width="920" height="280" aria-label="Continuous pitch trajectory C(t) and velocity derivative dC/dt plotted across rational shruti horizontals"></canvas>"""

hud_html = """              <!-- Real-Time Note, Flute & Acoustic Wave Tracker HUD -->
              <div class="ui-live-tracker" id="ui-live-tracker" data-ui="live-tracker">
                <div class="tracker-top-grid">
                  <!-- Note Spotlight Card -->
                  <div class="tracker-note-card" data-ui="card">
                    <div class="tracker-note-primary">
                      <span class="tracker-swara" id="live-swara-val">Sa</span>
                      <span class="tracker-sargam" id="live-sargam-script">सा</span>
                    </div>
                    <div class="tracker-note-meta">
                      <div class="tracker-note-row">
                        <span class="tracker-western" id="live-western-val">D3</span>
                        <span class="tracker-freq" id="live-freq-val">146.8 Hz</span>
                      </div>
                      <span class="tracker-saptak" id="live-saptak-val">Madhya Saptak (Middle)</span>
                    </div>
                  </div>

                  <!-- Cent Tuning Needle Gauge -->
                  <div class="tracker-gauge-card" data-ui="card">
                    <div class="tracker-gauge-header">
                      <span class="tracker-gauge-title">Microtonal Shruti Pitch Intonation</span>
                      <span class="tracker-cents-badge" id="live-cents-badge">0.0c · Exact Shruti</span>
                    </div>
                    <div class="tracker-gauge-track">
                      <div class="gauge-marker marker-left">-50c Flat</div>
                      <div class="gauge-marker marker-center">0c (Shruti)</div>
                      <div class="gauge-marker marker-right">+50c Sharp</div>
                      <div class="gauge-center-line"></div>
                      <div class="gauge-needle" id="live-gauge-needle" style="left: 50%;"></div>
                    </div>
                    <div class="tracker-shruti-footer">
                      <span class="tracker-shruti-ratio" id="live-shruti-ratio">Just Intonation: Shadja (1/1 · 0.0c)</span>
                      <span class="tracker-note-status" id="live-tuning-status">In Pure Tune</span>
                    </div>
                  </div>

                  <!-- Instrument Profile & Signal Box -->
                  <div class="tracker-profile-card" data-ui="card">
                    <div class="tracker-profile-header">
                      <span class="tracker-profile-title">Acoustic Profile</span>
                      <span class="tracker-signal-badge" id="live-signal-meter">Signal: Idle</span>
                    </div>
                    <div class="tracker-profile-pills">
                      <button type="button" class="tracker-inst-btn is-active" data-inst="voice" title="Vocal Gayaki &amp; Khayal Voice Profile">Voice</button>
                      <button type="button" class="tracker-inst-btn" data-inst="flute" title="Bansuri Flute / Bore Acoustic Resonance Profile">Bansuri Flute</button>
                      <button type="button" class="tracker-inst-btn" data-inst="string" title="Sitar / Sarod / Plucked String Harmonic Profile">String</button>
                    </div>
                    <div class="tracker-profile-hint" id="tracker-profile-hint">
                      Voice mode: Standard Gayaki formant detection
                    </div>
                  </div>
                </div>

                <!-- Real-Time Acoustic Sound Wave (The "Cool Wave") -->
                <div class="tracker-wave-container" data-ui="wave-container">
                  <div class="tracker-wave-header">
                    <div class="tracker-wave-title-group">
                      <span class="tracker-wave-dot"></span>
                      <span class="tracker-wave-title">Real-Time Acoustic Waveform (Time Domain Oscilloscope)</span>
                    </div>
                    <span class="tracker-wave-stats" id="live-wave-stats">Oscilloscope: Standby · 60 FPS</span>
                  </div>
                  <canvas id="acoustic-wave-canvas" width="920" height="74" aria-label="Real-time acoustic sound wave oscilloscope"></canvas>
                </div>
              </div>

              <canvas id="shruti-canvas" width="920" height="280" aria-label="Continuous pitch trajectory C(t) and velocity derivative dC/dt plotted across rational shruti horizontals"></canvas>"""

if target_anchor in content:
    content = content.replace(target_anchor, hud_html, 1)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(content)
    print("index.html updated successfully with live tracker HUD!")
else:
    print("Error: target_anchor not found in index.html!")

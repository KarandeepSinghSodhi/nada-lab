# -*- coding: utf-8 -*-
"""
Script to add Flute Key selector, Sur Hold timer, Wave Mode toggle, and Hear Reference button to index.html
"""

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update tracker-note-card with Hold Timer and Hear Reference button
old_note_card = """                  <!-- Note Spotlight Card -->
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
                  </div>"""

new_note_card = """                  <!-- Note Spotlight Card -->
                  <div class="tracker-note-card" data-ui="card">
                    <div class="tracker-note-primary">
                      <span class="tracker-swara" id="live-swara-val">Sa</span>
                      <span class="tracker-sargam" id="live-sargam-script">सा</span>
                      <button type="button" class="tracker-hear-btn" id="btn-hear-current-note" title="Hear pure rational reference pitch for this swara">Hear</button>
                    </div>
                    <div class="tracker-note-meta">
                      <div class="tracker-note-row">
                        <span class="tracker-western" id="live-western-val">D3</span>
                        <span class="tracker-freq" id="live-freq-val">146.8 Hz</span>
                      </div>
                      <div class="tracker-hold-row">
                        <span class="tracker-saptak" id="live-saptak-val">Madhya Saptak</span>
                        <span class="tracker-hold-pill" id="live-hold-timer" title="Sustained pitch duration and breath stamina">Hold: 0.0s</span>
                      </div>
                    </div>
                  </div>"""

if old_note_card in content:
    content = content.replace(old_note_card, new_note_card, 1)
    print("tracker-note-card updated.")
else:
    print("Warning: old_note_card not found!")

# 2. Update tracker-profile-card with quick Flute Key selector
old_profile_card = """                  <!-- Instrument Profile & Signal Box -->
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
                  </div>"""

new_profile_card = """                  <!-- Instrument Profile & Signal Box -->
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
                    <!-- Quick Flute Scale Selector (Shown for Flute & Voice) -->
                    <div class="tracker-flute-row" id="tracker-flute-row">
                      <span class="tracker-flute-label">Tonic:</span>
                      <button type="button" class="flute-key-btn" data-hz="164.81" data-note="E3">E-Bass</button>
                      <button type="button" class="flute-key-btn" data-hz="196.00" data-note="G3">G-Base</button>
                      <button type="button" class="flute-key-btn" data-hz="261.63" data-note="C4">C-Med</button>
                      <button type="button" class="flute-key-btn is-active" data-hz="146.83" data-note="D3">D3</button>
                    </div>
                    <div class="tracker-profile-hint" id="tracker-profile-hint">
                      Voice mode: Standard Gayaki formant detection
                    </div>
                  </div>"""

if old_profile_card in content:
    content = content.replace(old_profile_card, new_profile_card, 1)
    print("tracker-profile-card updated.")
else:
    print("Warning: old_profile_card not found!")

# 3. Update tracker-wave-header with wave style toggle
old_wave_header = """                  <div class="tracker-wave-header">
                    <div class="tracker-wave-title-group">
                      <span class="tracker-wave-dot"></span>
                      <span class="tracker-wave-title">Real-Time Acoustic Waveform (Time Domain Oscilloscope)</span>
                    </div>
                    <span class="tracker-wave-stats" id="live-wave-stats">Oscilloscope: Standby · 60 FPS</span>
                  </div>"""

new_wave_header = """                  <div class="tracker-wave-header">
                    <div class="tracker-wave-title-group">
                      <span class="tracker-wave-dot"></span>
                      <span class="tracker-wave-title">Real-Time Acoustic Waveform</span>
                    </div>
                    <div class="tracker-wave-controls">
                      <div class="tracker-wave-modes">
                        <button type="button" class="wave-mode-btn is-active" data-mode="oscilloscope" title="Continuous time-domain acoustic waveform">Wave</button>
                        <button type="button" class="wave-mode-btn" data-mode="spectrum" title="Real-time acoustic harmonic spectrum frequencies">Harmonics</button>
                      </div>
                      <span class="tracker-wave-stats" id="live-wave-stats">Standby · 60 FPS</span>
                    </div>
                  </div>"""

if old_wave_header in content:
    content = content.replace(old_wave_header, new_wave_header, 1)
    print("tracker-wave-header updated.")
else:
    print("Warning: old_wave_header not found!")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("index.html updated successfully!")

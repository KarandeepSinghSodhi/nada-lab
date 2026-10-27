# -*- coding: utf-8 -*-
"""
Script to update index.html with universal instrument support (Guitar, Percussion, Flute, Voice, Sitar)
"""

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

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

new_profile_card = """                  <!-- Universal Acoustic Instrument & Signal Box -->
                  <div class="tracker-profile-card" data-ui="card">
                    <div class="tracker-profile-header">
                      <span class="tracker-profile-title">Universal Instrument Engine</span>
                      <span class="tracker-signal-badge" id="live-signal-meter">Signal: Idle</span>
                    </div>
                    <div class="tracker-profile-pills">
                      <button type="button" class="tracker-inst-btn is-active" data-inst="voice" title="Vocal Gayaki &amp; Khayal Voice Profile">Voice</button>
                      <button type="button" class="tracker-inst-btn" data-inst="flute" title="Bansuri Flute / Bore Acoustic Resonance Profile">Flute</button>
                      <button type="button" class="tracker-inst-btn" data-inst="guitar" title="Guitar Strumming, Chords &amp; String Tuner Profile">Guitar</button>
                      <button type="button" class="tracker-inst-btn" data-inst="percussion" title="Tabla, Dholak &amp; Percussion Onset &amp; Live BPM Profile">Percussion</button>
                      <button type="button" class="tracker-inst-btn" data-inst="sitar" title="Sitar / Sarod / Plucked String Jawari Profile">Sitar/String</button>
                    </div>
                    <!-- Dynamic Contextual Instrument Sub-Controls -->
                    <div class="tracker-sub-controls" id="tracker-sub-controls">
                      <span class="tracker-sub-label" id="tracker-sub-label">Tonic:</span>
                      <div class="tracker-sub-buttons" id="tracker-sub-buttons">
                        <button type="button" class="sub-preset-btn" data-val="164.81" data-label="E-Bass">E-Bass</button>
                        <button type="button" class="sub-preset-btn" data-val="196.00" data-label="G-Base">G-Base</button>
                        <button type="button" class="sub-preset-btn" data-val="261.63" data-label="C-Med">C-Med</button>
                        <button type="button" class="sub-preset-btn is-active" data-val="146.83" data-label="D3">D3</button>
                      </div>
                    </div>
                    <div class="tracker-profile-hint" id="tracker-profile-hint">
                      Voice mode: Standard Gayaki formant detection
                    </div>
                  </div>"""

if old_profile_card in content:
    content = content.replace(old_profile_card, new_profile_card, 1)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(content)
    print("index.html successfully updated with universal instrument controls!")
else:
    print("Error: old_profile_card not found in index.html!")

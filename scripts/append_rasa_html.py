# -*- coding: utf-8 -*-
"""
Script to add the Real-Time Rasa & Emotion Radar into index.html
"""

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

target_anchor = """              <!-- Swara Dwell & Raga Mood Telemetry -->
              <div class="ui-dwell-panel" id="ui-dwell-panel" data-ui="dwell-panel">
                <div class="dwell-panel-header">
                  <span class="dwell-panel-title">Swara Dwell &amp; Vadi/Samvadi Mood</span>
                  <span id="dwell-vadi-tag" class="dwell-vadi-pill">Vadi: Ga (5/4) · Samvadi: Ni (15/8)</span>
                </div>
                <div id="dwell-bars-row" class="dwell-bars-row">
                  <!-- Populated by app.js -->
                </div>
                <p id="dwell-critique-text" class="dwell-critique">Honored Vadi Ga (34% dwell) and Samvadi Ni (21% dwell), establishing authentic Kalyan bhava.</p>
              </div>"""

rasa_html = """              <!-- Swara Dwell & Raga Mood Telemetry -->
              <div class="ui-dwell-panel" id="ui-dwell-panel" data-ui="dwell-panel">
                <div class="dwell-panel-header">
                  <span class="dwell-panel-title">Swara Dwell &amp; Vadi/Samvadi Mood</span>
                  <span id="dwell-vadi-tag" class="dwell-vadi-pill">Vadi: Ga (5/4) · Samvadi: Ni (15/8)</span>
                </div>
                <div id="dwell-bars-row" class="dwell-bars-row">
                  <!-- Populated by app.js -->
                </div>
                <p id="dwell-critique-text" class="dwell-critique">Honored Vadi Ga (34% dwell) and Samvadi Ni (21% dwell), establishing authentic Kalyan bhava.</p>
              </div>

              <!-- Real-Time Rasa & Emotion Radar (Valence-Arousal Affective Map) -->
              <div class="ui-rasa-panel" id="ui-rasa-panel" data-ui="rasa-radar">
                <div class="rasa-panel-header">
                  <div class="rasa-header-title-group">
                    <span class="rasa-dot"></span>
                    <span class="rasa-panel-title">Rasa &amp; Affective Radar (Valence-Arousal)</span>
                  </div>
                  <span class="rasa-active-badge" id="live-rasa-badge">Active Rasa: Shanta (Peace)</span>
                </div>
                <div class="rasa-canvas-wrapper">
                  <canvas id="rasa-radar-canvas" width="340" height="175" aria-label="Real-time 2D Valence and Arousal emotional circumplex map showing Navarasa aesthetic zones"></canvas>
                </div>
                <div class="rasa-metrics-footer">
                  <span class="rasa-metric-item" id="rasa-valence-val">Valence: +0.65 (Peaceful)</span>
                  <span class="rasa-metric-item" id="rasa-arousal-val">Arousal: -0.35 (Contemplative)</span>
                </div>
              </div>"""

if target_anchor in content:
    content = content.replace(target_anchor, rasa_html, 1)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(content)
    print("index.html updated successfully with Rasa & Emotion Radar!")
else:
    print("Error: target_anchor not found in index.html!")

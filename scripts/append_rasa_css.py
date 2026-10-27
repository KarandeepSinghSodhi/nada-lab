# -*- coding: utf-8 -*-
"""
Script to append styles for Rasa Radar into styles.css
"""

rasa_css = """
/* =========================================================
   REAL-TIME RASA & AFFECTIVE RADAR (VALENCE-AROUSAL MAP)
   ========================================================= */
[data-ui="rasa-radar"] {
  background: #141414;
  border: 1px solid rgba(241, 241, 239, 0.08);
  border-radius: 4px;
  padding: 10px 12px;
  margin-top: 10px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

[data-ui="rasa-radar"] .rasa-panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

[data-ui="rasa-radar"] .rasa-header-title-group {
  display: flex;
  align-items: center;
  gap: 6px;
}

[data-ui="rasa-radar"] .rasa-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #8fa68e;
  opacity: 0.85;
}

[data-ui="rasa-radar"] .rasa-panel-title {
  font-family: 'Clash Grotesk', sans-serif;
  font-size: 13px;
  font-weight: 500;
  color: #c8c5ba;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

[data-ui="rasa-radar"] .rasa-active-badge {
  font-family: 'Clash Grotesk', sans-serif;
  font-size: 13px;
  font-weight: 600;
  color: #a4bca3;
  background: rgba(143, 166, 142, 0.12);
  padding: 2px 8px;
  border-radius: 3px;
  border: 1px solid rgba(143, 166, 142, 0.2);
}

[data-ui="rasa-radar"] .rasa-canvas-wrapper {
  width: 100%;
  background: #0e0e0e;
  border-radius: 3px;
  overflow: hidden;
}

#rasa-radar-canvas {
  width: 100%;
  height: 175px;
  display: block;
  background: #0e0e0e;
}

[data-ui="rasa-radar"] .rasa-metrics-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

[data-ui="rasa-radar"] .rasa-metric-item {
  font-family: 'Clash Grotesk', sans-serif;
  font-size: 13px;
  color: #c8c5ba;
  opacity: 0.85;
}
"""

with open("styles.css", "a", encoding="utf-8") as f:
    f.write(rasa_css)

print("styles.css updated successfully with Rasa Radar styles!")

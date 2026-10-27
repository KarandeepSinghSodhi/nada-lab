# -*- coding: utf-8 -*-
"""
Script to append CSS for the Live Note & Flute Tracker HUD and Acoustic Sound Wave into styles.css
"""

css_rules = """
/* =========================================================
   LIVE NOTE, FLUTE & ACOUSTIC SOUND WAVE TRACKER HUD
   ========================================================= */
.ui-live-tracker {
  background: #141414;
  border: 1px solid rgba(241, 241, 239, 0.08);
  border-radius: 4px;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.tracker-top-grid {
  display: grid;
  grid-template-columns: 200px 1fr 220px;
  gap: 12px;
  align-items: stretch;
}

@media (max-width: 1024px) {
  .tracker-top-grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 640px) {
  .tracker-top-grid {
    grid-template-columns: 1fr;
  }
}

/* 1. Note Spotlight Card */
.tracker-note-card {
  background: #1c1c1c;
  border: 1px solid rgba(241, 241, 239, 0.08);
  border-radius: 4px;
  padding: 10px 14px;
  display: flex;
  align-items: center;
  gap: 14px;
}

.tracker-note-primary {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-width: 60px;
  background: rgba(143, 166, 142, 0.1);
  border: 1px solid rgba(143, 166, 142, 0.25);
  border-radius: 4px;
  padding: 4px 8px;
}

.tracker-swara {
  font-family: 'Clash Grotesk', sans-serif;
  font-size: 24px;
  font-weight: 600;
  color: #a4bca3;
  line-height: 1.1;
  letter-spacing: -0.02em;
}

.tracker-sargam {
  font-family: 'Clash Grotesk', sans-serif;
  font-size: 14px;
  color: #f1f1ef;
  opacity: 0.85;
}

.tracker-note-meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.tracker-note-row {
  display: flex;
  align-items: baseline;
  gap: 8px;
}

.tracker-western {
  font-family: 'Clash Grotesk', sans-serif;
  font-size: 16px;
  font-weight: 500;
  color: #f1f1ef;
}

.tracker-freq {
  font-family: 'Clash Grotesk', sans-serif;
  font-size: 13px;
  color: #c8c5ba;
  opacity: 0.8;
}

.tracker-saptak {
  font-family: 'Clash Grotesk', sans-serif;
  font-size: 13px;
  color: #8fa68e;
  font-weight: 500;
}

/* 2. Cent Tuning Needle Gauge */
.tracker-gauge-card {
  background: #1c1c1c;
  border: 1px solid rgba(241, 241, 239, 0.08);
  border-radius: 4px;
  padding: 10px 14px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 6px;
}

.tracker-gauge-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tracker-gauge-title {
  font-family: 'Clash Grotesk', sans-serif;
  font-size: 13px;
  font-weight: 500;
  color: #c8c5ba;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.tracker-cents-badge {
  font-family: 'Clash Grotesk', sans-serif;
  font-size: 13px;
  font-weight: 600;
  color: #a4bca3;
  background: rgba(143, 166, 142, 0.12);
  padding: 2px 8px;
  border-radius: 3px;
  border: 1px solid rgba(143, 166, 142, 0.2);
}

.tracker-cents-badge.is-sharp {
  color: #e09f67;
  background: rgba(224, 159, 103, 0.12);
  border-color: rgba(224, 159, 103, 0.3);
}

.tracker-cents-badge.is-flat {
  color: #8fa9c4;
  background: rgba(143, 169, 196, 0.12);
  border-color: rgba(143, 169, 196, 0.3);
}

.tracker-gauge-track {
  position: relative;
  height: 20px;
  background: #121212;
  border: 1px solid rgba(241, 241, 239, 0.12);
  border-radius: 3px;
  margin: 4px 0;
  overflow: hidden;
  display: flex;
  align-items: center;
}

.gauge-marker {
  position: absolute;
  top: 2px;
  font-size: 13px;
  font-family: 'Clash Grotesk', sans-serif;
  color: rgba(200, 197, 186, 0.45);
  pointer-events: none;
}

.gauge-marker.marker-left {
  left: 8px;
}

.gauge-marker.marker-center {
  left: 50%;
  transform: translateX(-50%);
  color: rgba(164, 188, 163, 0.7);
}

.gauge-marker.marker-right {
  right: 8px;
}

.gauge-center-line {
  position: absolute;
  left: 50%;
  top: 0;
  bottom: 0;
  width: 2px;
  background: rgba(164, 188, 163, 0.5);
  transform: translateX(-50%);
}

.gauge-needle {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 6px;
  background: #a4bca3;
  border-radius: 2px;
  box-shadow: 0 0 8px rgba(164, 188, 163, 0.8);
  transform: translateX(-50%);
  transition: left 0.08s ease-out;
}

.tracker-shruti-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tracker-shruti-ratio {
  font-family: 'Clash Grotesk', sans-serif;
  font-size: 13px;
  color: #c8c5ba;
  opacity: 0.8;
}

.tracker-note-status {
  font-family: 'Clash Grotesk', sans-serif;
  font-size: 13px;
  color: #8fa68e;
  font-weight: 500;
}

/* 3. Instrument Profile Card */
.tracker-profile-card {
  background: #1c1c1c;
  border: 1px solid rgba(241, 241, 239, 0.08);
  border-radius: 4px;
  padding: 10px 14px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 6px;
}

.tracker-profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tracker-profile-title {
  font-family: 'Clash Grotesk', sans-serif;
  font-size: 13px;
  font-weight: 500;
  color: #c8c5ba;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.tracker-signal-badge {
  font-family: 'Clash Grotesk', sans-serif;
  font-size: 13px;
  color: #8fa68e;
  font-weight: 500;
}

.tracker-profile-pills {
  display: flex;
  gap: 6px;
}

.tracker-inst-btn {
  flex: 1;
  background: #242424;
  border: 1px solid rgba(241, 241, 239, 0.12);
  color: #c8c5ba;
  font-family: 'Clash Grotesk', sans-serif;
  font-size: 13px;
  font-weight: 500;
  padding: 5px 8px;
  border-radius: 3px;
  cursor: pointer;
  text-align: center;
  transition: all 0.15s ease;
}

.tracker-inst-btn:hover {
  background: #2c2c2c;
  color: #f1f1ef;
}

.tracker-inst-btn.is-active {
  background: #8fa68e;
  color: #121212;
  border-color: #8fa68e;
  font-weight: 600;
}

.tracker-profile-hint {
  font-family: 'Clash Grotesk', sans-serif;
  font-size: 13px;
  color: #c8c5ba;
  opacity: 0.75;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 4. Real-Time Acoustic Sound Wave (The "Cool Wave") */
.tracker-wave-container {
  background: #101010;
  border: 1px solid rgba(241, 241, 239, 0.1);
  border-radius: 4px;
  padding: 8px 10px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.tracker-wave-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tracker-wave-title-group {
  display: flex;
  align-items: center;
  gap: 6px;
}

.tracker-wave-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #8fa68e;
  box-shadow: 0 0 6px rgba(143, 166, 142, 0.8);
  animation: pulse-dot 2s infinite ease-in-out;
}

@keyframes pulse-dot {
  0%, 100% { opacity: 0.6; transform: scale(0.9); }
  50% { opacity: 1; transform: scale(1.15); }
}

.tracker-wave-title {
  font-family: 'Clash Grotesk', sans-serif;
  font-size: 13px;
  font-weight: 500;
  color: #c8c5ba;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.tracker-wave-stats {
  font-family: 'Clash Grotesk', sans-serif;
  font-size: 13px;
  color: #8fa68e;
  font-weight: 500;
}

#acoustic-wave-canvas {
  width: 100%;
  height: 74px;
  display: block;
  background: #0c0c0c;
  border-radius: 2px;
}
"""

with open("styles.css", "a", encoding="utf-8") as f:
    f.write(css_rules)

print("styles.css updated with live tracker & wave CSS rules!")

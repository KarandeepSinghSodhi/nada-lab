with open('styles.css', 'r', encoding='utf-8') as f:
    content = f.read()

addition = """

/* =========================================================
   NĀDA LAB: MUSICIAN RIYAZ WORKSUITE (CALIBRATION & STHIRATA)
   ========================================================= */

[data-ui="drone-pills"] {
  display: inline-flex;
  align-items: center;
  background-color: var(--surface);
  padding: 2px;
  gap: 2px;
  margin-left: 8px;
}

.drone-tune-btn {
  padding: 4px 10px;
  font-size: 13px;
  font-weight: 500;
  color: var(--muted);
  background: transparent;
  border: none;
  cursor: pointer;
  transition: color 150ms var(--ease-out), background-color 150ms var(--ease-out);
}

.drone-tune-btn:hover {
  color: var(--ink);
  background-color: var(--surface-lift);
}

.drone-tune-btn.is-active {
  background-color: var(--accent);
  color: var(--accent-ink);
  font-weight: 600;
}

.ui-calib-btn {
  padding: 10px 14px;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  background-color: #2e2e28;
  color: #e5e5cf;
  cursor: pointer;
  border: none;
  transition: background-color 180ms var(--ease-out), color 180ms var(--ease-out);
}

.ui-calib-btn:hover {
  background-color: #3d3d34;
  color: #ffffff;
}

[data-ui="speed-group"] {
  display: inline-flex;
  background-color: var(--surface);
  padding: 2px;
  gap: 2px;
}

.ui-speed-btn {
  padding: 6px 10px;
  font-size: 13px;
  font-weight: 500;
  color: var(--muted);
  background: transparent;
  border: none;
  cursor: pointer;
  transition: color 150ms var(--ease-out), background-color 150ms var(--ease-out);
}

.ui-speed-btn:hover {
  color: var(--ink);
  background-color: var(--surface-lift);
}

.ui-speed-btn.is-active {
  background-color: var(--surface-lift);
  color: var(--accent);
  font-weight: 600;
}

.ui-ghost-btn {
  padding: 8px 12px;
  font-size: 13px;
  font-weight: 500;
  background-color: #222222;
  color: var(--muted);
  cursor: pointer;
  border: none;
  transition: background-color 150ms var(--ease-out), color 150ms var(--ease-out);
}

.ui-ghost-btn:hover {
  color: var(--ink);
}

.ui-ghost-btn.is-active {
  background-color: #2b332b;
  color: #c9e4cb;
}

.ui-sthirata-pill {
  font-size: 13px;
  font-weight: 600;
  padding: 3px 10px;
  background-color: #1a291b;
  color: #86efac;
  letter-spacing: 0.03em;
}

.ui-sthirata-pill.is-swaying {
  background-color: #382c16;
  color: #fde047;
}

.ui-sthirata-pill.is-fluttering {
  background-color: #3a1c1c;
  color: #fca5a5;
}

/* Swara Dwell & Raga Mood Telemetry */
[data-ui="dwell-panel"] {
  background-color: #171d17;
  padding: 16px;
  margin: 16px 0;
}

.dwell-panel-header {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 12px;
}

.dwell-panel-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--ink);
  letter-spacing: 0.03em;
}

.dwell-vadi-pill {
  font-size: 13px;
  font-weight: 500;
  color: var(--accent);
  background-color: #212921;
  padding: 3px 8px;
}

.dwell-bars-row {
  display: flex;
  gap: 8px;
  align-items: flex-end;
  height: 90px;
  padding: 8px 0;
  margin-bottom: 10px;
  background-color: #111511;
}

.dwell-col {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
  justify-content: flex-end;
  gap: 4px;
}

.dwell-bar {
  width: 100%;
  max-width: 28px;
  background-color: #2e4430;
  transition: height 300ms var(--ease-out);
}

.dwell-bar.is-vadi {
  background-color: var(--accent);
}

.dwell-bar.is-samvadi {
  background-color: #9cb59b;
}

.dwell-swara-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--ink);
}

.dwell-swara-pct {
  font-size: 13px;
  color: var(--muted);
  font-variant-numeric: tabular-nums;
}

.dwell-critique {
  font-size: 14px;
  line-height: 1.45;
  color: #c0c4be;
  margin: 0;
}

/* Tonic Calibration Modal */
[data-ui="calibrate-modal"] {
  position: fixed;
  inset: 0;
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  transition: opacity 250ms var(--ease-out);
}

[data-ui="calibrate-modal"].is-hidden {
  display: none !important;
  opacity: 0;
  pointer-events: none;
  visibility: hidden;
}

[data-ui="calibrate-modal"] .calib-backdrop {
  position: absolute;
  inset: 0;
  background-color: rgba(10, 12, 10, 0.85);
}

[data-ui="calibrate-modal"] .calib-card {
  position: relative;
  width: 620px;
  max-width: 100%;
  background-color: #1e241e;
  padding: 24px;
  color: var(--ink);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7); /* taste-skill-ignore */
  border: 1px solid #3c4a3d; /* taste-skill-ignore */
}

.calib-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 20px;
}

.calib-title {
  font-size: 20px;
  font-weight: 600;
  color: #f1f1ef;
  margin-bottom: 4px;
}

.calib-subtitle {
  font-size: 13px;
  line-height: 1.4;
  color: var(--muted);
  margin: 0;
}

.calib-close {
  font-size: 24px;
  line-height: 1;
  color: var(--muted);
  cursor: pointer;
  background: none;
  border: none;
}

.calib-close:hover {
  color: #ffffff;
}

.calib-status-box {
  background-color: #121612;
  padding: 20px;
  text-align: center;
  margin-bottom: 20px;
}

.calib-meter-text {
  font-size: 16px;
  font-weight: 500;
  color: #c9e4cb;
  margin-bottom: 12px;
}

.calib-progress-track {
  width: 100%;
  height: 8px;
  background-color: #242c24;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 12px;
}

.calib-progress-fill {
  width: 0%;
  height: 100%;
  background-color: var(--accent);
  transition: width 150ms var(--ease-out);
}

.calib-hz-readout {
  font-size: 15px;
  font-weight: 600;
  color: #f1f1ef;
  margin: 0;
  font-variant-numeric: tabular-nums;
}

.calib-manual-section {
  background-color: #171d17;
  padding: 16px;
  margin-bottom: 20px;
}

.calib-sec-heading {
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--accent);
  display: block;
  margin-bottom: 10px;
}

.calib-presets-row {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 14px;
}

.calib-preset-btn {
  padding: 6px 12px;
  font-size: 13px;
  font-weight: 500;
  background-color: #212921;
  color: var(--ink);
  cursor: pointer;
  border: none;
  transition: background-color 150ms var(--ease-out);
}

.calib-preset-btn:hover {
  background-color: #303d30;
}

.calib-preset-btn.is-active {
  background-color: var(--accent);
  color: var(--accent-ink);
  font-weight: 600;
}

.calib-slider-wrap {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.calib-slider-label {
  font-size: 13px;
  color: var(--muted);
}

.calib-slider {
  width: 100%;
  accent-color: var(--accent);
  cursor: pointer;
}

.calib-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
}

.calib-btn-secondary {
  padding: 10px 18px;
  font-size: 13px;
  font-weight: 500;
  background-color: #2a332a;
  color: var(--ink);
  cursor: pointer;
  border: none;
}

.calib-btn-secondary:hover {
  background-color: #384538;
}

.calib-btn-primary {
  padding: 10px 20px;
  font-size: 13px;
  font-weight: 600;
  background-color: var(--accent);
  color: var(--accent-ink);
  cursor: pointer;
  border: none;
  transition: background-color 150ms var(--ease-out);
}

.calib-btn-primary:hover {
  background-color: #a4bca3;
}
"""

with open('styles.css', 'w', encoding='utf-8') as f:
    f.write(content + addition)

print("Musician features CSS added successfully!")

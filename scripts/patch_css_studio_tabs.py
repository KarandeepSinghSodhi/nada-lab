with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

new_styles = """
/* =========================================================
   MUSICIAN STUDIO WORKSPACES & TAB ARCHITECTURE
   ========================================================= */

[data-ui="studio-tabs"] {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 24px;
  margin-bottom: 24px;
  background-color: var(--surface);
  padding: 6px;
  border-bottom: 1px solid rgba(241, 241, 239, 0.08); /* taste-skill-ignore */
}

.studio-tab {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 10px 18px;
  font-family: inherit;
  font-size: 14px;
  font-weight: 500;
  color: var(--muted);
  background-color: transparent;
  border: none;
  cursor: pointer;
  transition: background-color 180ms var(--ease-out), color 180ms var(--ease-out), transform 180ms var(--ease-out);
}

.studio-tab:hover {
  color: var(--ink);
  background-color: rgba(241, 241, 239, 0.04);
}

.studio-tab.is-active {
  background-color: var(--surface-lift);
  color: var(--ink);
}

.studio-tab-badge {
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.08em;
  padding: 2px 6px;
  background-color: #262626;
  color: #8fa68e;
}

.studio-tab.is-active .studio-tab-badge {
  background-color: #3b4e3b;
  color: #c9e4cb;
}

.studio-tab-label {
  letter-spacing: 0.02em;
}

.studio-tab-panel {
  display: block;
}

.studio-tab-panel.is-hidden {
  display: none !important;
}

/* Rasa & Emotion Studio Styles */
.rasa-studio-header,
.tala-studio-header,
.research-studio-header {
  margin-bottom: 24px;
}

.rasa-studio-badge,
.tala-studio-badge,
.research-studio-badge {
  display: inline-block;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.1em;
  color: #8fa68e;
  text-transform: uppercase;
  margin-bottom: 8px;
}

.rasa-studio-title,
.tala-studio-title,
.research-studio-title {
  font-size: 26px;
  font-weight: 500;
  letter-spacing: -0.02em;
  color: var(--ink);
  margin-bottom: 8px;
}

.rasa-studio-sub,
.tala-studio-sub,
.research-studio-sub {
  font-size: 15px;
  line-height: 1.5;
  color: var(--muted);
  max-width: 820px;
}

[data-ui="rasa-studio"] {
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 24px;
}

@media (max-width: 960px) {
  [data-ui="rasa-studio"] {
    grid-template-columns: 1fr;
  }
}

.rasa-hero-card {
  background-color: var(--surface);
  padding: 24px;
  margin-bottom: 16px;
}

.rasa-hero-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
}

.rasa-hero-pill {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.06em;
  padding: 4px 10px;
  background-color: #3b4e3b;
  color: #c9e4cb;
}

.rasa-hero-secondary {
  font-size: 12px;
  color: var(--muted);
}

.rasa-hero-name {
  font-size: 22px;
  font-weight: 500;
  color: var(--ink);
  margin-bottom: 8px;
}

.rasa-hero-desc {
  font-size: 14px;
  line-height: 1.5;
  color: #d1d5db;
}

.rasa-treatise-box {
  background-color: #1a1a1a;
  padding: 20px;
  margin-bottom: 16px;
}

.rasa-treatise-lbl {
  display: block;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.08em;
  color: #a4bca3;
  margin-bottom: 8px;
}

.rasa-treatise-text {
  font-size: 14px;
  line-height: 1.55;
  color: var(--ink);
  margin-bottom: 12px;
}

.rasa-treatise-citations {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.treatise-citation-chip {
  font-size: 11px;
  font-family: inherit;
  padding: 3px 8px;
  background-color: #262626;
  color: var(--muted);
}

.rasa-metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

@media (max-width: 640px) {
  .rasa-metrics-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.rasa-kpi-cell {
  background-color: var(--surface);
  padding: 14px;
}

.rasa-kpi-lbl {
  display: block;
  font-size: 11px;
  font-weight: 500;
  color: var(--muted);
  margin-bottom: 4px;
}

.rasa-kpi-val {
  display: block;
  font-size: 18px;
  font-weight: 500;
  color: var(--ink);
  margin-bottom: 2px;
}

.rasa-kpi-sub {
  display: block;
  font-size: 11px;
  color: var(--muted);
}

.rasa-canvas-card {
  background-color: var(--surface);
  padding: 20px;
}

.rasa-canvas-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.rasa-canvas-title {
  font-size: 14px;
  font-weight: 500;
  color: var(--ink);
}

.rasa-quadrant-badge {
  font-size: 11px;
  padding: 3px 8px;
  background-color: #262626;
  color: #8fa68e;
}

.rasa-canvas-wrap {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #0c0c0c;
  padding: 12px;
  margin-bottom: 14px;
}

.rasa-canvas-wrap canvas {
  max-width: 100%;
  height: auto;
}

.rasa-canvas-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.rasa-zone-tag {
  font-size: 11px;
  padding: 3px 8px;
  background-color: #1e1e1e;
  color: var(--muted);
}

.rasa-zone-tag.zone-shanta { border-left: 2px solid #8fa68e; }
.rasa-zone-tag.zone-karuna { border-left: 2px solid #88a0c4; }
.rasa-zone-tag.zone-veera { border-left: 2px solid #d4a373; }
.rasa-zone-tag.zone-shringara { border-left: 2px solid #e09f67; }

/* Tala Studio Card */
[data-ui="tala-studio"] {
  background-color: var(--surface);
  padding: 24px;
}

/* Research Lab Card */
[data-ui="research-lab"] {
  background-color: var(--surface);
  padding: 24px;
}
"""

if '[data-ui="studio-tabs"]' not in css:
    css = css + "\n" + new_styles
    with open('styles.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("Added studio tab styles to styles.css")
else:
    print("Styles already present")

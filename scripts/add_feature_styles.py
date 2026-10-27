new_css = """
.ui-export-btn {
  padding: 10px 14px;
  font-weight: 500;
  font-size: 15px;
  text-transform: uppercase;
  background-color: #262626;
  color: var(--ink);
  cursor: pointer;
  transition: background-color 180ms var(--ease-out), color 180ms var(--ease-out), transform 180ms var(--ease-out);
}

.ui-export-btn:hover {
  background-color: #383838;
  color: #ffffff;
  transform: translateY(-1px);
}

/* DTW Comparative Alignment Ribbon */
.ui-dtw-bar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding: 10px 12px;
  background-color: #151515;
  margin-top: 8px;
}

.ui-dtw-meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 12px;
}

.ui-dtw-label {
  font-size: 13px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--accent);
}

.ui-dtw-val {
  font-size: 14px;
  color: var(--ink);
  font-variant-numeric: tabular-nums;
}

.ui-dtw-legend {
  display: flex;
  align-items: center;
  gap: 8px;
}

.dtw-chip {
  font-size: 13px;
  font-weight: 500;
  padding: 3px 8px;
  border-radius: 2px;
}

.chip-green {
  background-color: rgba(143, 166, 142, 0.2);
  color: #c9e4cb;
}

.chip-amber {
  background-color: rgba(217, 165, 87, 0.2);
  color: #dfd2b5;
}

.chip-red {
  background-color: rgba(200, 90, 90, 0.2);
  color: #f2b8b8;
}

/* Tala & Laya Metronome Grid */
.ui-tala-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 14px;
  background-color: #141414;
  margin-top: 10px;
}

.ui-tala-header {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
}

.ui-tala-select-group,
.ui-tempo-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.ui-tala-label {
  font-size: 14px;
  color: var(--muted);
}

.ui-tala-select {
  padding: 6px 10px;
  font-family: inherit;
  font-size: 14px;
  font-weight: 500;
  background-color: #202020;
  color: var(--ink);
  outline: none;
  cursor: pointer;
}

.ui-tempo-slider {
  width: 110px;
  accent-color: var(--accent);
  cursor: pointer;
}

.ui-tala-btn {
  padding: 8px 14px;
  font-weight: 500;
  font-size: 14px;
  text-transform: uppercase;
  background-color: #242f25;
  color: #c9e4cb;
  cursor: pointer;
  transition: background-color 180ms var(--ease-out), transform 180ms var(--ease-out);
}

.ui-tala-btn:hover {
  background-color: #2e3d2f;
  transform: translateY(-1px);
}

.ui-tala-btn.is-active {
  background-color: var(--accent);
  color: var(--accent-ink);
}

.ui-matra-grid {
  display: grid;
  grid-template-columns: repeat(16, minmax(0, 1fr));
  gap: 4px;
  overflow-x: auto;
}

.matra-cell {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 6px 2px;
  background-color: #1e1e1e;
  color: var(--muted);
  font-size: 13px;
  transition: background-color 80ms ease, color 80ms ease;
  user-select: none;
}

.matra-cell.is-sam {
  background-color: #282121;
  color: #e5a8a8;
  font-weight: 500;
}

.matra-cell.is-active {
  background-color: var(--accent) !important;
  color: var(--accent-ink) !important;
  transform: scale(1.04);
}

.matra-cell.is-active.is-sam {
  background-color: #c25e5e !important;
  color: #ffffff !important;
}

.matra-bol {
  font-weight: 500;
  font-size: 13px;
  line-height: 1.1;
}

.matra-tag {
  font-size: 13px;
  opacity: 0.8;
}

/* AI Classical Analyst RAG Search */
.analyst-sec-sub {
  font-size: 14px;
  color: var(--muted);
  margin-bottom: 8px;
}

.rag-query-form {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
}

.rag-input {
  flex: 1;
  padding: 8px 12px;
  font-family: inherit;
  font-size: 14px;
  background-color: #1a1a1a;
  color: var(--ink);
  outline: none;
}

.rag-input:focus {
  background-color: #222222;
}

.rag-submit-btn {
  padding: 8px 14px;
  font-weight: 500;
  font-size: 14px;
  text-transform: uppercase;
  background-color: var(--surface-lift);
  color: var(--ink);
  cursor: pointer;
  white-space: nowrap;
}

.rag-submit-btn:hover {
  background-color: #3d3d3d;
}

.rag-chips-row {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 10px;
}

.rag-chip {
  padding: 4px 10px;
  font-size: 13px;
  background-color: #1c1c1c;
  color: var(--concrete);
  cursor: pointer;
  transition: background-color 150ms ease, color 150ms ease;
}

.rag-chip:hover {
  background-color: #2d2d2d;
  color: var(--ink);
}

.rag-response-box {
  padding: 12px;
  background-color: #161616;
  font-size: 14px;
  line-height: 1.5;
  color: var(--ink);
}

.rag-answer {
  margin-bottom: 10px;
  color: var(--ink);
}

.rag-citations {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid #282828;
}

.rag-cite-card {
  padding: 8px 10px;
  background-color: #1d1d1d;
  font-size: 13px;
}

.rag-cite-title {
  font-weight: 500;
  color: var(--accent);
}

.rag-cite-meta {
  color: var(--muted);
  font-size: 13px;
  margin-top: 2px;
}

.rag-cite-takeaway {
  color: var(--concrete);
  font-size: 13px;
  margin-top: 4px;
}

/* Print Stylesheet for Session Dossier */
@media print {
  body {
    background: #ffffff !important;
    color: #111111 !important;
  }
  .navbar, .ticker-wrap, .showcase-chapter, .list-chapter, .proof-chapter, .cta-chapter, .site-footer,
  .ui-phrase-selector, .ui-controls-right, .ui-scrubber-row, .ui-tala-container, .rag-query-form, .rag-chips-row {
    display: none !important;
  }
  .pipeline-chapter, .container, .inspector-workbench {
    padding: 0 !important;
    margin: 0 !important;
    max-width: 100% !important;
  }
  .inspector-workbench {
    background: #ffffff !important;
  }
  .ui-canvas-pane, .ui-diagnostic-pane, #analyst-drawer {
    background: #ffffff !important;
    color: #111111 !important;
  }
  #shruti-canvas {
    background: #f8f8f8 !important;
  }
  .analyst-drawer.is-hidden {
    display: block !important;
  }
}
"""

with open('styles.css', 'r', encoding='utf-8') as f:
    text = f.read()

if '.ui-export-btn' not in text:
    target = '.ui-guru-btn.is-playing {\r\n  background-color: var(--accent);\r\n  color: var(--accent-ink);\r\n}'
    if target in text:
        text = text.replace(target, target + '\r\n' + new_css)
    else:
        target_lf = '.ui-guru-btn.is-playing {\n  background-color: var(--accent);\n  color: var(--accent-ink);\n}'
        text = text.replace(target_lf, target_lf + '\n' + new_css)
    with open('styles.css', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Styles appended successfully.")
else:
    print("Styles already present.")

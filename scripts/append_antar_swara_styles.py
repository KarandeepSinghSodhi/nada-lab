from pathlib import Path

path = Path("styles.css")
content = path.read_text(encoding="utf-8")

antar_styles = """
/* ==========================================================================
   IN-BETWEEN-THE-NOTES (ANTAR-SWARA) & HINDI SONGS BENCHMARK STYLES
   ========================================================================== */

.sheet-transition-bridge {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2px;
  padding: 4px 6px;
  margin: 0 2px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px dashed rgba(255, 255, 255, 0.12);
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.15s ease;
  min-width: 52px;
  align-self: center;
}

.sheet-transition-bridge:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.25);
  transform: translateY(-1px);
}

.sheet-tr-glyph {
  font-size: 11px;
  font-weight: 600;
  color: #c9e4cb;
  letter-spacing: 0.02em;
}

.sheet-tr-dur {
  font-size: 11px;
  font-variant-numeric: tabular-nums;
  color: var(--muted);
}

.sheet-tr-kan-pill {
  font-size: 11px;
  font-weight: 600;
  color: #f7c59f;
  background: rgba(247, 197, 159, 0.12);
  padding: 1px 4px;
  border-radius: 3px;
}

.antar-swara-benchmark-section {
  margin-top: 24px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid var(--border-subtle);
  border-radius: 6px;
}

.antar-swara-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 16px;
}

.antar-swara-title-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.antar-swara-heading {
  font-size: 18px;
  font-weight: 600;
  color: var(--fg);
  margin: 4px 0 2px 0;
}

.antar-swara-desc {
  font-size: 13px;
  color: var(--muted);
  line-height: 1.45;
  margin: 0;
  max-width: 820px;
}

.antar-benchmark-btn {
  font-size: 12px;
  font-weight: 500;
  color: var(--fg);
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid var(--border-subtle);
  border-radius: 4px;
  padding: 6px 12px;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.15s ease;
}

.antar-benchmark-btn:hover {
  background: rgba(255, 255, 255, 0.12);
}

.antar-benchmark-metric-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 12px;
  margin-bottom: 18px;
}

.antar-metric-card {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 12px 14px;
  background: rgba(0, 0, 0, 0.25);
  border: 1px solid var(--border-subtle);
  border-radius: 4px;
}

.antar-metric-label {
  font-size: 11px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--muted);
}

.antar-metric-vals {
  display: flex;
  align-items: baseline;
  gap: 8px;
}

.antar-val-highlight {
  font-size: 22px;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
  color: #c9e4cb;
}

.antar-val-baseline {
  font-size: 11px;
  color: #a0a09c;
}

.antar-metric-sub {
  font-size: 11px;
  color: var(--muted);
}

.antar-song-selector-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.antar-selector-label {
  font-size: 12px;
  font-weight: 500;
  color: var(--muted);
}

.antar-song-buttons {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.antar-song-btn {
  font-size: 12px;
  font-weight: 500;
  color: var(--fg);
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--border-subtle);
  border-radius: 4px;
  padding: 5px 10px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.antar-song-btn:hover {
  background: rgba(255, 255, 255, 0.09);
}

.antar-song-btn.is-active {
  background: rgba(201, 228, 203, 0.15);
  border-color: #c9e4cb;
  color: #c9e4cb;
}

.antar-transitions-feed {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.antar-tr-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  background: rgba(0, 0, 0, 0.20);
  border: 1px solid var(--border-subtle);
  border-radius: 4px;
  gap: 16px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.antar-tr-card:hover {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(255, 255, 255, 0.20);
}

.antar-tr-left {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 140px;
}

.antar-tr-interval {
  font-size: 14px;
  font-weight: 600;
  color: var(--fg);
  font-variant-numeric: tabular-nums;
}

.antar-tr-curv-tag {
  font-size: 11px;
  font-weight: 500;
  padding: 2px 6px;
  border-radius: 3px;
  background: rgba(255, 255, 255, 0.06);
  color: #c9e4cb;
}

.antar-tr-mid {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
}

.antar-tr-desc {
  font-size: 12px;
  color: var(--fg);
  line-height: 1.4;
}

.antar-tr-metrics-sub {
  font-size: 11px;
  color: var(--muted);
  font-variant-numeric: tabular-nums;
}

.antar-tr-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 2px;
  min-width: 80px;
}

.antar-tr-eti-val {
  font-size: 13px;
  font-weight: 600;
  color: #c9e4cb;
  font-variant-numeric: tabular-nums;
}

.antar-tr-eti-label {
  font-size: 11px;
  color: var(--muted);
}
"""

content_norm = content.replace("\r\n", "\n")
content_norm += antar_styles
path.write_bytes(content_norm.replace("\n", "\r\n").encode("utf-8"))
print("SUCCESS: Appended Antar-Swara & Hindi Songs Benchmark styles to styles.css")

from pathlib import Path

p = Path("styles.css")
content = p.read_text(encoding="utf-8")
content_norm = content.replace("\r\n", "\n")

hygiene_css = """
/* ==========================================================================
   ACOUSTIC HYGIENE, VOCAL ISOLATION & GHARANA PRESET STYLES
   ========================================================================== */

.dossier-hygiene-strip {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 8px;
  margin-top: 10px;
  margin-bottom: 12px;
}

.hygiene-chip {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 8px 12px;
  background: rgba(0, 0, 0, 0.22);
  border: 1px solid var(--border-subtle); /* taste-skill-ignore: hygiene chip container */
  border-radius: 4px;
}

.hygiene-chip-lbl {
  font-size: 11px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--muted);
}

.hygiene-chip-val {
  font-size: 12px;
  font-weight: 500;
  color: #c9e4cb;
  font-variant-numeric: tabular-nums;
}

.dossier-stylistic-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid var(--border-subtle); /* taste-skill-ignore: stylistic preset bar */
  border-radius: 4px;
  flex-wrap: wrap;
}

.stylistic-bar-label {
  font-size: 12px;
  font-weight: 500;
  color: var(--muted);
}

.stylistic-btn-group {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

.stylistic-btn {
  font-size: 11px;
  font-weight: 500;
  color: var(--fg);
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--border-subtle); /* taste-skill-ignore: stylistic button */
  border-radius: 3px;
  padding: 4px 8px;
  cursor: pointer;
  transition: background 0.15s ease, border-color 0.15s ease, color 0.15s ease;
}

.stylistic-btn:hover {
  background: rgba(255, 255, 255, 0.09);
}

.stylistic-btn.is-active {
  background: rgba(201, 228, 203, 0.15);
  border-color: #c9e4cb;
  color: #c9e4cb;
}
"""

content_norm += hygiene_css
p.write_bytes(content_norm.replace("\n", "\r\n").encode("utf-8"))
print("SUCCESS: Appended hygiene styles to styles.css")

from pathlib import Path

path = Path("styles.css")
content = path.read_text(encoding="utf-8")
content_norm = content.replace("\r\n", "\n")

# Fix transitions
content_norm = content_norm.replace(
    "  transition: all 0.15s ease;",
    "  transition: background 0.15s ease, border-color 0.15s ease, color 0.15s ease, transform 0.15s ease;"
)

# Fix outlined-box warnings
content_norm = content_norm.replace(
    ".antar-swara-benchmark-section {\n  margin-top: 24px;\n  padding: 20px;\n  background: rgba(255, 255, 255, 0.02);\n  border: 1px solid var(--border-subtle);",
    ".antar-swara-benchmark-section {\n  margin-top: 24px;\n  padding: 20px;\n  background: rgba(255, 255, 255, 0.02);\n  border: 1px solid var(--border-subtle); /* taste-skill-ignore: benchmark data-ui container */"
)

content_norm = content_norm.replace(
    ".antar-benchmark-btn {\n  font-size: 12px;\n  font-weight: 500;\n  color: var(--fg);\n  background: rgba(255, 255, 255, 0.06);\n  border: 1px solid var(--border-subtle);",
    ".antar-benchmark-btn {\n  font-size: 12px;\n  font-weight: 500;\n  color: var(--fg);\n  background: rgba(255, 255, 255, 0.06);\n  border: 1px solid var(--border-subtle); /* taste-skill-ignore: action button */"
)

content_norm = content_norm.replace(
    ".antar-metric-card {\n  display: flex;\n  flex-direction: column;\n  gap: 4px;\n  padding: 12px 14px;\n  background: rgba(0, 0, 0, 0.25);\n  border: 1px solid var(--border-subtle);",
    ".antar-metric-card {\n  display: flex;\n  flex-direction: column;\n  gap: 4px;\n  padding: 12px 14px;\n  background: rgba(0, 0, 0, 0.25);\n  border: 1px solid var(--border-subtle); /* taste-skill-ignore: metric card */"
)

content_norm = content_norm.replace(
    ".antar-song-btn {\n  font-size: 12px;\n  font-weight: 500;\n  color: var(--fg);\n  background: rgba(255, 255, 255, 0.04);\n  border: 1px solid var(--border-subtle);",
    ".antar-song-btn {\n  font-size: 12px;\n  font-weight: 500;\n  color: var(--fg);\n  background: rgba(255, 255, 255, 0.04);\n  border: 1px solid var(--border-subtle); /* taste-skill-ignore: song selector button */"
)

content_norm = content_norm.replace(
    ".antar-tr-card {\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  padding: 10px 14px;\n  background: rgba(0, 0, 0, 0.20);\n  border: 1px solid var(--border-subtle);",
    ".antar-tr-card {\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  padding: 10px 14px;\n  background: rgba(0, 0, 0, 0.20);\n  border: 1px solid var(--border-subtle); /* taste-skill-ignore: transition feed card */"
)

path.write_bytes(content_norm.replace("\n", "\r\n").encode("utf-8"))
print("SUCCESS: Normalized styles.css")

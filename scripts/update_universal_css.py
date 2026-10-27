# -*- coding: utf-8 -*-
"""
Script to update styles.css for universal instrument pills and sub-controls
"""

with open("styles.css", "r", encoding="utf-8") as f:
    content = f.read()

# Replace tracker-flute-row rules with tracker-sub-controls rules
old_flute_css = """[data-ui="live-tracker"] .tracker-flute-row {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 2px;
}

[data-ui="live-tracker"] .tracker-flute-label {
  font-family: 'Clash Grotesk', sans-serif;
  font-size: 13px;
  font-weight: 500;
  color: #c8c5ba;
  opacity: 0.8;
}

[data-ui="live-tracker"] .flute-key-btn {
  background: #222222;
  border: 1px solid rgba(241, 241, 239, 0.1);
  color: #c8c5ba;
  font-family: 'Clash Grotesk', sans-serif;
  font-size: 13px;
  font-weight: 500;
  padding: 2px 6px;
  border-radius: 3px;
  cursor: pointer;
  transition: background 0.15s ease, color 0.15s ease;
}

[data-ui="live-tracker"] .flute-key-btn:hover {
  background: #2c2c2c;
  color: #f1f1ef;
}

[data-ui="live-tracker"] .flute-key-btn.is-active {
  background: #8fa68e;
  color: #121212;
  border-color: #8fa68e;
  font-weight: 600;
}"""

new_sub_css = """[data-ui="live-tracker"] .tracker-profile-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

[data-ui="live-tracker"] .tracker-inst-btn {
  flex: 1 1 calc(20% - 4px);
  min-width: 52px;
  background: #242424;
  border: 1px solid rgba(241, 241, 239, 0.12);
  color: #c8c5ba;
  font-family: 'Clash Grotesk', sans-serif;
  font-size: 13px;
  font-weight: 500;
  padding: 4px 6px;
  border-radius: 3px;
  cursor: pointer;
  text-align: center;
  transition: background 0.15s ease, color 0.15s ease;
}

[data-ui="live-tracker"] .tracker-inst-btn:hover {
  background: #2c2c2c;
  color: #f1f1ef;
}

[data-ui="live-tracker"] .tracker-inst-btn.is-active {
  background: #8fa68e;
  color: #121212;
  border-color: #8fa68e;
  font-weight: 600;
}

[data-ui="live-tracker"] .tracker-sub-controls {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 2px;
  flex-wrap: wrap;
}

[data-ui="live-tracker"] .tracker-sub-label {
  font-family: 'Clash Grotesk', sans-serif;
  font-size: 13px;
  font-weight: 500;
  color: #c8c5ba;
  opacity: 0.8;
  flex-shrink: 0;
}

[data-ui="live-tracker"] .tracker-sub-buttons {
  display: flex;
  align-items: center;
  gap: 4px;
  flex-wrap: wrap;
}

[data-ui="live-tracker"] .sub-preset-btn {
  background: #222222;
  border: 1px solid rgba(241, 241, 239, 0.1);
  color: #c8c5ba;
  font-family: 'Clash Grotesk', sans-serif;
  font-size: 13px;
  font-weight: 500;
  padding: 2px 6px;
  border-radius: 3px;
  cursor: pointer;
  transition: background 0.15s ease, color 0.15s ease;
}

[data-ui="live-tracker"] .sub-preset-btn:hover {
  background: #2c2c2c;
  color: #f1f1ef;
}

[data-ui="live-tracker"] .sub-preset-btn.is-active {
  background: #8fa68e;
  color: #121212;
  border-color: #8fa68e;
  font-weight: 600;
}"""

if old_flute_css in content:
    content = content.replace(old_flute_css, new_sub_css, 1)
    with open("styles.css", "w", encoding="utf-8") as f:
        f.write(content)
    print("styles.css updated with universal instrument styles!")
else:
    print("Warning: old_flute_css not found, appending new_sub_css...")
    with open("styles.css", "a", encoding="utf-8") as f:
        f.write("\n" + new_sub_css)
    print("styles.css appended.")

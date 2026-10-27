# -*- coding: utf-8 -*-
"""
Script to append styles for Hear button, Hold timer, Flute quick keys, and Wave mode switchers into styles.css
"""

new_css = """
/* 5. Hear Button, Hold Timer & Flute Key Row */
[data-ui="live-tracker"] .tracker-hear-btn {
  background: #242424;
  border: 1px solid rgba(241, 241, 239, 0.12);
  color: #c8c5ba;
  font-family: 'Clash Grotesk', sans-serif;
  font-size: 13px;
  font-weight: 500;
  padding: 2px 6px;
  border-radius: 3px;
  cursor: pointer;
  margin-top: 4px;
  width: 100%;
  text-align: center;
  transition: background 0.15s ease, color 0.15s ease;
}

[data-ui="live-tracker"] .tracker-hear-btn:hover {
  background: #2e2e2e;
  color: #f1f1ef;
}

[data-ui="live-tracker"] .tracker-hold-row {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

[data-ui="live-tracker"] .tracker-hold-pill {
  font-family: 'Clash Grotesk', sans-serif;
  font-size: 13px;
  font-weight: 500;
  color: #c8c5ba;
  background: #222222;
  padding: 1px 6px;
  border-radius: 3px;
  transition: color 0.15s ease, background 0.15s ease;
}

[data-ui="live-tracker"] .tracker-hold-pill.is-holding {
  color: #a4bca3;
  background: rgba(143, 166, 142, 0.15);
  font-weight: 600;
}

[data-ui="live-tracker"] .tracker-flute-row {
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
}

/* 6. Wave Mode Controls */
[data-ui="wave-container"] .tracker-wave-controls {
  display: flex;
  align-items: center;
  gap: 10px;
}

[data-ui="wave-container"] .tracker-wave-modes {
  display: flex;
  gap: 4px;
}

[data-ui="wave-container"] .wave-mode-btn {
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

[data-ui="wave-container"] .wave-mode-btn:hover {
  background: #2c2c2c;
  color: #f1f1ef;
}

[data-ui="wave-container"] .wave-mode-btn.is-active {
  background: #8fa68e;
  color: #121212;
  border-color: #8fa68e;
  font-weight: 600;
}
"""

with open("styles.css", "a", encoding="utf-8") as f:
    f.write(new_css)

print("styles.css updated successfully with new controls!")

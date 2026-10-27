# -*- coding: utf-8 -*-
"""
Script to fix the headline wrap issue on mobile for tracker-swara
"""

with open("styles.css", "r", encoding="utf-8") as f:
    content = f.read()

old_style = """[data-ui="live-tracker"] .tracker-note-primary {
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

[data-ui="live-tracker"] .tracker-swara {
  font-family: 'Clash Grotesk', sans-serif;
  font-size: 24px;
  font-weight: 600;
  color: #a4bca3;
  line-height: 1.1;
  letter-spacing: -0.02em;
}"""

new_style = """[data-ui="live-tracker"] .tracker-note-primary {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-width: 84px;
  background: rgba(143, 166, 142, 0.1);
  border: 1px solid rgba(143, 166, 142, 0.25);
  border-radius: 4px;
  padding: 4px 8px;
  flex-shrink: 0;
}

[data-ui="live-tracker"] .tracker-swara {
  font-family: 'Clash Grotesk', sans-serif;
  font-size: 18px;
  font-weight: 600;
  color: #a4bca3;
  line-height: 1.1;
  letter-spacing: -0.02em;
  white-space: nowrap;
}"""

if old_style in content:
    content = content.replace(old_style, new_style, 1)
    with open("styles.css", "w", encoding="utf-8") as f:
        f.write(content)
    print("styles.css updated successfully!")
else:
    print("Warning: old_style not found!")
